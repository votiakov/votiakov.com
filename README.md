# votiakov.com

Personal site of Andrii Votiakov. Static HTML and one CSS file, no build step, no trackers.

- `site/index.html`: the home page. Hero with the animated fetch ladder, results, products (Cartpie, Fabla, mieszkanko, reducecost.cloud, Apify), three case studies with SVG diagrams, how I work, now, writing, contact, background.
- `site/work/{basket,locket,hero-labs}/`: the long case studies.
- `site/assets/site.css`: the design system (light and dark, self-hosted Inter, Instrument Serif and JetBrains Mono).
- `site/assets/products/`: product screenshots (1200×750 WebP). Re-take them when a product site changes.
- `tools/og-card.html` and `tools/render.sh`: rebuild `site/og-image.png` and the icons with headless Chrome and ImageMagick.
- `RESEARCH.md`: what the best engineer and CTO sites do, and how this site uses it.
- `DEPLOY.md`: how to publish on GitHub Pages or Cloudflare Pages, with the DNS records.

Preview locally:

```sh
python3 -m http.server 8000 --directory site
# open http://localhost:8000
```

Content rules: facts only from the career knowledge base, the plain CV and the product sites themselves. First person, plain words, no em dashes, no phone number or street address. Update the "Now" block when something changes, and keep its date current.
