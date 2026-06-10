# Three-Tier DITA Map Architecture for SoC Documentation

The content architecture uses a three-tier model — IP, SubSystem, SoC — where each tier
references the tier below it. This allows a single IP specification to publish both standalone
(for IP-level review by the design team) and as part of multiple SoC reference manuals
without modification or duplication.

## Tier 1: IP-Level DITA Map

Each IP block (FlexCAN, DMA, UART, GPIO, etc.) has a self-contained DITA map that can
publish independently. The map references concept topics, reference topics for register
descriptions, and task topics for programming sequences.

```
IP_FlexCAN.ditamap
├── topicref: FlexCAN_Overview.dita           (concept)
│   ├── topicref: FlexCAN_Features.dita       (reference)
│   └── topicref: FlexCAN_Block_Diagram.dita  (concept)
├── topicref: FlexCAN_Functional_Description.dita (concept)
│   ├── topicref: FlexCAN_Protocol_Engine.dita     (concept)
│   ├── [conditional] FlexCAN_CANFD_Support.dita   (concept — included only when CAN_FD_ENABLE=true)
│   └── topicref: FlexCAN_Error_Handling.dita      (concept)
├── topicref: FlexCAN_Programming_Model.dita       (concept)
│   ├── topicref: FlexCAN_Register_Summary.dita    (reference)
│   └── [generated] Register Descriptions          (auto-generated from .rdb → DITA)
├── topicref: FlexCAN_Application_Notes.dita       (concept)
│   ├── topicref: FlexCAN_Bit_Timing_Calc.dita     (reference)
│   └── topicref: FlexCAN_Initialization.dita      (task)
└── topicref: FlexCAN_Revision_History.dita        (reference)
```

### Parameter-Conditional Content

The `pm:cond_*` attributes on topicref elements determine whether a topic is included
in the output based on the resolved parameter values for a specific chip instance:

```xml
<!-- Included only when CAN_FD_ENABLE resolves to "true" for this instance -->
<topicref href="FlexCAN_CANFD_Support.dita"
          navtitle="CAN-FD Operation"
          type="concept"
          pm:cond_CAN_FD_ENABLE="true"/>

<!-- Included only when PUBLISH_MODE is "FULL" -->
<topicref href="FlexCAN_Application_Notes.dita"
          navtitle="Application Information"
          type="concept"
          pm:cond_PUBLISH_MODE="FULL"/>
```

This mechanism replaces DITAVAL filtering with a design-aware approach: parameter values
come directly from the RTL elaboration, guaranteeing that the documentation's conditional
logic matches the actual hardware configuration.

## Tier 2: SubSystem-Level DITA Map

A SubSystem (like AHB_BUS) aggregates multiple IP instances into a single documentation
scope. The SubSystem map references IP-level maps and provides SubSystem-specific
documentation.

```
SS_AHB.ditamap
├── topicref: SS_AHB_Overview.dita                                (concept)
├── topicref: ssmap:IP_DMA_SPEC   [DMA instance at 0x4001_0000]   (aggregated from IP map)
├── topicref: topicref: SS_AHB_Arbitration.dita                   (concept)
├── topicref: ssmap:IP_GPIO_SPEC  [GPIO instance at 0x4003_0000]  (aggregated from IP map)
└── topicref: SS_AHB_Register_Summary.dita                        (reference)
```

## Tier 3: SoC-Level DITA Map

The top-level SoC map aggregates multiple SubSystem maps and directly-attached IP maps.
It also includes SoC-specific chapters — clocking architecture, reset architecture,
interrupt mapping, power domains, and the complete system memory map.

```
SOC_XYZ_top.ditamap
├── SoC Overview
│   ├── topicref: SOC_Overview.dita              (concept)
│   ├── topicref: SOC_Block_Diagram.dita         (concept)
│   └── topicref: SOC_Feature_Summary.dita       (reference)
├── System Memory Map
│   └── topicref: SOC_Memory_Map.dita            (reference — auto-generated from XLSX)
├── IP Chapter References
│   ├── prmref:IP_FlexCAN_SPEC  (FlexCAN_0 at 0x4002_4000, CAN_NUM_MB=64)
│   ├── prmref:IP_FlexCAN_SPEC  (FlexCAN_1 at 0x4002_8000, CAN_NUM_MB=32)
│   ├── prmref:IP_DMA_SPEC      (DMA_engine_0 at 0x4001_0000)
│   ├── prmref:IP_UART_SPEC     (UART_inst_0 at 0x4002_C000)
│   └── prmref:IP_GPIO_SPEC     (GPIO_block_0 at 0x4003_0000)
├── SubSystem Chapters
│   └── ssmap:SS_AHB_BUS
├── SoC Architecture Chapters (AI-generated from arch spec)
│   ├── topicref: SOC_Clocking_Strategy.dita     (concept)
│   ├── topicref: SOC_Reset_Architecture.dita    (concept)
│   ├── topicref: SOC_Interrupt_Map.dita         (reference)
│   └── topicref: SOC_Power_Domains.dita         (concept)
└── SoC-Level Registers
    └── topicref: rdbref:SOC_TOP_REGS            (reference)
```

### Reference Resolution

The DITA map uses three custom reference types to compose the document:

| Reference Type | Points To | Resolution |
|:---------------|:----------|:-----------|
| `prmref:IP_*_SPEC` | An IP-level DITA map | The reference is resolved to the IP's map. Multiple prmrefs to the same IP spec with different instance names produce per-instance chapters with distinct memory map entries. |
| `ssmap:SS_*` | A SubSystem-level DITA map | The SubSystem map is pulled in, recursively expanding its own prmref and topicref children. |
| `rdbref:REG_SET` | A register resolution group defined in the `.pub` file | The DITA-OT pipeline resolves the register group, applies parameter overrides, and generates register reference topics with SVG diagrams. |

---

## Parameter Resolution Pipeline

When the DITA-OT plugin processes a DITA map, it follows this resolution order for
every topic/section:

1. **Load Parameter Definitions** — Read the `.prm` file for the current scope, establishing
   all known parameters with their default values.

2. **Apply IMAP Overrides** — The `.imap` file provides per-instance overrides. For the
   SoC-level map, the unified `SOC_XYZ_top.imap` contains all resolved parameter values
   for every IP instance.

3. **Apply Non-RTL Parameter DB** — Documentation-specific parameters (security
   classification, publish mode, document revision) that have no RTL representation are
   merged from the JSON parameter database.

4. **Validate Bounds** — Every integer parameter is checked against its `low_limit` and
   `high_limit`. Enumerated parameters are validated against `accepted_values`. Mismatches
   are reported as build errors — the pipeline refuses to publish with invalid parameters.

5. **Resolve Conditions** — All `pm:cond_*` attributes are evaluated against the resolved
   parameter values. Topics whose conditions do not match the instance configuration
   are suppressed.

6. **Generate Register Content** — The `.rdb` register database files are transformed into
   DITA reference topics with auto-generated SVG bit-field diagrams and HTML tables.

The final output is a fully resolved, parameter-free DITA document that can be processed
by the standard DITA-OT PDF or WebHelp transforms — no custom parameter handling needed
at the rendering stage. All conditional logic is resolved upstream.

*This content architecture is representative of production DITA implementations
for large-scale SoC documentation. The structure, reference types, and resolution
pipeline are abstracted from actual semiconductor documentation systems.*