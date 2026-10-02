# n8n for Business — DeTLeng

Static educational website for https://n8nforbusiness.detleng.com.

## Design
A warm white editorial guide with coral, deep navy and teal. A custom typographic wordmark and workflow-to-outcome hero introduce the commercial journey. Source wording is unchanged. Nodes receive inline labels; existing principles receive callouts; before/after situations retain their original sequence; the closing source sections receive special visual treatment.

## Structure
- `index.html`: full source article, 86 source-heading contents entries, hero, journey and ecosystem/footer.
- `assets/css/style.css`: large responsive typography, reading layouts, node labels and mobile navigation.
- `assets/js/app.js`: accessible navigation, contents filtering/current section and reading progress.
- `assets/favicon.svg`: custom local favicon, not an official n8n logo.
- `CNAME`: n8nforbusiness.detleng.com.
- `.nojekyll`: serve static assets directly through GitHub Pages.
- `tools/generate_site.py`: rebuild source HTML from the authoritative DOCX without modifying it.
- `tools/content-exclusions.json`: the six exact user-approved accidental blocks.
- `tools/verify_content.py`: independent source extraction, hash validation and ordered HTML/browser text comparison.
- `tools/source-manifest.json`: source blocks, approved exclusion count and original DOCX hash.
- `tools/integrity-report.json`, `tools/browser-report.json`, `tools/external-links-report.json`, `tools/contrast-report.json`: local QA results.

## Preview / GitHub Pages
Open `index.html` directly or serve this folder using any static HTTP server. The committed output needs no build step, Node server, Python backend, database, external webfont or framework. GitHub Pages can serve from the repository root. A Python runtime is needed only if you choose to run the development verification/rebuild tools.

The initial local project folder was empty, with no CNAME, README or `.git`. A correct local CNAME was created. No remote file was altered. No commit, push, PR or deployment was performed.

## Content integrity
The latest authoritative source is `D:\Web-Sites-Ideas\02 Sell n8n Workflows.docx`. The user confirmed the six opening LFDS card-proposal notes were accidental and approved their exclusion. `tools/content-exclusions.json` records those exact six blocks, preventing silent exclusions or reintroduction. All 1,663 teaching blocks remain in their original order; the untouched DOCX contains 1,669 meaningful blocks total. Empty spacing paragraphs are excluded from counts. Line breaks, punctuation, quotations, examples, lists, subheadings and final sections are preserved. The source DOCX is never written by either development tool.

Repeat the check with `python tools/verify_content.py`. To additionally compare rendered browser content, supply a JSON array of strings as the first argument. Each string must be the `innerText` of a `[data-source-block]` element in document order.

## Navigation and reading
Desktop has sticky navigation plus searchable/collapsible source-heading contents. Mobile has an accessible menu, Escape handling and compact contents. LFDS links use `target="_blank"` and `rel="noopener noreferrer"`. The progress line measures the article; the current section is identified with `aria-current="location"`. All content and links remain accessible without JavaScript.

Segoe UI/Arial provide interface and headings. Georgia/Times New Roman provide long-form body text. Body text is 22px on desktop, 21px on tablets and 20px on phones. Long-form content stays within a 790px reading column. Reduced motion is respected; source paragraphs are not animated.

## Validation
Checked 12 viewport widths from 320 to 1920px; no document overflow or clipped source blocks. Verified all 97 internal anchor links, source text against rendered browser content, contents search, mobile menu and Escape behavior, mobile contents, progress completion, LFDS new-tab behavior and no browser console errors. LFDS, n8n DeTLeng, n8n Lab and DeTLeng Ops all returned HTTP 200 in a real browser check. Color contrast pairs are recorded separately.

The footer contains the requested human-curated attribution, LFDS/ecosystem relationship, custom domain, year and discreet independent-resource clarification.
