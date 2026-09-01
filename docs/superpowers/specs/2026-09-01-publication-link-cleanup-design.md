# Publication Link Cleanup Design

## Goal

Make the Publications section show only useful project, code, and dataset actions while preserving each publication title's existing primary paper destination.

## Scope

- Change only publication auxiliary links and their regression contract.
- Keep all publication titles, authors, venues, years, ordering, and primary title URLs unchanged.
- Keep the site's current typography unchanged; Gill Sans is explicitly out of scope.
- Preserve the existing compact bibliography layout and link styling.

## Exact Auxiliary-Link Contract

| Publication | Auxiliary links after the change |
| --- | --- |
| MemeBridge | `Project` → `https://flypig23.github.io/memebridge-homepage/`; `Dataset` → `https://drive.google.com/drive/folders/152AN3iREfi71WThArmr8OcUWM5cV8YZy` |
| SciImpact | `Project` → `https://flypig23.github.io/sciimpact-homepage/`; `Dataset and Code` → `https://github.com/FlyPig23/SciImpact` |
| Inference-Time Control for Trustworthy Large Language Models | `Project` → `https://leopoldwhite.github.io/Awesome-Inference-Time-Trustworthiness/`; `Code` → `https://github.com/leopoldwhite/Awesome-Inference-Time-Trustworthiness` |
| Beyond Semantic Similarity | `Code` → `https://github.com/vvjohn/DCI` |
| Survivors, Complainers, and Borderliners | None |
| TutorUp | None |
| From Text to Trust | None |
| Mending Trust in AI | None |
| Synthetic Data Generation with Large Language Models for Text Classification | None |

The MemeBridge auxiliary `DOI` action and the PDF hosted at `xiameng.org/KDD_Meme_Bridge.pdf` will be removed. The TutorUp and From Text to Trust auxiliary arXiv actions will be removed. The Synthetic Data Generation auxiliary DOI action will be removed.

## DOI Boundary

"Remove DOI" applies to standalone auxiliary `DOI` actions. It does not remove or rewrite a publication title's primary paper link when that official destination happens to use a `doi.org` URL. This preserves a paper entry point for MemeBridge, TutorUp, and From Text to Trust.

## Markup and Accessibility

- Keep each `.publication-links` list so the existing markup pattern remains uniform; empty lists stay visually hidden through the existing `.publication-links:empty` rule.
- Keep external-link safety attributes (`target="_blank"` and `rel="noopener noreferrer"`).
- Give the SciImpact combined action the visible label and accessible name `Dataset and Code` / `Dataset and Code for SciImpact`.
- Give the MemeBridge project action the visible label and accessible name `Project` / `Project for MemeBridge`.

## Verification

1. Add a failing contract test that asserts the exact visible label, accessible label, and URL sequence for every publication's auxiliary links.
2. Assert that no auxiliary action is labeled `DOI`, the removed MemeBridge PDF URL is absent, and the existing primary title-link sequence remains unchanged.
3. Apply the minimal `index.html` changes and make the focused contract green.
4. Run the complete test suite and a browser check of the Publications section.
5. Push `main`, wait for GitHub Pages to build the target commit, and verify the live HTML contains the exact link contract.

## Success Criteria

- MemeBridge shows exactly `Project` and `Dataset` actions.
- SciImpact shows exactly `Project` and `Dataset and Code` actions.
- TutorUp, From Text to Trust, and Synthetic Data Generation show no auxiliary actions.
- No standalone auxiliary `DOI` action remains anywhere in Publications.
- No font or unrelated content changes are introduced.
- Local tests and live GitHub Pages verification pass.
