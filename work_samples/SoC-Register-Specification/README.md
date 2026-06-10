# SoC Register Specification — FlexCAN Module

This work sample demonstrates a production-quality IP register specification for a FlexCAN
Controller Area Network module within a 32-bit automotive SoC. The document covers register
layout, bit-field definitions, access semantics, enumerated encodings, and multi-instance
address mapping across chip variants.

It reflects a register database format designed for automated processing — the same
definitions feed into DITA-OT pipelines that generate PDF reference manuals, interactive
WebHelp, and SVG register diagrams from a single source.

## Contents

| File | Description |
|:-----|:------------|
| `flexcan_register_spec.md` | Complete register specification with reset values, access types, bit-field encodings, and functional descriptions |
| `memory_map.md` | Multi-instance SoC memory map showing base addresses, slot sizes, and per-instance parameter overrides across two chip variants |