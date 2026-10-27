# CircleWeb · Marzban subscription template

A responsive subscriber page based on the supplied CircleWeb brandbook and identity kit. Deep ink, signal lime, the original vector logo, embedded Inter, Poppins, and AradNL for Persian, and English / Persian with RTL layout.

## What is included

- Actual Marzban account status, data usage, remaining allowance, expiry, and reset schedule.
- Unlimited plans and on-hold, disabled, expired, and limited accounts.
- Streisand and Happ import, subscription clipboard copy, local QR codes, individual configuration copy / QR, and copy all.
- Setup instructions, connection help, light / dark theme, keyboard focus, and reduced-motion support.
- No analytics, external runtime fonts, JavaScript CDN, or external QR service. Fonts, vector assets, styles, scripts, and QR encoder are embedded in one HTML file.

## Install on your Marzban server

The deployable file is `templates/subscription/index.html`. The `preview/index.html` file contains sample data and must not be installed as the server template.

1. Copy the deployable file to `/var/lib/marzban/templates/subscription/index.html` on your server. Back up any existing template first.
2. Set these entries in your existing Marzban `.env` (usually `/opt/marzban/.env`), replacing existing values rather than duplicating them:

```dotenv
CUSTOM_TEMPLATES_DIRECTORY="/var/lib/marzban/templates/"
SUBSCRIPTION_PAGE_TEMPLATE="subscription/index.html"
```

3. If you use Docker, ensure `/var/lib/marzban` is mounted into the container at the same path. Preserve existing volumes and settings.
4. Restart Marzban with `marzban restart`, or use the restart command appropriate to your installation.
5. Open a subscriber’s HTTPS subscription URL in a browser. Marzban renders the template with that subscriber’s `user` object.

Only the single deployable HTML file is needed at runtime. No Node, Python build tools, or asset route is required on your server. Existing Marzban configuration-generation templates remain under Marzban’s fallback template loader; retain any custom templates you already use.

Use your subscriber domain with HTTPS. This page displays subscription status, not live tunnel connectivity or server latency. App launch requires the selected app (Streisand or Happ) to be installed; clipboard import is the fallback. The buttons use `streisand://import/<subscription-url>` and `happ://add/<subscription-url>`; the copied link and QR code remain the plain subscription URL for either app. Actual app handoff and your server installation need a final smoke check on your device.

## Preview and development

Open `preview/index.html` directly in a browser, or serve the `preview` directory. The preview uses fictional data; its import, copy, and QR actions are intentionally disabled.

```sh
python3 scripts/build.py
python3 -m venv .venv
.venv/bin/pip install -r requirements-dev.txt
.venv/bin/python scripts/preview.py
.venv/bin/python -m unittest discover -s tests -v
python3 -m http.server 4173 --directory preview --bind 127.0.0.1
```

Edit `src/page.html`, `src/styles.css`, and `src/app.js`, then rebuild. Build itself uses only the Python standard library. Jinja2 is required only for preview rendering and template tests.

Stored theme and language preferences are the only localStorage values. Subscription tokens are not stored in localStorage. Account data comes from the server-rendered page; reload it for current usage. The UI uses binary data units (1024 bytes per KB), matching Marzban’s byte-based accounting.

## Verification

Five template tests cover state serialization, enum and string compatibility, omitted optional fields, injection escaping, embedded assets, and byte values. Browser checks covered desktop and mobile layouts, Persian RTL, light mode, QR generation, and clipboard copying using a fictional subscription link. This has not been deployed to a live Marzban instance.

## Upstream references and licenses

- [Marzban subscription setup](https://gozargah.github.io/marzban/en/docs/subscription)
- [Marzban subscription router and user context](https://github.com/Gozargah/Marzban/blob/master/app/routers/subscription.py)
- [Streisand developer website](https://streisand.pages.dev/)
- [Streisand App Store](https://apps.apple.com/app/streisand/id6450534064)
- [Happ official downloads](https://happ.info/)
- QRCode.js: MIT, license in `vendor/qrcode.LICENSE`.
- Inter and Poppins: SIL OFL, licenses in `assets/`.
- CircleWeb logos and `assets/AradNL-VF.woff2` are user-supplied branding assets. AradNL is embedded as a variable WOFF2 font for the Persian interface.
# m-template
