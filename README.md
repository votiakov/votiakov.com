# votiakov.com

Personal site of Andrii Votiakov. Static HTML and one CSS file, no build step, no trackers.

- `site/index.html`: the whole site on one page. Hero with an animated Cartpie demo, six numbers, products (Cartpie, Fabla, mieszkanko, reducecost.cloud, Apify), three company stories with outcome visuals, how I work, now, writing, contact, background.
- `site/pl/` and `site/ua/`: Polish and Ukrainian versions, generated. Edit the English page, add or update the matching (en, pl, ua) pair in `tools/i18n.py`, then run `python3 tools/i18n.py`. The script stops if an English string it expects is missing.
- `site/assets/site.css`: the design system (light and dark, self-hosted Inter, Instrument Serif and JetBrains Mono; Cormorant Garamond italic stands in for the serif in Cyrillic).
- `site/assets/products/`: product screenshots (1200×750 WebP). Re-take them when a product site changes.
- `tools/og-card.html` and `tools/render.sh`: rebuild `site/og-image.png` with headless Chrome. The favicons are the portrait on the accent colour.
- `RESEARCH.md`: what the best engineer and CTO sites do, and how this site uses it.
- `DEPLOY.md`: how to publish on GitHub Pages or Cloudflare Pages, with the DNS records.

Preview locally:

```sh
python3 -m http.server 8000 --directory site
# open http://localhost:8000
```

Content rules: facts only from the career knowledge base, the plain CV and the product sites themselves. Employer work is described by role and outcome only: no internal architecture, vendors, costs or tooling of another company. First person, plain words, no em dashes, no phone number or street address. Update the "Now" block when something changes, and keep its date current.
