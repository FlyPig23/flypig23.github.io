# Publication Link Cleanup Implementation Plan

> **For agentic workers:** REQUIRED SUB-SKILL: Use superpowers:subagent-driven-development (recommended) or superpowers:executing-plans to implement this plan task-by-task. Steps use checkbox (`- [ ]`) syntax for tracking.

**Goal:** Replace low-value publication action links with an exact Project / Dataset / Code contract while preserving every publication title's current primary paper URL.

**Architecture:** Keep the static HTML structure and existing `.publication-links` styling. Extend the semantic site contract with one exact per-publication auxiliary-link mapping, then make only the matching `index.html` list-item changes. No CSS, typography, publication metadata, or primary title-link changes are required.

**Tech Stack:** Static HTML5, CSS contract already present, Python 3 standard-library `unittest`, GitHub Pages.

---

### Task 1: Lock the auxiliary-link contract with a failing test

**Files:**
- Modify: `tests/test_site.py:140-150`
- Modify: `tests/test_site.py:1260-1290`
- Test: `tests/test_site.py`

- [ ] **Step 1: Add the exact expected mapping**

Add this constant immediately after `EXPECTED_PUBLICATION_LINKS`:

```python
EXPECTED_PUBLICATION_AUXILIARY_LINKS = [
    [
        (
            "Project",
            "Project for MemeBridge",
            "https://flypig23.github.io/memebridge-homepage/",
        ),
        (
            "Dataset",
            "Dataset for MemeBridge",
            "https://drive.google.com/drive/folders/"
            "152AN3iREfi71WThArmr8OcUWM5cV8YZy",
        ),
    ],
    [
        (
            "Project",
            "Project for SciImpact",
            "https://flypig23.github.io/sciimpact-homepage/",
        ),
        (
            "Dataset and Code",
            "Dataset and Code for SciImpact",
            "https://github.com/FlyPig23/SciImpact",
        ),
    ],
    [
        (
            "Project",
            "Project for Inference-Time Control for Trustworthy Large "
            "Language Models",
            "https://leopoldwhite.github.io/"
            "Awesome-Inference-Time-Trustworthiness/",
        ),
        (
            "Code",
            "Code for Inference-Time Control for Trustworthy Large "
            "Language Models",
            "https://github.com/leopoldwhite/"
            "Awesome-Inference-Time-Trustworthiness",
        ),
    ],
    [
        (
            "Code",
            "Code for Beyond Semantic Similarity",
            "https://github.com/vvjohn/DCI",
        ),
    ],
    [],
    [],
    [],
    [],
    [],
]
```

- [ ] **Step 2: Add a semantic regression test**

Add this method immediately after `test_publication_primary_links_are_exact_and_ordered`:

```python
def test_publication_auxiliary_links_are_exact_and_useful(self):
    rows = self.publication_rows()
    self.assertEqual(
        len(rows),
        len(EXPECTED_PUBLICATION_AUXILIARY_LINKS),
    )

    actual_by_publication = []
    for row in rows:
        links = self.one(
            self.with_class(row, "publication-links", tag="ul"),
            "publication auxiliary links",
        )
        actual_by_publication.append(
            [
                (
                    anchor.visible_text,
                    anchor.attr("aria-label"),
                    anchor.attr("href"),
                )
                for anchor in self.elements(links, tag="a")
            ]
        )

    self.assertEqual(
        actual_by_publication,
        EXPECTED_PUBLICATION_AUXILIARY_LINKS,
    )

    auxiliary_links = [
        item
        for publication_links in actual_by_publication
        for item in publication_links
    ]
    self.assertNotIn("DOI", [label for label, _, _ in auxiliary_links])
    self.assertNotIn(
        "https://www.xiameng.org/KDD_Meme_Bridge.pdf",
        [href for _, _, href in auxiliary_links],
    )
```

- [ ] **Step 3: Run the focused test and verify RED**

Run:

```bash
python3 -m unittest \
  tests.test_site.SiteContractTests.test_publication_auxiliary_links_are_exact_and_useful \
  -v
```

Expected: `FAIL`; the actual MemeBridge list still begins with `DOI` and `Paper`, SciImpact still says `Code`, and the three removable arXiv/DOI actions are still present.

- [ ] **Step 4: Confirm the remaining suite has no unrelated failures**

Run:

```bash
python3 -m unittest discover -s tests -v
```

Expected: 38 tests run; only `test_publication_auxiliary_links_are_exact_and_useful` fails.

- [ ] **Step 5: Commit the RED contract**

```bash
git add tests/test_site.py
git diff --cached --check
git commit -m "test: specify publication auxiliary links"
```

### Task 2: Apply the minimal publication-link cleanup

**Files:**
- Modify: `index.html:279-302`
- Modify: `index.html:371-424`
- Test: `tests/test_site.py`

- [ ] **Step 1: Replace the MemeBridge action list**

The final list must be exactly:

```html
<ul class="publication-links" aria-label="Links for MemeBridge">
    <li><a href="https://flypig23.github.io/memebridge-homepage/" target="_blank" rel="noopener noreferrer" aria-label="Project for MemeBridge">Project</a></li>
    <li><a href="https://drive.google.com/drive/folders/152AN3iREfi71WThArmr8OcUWM5cV8YZy" target="_blank" rel="noopener noreferrer" aria-label="Dataset for MemeBridge">Dataset</a></li>
</ul>
```

- [ ] **Step 2: Rename the SciImpact repository action**

Keep the existing project link and replace the GitHub action with:

```html
<li><a href="https://github.com/FlyPig23/SciImpact" target="_blank" rel="noopener noreferrer" aria-label="Dataset and Code for SciImpact">Dataset and Code</a></li>
```

- [ ] **Step 3: Remove the three low-value action items**

Leave these lists present but empty so the existing CSS hides them:

```html
<ul class="publication-links" aria-label="Links for TutorUp"></ul>
<ul class="publication-links" aria-label="Links for From Text to Trust"></ul>
<ul class="publication-links" aria-label="Links for Synthetic Data Generation with Large Language Models for Text Classification"></ul>
```

Do not modify their title anchors. The TutorUp and From Text to Trust title URLs remain DOI destinations, and Synthetic Data Generation remains linked to ACL Anthology.

- [ ] **Step 4: Run focused GREEN verification**

Run:

```bash
python3 -m unittest \
  tests.test_site.SiteContractTests.test_publication_auxiliary_links_are_exact_and_useful \
  tests.test_site.SiteContractTests.test_publication_primary_links_are_exact_and_ordered \
  -v
```

Expected: 2 tests pass.

- [ ] **Step 5: Run the complete suite**

Run:

```bash
python3 -m unittest discover -s tests -v
```

Expected: 38 tests pass.

- [ ] **Step 6: Verify the change is surgical and commit**

Run:

```bash
git diff --check
git diff -- css/style.css
git diff -- index.html tests/test_site.py
```

Expected: no CSS diff; only the specified publication action items changed in `index.html`.

Commit:

```bash
git add index.html
git commit -m "refactor: clean publication action links"
```

### Task 3: Browser QA and GitHub Pages deployment

**Files:**
- Verify: `index.html`
- Verify: `tests/test_site.py`
- No new files

- [ ] **Step 1: Run fresh pre-deployment verification**

```bash
python3 -m unittest discover -s tests -q
git diff --check main..HEAD
git status --short
```

Expected: 38 tests pass, no diff-check errors, and a clean worktree.

- [ ] **Step 2: Inspect the Publications section in a real browser**

Serve the repository and use Playwright CLI at desktop and 320px mobile widths. Confirm:

```text
MemeBridge: Project | Dataset
SciImpact: Project | Dataset and Code
TutorUp: no action row
From Text to Trust: no action row
Synthetic Data Generation: no action row
```

Also confirm the browser console has zero errors and there is no horizontal overflow at 320px.

- [ ] **Step 3: Merge the verified branch to main**

```bash
git switch main
git pull --ff-only origin main
git merge --ff-only feat/publication-link-cleanup
python3 -m unittest discover -s tests -q
```

Expected: fast-forward merge and 38 passing tests on `main`.

- [ ] **Step 4: Push and wait for the exact Pages build**

```bash
git push origin main
gh api repos/FlyPig23/flypig23.github.io/pages/builds/latest \
  --jq '{status,commit,error}'
```

Poll until `status` is `built`, `error.message` is null, and `commit` equals local `main` HEAD.

- [ ] **Step 5: Verify the public HTML contract**

Fetch `https://flypig23.github.io/?publication-links=<short-head>` with cache busting and verify:

```text
https://flypig23.github.io/memebridge-homepage/
Dataset and Code for SciImpact
```

Verify the live Publications auxiliary-link subtree contains neither:

```text
https://www.xiameng.org/KDD_Meme_Bridge.pdf
aria-label="DOI for
aria-label="arXiv for TutorUp"
aria-label="arXiv for From Text to Trust"
```

- [ ] **Step 6: Clean up the merged feature branch**

```bash
git branch -d feat/publication-link-cleanup
git status --short
```

Expected: the branch is deleted and `main` remains clean at the deployed commit.
