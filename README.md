# votiakov.com

Personal site of Andrii Votiakov. Static HTML and one CSS file, no build step.

- `site/`: everything that is published (home page, three deep-dive pages under `work/`, 404, CV PDF, icons, OG image, robots, sitemap, CNAME).
- `tools/og-card.html` and `tools/render.sh`: rebuild `site/og-image.png` and the icons with headless Chrome and ImageMagick.
- `DEPLOY.md`: how to publish on GitHub Pages or Cloudflare Pages, with the DNS records.

Preview locally:

```sh
python3 -m http.server 8000 --directory site
# open http://localhost:8000
```

Content rules: facts only from the career knowledge base and the plain CV, plain Simplified Technical English, no phone number or street address.
