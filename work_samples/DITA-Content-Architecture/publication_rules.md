# Publishing Rules for Multi-Instance Semiconductor Specs

When a single IP specification publishes across multiple SoC configurations, a publishing
manifest defines how register instances are resolved, merged, and rendered. This document
describes the structure and logic of these publishing rules.

## Publishing Manifests

A publishing manifest is paired with a DITA map and controls four aspects of the build:

1. **Register resolution groups** — which register database files to process and which instances to include
2. **Merging rules** — how to handle multi-instance content (keep first, merge, concatenate)
3. **Output configuration** — where to write resolved DITA, PDF, and WebHelp
4. **Parameter resolution order** — the sequence for loading and overriding parameters

## Register Resolution Groups

Each register set is wrapped in a _resolve group_. The group links to an instance map,
selects a specific instance, and defines how its registers should be rendered.

```
resolve_group: FLEXCAN_CORE_REGS
├── instance_selector (type: imap)
│   ├── imap_ref → IP_FlexCAN_top.imap
│   └── select_imap → FlexCAN_core_0
├── merging_rules
│   ├── common_region_strategy: keep_first
│   ├── address_grouping: concatenate
│   └── merge_on_field: register_offset
└── output_regmap
    └── format: dita_table_with_diagram
```

When multiple instances of the same IP exist (FlexCAN_0, FlexCAN_1, FlexCAN_2), each
gets its own resolve group. The merge-on-field rule tells the pipeline to group registers
by offset, keeping the first instance's register descriptions and generating a memory
map table showing each instance's base address and any parameter differences.

## Merging Strategies

| Strategy | Behaviour | When to Use |
|:---------|:----------|:------------|
| `keep_first` | The first instance's register descriptions are published in full. Subsequent instances contribute only address and override information to the memory map table. | Most common — identical IP instances where only base addresses differ. |
| `merge` | Register descriptions are merged. If two instances have different parameter values (e.g., FlexCAN_0 has 64 mailboxes, FlexCAN_1 has 32), both configurations are documented with instance-tagged annotations. | Complex IPs with significant per-instance configuration differences. |
| `duplicate` | Each instance gets its own fully-rendered register chapter. | Rare — used when instances have fundamentally different register layouts (e.g., different IP versions on the same chip). |

## Address Grouping

| Strategy | Behaviour |
|:---------|:----------|
| `concatenate` | All instances appear in a single memory map table, ordered by base address. FlexCAN_0, FlexCAN_1, FlexCAN_2 appear as consecutive rows. |
| `interleave` | Register descriptions from multiple instances are interleaved at the register-offset level — useful for comparative documentation. |
| `separate` | Each instance gets its own memory map section with a dedicated heading. A prefix or suffix differentiates instance chapters. |

## Parameter Resolution Order

The publishing pipeline resolves parameters in a strict four-step sequence. Each step
can override values from the previous step:

**Priority 1: Load parameter definitions (`.prm`)**

The IP-level, SubSystem-level, and SoC-level parameter definition files establish the
universe of known parameters and their default values. If a parameter is not declared in
any `.prm` file, the pipeline treats it as unknown and issues a build warning.

**Priority 2: Load IMAP overrides (`.imap`)**

The instance map provides per-instance parameter overrides. These values come from the
RTL design elaboration (for RTL parameters) or from the Non-RTL Parameter Database (for
documentation-specific parameters). IMAP overrides replace default values.

**Priority 3: Apply Non-RTL Parameter DB overrides**

The JSON-based Non-RTL Parameter Database may contain chip-specific overrides for
documentation parameters. These are applied after IMAP overrides, allowing the
documentation team to adjust security classifications, publish modes, and revision
strings without modifying the RTL-generated `.imap` files.

**Priority 4: Validate bounds**

Every parameter value is validated:
- Integer parameters: checked against `low_limit` and `high_limit`
- Boolean parameters: must be `true` or `false`
- Enumerated parameters: must match one of the `accepted_values`
- String parameters: no validation beyond type

Validation failures stop the build. The error report includes the parameter name,
the invalid value, the expected range or accepted values, and the instance path
where the violation occurred. This catches errors like "FlexCAN_0 configured with
CAN_NUM_MB=256 when the IP maximum is 128" before the error reaches the published
document.

## Output Configuration

The final section of the publishing manifest specifies where output artifacts are written:

```xml
<output_config>
  <target name="dita_resolved" dir="../../output/resolved_dita/"/>
  <target name="pdf" dir="../../output/pdf/" template="corporate_rm_template.xsl"/>
  <target name="webhelp" dir="../../output/webhelp/" skin="modern_skin"/>
  <memory_map include_offset_bars="true"/>
</output_config>
```

The resolved DITA is an intermediate artifact — fully parameter-resolved but still in
DITA XML format. It becomes the input for both the PDF and WebHelp transforms. The PDF
target uses a custom XSL-FO stylesheet that matches corporate publication standards
( headers, footers, watermarking based on security classification). The WebHelp target
produces responsive HTML5 with collapsible TOC, full-text search, and bookmark
persistence.

---

*These publishing rules are representative of production DITA-OT configurations for
semiconductor documentation. The manifest structure, merge strategies, and resolution
pipeline reflect actual build systems used for multi-instance SoC specifications.*