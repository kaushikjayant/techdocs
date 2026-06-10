# Managing Non-RTL Parameters for SoC Documentation: A Git-Versioned Approach

**Published:** June 2026 | **Category:** Parameter Management, DevOps, Semiconductor

---

Not every parameter in a semiconductor documentation system comes from the RTL.
Document revision strings, security classification labels, publishing mode
configurations, and chip family prefixes have no representation in the hardware
design — they live exclusively in the documentation domain. Yet they must be
managed with the same rigour as RTL-extracted parameters: version-controlled,
schema-validated, and auditable.

I built a JSON-based Non-RTL Parameter Database with a CI-integrated contribution
workflow to address exactly this problem. Here's how it works and why JSON beat SQL.

## The Problem: Shadow Configuration

Before the system existed, non-RTL parameters were managed in per-chip spreadsheets
maintained individually by each technical writer. The problems were predictable
and severe:

- **No versioning.** When a security classification changed from "Internal" to
  "Confidential," there was no record of who changed it, when, or why. If the change
  caused a downstream issue — a watermarked PDF that shouldn't have been watermarked
  — there was no commit history to audit.

- **No schema enforcement.** A writer could type "CONFIDENTIAL" (misspelled), and
  the build system would silently accept it. The published document would be missing
  its security watermark because the parameter didn't match any recognized value.

- **No traceability.** When the same IP appeared on three different chips with three
  different document revision strings, there was no way to guarantee consistency.
  Each writer maintained their own copy of the revision string, and they diverged.

- **No automation integration.** The spreadsheets were consumed by humans, not by
  scripts. Every time a parameter value was needed, a writer had to open the
  spreadsheet, find the right cell, and transcribe the value into an XML file.

## The Solution: JSON as a Database

I made an intentionally unconventional choice: implementing the parameter database
as a Git-versioned JSON file rather than using SQL. This decision was driven by
four requirements specific to the documentation workflow:

**Version-control integration.** Technical writers already use Git for DITA source
files. Adding a JSON file to the same repository means parameter changes are
tracked in the same commit history, reviewed through the same pull request process,
and deployed through the same CI pipeline. No new tools, no new workflows.

**Zero infrastructure.** A JSON file requires no database server, no connection
management, no backup infrastructure beyond what Git already provides. For a
documentation team with no dedicated DBA, this is not a convenience — it's a
necessity.

**Hierarchical data representation.** The parameter space is deeply nested:
parameters belong to IP instances, which belong to subsystems, which compose
into SoCs, which belong to chip families. A relational schema for this would
require multiple join tables and recursive queries. JSON represents the hierarchy
directly, matching the way writers already think about parameter associations.

**Direct consumption by Python and JavaScript.** The pipeline tools are written
in Python and TypeScript. Both languages parse JSON natively. No ORM, no SQL
drivers, no connection strings. The JSON file is read into memory as a dictionary
and manipulated with standard language constructs.

## The Contribution Workflow

Manual editing of the JSON file — even by experienced technical writers — is
error-prone. A missing comma or a misplaced brace breaks the entire database.
The solution is a CI-integrated contribution workflow that automates discovery
and validation while keeping humans in control of the values.

### Trigger Detection

A CI hook runs on every commit. It checks whether any `.prm` parameter definition
files or memory map `.xlsx` spreadsheets were modified. If changes are detected,
the hook invokes the gap analyzer. If no relevant files changed, the hook exits
cleanly — no overhead on unrelated commits.

### Gap Analysis

The analyzer diffs `.prm` parameter definitions against existing database entries
for each chip prefix. It detects four kinds of gaps:

**New parameter gap:** A writer adds a `source=nonrtl` parameter to a `.prm` file
but the JSON database has no entry for it. The analyzer creates a contribution slot
with the parameter's default value pre-filled from the `.prm` definition.

**Orphaned entry:** A parameter is removed from the `.prm` but the database still
holds a value. The entry is flagged for removal review — someone may still need it
for a legacy chip variant.

**Missing instance:** A new SoC memory map adds an IP instance that has no database
entry. The analyzer creates a stub instance entry with a `copy_from` reference to
the parent chip, inheriting all existing parameter values.

**Stale instance:** An IP instance exists in the database but is no longer
referenced in any SoC memory map. The instance is flagged for removal.

### Contribution YAML

If gaps are found, the analyzer generates a YAML file with empty slots for each
gap. Each slot is auto-assigned to the author responsible for that specification
(based on a simple author assignment map stored in the database metadata).

```yaml
slots:
  - action: add_param
    param_id: CAN_DOC_REVISION
    spec_ref: IP_FlexCAN_SPEC
    chip_prefix: MCU_X9Z
    assigned_to: can-team
    status: pending
    value: null
    notes: "Auto-detected new non-RTL parameter in .prm"
```

The YAML file is placed in a `db-contributions/` directory and committed to a
new branch.

### Pull Request and Validation

The CI hook creates a PR. The assigned author fills in the missing values and
submits for review. When the PR is approved, a schema validator runs automatically
and checks every slot:

- Integer parameters: value within `low_limit` and `high_limit`
- Boolean parameters: value is `true` or `false`
- Enumerated parameters: value matches one of the `accepted_values`
- String parameters: no type validation beyond being a string

Validation failures block the merge. The author must correct the value and push
a fixup commit. Only when all slots pass validation and the PR is reviewed does
the branch merge.

## What I Would Do Differently

The JSON database has worked well in production — it's simple, version-controlled,
and directly consumable by all pipeline tools. But at scale (50+ chip variants,
hundreds of IP instances), some limitations emerged:

**Concurrent edits are hard.** Two writers editing the same JSON file on different
branches creates merge conflicts. A proper database with transactional writes
would eliminate this, at the cost of infrastructure complexity.

**Schema evolution is manual.** When the JSON structure changes (adding a new
field, renaming a key), every consumer of the database must be updated. A
formal schema (JSON Schema or Protocol Buffers) would enforce structure at
the interface boundary.

**Querying is linear.** Finding "all parameters for FlexCAN instances across
all chip families" requires iterating through the entire nested structure.
A query language (even a simple JSON path expression language) would help.

For the scale the system currently operates at (five product lines, roughly
40 active authors, hundreds of non-RTL parameters), these limitations are
acceptable tradeoffs against the operational simplicity of a flat JSON file
in a Git repository.

---

*This database design is abstracted from a production system. Implementation
details have been generalized.*