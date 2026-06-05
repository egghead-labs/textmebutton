# DailyDoseBox

The pill box that texts you back. A wooden medication box with a contact switch in
the lid: open it during your daily dose window and that is your check-in. Miss the
window and it escalates (chime → text → spoken message → caregiver text → call).

A daily check-in aid, **not a medical device**. Reports whether the box was opened,
not whether a dose was taken.

## Pages
- `index.html` — landing / marketing page
- `setup.html` — the per-box setup page the lid QR resolves to (`/setup?box=<id>`)
- `assets/` — real product photo, QR-on-lid composite, branded QR card
- `build_assets.py` — regenerates the QR card + lid composite (set `URL` / `BOX_ID`)

## Brand
Navy `#0E2A3B` · Teal `#14B8A6` · Coral `#FF6B5E`.

## Hosting
Static site. Deployed to Cloudflare Pages (`dailydosebox.pages.dev`).
Production domains (to attach): **dailydosebox.com** (primary) and **dosebox.com**.

Sibling product to TextMeButton; shares the one-action setup pattern, separate brand.
