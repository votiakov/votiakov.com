## Status (live since 2026-10-13)

- GitHub Pages: repo `votiakov/votiakov.com` (public), deployed by `.github/workflows/pages.yml` on every push to `main`. Custom domain `votiakov.com`, certificate approved, HTTPS enforced.
- GoDaddy DNS (email records untouched):
  - `A @` → 185.199.108.153, 185.199.109.153, 185.199.110.153, 185.199.111.153
  - `AAAA @` → 2606:50c0:8000::153, 2606:50c0:8001::153, 2606:50c0:8002::153, 2606:50c0:8003::153
  - `CNAME www` → votiakov.github.io
  - `TXT @` → google-site-verification (Search Console domain property). Keep it, or the property loses verification.
- Google Search Console: domain property `votiakov.com` verified by DNS TXT; sitemap `https://votiakov.com/sitemap.xml` submitted; indexing requested for the home page.

# Deploying votiakov.com

The site is the static folder `site/`. There is no build step.

## Current DNS (checked 2026-10-13)

| Record | Value |
|---|---|
| Nameservers | `ns07.domaincontrol.com`, `ns08.domaincontrol.com` (GoDaddy) |
| `A @` | `15.197.148.33`, `3.33.130.190` (GoDaddy parking/forwarding; http://votiakov.com does not answer) |
| `www` | CNAME to `votiakov.com` |
| `MX @` | `smtp.secureserver.net` (0), `mailstore1.secureserver.net` (10) |
| `TXT @` | `v=spf1 include:secureserver.net -all` |

Do not change the MX and TXT (SPF) records. They belong to GoDaddy email.

## Option A: GitHub Pages (recommended)

DNS stays at GoDaddy. You only replace the web records.

1. Create a public repo, for example `votiakov/votiakov.com`, and push this folder.
2. Repo **Settings → Pages → Source: GitHub Actions**. The workflow in `.github/workflows/pages.yml` publishes `site/` on every push to `main`.
3. Optional, but recommended: **GitHub profile Settings → Pages → Add a verified domain** `votiakov.com`. Add the TXT record that GitHub shows (`_github-pages-challenge-votiakov`). This stops other accounts from taking over the domain.
4. At GoDaddy (**My Products → votiakov.com → DNS**):
   - Turn off domain forwarding, if it is on.
   - Delete the two `A @` records `15.197.148.33` and `3.33.130.190`.
   - Add these records:

   | Type | Name | Value |
   |---|---|---|
   | A | @ | 185.199.108.153 |
   | A | @ | 185.199.109.153 |
   | A | @ | 185.199.110.153 |
   | A | @ | 185.199.111.153 |
   | AAAA | @ | 2606:50c0:8000::153 |
   | AAAA | @ | 2606:50c0:8001::153 |
   | AAAA | @ | 2606:50c0:8002::153 |
   | AAAA | @ | 2606:50c0:8003::153 |
   | CNAME | www | votiakov.github.io |

5. Repo **Settings → Pages → Custom domain**: `votiakov.com`. Wait for the DNS check to pass, then tick **Enforce HTTPS** (the certificate can take up to about an hour).
6. Check: `dig +short votiakov.com` shows the four `185.199.x.153` addresses, and https://www.votiakov.com redirects to https://votiakov.com.

`site/CNAME` already contains `votiakov.com`. The Actions deployment uses the domain from the Pages settings; the file is there for the branch-based deployment too.

## Option B: Cloudflare Pages

Cloudflare Pages needs the domain's nameservers at Cloudflare for an apex domain (`votiakov.com` without `www`).

1. Add `votiakov.com` to a free Cloudflare account. Check that the imported DNS has the MX and SPF records above, then change the nameservers at GoDaddy to the two that Cloudflare gives you.
2. Deploy one of two ways:
   - **Connect the repo:** Workers & Pages → Create → Pages → Connect to Git. Framework preset: none. Build command: empty. Build output directory: `site`. The repo can be private.
   - **Direct upload:** `npx wrangler pages deploy site --project-name votiakov-com`
3. Pages project → **Custom domains** → add `votiakov.com` and `www.votiakov.com`. Cloudflare creates the records:

   | Type | Name | Value |
   |---|---|---|
   | CNAME (flattened) | @ | votiakov-com.pages.dev |
   | CNAME | www | votiakov-com.pages.dev |

4. Delete the old GoDaddy `A @` records (`15.197.148.33`, `3.33.130.190`) if Cloudflare imported them. HTTPS is automatic.

## Why A is recommended

- No nameserver change, so the GoDaddy email records stay as they are.
- Free, the deploy is a git push, and the workflow file is already in the repo.
- Option B is better if you want a private repo or plan to move DNS to Cloudflare anyway.

## After it is live

- Add https://votiakov.com to the LinkedIn profile (Contact info → Website, and the Featured section).
- Paste a page URL into https://www.linkedin.com/post-inspector/ to refresh the preview image (`og-image.png`).
- After a CV change: `python3 scripts/cv/build_plain_cv.py` in the job-search repo, then copy `cv/plain/Andrii_Votiakov_CV.pdf` to `site/Andrii_Votiakov_CV.pdf`.
- After a change to the portrait or the card text: `sh tools/render.sh` rebuilds `og-image.png` and the icons.
- fabla.si answers only on http (it redirects to fabla.pl). Set up HTTPS for fabla.si at the registrar, or change the link to https://fabla.pl.
