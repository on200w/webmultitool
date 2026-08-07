# Webmultiverktøy

En samling frittstående nettbaserte verktøy. Ingen backend, ingen bygg-steg — hvert verktøy er én HTML-fil med inline CSS og JavaScript. Åpne [index.html](index.html) i nettleseren for å starte.

## Mappestruktur

```
index.html                 Hovedmeny med lenker til alle verktøy/kategorier
tools/
  qr/index.html            Undermeny: velg mellom enkel og utvidet QR-generator
  qr-simple/index.html      QR-kode generator (enkel)
  qr-plus/index.html        QR-kode generator (utvidet)
  innhold/index.html        Undermeny: plakat, infoskjerm og video
  plakat/index.html         Plakatgenerator
  infoskjerm/index.html     Infoskjerm-planlegger
  video/index.html          Videomanus-kort
  fargepalett/index.html    Fargepalett-verktøy
  tekstteller/index.html    Tekst-/ord-teller
  strekkode/index.html      Strekkode-generator
```

## Verktøy

| Verktøy | Beskrivelse |
| --- | --- |
| QR-kode generator (enkel) | Generer QR-koder med farge og logo, last ned som PNG/JPG/SVG. |
| QR-kode generator (utvidet) | Som over, pluss feilkorrigeringsnivå, størrelse, margin og auto-generering. |
| Plakatgenerator | Lag plakater med tittel, tekst og kontaktfelt i flere formater, last ned som PNG. |
| Infoskjerm-planlegger | Bygg en spilleliste med slides og forhåndsvis den som en automatisk loop. |
| Videomanus-kort | Scene-for-scene manus med varighet, eksporter til tekstfil. |
| Fargepalett-verktøy | Lag nyanser og beslektede farger fra en basisfarge, sjekk WCAG-kontrast mellom to farger. |
| Tekst-/ord-teller | Tell tegn, ord, setninger og avsnitt, og få et estimat på lesetid. |
| Strekkode-generator | Lag strekkoder (CODE128, EAN, UPC, CODE39, ITF-14), last ned som PNG eller SVG. |

## Design

Alle sider deler samme fargepalett og stil:

- `--brand-green: #009d4f`
- `--brand-deep-green: #005850`
- `--brand-light: #cfd2d3`
- `--text: #12332f`
- `--muted: #385552`
- `--border: #afbbbb`

Hver verktøyside har en "Tilbake"-lenke til foreldrenivået (kategori eller hovedmeny).

## Eksterne avhengigheter

Lastes fra CDN kun der det trengs, ingen `npm install`:

- `qrcode-generator` (QR-verktøyene)
- `JsBarcode` (strekkode-generatoren)
