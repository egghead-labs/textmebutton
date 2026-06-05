# DailyDoseBox — Hardware / Firmware / Provisioning Spec v1.0 (Otto, 2026-06-05)

**Bottom line:** Cellular LTE-M + mains USB-C + small backup cell is the only architecture that does *absence* detection with in-room audio. The 3-word code is a provisioning convenience, NOT the security boundary: bind it to the device ID at the factory, claim-on-first-setup, rate-limit lookups, PIN for caregiver changes.

## 1. Architecture
- **Sensor:** reed switch in lid + magnet in body (zero quiescent current). Edge interrupt wake, 50ms debounce. Keep magnet 15mm+ from ferrous hinge hardware.
- **Link:** LTE-M primary, NB-IoT fallback (one modem). LTE-M needed for low-latency two-way to trigger in-room chime/voice. No wifi (defeats the no-password goal).
- **Audio local, triggered remote:** chime + spoken message play from onboard speaker + audio flash; cloud sends "play rung N" downlink. No audio streaming.
- **Power:** USB-C mains primary; backup 18650 (LiFePO4 for thermal safety) + charger, sized to ride through an outage AND report "lost mains" as a distinct alert. Battery-free harvesting is off the table.

### Rough BOM (100-500 units, USD/unit)
Cellular modem (nRF9160 SiP or Quectel BG95) $12-18 · soldered eSIM $1.50+plan · LTE antenna $1.50 · reed $0.30 · magnet $0.15 · audio amp+speaker $2.50 · SPI flash 8-16MB $0.80 · USB-C + charger PMIC $2.00 · backup cell+protection $4.50 · RTC $0.50 · RGB LED $0.10 · PCB+passives+assembly $8-12. **Electronics subtotal ~$38-50** (wood enclosure separate). Pick: **nRF9160** (integrated M33, mature Zephyr/NCS, no separate host MCU).

## 2. Heartbeat + watchdog (the heart of the product)
Silence is the signal, so never confuse "box can't talk" with "dose not taken." Two independent timers.
- **Heartbeat every 15 min** (CoAP/UDP, tens of bytes): box_id, fw, uptime, last_lid_open_ts, lid_state, power_source, battery_pct, rssi, seq, local_rung.
- **Immediate uplink on lid-open.**
- **Timer A "box offline":** no heartbeat ~40 min → mark OFFLINE, alert caregiver (connectivity issue, NOT a dose alert).
- **Timer B "dose missed":** dose window passes with no lid-open AND box ONLINE → run ladder. If OFFLINE, hold dose escalation, run offline alert instead.
- **Escalation ladder:** rung1 chime (box, fires autonomously even offline via RTC+cached schedule), rung2 text (cloud +15m), rung3 spoken message (box local audio +30m), rung4 caregiver text (cloud +60m), rung5 call (cloud +90m). Box owns rungs 1&3; cloud owns anything with a phone book.

## 3. 3-word code ↔ identity
- Factory: each box gets immutable IMEI + eSIM IMSI/ICCID. 3-word code is a **separately assigned** label mapped to IMEI (do NOT derive words from IMEI). Words + QR encode the same code.
- **Wordlist: 2048 curated words, 3 words = 8.59B combos.** Centrally assigned = zero collisions by construction; random-guess hits a live box ~1 in 86,000 at 100k fleet. Curate: 4-7 letters, common, no homophones/profanity, and screen whole 3-word combos for offensive phrasing.
- **Security:** the code is visible on the lid, so: (1) claim-on-first-setup binds it; after that the code alone can't reconfigure; (2) rate-limit `/demo/<words>` (per-IP + global, backoff, CAPTCHA) — REQUIRED for the endpoint; (3) PIN / SMS second factor for caregiver-facing changes; (4) re-claim needs verified reset. Guessing isn't the threat; line-of-sight to the lid is, which claim+PIN neutralizes.

## 4. Firmware modules + cloud record
Modules: lid_sensor, rtc_clock, schedule_cache, escalation_local, audio, modem_mgr, telemetry, downlink, power_mgr, provisioning, ota, watchdog_hw.
Cloud box record: box_id, three_words(idx), imei/imsi/iccid, qr_url, fw_version, status(PROVISIONED|READY|CLAIMED|OFFLINE|RETIRED), claimed_by/at, owner_phone, caregiver_phones[], pin_hash, dose_schedule[], last_heartbeat_ts, last_seq, last_lid_open_ts, power_source, battery_pct, rssi, current_dose_window_state, escalation_rung, alert_log[]. `status` (connectivity) is orthogonal to the dose-window state machine by design.

## 5. Top risks + next prototype
1. Cellular reliability indoors + data-plan economics. 2. Backup-cell ride-through + "lost mains" alert latency. 3. False missed-dose from the offline/window race (trust killer).
**Cheapest de-risk:** breadboard nRF9160 DK + reed + eSIM running ONLY heartbeat + offline-watchdog vs a throwaway endpoint; leave on home cellular a week, yank mains a few times, confirm cloud distinguishes offline / lost-mains / missed-dose with no false positives. Validates risks 1-3 at once.
Decisions for BOM lock: nRF9160 (rec) vs BG95; LiFePO4 (rec) vs Li-ion backup.
