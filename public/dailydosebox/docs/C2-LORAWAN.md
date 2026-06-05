# DailyDoseBox C2 (care homes) — LoRaWAN Fleet Option (Stan, 2026-06-05)

**Bottom line:** For one building with dozens of boxes, LoRaWAN beats cellular on recurring cost and wifi on operational simplicity. The one constraint: the in-box chime must be a LOCAL node decision, not a cloud-pushed downlink (LoRaWAN Class A can't push a fast chime on battery). Accept that and C2-LoRaWAN is right. Keep cellular for the consumer (C1) box and for scattered single-box deployments. Don't share a transport between C1 and C2.

## Architecture
Battery node per box (reed + MCU + LoRa radio) → 1 building gateway (2 for redundancy) → network server → existing cloud/escalation engine.
- Gateway: 8-ch indoor, SX1302/03, **Basics Station** over TLS. One covers a 3-5 story home.
- Network server: **The Things Stack (TTI Cloud)** under ~500 boxes, or **AWS IoT Core for LoRaWAN** at scale. Do NOT self-host ChirpStack.
- **Class A** (battery life). **OTAA** always. **US915** (sub-band 2) / EU868. **ADR on** (fixed sensors).

## Absence detection on LoRaWAN
Two uplinks: immediate **lid-open event** + hourly **heartbeat** (battery). Cloud logic:
- Dose missed = no lid-open uplink in window → escalate.
- Node offline = no heartbeat > ~3h → alert dashboard/caregiver, do NOT tell resident they missed a dose.
Dashboard shows two orthogonal columns: adherence vs device health.
**Chime = local:** node caches its schedule; if lid not opened by window end it chimes itself (zero latency, survives gateway/backhaul outage), then uplinks "chimed." Later rungs (text/voice/caregiver/call) are cloud-side and latency-tolerant.

## Payload (fPort-keyed, DevEUI = box id)
- fPort1 lid event (2B): type(open/close) + flags(in-window, self-chimed, test).
- fPort2 heartbeat (4B): battery%, status flags, uptime hours (uint16).
- fPort3 window summary (3B): window index, outcome, battery%.
Decoder: switch on fPort, preserve raw base64, never throw on unknown port.

## Cost model (planning-grade)
- Per-node BOM ~$6-11 CHEAPER than cellular (LoRa SoC ~$3-5 vs LTE-M ~$8-12; no SIM; no carrier cert).
- Gateway $120-300 hw; ~$400-900 all-in/building incl install; double for redundant.
- Recurring: **$0 SIM.** 40-box home on cellular = 40 SIM × ~$2/mo = ~$960/yr forever. Same on LoRaWAN = one gateway (one-time) + NS at a few $/device/yr → under ~$20/mo for the whole building. Gateway pays back in ~6-12 months; gap widens per box.

## When each wins
- LoRaWAN: many boxes, one building, one owner; long battery; one dashboard, no per-resident network setup; you accept local-chime.
- Cellular: the consumer C1 box; geographically scattered single boxes (that's C1-at-scale).
- WiFi: only if boxes are mains-powered and the building has managed wifi the operator controls.
**Don't** pick Class C "so the cloud can chime instantly" — it forces mains and erases the battery advantage. Local chime on Class A is correct.
