# Automated SoC Reference Manual Generation Pipeline — Architecture

## Overview

This document describes the architecture of a production-deployed automation platform
that generates SoC Reference Manuals from RTL design source, memory map spreadsheets,
and AI-assisted content extraction. The platform replaces a manual, multi-week document
assembly process with an automated pipeline that extracts hardware parameters directly
from RTL elaboration, assembles DITA-based content structures programmatically, resolves
parameter-conditional content automatically, and produces multi-format output from a
single source of truth.

The platform serves approximately 40 technical authors and front-end designers across
multiple product lines and geographies, and has been deployed on multiple tape-out programs.

## Design Principles

Four principles guided the architecture:

**Single Source of Truth.** Every data element — RTL parameter values, register definitions,
memory map addresses, non-RTL configuration parameters — originates from exactly one
authoritative source and flows automatically through the pipeline. No manual transcription
step exists between the design database and the published document.

**Full Automation with Human Oversight.** The pipeline handles 100% of the parameter
extraction, content assembly, conditional resolution, and register validation. Human
authors create the narrative content (functional descriptions, application notes) and
review AI-generated chapters. The machine assembles; the human verifies.

**Defense in Depth.** Multiple validation layers check consistency at every pipeline stage:
RTL-vs-documentation parameter cross-check, address space collision detection, parameter
bound validation, and conditional processing verification. Errors are caught at build
time, not post-publication.

**Tool-Agnostic Interfaces.** Every subsystem has abstracted interfaces. The RTL
elaboration engine can be Verific or Yosys. The publishing engine can be DITA-OT or
Sphinx. The AI model can be Claude or GPT-4. Swapping a component does not require
architectural changes.

## Pipeline Stages

### Stage 1: RTL Design Analysis and Parameter Extraction

The pipeline begins with the RTL source files. A SystemVerilog/VHDL parser (Verific)
analyzes the source, elaborates the design hierarchy from the top module, and extracts
every parameter with:

- Full type resolution (integer, boolean, string, enumerated, float)
- Hierarchical override tracing (defparam, generate blocks, module instantiation)
- Source location tracking (file path, line number)
- Resolved values after all overrides have been applied

The output is a structured JSON file (`module_parameters.json`) mapping every module
instance in the elaborated design hierarchy to its parameter set. This file becomes
the single source of truth for all RTL parameters across the pipeline.

### Stage 2: Memory Map-Driven Instance Map Generation

The SoC architecture team maintains the chip's memory map in a structured spreadsheet
with columns for IP name, instance name, start address, end address, slot size, and
register file reference.

The Instance Map Generator reads this spreadsheet and the `module_parameters.json`,
then produces a structured Instance Map file for each documentation scope (IP-level,
SubSystem-level, SoC-level). The IMAP file links register database references to base
addresses and provides per-instance parameter overrides.

This stage automatically handles complex multi-instance scenarios where the same IP
appears at multiple base addresses with different parameter configurations (e.g.,
FlexCAN_0 with 64 mailboxes at 0x4002_4000 vs. FlexCAN_1 with 32 mailboxes at
0x4002_8000).

### Stage 3: Non-RTL Parameter Enrichment

Not all parameters exist in RTL. Documentation-specific parameters — document revision
strings, security classification labels, publishing mode flags, chip family prefixes —
are managed in a Git-versioned JSON database with hierarchical associations:

```
Parameter → IP Instance → SubSystem → SoC → Chip Family
```

The enrichment step merges RTL parameters from the IMAP with non-RTL parameters from
the JSON database, producing a unified parameter file that covers both hardware-driven
and documentation-driven configuration.

### Stage 4: DITA Source Auto-Generation

With all parameters resolved, the pipeline generates the complete DITA source structure
programmatically:

- **DITA Map:** SoC-level map with hierarchical references to IP specs, SubSystem specs,
  and SoC-specific chapters, grouped by memory map ordering
- **Publishing Manifest:** Register resolution groups with merge rules, parameter
  resolution ordering, and multi-format output configuration
- **Parameter Definitions:** Consolidated SoC-level parameter file aggregating all
  referenced parameters

For SoC-specific chapters (clocking architecture, reset architecture, interrupt mapping,
power domains), an AI agent processes the SoC architecture specification PDF and extracts
structured content into DITA topic types (concept, reference, task). The AI-generated
chapters are reviewed by human authors before inclusion.

### Stage 5: DITA-OT Resolution and Register Diagram Generation

A custom DITA-OT plugin processes the parameterized DITA source through four sub-stages:

1. **Parameter Resolution:** Evaluates conditional attributes (`pm:cond_*`) against
   instantiated parameter values. Content whose conditions do not match the instance
   configuration is suppressed.

2. **Register File Transformation:** Register database files are transformed into DITA
   reference topics with SVG bit-field diagrams showing register layout with colour-coded
   access types (Blue: R/W, Green: RO, Orange: W1C) and HTML tables with offset, field
   name, bit range, access type, reset value, and description columns.

3. **Memory Map Generation:** For multi-instance IPs, memory map tables show each
   instance's base address, address range, and instance-specific configuration.
   Common register descriptions are shared; only address and override information varies.

4. **Multi-Format Output:** The resolved, parameter-free DITA is rendered into PDF
   (via custom XSL-FO stylesheets), responsive WebHelp (HTML5 with collapsible TOC
   and full-text search), and a chunked knowledge base for RAG ingestion.

### Stage 6: RAG Knowledge Base and AI Chatbot

Resolved DITA content is chunked by topic boundaries and section headings. Each chunk
is embedded into a vector space. Topic metadata (IP name, register offset, chapter
heading) is stored alongside embeddings.

A Flask-based web application provides:
- Collapsible sidebar TOC from the resolved DITA map
- Interactive SVG register diagrams with hover tooltips
- System-level memory map visualization with colour-coded IP blocks
- Full-text search across all documentation topics
- RAG-powered chatbot that answers natural language queries with source citations

The chatbot answers register-level questions (reset values, bit-field encodings, access
semantics) in under 3 seconds with grounded responses that cite specific documentation
sections for verification.

## Integration Architecture

The pipeline is delivered as a VS Code extension with a command palette and sidebar
panel. A local Python server handles heavy computation (RTL elaboration, DITA-OT
processing, AI API calls) and communicates with the extension over JSON-RPC. This
architecture lets authors trigger pipeline stages from the editor they already use
for DITA authoring, while keeping the computationally intensive work on a server
or local backend.

## Quantitative Results

| Metric | Before Pipeline | After Pipeline |
|:-------|:---------------:|:--------------:|
| End-to-end RM generation time | 3–4 weeks | Under 1 working day |
| Parameter extraction accuracy | ~85% (manual transcription errors) | 100% (automated from RTL) |
| Register address errors per SoC | ~12 per tape-out | 0 |
| Build failures per release | 3–5 | 0–1 |
| Internal support queries | Baseline | 40% reduction (self-service via chatbot) |
| IP spec reuse across SoCs | ~30% | ~95% (single-source publishing) |

---

*This architecture description is representative of a production-deployed documentation
automation platform. Implementation details are abstracted from actual semiconductor
documentation engineering work.*