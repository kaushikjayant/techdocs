# Designing a Hierarchical Content Architecture for Multi-Product Semiconductor Documentation

**Published:** June 2026 | **Category:** Content Architecture, DITA, Semiconductor

---

When your documentation needs to support a single IP specification that publishes
standalone, as part of a SubSystem manual, and as part of multiple SoC-level
Reference Manuals — all without content duplication — you need a content architecture
that understands hierarchy, parameterization, and conditional resolution. This article
describes the three-tier DITA model I designed for large-scale SoC documentation and
the design decisions that made it work across five product lines.

## The Problem: One Source, Many Publications

A modern SoC integrates dozens of IP blocks. Each IP has a reusable documentation
specification. That specification must publish in at least three contexts:

1. **Standalone IP Manual** — for the IP design team to review register definitions,
   programming models, and functional descriptions in isolation

2. **SubSystem Manual** — aggregating multiple IPs that share a bus, clock domain,
   or functional grouping

3. **SoC Reference Manual** — the full-chip document that includes every IP instance
   at its resolved base address, with chip-specific parameter overrides applied

The challenge is that these are not three separate documents. They are three views
of the same source material, each with different scope, different addresses, and
different parameter-driven content inclusion rules.

The solution requires a content architecture where:

- IP-level content is authored once and never duplicated
- Parameter values are resolved per-instance, not hard-coded
- Conditional content (e.g., CAN-FD support documentation) is included or excluded
  based on the instance's actual hardware configuration, not the writer's guess
- DITA maps compose hierarchically — IP into SubSystem, SubSystem into SoC — with
  parameter values cascading downward through the hierarchy

## The Three-Tier Model

### Tier 1: IP-Level DITA Maps

Each IP block — FlexCAN, DMA, UART, GPIO — has a self-contained DITA map that
serves as the authoritative source for that IP's documentation structure. The map
references concept topics (functional descriptions, block diagrams), reference topics
(register summaries, revision histories), and task topics (initialization sequences,
programming examples).

The IP map uses custom `pm:cond_*` attributes on `topicref` elements to mark content
as parameter-conditional:

```xml
<topicref href="FlexCAN_CANFD_Support.dita"
          navtitle="CAN-FD Operation"
          pm:cond_CAN_FD_ENABLE="true"/>
```

This topic is included only when the `CAN_FD_ENABLE` parameter resolves to `true`
for a given instance. At the IP level — where the map publishes standalone for
design review — the parameter's default value is used. At the SoC level, the
instance-specific override value drives the inclusion decision.

The IP map can publish independently. Running the DITA-OT pipeline against the
IP map alone produces a standalone FlexCAN manual suitable for IP-level design
review. This is critical for the IP design team, who need to review register
definitions and functional descriptions without waiting for SoC-level integration.

### Tier 2: SubSystem-Level DITA Maps

A SubSystem — such as the AHB bus SubSystem — aggregates multiple IP instances.
The SubSystem map contains custom `ssmap` references that pull in IP-level maps
with SubSystem-specific parameter overrides:

```xml
<topicref href="ssmap:IP_DMA_SPEC"
          navtitle="DMA Controller"/>
<topicref href="ssmap:IP_GPIO_SPEC"
          navtitle="GPIO Controller"/>
```

The `ssmap` reference type tells the DITA-OT plugin to resolve the referenced IP
map, apply the SubSystem-level parameter overrides from the instance map, and
insert the resolved content at the SubSystem level.

The SubSystem map also contains SubSystem-specific topics — arbitration
architecture, bus performance characteristics, address space allocation — that are
not part of any individual IP specification.

### Tier 3: SoC-Level DITA Map

The top-level SoC map is the most complex. It references:

- **IP maps directly** (`prmref`) for IPs that attach directly to the SoC fabric
- **SubSystem maps** (`ssmap`) that themselves contain IP references
- **SoC-specific chapters** for clocking architecture, reset architecture, interrupt
  mapping, and power domains — many of which are AI-generated from the architecture
  specification and reviewed by human authors

The SoC map also defines the global parameter context. When the SoC-level instance
map overrides `CAN_NUM_MB=32` for `FlexCAN_1`, that override propagates through
the hierarchy, affecting every conditional content decision in the FlexCAN IP map
for that instance.

## Parameter Resolution Pipeline

The parameter resolution follows a strict four-step sequence:

**Step 1: Load parameter definitions.** The IP-level `.prm` file establishes the
universe of known parameters and their default values for that IP. Parameters not
declared in any `.prm` file generate build warnings.

**Step 2: Apply IMAP overrides.** The instance map provides per-instance parameter
overrides. At the SoC level, the unified IMAP file contains all resolved parameter
values for every IP instance, sourced from RTL elaboration and the Non-RTL
Parameter Database.

**Step 3: Apply Non-RTL overrides.** Documentation-specific parameters — security
classification, publish mode, revision strings — are merged from the JSON parameter
database. These override any values from Steps 1 and 2.

**Step 4: Validate bounds.** Every integer parameter is checked against its declared
range. Enumerated parameters are checked against their accepted values list.
Validation failures stop the build — the pipeline refuses to publish with
invalid parameters.

After resolution, the resulting DITA is fully parameter-free. All conditional
content decisions have been made. The output can be processed by the standard
DITA-OT PDF or WebHelp transforms without any custom parameter handling.
All conditional logic is resolved upstream, at build time, based on values that
flow directly from the hardware design.

## What Made This Work in Production

Several architectural decisions proved critical:

**Parameter values come from RTL, not from writers.** The IMAP files that drive
parameter resolution are generated by the design analysis pipeline, not written
by documentation authors. This eliminates the class of errors where a writer
hard-codes a parameter value that diverges from the RTL.

**The `.prm` file is the contract.** Every parameter — RTL and non-RTL — is declared
in a `.prm` file with a type, default value, and constraints. The build system
enforces these constraints at every stage. A parameter that appears in an IMAP
override but is not declared in any `.prm` file generates a build error.

**Conditional content uses parameter values, not DITAVAL.** The `pm:cond_*`
mechanism replaces DITAVAL filtering because parameter values have semantic
meaning — they represent hardware configuration choices — while DITAVAL values
are arbitrary metadata. When the documentation says "include this topic if
CAN-FD is enabled," it reflects a real hardware condition, not an editorial
preference.

**The three-tier model reflects the actual hardware hierarchy.** IP maps map to
IP blocks. SubSystem maps map to bus domains. SoC maps map to chips. This
alignment between documentation structure and hardware structure makes the
architecture intuitive for both documentation authors and hardware engineers.

---

*This architecture was designed for production semiconductor documentation
and has been deployed across multiple product lines with 40+ authors.*