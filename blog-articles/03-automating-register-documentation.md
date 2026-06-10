# Automating Register Documentation: From RTL to Published Spec

**Published:** June 2026 | **Category:** Register Documentation, Automation, Semiconductor

---

Register documentation is the most error-prone activity in semiconductor technical
writing. A single SoC contains thousands of registers, each with multiple bit fields,
access semantics, reset values, and enumerated encodings. A single transcription error
— a wrong address, a swapped MSB/LSB, an outdated reset value — can propagate into
customer-facing errata.

I spent the better part of a year designing a system that eliminates manual register
documentation entirely. Here's how it works, and what I learned about bridging the
gap between RTL design and published documentation.

## The Scale of the Problem

A mid-range automotive SoC might contain 10,000 to 15,000 individually documented
registers. Each register has:

- An offset address within its IP block's memory map
- A register width (8, 16, 32, or 64 bits)
- An access type (read/write, read-only, write-1-to-clear, etc.)
- A reset value
- Between 1 and 32 bit fields, each with its own name, bit range, access type, and
  functional description
- Enumerated encodings for multi-bit fields

In a traditional workflow, a technical writer receives this information from the
design team — typically as a spreadsheet export, a SystemRDL file, or an IP-XACT
description — and manually transcribes it into the documentation format (DITA XML,
FrameMaker tables, or structured Markdown). Every value is typed by hand.

The error rate for manual transcription of register data is not zero. Studies within
my organization found that roughly 12% of manually transcribed register entries
contained at least one error — wrong offset, wrong access type, outdated reset value,
or bit-field range mismatch. These errors survived multiple review cycles because
reviewers were comparing the documentation to the same (potentially outdated)
spreadsheet rather than to the authoritative RTL source.

## The Solution: Register Database as Single Source of Truth

The foundation of the solution is a **register database** — a structured XML format
that defines every register, bit field, access type, reset value, and encoding for
an IP block. This database is the single source of truth for all register-level
documentation across the IP.

The key insight: the register database must be **machine-writable as well as
machine-readable**. The pipeline must be able to generate it, validate it, and
transform it — writers should never manually type register values into it.

The pipeline generates the register database through three paths:

**Path 1: RTL Extraction (Verific/Yosys).** The design elaboration engine extracts
register definitions directly from the RTL. This requires the design to follow
consistent register declaration patterns — SystemVerilog structs with standard
naming conventions, IP-XACT metadata embedded in RTL attributes, or separate
SystemRDL descriptions that accompany the RTL.

**Path 2: Hjson Import (OpenTitan/Reggen model).** Many teams define registers in
human-readable Hjson or YAML files that serve as input to both RTL generation and
documentation generation. The pipeline imports these files and converts them to
the standard register database format.

**Path 3: Conversion from IP-XACT/SystemRDL.** For teams using IEEE 1685 IP-XACT
or Accellera SystemRDL, the pipeline includes converters that produce the standard
format without loss of information.

Once the register database exists, it feeds directly into the DITA-OT publishing
pipeline, which transforms it into DITA reference topics with auto-generated
SVG bit-field diagrams.

## Register Validation: Catching Errors Before Publication

Having a machine-readable register database is necessary but not sufficient. The
database must be validated against the RTL source. The pipeline implements a
validation step that cross-references every register entry against the elaborated
design:

- **Offset validation:** Does the documented offset match the RTL-elaborated address?
- **Reset value validation:** Does the documented reset value match the RTL default?
- **Bit-field range validation:** Do the documented MSB/LSB match the RTL bit positions?
- **Access type validation:** Does the documented access type (RW/RO/W1C) match the
  RTL implementation?
- **Register existence:** Are there registers in the documentation that don't exist
  in the RTL? Are there registers in the RTL that aren't documented?

Any mismatch generates a build error. The pipeline refuses to publish documentation
with unvalidated register entries. This single enforcement eliminated a class of
post-silicon errata that had previously been caught only during customer integration.

## SVG Register Diagrams: Documentation That Engineers Actually Read

One complaint I consistently heard from hardware engineers: "I don't read the register
tables. I look at the diagram." The solution was auto-generated SVG register diagrams
that render directly from the register database.

Each diagram shows:

- The register name and offset at the top
- Colour-coded bit-field blocks: Blue for read/write, green for read-only, orange
  for write-1-to-clear
- Bit-field names displayed inline within each block
- A legend and reset value annotation

The diagrams are generated by a Python script that reads the register database,
computes the visual layout (bit-field widths, colours, spacing), and writes SVG XML
directly. No manual diagram creation. No Visio files. No screenshot exports.

The result is that every register in the published Reference Manual has a consistent,
accurate, auto-generated SVG diagram that reflects the actual hardware — because it's
generated from the same data that feeds the RTL-to-documentation validation step.

## The Hardest Part

The technical components of this system — the XML formats, the SVG generation, the
validation logic — were straightforward to implement. The hard part was cultural.

Register documentation has always been "the writer's responsibility" — a manual task
that lives in the documentation domain. Moving the source of truth from the writer's
document to a machine-generated database that lives in the RTL repository required
renegotiating responsibilities between the design team and the documentation team.

The compromise that worked: **IP designers own the register database format and content.
Technical writers own the functional descriptions and the presentation layer. The
validation pipeline enforces consistency between the two.**

Designers are responsible for ensuring the register database accurately reflects the
RTL. Writers are responsible for writing clear, useful descriptions of what each
register and bit field does. The pipeline guarantees that the two never diverge.

---

*This article describes a production register documentation system. Specific
implementation details have been generalized.*