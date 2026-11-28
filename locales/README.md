# BiXCore localization

Canonical English HTML lives in `site-source/`; reviewed German and Russian dictionaries live in `locales/`. The `docs/` tree is generated and must not be edited independently. German is first in the selector; the original English root and x-default remain stable. Localized articles retain the same section identifiers.

Each locale JSON contains the original English page path, its Git blob fingerprint and reviewed translations. English changes invalidate the matching translations until reviewed. Numeric tokens must agree; localized separators do not change the underlying value. The renderer reuses HTML structure, CSS, assets, anchor IDs and navigation. These checks complement, rather than replace, editorial review.

- `python3 tools/localize.py --check`: validate and render in memory.
- `python3 tools/localize.py --require-complete --output /tmp/bixcore-release`: generate the complete site into a new directory.
- `python3 tools/localize.py --preview --output /tmp/bixcore-preview`: explicitly labeled preview for incomplete translations.

Serve the output at the root of a local HTTP server. Never publish an incomplete preview. The release workflow compares the complete generated tree with docs and runs browser tests. The language switch keeps the current section when a matching anchor exists; without JavaScript it remains ordinary accessible navigation.

## Release protection

The GitHub Actions workflow runs source/privacy checks, a complete reproducible build, a byte comparison with the committed site, and Chromium checks at ten viewport widths for every language. Only a successful main-branch run may upload the verified artifact for Pages deployment. A stale main commit is rejected before deployment.

Repository settings must match this workflow:
- Settings → Pages → Build and deployment → Source: **GitHub Actions**, not branch publishing.
- Settings → Branches (or Rulesets) → protect main and require the **safety-and-links** status check before accepting changes. Require the candidate branch to be up to date; disallow force pushes and deletion of main.

The workflow detects legacy branch publishing and warns rather than creating a competing deployment. Until those settings are enabled, staging and checking the complete commit before a fast-forward to main is essential. After changing the Pages source, run Check public portfolio from main (workflow dispatch) to verify and publish.

The generated site uses a local, dependency-free language-switch script, a meta CSP, and a referrer policy. GitHub Pages controls HTTP response headers; HSTS and frame-ancestors cannot be enforced through these HTML meta tags.
