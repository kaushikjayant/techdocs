# Building an RTL-Driven Documentation Pipeline for SoC Reference Manuals

**Published:** June 2026 | **Category:** Documentation Automation, Semiconductor

---

At the pace of modern tape-out schedules, a manual SoC documentation workflow
is a liability. When a chip integrates 80 to 120 IP blocks — each parameterizable,
each appearing at multiple base addresses across product variants — the
documentation surface can exceed 10,000 pages. Manually extracting RTL parameters,
assembling XML content structures, and hand-crafting architectural chapters simply
does not scale.

Over the past two years, my team and I have designed and deployed an automated
Reference Manual generation pipeline that compresses this workflow from three to four
weeks of manual effort to under one working day of automated assembly, with parameter
accuracy improving from roughly 85% to 100%. This article walks through the
architecture of that pipeline and the design decisions that made it production-viable.

## The Problem: Documentation as a Manual Process

In the traditional workflow, technical writers faced a recurring set of tasks at each
tape-out cycle:

**Parameter extraction** meant querying RTL design databases or chasing design engineers
for current parameter values. This was vulnerable to version skew, communication lag,
and transcription error. When a parameter changed late in the design cycle, there was
no automated notification — writers discovered it during review, if at all.

**Spec assembly** involved hand-crafting XML content instance files, DITA map references,
and publishing manifest files. A SoC with 80 IP blocks might require 80+ individual
reference entries, each with correct base addresses, register file paths, and parameter
overrides. Errors in any one entry could produce incorrect addresses in the published
document.

**No register validation existed.** Discrepancies between RTL register definitions and
documented register specifications were caught during post-silicon review — too late to
prevent errata. A writer might document a reset value of `0x0000_0000` for a register
that the RTL actually initializes to `0x5000_000F`, and no tool would flag the mismatch.

## The Architecture: Seven Components, One Pipeline

The pipeline addresses each pain point with a targeted automation stage. All stages
are orchestrated through a VS Code extension, giving authors a graphical interface
over what is fundamentally a command-line toolchain.

### 1. RTL Elaboration and Parameter Extraction

The first stage replaces manual parameter queries with automated RTL elaboration.
Using a commercial SystemVerilog/VHDL parser, the pipeline reads the complete RTL
file list, elaborates the design hierarchy from the top module, and extracts every
parameter with full type resolution, hierarchical override tracing, and source
location tracking.

The key requirement here is **accuracy through hierarchy**. A parameter like
`CAN_NUM_MB` might be defined at the IP level as 64, overridden at the SoC level to
32 for a particular instance, and further modified by a generate block. The
elaboration engine must resolve the entire override chain to produce the value that
actually reaches synthesis — not the value declared in the IP source.

The output is a structured JSON file mapping every module instance in the
elaborated design to its resolved parameter set. This file becomes the single source
of truth for all RTL-driven content decisions throughout the pipeline.

### 2. Memory Map-Driven Instance Map Generation

The SoC architecture team maintains the chip's address map in a structured
spreadsheet. The Instance Map Generator reads this spreadsheet along with the
parameter JSON and produces per-instance configuration files that link register
database references to base addresses with parameter overrides.

The generator handles complex multi-instance scenarios automatically: the same IP
appearing at three different base addresses with three different parameter
configurations (64 mailboxes at `0x4002_4000`, 32 mailboxes at `0x4002_8000`,
64 mailboxes with CAN-FD at `0x400A_0000`) is expressed as three entries in the
same IMAP file, each pulling from the same register database but with different
override values.

### 3. Non-RTL Parameter Enrichment

Not all documentation parameters exist in RTL. Document revision strings, security
classification labels, publishing mode flags, and chip family prefixes are managed
in a Git-versioned JSON database that merges with RTL parameters during the build.

This separation — RTL parameters from elaboration, non-RTL parameters from a curated
database — ensures that design changes flow automatically while documentation-specific
configuration remains under author control.

### 4. DITA Source Auto-Generation

With all parameters resolved, the pipeline generates the complete DITA source
structure programmatically: the SoC-level DITA map with hierarchical references
to IP and SubSystem specs, the publishing manifest with register resolution groups
and merge rules, and a consolidated parameter definition file.

### 5. AI-Assisted Chapter Authoring

SoC-specific architectural chapters — clocking architecture, reset architecture,
interrupt mapping, power domains — are structurally similar across products but
require chip-specific content. An AI agent processes the SoC architecture
specification PDF and extracts structured content into DITA topic types. All
AI-generated chapters are reviewed by human authors before inclusion.

The AI handles extraction and initial structuring; humans verify technical accuracy
and refine the prose. This division of labour reduces repetitive writing effort
while preserving human judgement over the final published content.

### 6. DITA-OT Resolution and Register Diagram Generation

A custom DITA-OT plugin processes the parameterized DITA source through four
sub-stages: parameter resolution (evaluating conditional attributes against
instantiated values), register file transformation (`.rdb` to DITA reference topics
with auto-generated SVG bit-field diagrams), memory map generation (per-instance
address tables), and multi-format output (PDF, WebHelp, RAG knowledge base chunks).

### 7. RAG-Powered Documentation Explorer

The final stage of the pipeline transforms the resolved documentation into an
interactive knowledge base. A Flask-based web application provides full-text search,
collapsible TOC navigation, and an AI chatbot that answers natural language
questions about registers, parameters, and architecture — with source citations
linked back to specific documentation sections.

## Results

The pipeline reduced end-to-end Reference Manual generation time from 3–4 weeks
to under one working day. Parameter extraction accuracy improved from approximately
85% to 100%. Register address errors — previously averaging 12 per tape-out —
dropped to zero. Internal support queries decreased by 40% as engineers adopted the
RAG-powered chatbot for self-service access to register information.

More significantly, the pipeline eliminated an entire class of post-release errata:
the discrepancy between what the RTL implements and what the documentation claims.
When the published register values flow directly from design elaboration through
automated XML generation, the documentation reflects the actual hardware by
construction, not by manual verification.

## What I Learned

Three lessons stand out from this project:

**Design elaboration is non-negotiable.** Attempting to extract parameters from
synthesis or verification logs cannot achieve 100% accuracy because those tools
optimize away hierarchy information. Full design elaboration through a parser
that understands the complete SystemVerilog type system is the only reliable
approach.

**Automation threatens, then empowers.** Initial resistance from authors who
feared automation would eliminate their roles was overcome by demonstrating that
the platform handles tedious mechanical work — parameter transcription, XML
assembly, conditional resolution — freeing authors to focus on high-value
content creation and review.

**Cross-functional buy-in is critical.** The pipeline spans RTL design,
architecture, verification, and documentation teams. Early engagement with all
stakeholders — particularly the architecture team that maintains the memory map
spreadsheet — was essential for establishing the single-source-of-truth principle
that makes the entire pipeline work.

---

*This article is based on work deployed in production at a semiconductor
company. Implementation details have been abstracted and generalized.*