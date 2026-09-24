# AX Gaia Intelligence website

Static company website published by GitHub Pages from the root of `main`.

## Editing and publishing

For a local development preview in PowerShell, run
`powershell -NoProfile -ExecutionPolicy Bypass -File .\preview.ps1`, then open
http://localhost:8000. Keep that terminal running, refresh after edits, and stop
with Ctrl+C. This serves local files only and does not publish anything.
The script binds to this computer only. Cloudflare-specific `_headers` are
not applied by this simple local preview server.

- `index.html` and `privacy.html` contain the page content.
- `assets/index.css` and `assets/privacy.css` contain page styles.
- `assets/site.js` updates the copyright year.
- `assets/coastal-intelligence.png` is an AI-generated conceptual illustration
  used in the reference-inspired layout. Its heatmaps are illustrative, not
  measured site data or evidence of completed validation.
- The platform diagram and process timeline are responsive HTML/CSS. The
  development details expand without JavaScript.
- Keep `CNAME` set to `axgaiaintelligence.com`.
- Preview using a local HTTP server, not a `file://` URL. Check both pages,
  navigation, images, email links, and the browser console before publishing.
- Pushing to `main` publishes the changes through the existing Pages setup.

## Security baseline

Both pages restrict scripts, styles, and images to this site's origin using a
Content Security Policy. Inline scripts/styles, embedded frames, plugins,
network API calls, and form submissions are blocked. Keep future styles and
scripts in local files; review the policy before adding integrations.

The policy is delivered through HTML metadata. It cannot enforce
`frame-ancestors` to prevent other sites embedding this site; that directive
requires an HTTP response header from a hosting provider or proxy. Referrer
metadata and external-link attributes reduce information shared on navigation.

Do not commit credentials, private documents, customer data, or internal product
code. `.gitignore` helps prevent accidental additions but does not remove files
already tracked or secrets in history. Rotate any exposed credential immediately.

## Owner settings to verify

These settings are not changed by editing the website:

1. Enable **Enforce HTTPS** in repository Settings > Pages.
2. Verify the custom domain in the owning account's Pages settings using the
   DNS TXT record GitHub supplies. Keep that verification record.
3. Enable two-factor authentication for GitHub and the domain registrar; review
   collaborators and restrict write access to people who maintain the site.
4. Enable secret scanning and push protection where available.
5. Confirm the account's plan supports Pages from private repositories before
   changing repository visibility. GitHub Free requires a public repository for
   Pages; a private-repository host migration is another option. Preserve the
   live website and domain configuration during any transition.

A private repository hides the repository and history from general browsing,
but visitors can still download the HTML, CSS, JavaScript, and images served by
the public website. Previously public clones cannot be recalled.

References:
- https://docs.github.com/en/pages/getting-started-with-github-pages/securing-your-github-pages-site-with-https
- https://docs.github.com/en/pages/configuring-a-custom-domain-for-your-github-pages-site/verifying-your-custom-domain-for-github-pages
- https://developer.mozilla.org/en-US/docs/Web/HTTP/Reference/Headers/Content-Security-Policy/frame-ancestors

## Prepared migration: Cloudflare Pages

Cloudflare Pages supports private GitHub repositories and custom domains on its
Free plan. The domain registration stays with the current registrar.

1. Create a Cloudflare Pages project connected only to this GitHub repository.
   Select `main`, framework preset **None**, build command `sh build.sh`, and
   output directory `dist`. The build copies only public website assets.
2. Test the generated `pages.dev` preview on desktop and mobile: both pages,
   images, navigation, email links, and console errors. Confirm response headers
   include the policy in `_headers`, including `frame-ancestors 'none'`.
   `_headers` is Cloudflare configuration; GitHub Pages does not apply it.
3. Export current DNS records. Add the domain to Cloudflare and verify all
   imported records, especially email MX, SPF, DKIM, DMARC and verification TXT
   records. Check DNSSEC with the registrar before a nameserver change; coordinate
   any existing DS record with the new DNS provider to avoid resolution failures.
4. Change nameservers at the registrar to the exact pair Cloudflare assigns.
   Preserve existing GitHub website DNS records until Cloudflare DNS is active.
   In the Pages project's **Custom domains**, add `axgaiaintelligence.com` and
   follow its DNS setup. Add `www` too if currently used. Do not only add a manual
   CNAME without registering the domain in the Pages project.
5. Verify HTTPS, both pages, HTTP-to-HTTPS behavior, and email delivery on the
   actual domain. Before publishing the migration, update the privacy page's
   hosting description from GitHub to Cloudflare and its last-updated date.
   Review that text against the final hosting configuration; do not enable
   analytics or extra tracking without reviewing the privacy disclosure.
6. Only once the new host and DNS work, disable the old GitHub Pages deployment
   and make the repository private in GitHub Settings > General > Danger Zone.
   Verify Cloudflare still deploys successfully from the private repository.

For rollback, retain the original DNS export and working GitHub deployment
until the new site is verified. Making the repository private on GitHub Free
before completing migration can take the current website offline.

Documentation:
- https://developers.cloudflare.com/pages/get-started/git-integration/
- https://developers.cloudflare.com/pages/configuration/custom-domains/
- https://developers.cloudflare.com/pages/configuration/headers/

Local review: no common private-key, GitHub-token or AWS access-key patterns were
found across the 51 locally available commits during the initial review. This
was a limited pattern scan, not a guarantee that history contains no sensitive
information. Account permissions, DNS ownership and production response headers
still require verification.
