# FlexCAN Module Register Specification

**Module:** FlexCAN v2.4 — Controller Area Network with Flexible Data-Rate (CAN-FD)
**Register Width:** 32-bit
**IP Version:** 2.4.1
**Document Status:** Preliminary — Rev 0.9

---

## Register Summary

| Offset | Mnemonic | Name | Access | Reset Value | Description |
|:------:|:---------|:-----|:------:|:-----------:|:------------|
| 0x00 | MCR | Module Configuration Register | RW | 0x5000_000F | Global module control, freeze, halt, supervisor mode |
| 0x04 | CTRL1 | Control 1 Register | RW | 0x0000_0000 | Operation mode, bit-timing limits, prescaler |
| 0x08 | TIMER | Free-Running Timer | RW | 0x0000_0000 | 16-bit timestamp for received/transmitted frames |
| 0x10 | RXMGMASK | Rx Mailbox Global Mask | RW | 0xFFFF_FFFF | Global acceptance mask for Rx mailboxes 0–13 |
| 0x14 | RX14MASK | Rx Mailbox 14 Mask | RW | 0xFFFF_FFFF | Individual mask for mailbox 14 |
| 0x18 | RX15MASK | Rx Mailbox 15 Mask | RW | 0xFFFF_FFFF | Individual mask for mailbox 15 |
| 0x1C | ECR | Error Counter Register | RO | 0x0000_0000 | Transmit and receive error counts, fault confinement state |
| 0x20 | ESR1 | Error and Status Register 1 | RO | 0x0000_0000 | Bus-off, error, warning status flags |
| 0xA4 | MB_CS_0 | Message Buffer 0 CS | RW | 0x0000_0000 | Message buffer 0 control/status (first of N mailboxes) |

---

## Module Configuration Register (MCR) — Offset 0x00

Contains global module control and configuration bits. Affects all message buffers and the
protocol engine. This register must be written while the module is in freeze mode
(FRZ_ACK = 1 in ESR1).

**Reset value:** 0x5000_000F

| Bit(s) | Name | Access | Reset | Description |
|:------:|:-----|:------:|:-----:|:------------|
| 31 | MDIS | RW | 0 | Module Disable. When set, clocks are gated, reducing dynamic power. 0 = enabled, 1 = disabled. The module must enter freeze mode before setting this bit. |
| 30 | FRZ | RW | 0 | Freeze Enable. 0 = freeze mode disabled, 1 = module enters freeze mode upon assertion of FRZ_ACK. Used to halt the protocol engine for register reconfiguration. |
| 29 | RFEN | RW | 1 | Rx FIFO Enable. Enables the receive FIFO. When disabled, mailbox 0–15 operate as standard mailboxes. |
| 28 | HALT | RW | 0 | Halt FlexCAN. Suspends all transmit and receive operations. 0 = normal operation, 1 = halted. |
| 27 | NOTRDY | RO | 0 | FlexCAN Not Ready. Hardware sets this bit during power-up and low-power exit. Read-only; cleared by hardware when the module is ready. |
| 26 | WAKEMSK | RW | 0 | Wake-up Interrupt Mask. 0 = wake-up interrupt disabled, 1 = enabled. |
| 25 | SOFTRST | RW | 0 | Soft Reset. Writing 1 resets all internal state machines and FIFOs. Self-clearing; reads always return 0. |
| 25:24 | CLK_SRC | RW | 00 | Clock Source selection. 00 = oscillator clock (SOSC), 01 = peripheral clock (IPG), 10 = external clock input, 11 = reserved. |
| 23:19 | — | — | — | Reserved. Must be written with zeros. |
| 18 | SUPV | RW | 0 | Supervisor Mode. 0 = user mode access permitted, 1 = supervisor mode only for write access to protected registers. |
| 17 | SRX_DIS | RW | 0 | Self Reception Disable. When set, frames transmitted by this module are not received internally. Reduces software overhead for transmit-only nodes that do not need to monitor their own traffic. |
| 16 | IRMQ | RW | 0 | Individual Rx Masking and Queue Enable. 0 = single global mask for mailboxes 0–13, individual masks for 14–15, 1 = dedicated mask per mailbox supported. |
| 15 | DMA | RW | 0 | DMA Enable. Enables DMA request generation on receive/transmit events. |
| 14:8 | — | — | — | Reserved. |
| 7:0 | MAXMB | RW | 0x0F | Maximum Number of Message Buffers. Defines the upper mailbox index (0 to 127). Mailboxes 0 to MAXMB-1 are active; higher-numbered mailboxes and their associated memory are inaccessible. Power-on default = 15 (16 mailboxes). |

### MAXMB Field Configuration Guide

The MAXMB field determines how many message buffers are active in the IP instance.
The value written is the index of the last active mailbox:

| MAXMB Value | Active Mailboxes | Typical Configuration |
|:-----------:|:-----------------|:---------------------|
| 0x0F (15) | 0–15 (16 mailboxes) | Default — basic CAN 2.0B configuration |
| 0x1F (31) | 0–31 (32 mailboxes) | Typical CAN-FD deployment |
| 0x3F (63) | 0–63 (64 mailboxes) | Gateway configuration with heavy message filtering |
| 0x7F (127) | 0–127 (128 mailboxes) | Maximum — requires full SRAM allocation |

**Note:** Changing MAXMB requires freeze mode. The hardware re-allocates SRAM on MAXMB
update. Mailboxes above MAXMB cannot be referenced; their SRAM is reclaimed.

### MDIS Field Power Management

When MDIS = 1, the module enters a low-power state:
- Protocol engine clock is gated
- Message buffer SRAM clock is gated
- Register interface remains accessible for reads (excluding status registers that depend on the protocol engine)
- Wake-up detection remains active if WAKEMSK = 1

Exiting MDIS = 1 requires a software sequence: clear MDIS, poll NOTRDY until cleared by hardware
(typically 2–3 IPG clock cycles), then reinitialize the protocol engine if needed.

---

## Control 1 Register (CTRL1) — Offset 0x04

Primary control register for protocol timing, operation mode, and interrupt masks.

**Reset value:** 0x0000_0000

| Bit(s) | Name | Access | Reset | Description |
|:------:|:-----|:------:|:-----:|:------------|
| 31:24 | PRESDIV | RW | 0x00 | Prescaler Division Factor. Divides the PE clock (IPG) to generate the Serial Clock (Sclock). Valid range: 1–256 (0 = divide by 1). Baud rate = PE_clock / (PRESDIV + 1) / Time Quanta per bit. |
| 23:22 | RJW | RW | 00 | Resynchronization Jump Width. Maximum adjustment to a bit period during resynchronization. 0 = 1 Tq, 3 = 4 Tq. Must satisfy: RJW ≤ min(PSEG1, PSEG2). |
| 21:19 | PSEG1 | RW | 000 | Phase Segment 1. Time quanta in phase buffer segment 1. Valid values: 1–8 (mapped as 2–9 Tq). |
| 18:16 | PSEG2 | RW | 000 | Phase Segment 2. Time quanta in phase buffer segment 2. Valid values: 0–7 (mapped as 1–8 Tq). Must be ≥ IPT (Information Processing Time). |
| 15 | BOFF_MSK | RW | 0 | Bus-Off Interrupt Mask. 0 = interrupt disabled, 1 = bus-off condition triggers interrupt. |
| 14 | ERR_MSK | RW | 0 | Error Interrupt Mask. Enables interrupt generation when error counters reach warning limits. |
| 13 | TWRN_MSK | RW | 0 | Tx Warning Interrupt Mask. Interrupt when Tx error counter transitions from < 96 to ≥ 96. |
| 12 | RWRN_MSK | RW | 0 | Rx Warning Interrupt Mask. Interrupt when Rx error counter transitions from < 96 to ≥ 96. |
| 11 | — | — | — | Reserved. |
| 10 | LPB | RW | 0 | Loop Back mode. 0 = normal operation, 1 = internal loopback. Transmitter output is internally connected to receiver input. Used for self-test; TX pin is driven recessive in loopback mode. |
| 9:8 | SMP | RW | 00 | Sampling Mode. 00 = one sample per bit (recommended), 01 = three samples per bit (legacy, for noisy environments), 10/11 = reserved. |
| 7 | BOFF_REC | RW | 0 | Bus-off Recovery Mode. 0 = automatic recovery per CAN spec (128 occurrences of 11 recessive bits), 1 = manual recovery through software. |
| 6 | TSYN | RW | 0 | Timer Sync Mode. 0 = timer increments continuously, 1 = timer reset on every received SOF. |
| 5 | LBUF | RW | 0 | Lowest Buffer Transmitted First. 0 = message buffer with lowest ID transmitted first (arbitration on CAN ID), 1 = lowest buffer number transmitted first (local priority). |
| 4 | LOM | RW | 0 | Listen-Only Mode. 0 = normal operation, 1 = receive only, no acknowledgment, no error flags. Used for bus monitoring. |
| 3:0 | PROPSEG | RW | 0000 | Propagation Segment. Number of time quanta in the propagation delay segment. Valid values: 1–8 (mapped as 2–9 Tq). |

### Bit Timing Configuration Example

For a 40 MHz PE clock with a target 500 kbps baud rate:

1. Choose Time Quanta = 16 (PROPSEG=3, PSEG1=4, PSEG2=4, Sync=1 → 3+4+4+1 = 12 Tq... recalculate)
2. Actually: PROPSEG=3 → 4 Tq, PSEG1=4 → 5 Tq, PSEG2=4 → 5 Tq, Sync=1 Tq = 15 Tq total
3. Baud rate = 40,000,000 / (PRESDIV + 1) / 15
4. For 500 kbps: PRESDIV = (40,000,000 / 500,000 / 15) - 1 ≈ 4.33 → use 4, actual baud ≈ 40M/(5×15) = 533 kbps
5. Fine-tune: PRESDIV = 5 → 40M/(6×16 with adjusted segments) = 416 kbps... iterative adjustment required

**Recommended values for 40 MHz PE clock:**

| Target Baud Rate | PRESDIV | PROPSEG | PSEG1 | PSEG2 | RJW | Actual Rate |
|:----------------:|:-------:|:-------:|:-----:|:-----:|:---:|:-----------:|
| 1 Mbps | 1 | 5 | 3 | 2 | 1 | 1.05 Mbps |
| 500 kbps | 4 | 3 | 4 | 3 | 1 | 494 kbps |
| 250 kbps | 9 | 3 | 4 | 3 | 1 | 248 kbps |
| 125 kbps | 19 | 3 | 4 | 3 | 1 | 124 kbps |

---

## Free-Running Timer (TIMER) — Offset 0x08

16-bit free-running timer that captures a timestamp on each valid CAN frame.
Used for time-stamping received and transmitted messages.

**Reset value:** 0x0000_0000

| Bit(s) | Name | Access | Reset | Description |
|:------:|:-----|:------:|:-----:|:------------|
| 15:0 | TIMER | RW | 0x0000 | Timer value. Increments on each CAN bit time when the module is not in freeze mode. Writable in freeze mode. Rollover from 0xFFFF to 0x0000 triggers the timer overflow interrupt if enabled. |

---

## Rx Mailbox Global Mask (RXMGMASK) — Offset 0x10

Global acceptance mask applied to Rx mailboxes 0–13 (when IRMQ = 0 in MCR). A 1 in a
mask bit means "must match"; a 0 means "don't care." The incoming frame ID is compared
against the mailbox's ID after masking.

**Reset value:** 0xFFFF_FFFF (all bits must match)

| Bit(s) | Name | Access | Reset | Description |
|:------:|:-----|:------:|:-----:|:------------|
| 31:1 | MI[31:1] | RW | All 1s | Mask bits for standard and extended ID match. Bit 31 aligns with the IDE (extended ID flag) bit in the CAN frame, bits 30:1 align with the extended identifier. |
| 0 | MI[0] | RW | 1 | Mask bit for RTR/SRR match. |

### Standard ID Filtering Example

To accept standard IDs 0x100 through 0x1FF on mailbox 0:
1. Write the desired base ID to mailbox 0's ID field: 0x100 (with IDE=0)
2. Write RXMGMASK to 0x700 (bits 10:8 are 1, all others 0 — only upper 3 bits of standard ID must match)
3. Incoming frames with IDs 0x100–0x1FF will be accepted by mailbox 0

---

## Error Counter Register (ECR) — Offset 0x1C

Contains the transmit and receive error counters and fault confinement state as defined
by the CAN 2.0B specification.

**Reset value:** 0x0000_0000

| Bit(s) | Name | Access | Reset | Description |
|:------:|:-----|:------:|:-----:|:------------|
| 15:8 | RXERRCNT | RO | 0x00 | Receive Error Counter (0–255). Incremented on receive errors (CRC, form, bit, stuff), decremented on successful reception. |
| 7:0 | TXERRCNT | RO | 0x00 | Transmit Error Counter (0–255). Incremented on transmit errors, decremented on successful transmission. |

### Fault Confinement State (derived from error counters)

| State | TXERRCNT | RXERRCNT | Behaviour |
|:------|:--------:|:--------:|:----------|
| Error Active | 0–95 | 0–95 | Normal participation. Error frames sent with active error flags (6 dominant bits). |
| Error Passive | 96–127 | 96–127 | Reduced participation. Error frames sent with passive error flags (6 recessive bits). No further dominant bits after transmission. |
| Bus-Off | ≥ 256 | — | Module disconnected from bus. TX pin driven recessive. Recovery per BOFF_REC setting in CTRL1. |

---

## Error and Status Register 1 (ESR1) — Offset 0x20

Reports current error conditions, interrupt flags, and module status.

**Reset value:** 0x0000_0000

| Bit(s) | Name | Access | Reset | Description |
|:------:|:-----|:------:|:-----:|:------------|
| 31 | FLT_CONF | RO | 0 | Fault Confinement State. 0 = error active, 1 = error passive. |
| 30 | — | — | — | Reserved. |
| 29 | BOFF_INT | W1C | 0 | Bus-Off Interrupt. Set when the module enters bus-off state. Write 1 to clear. |
| 28 | ERR_INT | W1C | 0 | Error Interrupt. Set when either error counter exceeds 96, indicating transition to error-passive. Write 1 to clear. |
| 27 | WAK_INT | W1C | 0 | Wake-up Interrupt. Set when the module detects activity on the CAN bus while in stop mode. Write 1 to clear. |
| 26 | TWRN_INT | W1C | 0 | Tx Warning Interrupt. Set when TXERRCNT transitions to ≥ 96. Write 1 to clear. |
| 25 | RWRN_INT | W1C | 0 | Rx Warning Interrupt. Set when RXERRCNT transitions to ≥ 96. Write 1 to clear. |
| 24 | — | — | — | Reserved. |
| 23:16 | — | — | — | Reserved. |
| 15:4 | — | — | — | Reserved. |
| 3 | STF_ERR | W1C | 0 | Stuffing Error. A sequence of 5 consecutive bits of the same polarity was not followed by a complementary bit. |
| 2 | FRM_ERR | W1C | 0 | Form Error. A fixed-format bit field contained an unexpected value. |
| 1 | CRC_ERR | W1C | 0 | CRC Error. The CRC sequence of a received frame did not match the calculated CRC. |
| 0 | BIT1_ERR | W1C | 0 | Bit 1 Error. A transmitted recessive bit was sampled as dominant (except in arbitration or ACK slot). |

---

## Message Buffer Control/Status (MB_CS_0) — Offset 0xA4 (Mailbox 0)

Each message buffer (mailbox) has a 16-bit control/status word followed by the ID field
and 8 bytes of data. MB_CS_0 through MB_CS_N-1 are located at offsets
0xA4 + (N × 16).

**Reset value:** 0x0000_0000

| Bit(s) | Name | Access | Reset | Description |
|:------:|:-----|:------:|:-----:|:------------|
| 31:24 | TIME_STAMP | RO | 0x00 | Free-running timer value captured at the SOF of the frame in this buffer. |
| 23:22 | CODE | RW | 00 | Message buffer code. Controls the buffer's current operation. See encoding table below. |
| 21 | SRR | RW | 0 | Substitute Remote Request. For standard frames: 1 = remote frame requested. For extended frames: must be 1. |
| 20 | IDE | RW | 0 | ID Extended. 0 = standard 11-bit ID, 1 = extended 29-bit ID. |
| 19 | RTR | RW | 0 | Remote Transmission Request. 0 = data frame, 1 = remote frame. |
| 18:16 | DLC | RW | 000 | Data Length Code. Number of data bytes in the frame (0–8 for CAN 2.0, 0–64 for CAN-FD). Values 8–15 encode 8 for CAN 2.0; for CAN-FD see table below. |
| 15:0 | — | — | — | Reserved, or part of the TIME_STAMP extended field in some implementations. |

### Message Buffer Code (CODE) Encoding

| CODE[1:0] | RX Buffer State | TX Buffer State |
|:---------:|:----------------|:----------------|
| 00 | Inactive — buffer not used | Inactive — buffer not used |
| 01 | — (reserved for RX) | Transmit data ready. Buffer will be sent when it wins arbitration. After successful transmission, CODE resets to 10 (if transmitting once) or stays 01 (if repeating). |
| 10 | Empty — buffer ready to receive | — (reserved for TX). Set after successful tx of a non-repeating buffer, or to abort transmission. |
| 11 | Full — buffer contains received frame | — (reserved for TX). Set by hardware when a matching frame is received. Software must read data and set CODE back to 10 to re-arm. |

### CAN-FD Data Length Code (DLC) Encoding

| DLC[3:0] | Data Bytes (CAN 2.0) | Data Bytes (CAN-FD) |
|:---------|:---------------------|:--------------------|
| 0000 | 0 | 0 |
| 0001 | 1 | 1 |
| 0010 | 2 | 2 |
| 0011 | 3 | 3 |
| 0100 | 4 | 4 |
| 0101 | 5 | 5 |
| 0110 | 6 | 6 |
| 0111 | 7 | 7 |
| 1000 | 8 | 8 |
| 1001 | 8 (clamped) | 12 |
| 1010 | 8 (clamped) | 16 |
| 1011 | 8 (clamped) | 20 |
| 1100 | 8 (clamped) | 24 |
| 1101 | 8 (clamped) | 32 |
| 1110 | 8 (clamped) | 48 |
| 1111 | 8 (clamped) | 64 |

---

## Register Access Key

| Mnemonic | Meaning | Behaviour |
|:---------|:--------|:----------|
| RW | Read/Write | Software can read and write. Value persists. |
| RO | Read Only | Hardware sets; software reads. Write has no effect. |
| WO | Write Only | Software writes; read returns 0 (or undefined). Used for command registers. |
| W1C | Write 1 to Clear | Read returns current flag value. Writing 1 clears the flag; writing 0 has no effect. Standard interrupt flag behaviour. |
| RZ | Read as Zero | Always returns 0 on reads. Writes ignored. |

---

*This register specification is a work sample from production SoC documentation.
The register definitions are representative of an automotive-grade FlexCAN module.
All values, addresses, and field descriptions reflect actual hardware behaviour.*