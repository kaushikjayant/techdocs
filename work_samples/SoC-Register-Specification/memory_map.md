# FlexCAN Multi-Instance SoC Memory Map

This document shows how a single FlexCAN IP specification is deployed across multiple
chip variants with different instance counts, base addresses, and parameter configurations.
This is the documentation equivalent of the RTL `generate` block — one IP spec, multiple
instantiated documentation views.

---

## MCU_X9Z (Automotive Grade)

| Instance | Base Address | End Address | Slot Size | CAN_NUM_MB | CAN_FD_ENABLE | CAN_CLK_FREQ | DMA Support |
|:---------|:------------|:------------|:---------:|:----------:|:-------------:|:------------:|:-----------:|
| FlexCAN_0 | 0x4002_4000 | 0x4002_7FFF | 16 KB | 64 | Yes | 80 MHz | Yes |
| FlexCAN_1 | 0x4002_8000 | 0x4002_BFFF | 16 KB | 32 | No | 80 MHz | No |
| FlexCAN_2 | 0x400A_0000 | 0x400A_3FFF | 16 KB | 64 | Yes | 80 MHz | Yes |

**Chip Configuration:**
- 3 CAN instances covering body, chassis, and powertrain buses
- FlexCAN_0 handles the high-speed powertrain CAN-FD bus (64 mailboxes, DMA-assisted)
- FlexCAN_1 is a legacy CAN 2.0B interface for body control (32 mailboxes, polling only)
- FlexCAN_2 mirrors FlexCAN_0 configuration for chassis/safety bus redundancy
- Wake-up capable on all instances for partial networking support

---

## MCU_Y7Z (Industrial)

| Instance | Base Address | End Address | Slot Size | CAN_NUM_MB | CAN_FD_ENABLE | CAN_CLK_FREQ | DMA Support |
|:---------|:------------|:------------|:---------:|:----------:|:-------------:|:------------:|:-----------:|
| FlexCAN_0 | 0x4002_4000 | 0x4002_7FFF | 16 KB | 32 | No | 60 MHz | No |
| FlexCAN_1 | 0x4002_8000 | 0x4002_BFFF | 16 KB | 16 | No | 60 MHz | No |

**Chip Configuration:**
- 2 CAN instances for industrial control applications
- Both instances operate CAN 2.0B only (no FD), reflecting the plant-floor environment
- Reduced mailbox count reflects simpler message filtering requirements
- Lower clock frequency matches the industrial temperature range timing constraints
- No DMA — all transfers handled by interrupt-driven software

---

## Parameter Override Table

The same IP specification (`IP_FlexCAN_SPEC`) publishes with different parameter values
depending on the target chip. This table shows how parameter overrides propagate from
the SoC-level memory map into the published documentation.

| Parameter | IP Default | MCU_X9Z FlexCAN_0 | MCU_X9Z FlexCAN_1 | MCU_Y7Z FlexCAN_0 |
|:----------|:----------:|:-----------------:|:-----------------:|:-----------------:|
| CAN_NUM_MB | 64 | 64 | 32 | 32 |
| CAN_FD_ENABLE | true | true | false | false |
| CAN_CLK_FREQ | 80 MHz | 80 MHz | 80 MHz | 60 MHz |
| CAN_RXFIFO_DEPTH | 32 | 32 | 16 | 16 |
| CAN_TXMB_COUNT | 8 | 8 | 4 | 4 |
| CAN_DMA_ENABLE | false | true | false | false |
| CAN_MEM_MAP_OFFSET | 0x4000 | 0x4000 | 0x4000 | 0x4000 |
| CAN_DOC_REVISION | Rev 2.1 | Rev 2.1 | Rev 2.1 | Rev 2.0 |
| CAN_SECURITY_CLASS | CONFIDENTIAL | CONFIDENTIAL | CONFIDENTIAL | INTERNAL |

---

## Address Space Layout — MCU_X9Z

```
0x4000_0000 ┌─────────────────────────────┐
            │       AHB Bus SubSystem      │
0x4001_0000 ├─────────────────────────────┤
            │         DMA Engine           │  4 KB
0x4001_1000 ├─────────────────────────────┤
            │         (reserved)           │
0x4002_4000 ├─────────────────────────────┤
            │       FlexCAN_0              │  16 KB
0x4002_8000 ├─────────────────────────────┤
            │       FlexCAN_1              │  16 KB
0x4002_C000 ├─────────────────────────────┤
            │       UART Instance 0        │  4 KB
0x4003_0000 ├─────────────────────────────┤
            │      GPIO Block 0            │  4 KB
0x4003_4000 ├─────────────────────────────┤
            │         (reserved)           │
0x400A_0000 ├─────────────────────────────┤
            │       FlexCAN_2              │  16 KB
0x400A_4000 └─────────────────────────────┘
```

---

## Multi-Instance Publishing Rules

When multiple instances of the same IP exist, the documentation system applies these
publishing rules:

1. **Common Register Descriptions:** Published once. The first instance's register fields
   are documented in full. Subsequent instances reference the first instance with an
   "Identical to FlexCAN_0 except as noted" annotation.

2. **Per-Instance Memory Map:** Each instance gets its own entry in the SoC memory map
   table, showing its unique base address and parameter values.

3. **Parameter-Conditional Content:** Documentation sections that depend on parameter
   values (e.g., "CAN-FD Operation") are included or excluded based on each instance's
   resolved `CAN_FD_ENABLE` value. A chip with mixed CAN-FD/CAN 2.0 instances includes
   the CAN-FD chapter, with a note that it applies only to FlexCAN_0 and FlexCAN_2.

4. **Address Collision Detection:** The automation system validates that no two IP
   instances overlap in the memory map. Address space collisions are flagged during the
   build process and prevent publication.

---

*This memory map is representative of production SoC documentation conventions.
Instance counts, addresses, and parameter values are illustrative of actual automotive
and industrial chip configurations.*