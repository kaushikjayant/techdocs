# Non-RTL Parameter Database — Design and Operation

## Problem Statement

Semiconductor documentation requires two fundamentally different classes of parameters:

- **RTL Parameters** exist in the hardware design and can be extracted automatically
  from RTL elaboration. Examples: number of DMA channels, CAN-FD enable, FIFO depth.

- **Non-RTL Parameters** are documentation-specific configurations that have no
  representation in RTL. Examples: document revision string, security classification
  label, publishing mode (full/internal/draft), chip family prefix for output paths.

Before automation, non-RTL parameters were tracked in per-chip spreadsheets maintained
individually by each technical writer. There was no schema enforcement, no versioning,
no traceability to published content, and no way to validate that a parameter value was
correct before it appeared in a shipped document.

## Design Decisions

### JSON Over SQL

The database is implemented as a Git-versioned JSON file (`nonrtl_param_db.json`)
rather than a traditional SQL database. This was an intentional design choice based
on four requirements:

1. **Version-control friendly.** A JSON file is diffable and mergeable in Git. When a
   parameter changes, the commit history shows who changed it, when, and why. Branching
   and merging work naturally — a chip variant branch can hold its parameter values
   while the main branch tracks the primary product line.

2. **Zero infrastructure.** No database server to install, configure, maintain, back up,
   or secure. The technical writing team works with the same Git workflow they already
   use for DITA source files.

3. **Schema-flexible.** The nested JSON structure naturally accommodates the
   deeply hierarchical parameter space: parameters are associated with IP instances,
   which belong to subsystems, which compose into SoCs, which belong to chip families.
   A relational schema for this would require multiple join tables; JSON expresses it
   directly.

4. **Direct consumption by pipeline tools.** Every tool in the pipeline (Python scripts,
   VS Code extension TypeScript, DITA-OT XSLT transforms, TCL automation scripts) can
   read JSON natively. No ORM, no SQL drivers, no connection strings.

### Hierarchical Organization

Parameters are organized by chip prefix, then by instance within a chip family:

```
chip_prefix: MCU_X9Z
├── instances
│   ├── FlexCAN_core_0
│   │   ├── spec_ref: IP_FlexCAN_SPEC
│   │   └── nonrtl_params: { CAN_DOC_REVISION = "Rev. 2.1", ... }
│   ├── FlexCAN_core_1
│   └── DMA_engine_0
├── subsystems
│   └── SS_AHB_BUS
└── soc_level_params: { SOC_CHIP_NAME = "MCU_X9Z", ... }
```

The `chip_prefix` serves as the primary lookup key. This enables the same instance name
(e.g., `FlexCAN_core_0`) to have different non-RTL parameter values in different chip
families (e.g., MCU_X versus MCU_Y). The enrichment step in the documentation pipeline
merges RTL parameters from the design analysis JSON with non-RTL parameters from the
database to produce a unified parameter set for each documentation instance.

## CI-Integrated Update Workflow

When a technical author adds a new non-RTL parameter to a `.prm` file or when a new
SoC is added to the memory map spreadsheet, the database must be updated. Instead of
requiring authors to manually edit the JSON file (which risks structural errors), the
system provides an automated contribution pipeline:

**Trigger Detection.** A CI hook (GitHub Actions or GitLab CI) runs on every commit
and checks whether any `.prm` or memory map `.xlsx` files were modified. If changes
are detected, the hook invokes the gap analyzer.

**Gap Analysis.** The gap analyzer diffs the `.prm` parameter definitions against
existing database entries for each chip prefix. It detects four kinds of gaps:

| Gap | Cause | Action |
|:----|:------|:-------|
| New parameter in `.prm` | A non-RTL parameter was added to a parameter definition file but the database has no entry for it | Create a contribution slot with the parameter's default value pre-filled |
| Orphaned database entry | A parameter was removed from the `.prm` but the database still holds a value | Flag the entry for removal review |
| Missing instance | A new SoC memory map defines an IP instance that has no database entry | Create a stub instance entry with `copy_from` reference to a parent chip |
| Stale instance | An IP instance exists in the database but is no longer referenced in any SoC memory map | Flag the instance for removal review |

**Contribution YAML Generation.** If gaps are found, the analyzer generates a YAML file
with empty slots for each missing parameter. Each slot is auto-assigned to the author
responsible for that specification (based on author assignments stored in the database
metadata). The YAML file is placed in a `db-contributions/` branch.

**Pull Request and Review.** The CI hook creates a PR from the `db-contributions/`
branch. The assigned authors fill in the missing values and submit for review. When
the PR is approved, a schema validator runs automatically.

**Schema Validation.** Before merge, every slot is checked:
- Integer parameters: value within `low_limit` and `high_limit` range
- Boolean parameters: value is `true` or `false`
- Enumerated parameters: value matches one of the `accepted_values`
- String parameters: no additional type validation

Validation failures block the PR merge. The author must correct the value and re-submit.

**Merge.** Once validation passes and the PR is reviewed, the branch is merged. The
updated JSON database is immediately available to the documentation pipeline.

## Chip Variant Inheritance

A common pattern in semiconductor documentation is the chip variant — a derivative
product that inherits most parameters from a parent chip but overrides a few. The
database supports this through `copy_from` directives:

```json
{
  "chip_prefix": "MCU_X9Z_LITE",
  "copy_from": "MCU_X9Z",
  "overrides": {
    "SOC_PUBLISH_MODE": "PREVIEW",
    "SOC_SECURITY_CLASS": "INTERNAL"
  }
}
```

This creates a new chip prefix that inherits all parameter values from the parent
(`MCU_X9Z`) except for the explicit overrides. No duplication of the parent's data.

## Parameter Association Registry

A `parameter_associations` section in the database tracks metadata about each non-RTL
parameter:

```
CAN_DOC_REVISION:
  description: "Document revision for FlexCAN spec"
  applies_to: ["IP_FlexCAN_SPEC"]
  type: "per_instance"
  chip_specific: true

CAN_SECURITY_CLASS:
  description: "Security classification for FlexCAN documentation"
  applies_to: ["IP_FlexCAN_SPEC"]
  type: "per_instance"
  chip_specific: true
```

This registry enables the gap analyzer to assign the correct parameter to the correct
author and validates that parameters are only applied to the specifications they belong
to.

---

*This database design is representative of production parameter management systems
used in semiconductor documentation automation. Schema details and implementation
patterns are abstracted from actual deployment experience.*