# votiakov.com

Personal site of Andrii Votiakov. Static HTML and one CSS file, no build step, no trackers.

- `site/index.html`: the home page. Hero with an animated Cartpie lookup demo (a real Primark product, as the free playground on cartpie.com returns it), six numbers, products (Cartpie, Fabla, mieszkanko, reducecost.cloud, a SHEIN data strip, Apify), three company stories with outcome visuals, how I work, now, writing, contact, background.
- `site/shein-data/index.html`: since 2026-11-12 an instant redirect (meta refresh plus canonical) to cartpie.com/datasets/shein. cartpie.com is the only place that sells and describes the data; this site links to it and carries no Dataset structured data. The old page is in git history. `og.png` stays for old shares.
- `site/samples/`: the SHEIN sample zips. Keep them: posts and READMEs link here. cartpie.com hosts identical copies under `/samples/`.
- `site/reports/`: downloadable reports, such as `shein-by-the-numbers-uk-2026-10.pdf`.
- `site/assets/site.css`: the design system (light and dark, self-hosted Inter, Instrument Serif and JetBrains Mono).
- `site/assets/products/`: product screenshots (1200×750 WebP). Re-take them when a product site changes.
- `tools/og-card.html`, `tools/og-shein.html` and `tools/render.sh`: rebuild `site/og-image.png` and `site/shein-data/og.png` with headless Chrome. The favicons are the portrait on the accent colour.
- `RESEARCH.md`: what the best engineer and CTO sites do, and how this site uses it.
- `DEPLOY.md`: how to publish on GitHub Pages or Cloudflare Pages, with the DNS records.

Preview locally:

```sh
python3 -m http.server 8000 --directory site
# open http://localhost:8000
```

Content rules: facts only from the career knowledge base, the plain CV and the product sites themselves. Employer work is described by role and outcome only: no internal architecture, vendors, costs or tooling of another company. First person, plain words, no em dashes, no phone number or street address. Update the "Now" block when something changes, and keep its date current.
