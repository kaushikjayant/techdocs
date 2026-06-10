# DITA Content Architecture — Semiconductor Specifications

This work sample demonstrates a hierarchical DITA content architecture for semiconductor
documentation. It shows how IP-level, SubSystem-level, and SoC-level specifications are
structured using custom parameter-driven DITA extensions that enable single-source publishing
across multiple chip variants.

## Content Architecture

| File | Description |
|:-----|:------------|
| `ditamap_structure.md` | Three-tier DITA map hierarchy with parameter-conditional topic inclusion rules |
| `publication_rules.md` | Publishing manifest that defines register resolution groups, instance selectors, and merging strategies |