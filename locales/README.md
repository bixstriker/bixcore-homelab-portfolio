# BiXCore localization

The existing English HTML under `docs/` remains canonical and is published unchanged until the multilingual release is ready. German is the first language in the selector; Russian is the third. Existing English URLs remain stable. Localized URLs use /de/ and /ru/ with the same page paths and anchors.

Each locale JSON contains the original English page path, its Git blob fingerprint and reviewed translations for every visible text unit and relevant accessible/SEO attribute. The renderer reuses HTML structure, CSS, assets, anchor IDs and navigation. Common interface labels live in one dictionary. Any English source change invalidates its corresponding translation until reviewed; numeric tokens must match. This avoids silently publishing stale translated facts. It does not replace editorial review for semantic accuracy.

- `python3 tools/localize.py --check`: validates staged translations and renders them in memory.
- `python3 tools/localize.py --preview --output /tmp/bixcore-preview`: standalone preview; missing translated articles explicitly fall back to English, and a preview notice is shown.
- `python3 tools/localize.py --require-complete --output /tmp/bixcore-release`: refuses to generate a release until both translations cover every canonical English page.

Language selectors link to the same article in each available language. Localized links retain the selected language. No automatic redirect or browser translation service is used. Do not copy a partial preview into the published docs directory. The final deployment workflow and visual verification across all three languages are separate release steps.

The translation dictionaries are staged work. The original English Markdown project notes remain the technical reference.

The CI job also builds the preview, checks generated links, anchors, canonical and hreflang metadata, and saves the static output as a short-lived GitHub Actions artifact. Serve the extracted preview at the root of a local HTTP server; its absolute site paths are not designed for file:// browsing. The incomplete preview cannot be released by the strict build command.
