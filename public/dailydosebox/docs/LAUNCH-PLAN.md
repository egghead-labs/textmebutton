# DailyDoseBox — Launch Plan & PM Brief (Tom, 2026-06-05)

## BUILD NOW (prioritized website gaps)
1. **Pricing page** — biggest conversion blocker; no price signal today. ✅ built (`pricing.html`)
2. **/demo entry page** — "got a box? enter your 3 words." ✅ built (`demo.html`)
3. **FAQ / "what does it need to work?"** — top objection (wifi? phone nearby? cost?). ✅ built (`faq.html`)
4. **Ongoing-cost / subscription clarity** — say it plainly. (addressed in pricing + FAQ)
5. **Real product photo on hero** — using the real box composite. ✅
6. **"How it connects" one-liner** — cellular, no wifi/hub. (added to FAQ)
7. **Real waitlist backend** — the Notify form collected nothing (P0). ✅ wired to Cloudflare KV via `/api/waitlist`.

## Pricing (PROPOSED / DRAFT — confirm against real BOM)
Core tension: texts/calls cost money (~$1-5/box/mo at scale). Two honest models:
- **Maya's "no subscription" model:** $99 / $169 / $399 one-time, alerts included. Sharpest weapon vs MedMinder/Hero ($40-65/mo). Risk: carrying cellular cost forever.
- **Tom's hybrid:** $129 founder hardware + 12 months service included, then $59-79/yr. Safer on unit economics.
Shipped page uses the founder one-time framing with an honest connectivity note. Lock numbers after Otto's BOM spike.

## Launch timeline
- **Phase 0 (now–Aug 2026):** Otto's <$300 spike (nRF9160 + reed + SIM + Firebase + Twilio). GATE: unplug mid-window → cloud shows "offline" distinct from "missed dose." Fix waitlist backend (done). 
- **Phase 1 (Sep–Oct):** buy domains, ship pricing/FAQ/demo pages, real photos, start FCC/CE/cellular cert quotes (3-5 mo lead).
- **Phase 2 (Nov):** pre-order / Kickstarter, locked pricing, working prototype + demo video.
- **Phase 3 (Q1 2027):** ship (buffer to Q2).

## Top risks
1. Cellular in a wood box at consumer price (the spike).
2. Certification lead time (4-6 mo).
3. BOM → price (founder $ only works if COGS < ~$55-65).
4. Waitlist size at campaign launch (capture emails NOW).
5. Single-source enclosure supplier.

## QA verdict: FIX (not REDO)
Applied: real waitlist backend; absolute nav links; softened "dashboard exists" claim; setup page back-link, spoken-message length hint, plain `///` slashes; footer links to pricing/faq. Design + honesty (not-a-medical-device) approved.

## The open decision (founder)
Plugged-in cellular (full features + subscription, honest) vs battery-only (cut voice + cloud absence detection). Everything assumes cellular. Resolve right after the spike.
