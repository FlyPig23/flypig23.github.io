# Compact Zhu Logo Deployment Implementation Plan

> **For agentic workers:** REQUIRED SUB-SKILL: Use superpowers:subagent-driven-development (recommended) or superpowers:executing-plans to implement this plan task-by-task. Steps use checkbox (`- [ ]`) syntax for tracking.

**Goal:** Publish the approved compact seal-script “朱” logo as transparent PNG web assets, use it in the Texas A&M navigation lockup and browser favicon, and deploy the verified site through GitHub Pages.

**Architecture:** Keep the site dependency-free and static. Export four deterministic PNG derivatives from the approved Figma nodes: a 210px positive master, a 37px warm-white navigation mark, and 16px/32px positive favicon masters. Reference only the navigation and favicon derivatives from `index.html`; use the existing official-color `images/tamu.png` beside the personal mark, and make surgical CSS changes to the existing `.brand` rules.

**Tech Stack:** Static HTML/CSS, Python `unittest`, Figma PNG exports, Git/GitHub Pages.

---

### Task 1: Add a failing logo and favicon contract

**Files:**
- Modify: `tests/test_site.py`

- [ ] **Step 1: Add PNG inspection helpers and expected assets**

Add `import struct`, then define the expected output contract near the existing asset constants:

```python
EXPECTED_LOGO_ASSETS = {
    "images/zhu-logo.png": (210, 210),
    "images/zhu-logo-nav.png": (37, 37),
    "images/favicon-16.png": (16, 16),
    "images/favicon-32.png": (32, 32),
}


def png_info(path):
    with path.open("rb") as handle:
        signature = handle.read(8)
        if signature != b"\x89PNG\r\n\x1a\n":
            raise AssertionError(f"Not a PNG file: {path}")
        length = struct.unpack(">I", handle.read(4))[0]
        chunk_type = handle.read(4)
        if length != 13 or chunk_type != b"IHDR":
            raise AssertionError(f"Missing PNG IHDR: {path}")
        width, height, _, color_type, _, _, _ = struct.unpack(
            ">IIBBBBB", handle.read(13)
        )
        remaining = handle.read()
    has_alpha = color_type in {4, 6} or b"tRNS" in remaining
    return width, height, has_alpha
```

- [ ] **Step 2: Add the semantic brand and favicon test**

Add this test to `SiteContractTests`:

```python
def test_compact_zhu_brand_lockup_and_favicons(self):
    for relative_path, expected_size in EXPECTED_LOGO_ASSETS.items():
        with self.subTest(asset=relative_path):
            path = ROOT / relative_path
            self.assertTrue(path.is_file(), f"Missing logo asset: {relative_path}")
            width, height, has_alpha = png_info(path)
            self.assertEqual((width, height), expected_size)
            self.assertTrue(has_alpha, f"Logo asset needs transparency: {relative_path}")

    brand = self.one(self.with_class(self.dom, "brand", tag="a"), "a.brand")
    lockup = self.one(
        self.with_class(brand, "brand-lockup"),
        ".brand-lockup",
    )
    personal = self.one(
        self.with_class(lockup, "brand-mark", tag="img"),
        "img.brand-mark",
    )
    institution = self.one(
        self.with_class(lockup, "brand-institution-mark", tag="img"),
        "img.brand-institution-mark",
    )
    self.assertEqual(personal.attr("src"), "images/zhu-logo-nav.png")
    self.assertEqual((personal.attr("width"), personal.attr("height")), ("37", "37"))
    self.assertEqual(personal.attr("alt"), "")
    self.assertEqual(institution.attr("src"), "images/tamu.png")
    self.assertEqual(lockup.attr("aria-hidden"), "true")

    icons = {}
    for link in self.elements(tag="link"):
        rel = set((link.attr("rel") or "").lower().split())
        if "icon" in rel:
            icons[link.attr("sizes")] = (link.attr("href"), link.attr("type"))
    self.assertEqual(
        icons,
        {
            "16x16": ("images/favicon-16.png", "image/png"),
            "32x32": ("images/favicon-32.png", "image/png"),
        },
    )
```

- [ ] **Step 3: Run the focused test and verify RED**

Run:

```bash
python3 -m unittest tests.test_site.SiteContractTests.test_compact_zhu_brand_lockup_and_favicons -v
```

Expected: FAIL because the four logo files and new HTML contract do not exist yet.

### Task 2: Export the approved PNG derivatives

**Files:**
- Create: `images/zhu-logo.png`
- Create: `images/zhu-logo-nav.png`
- Create: `images/favicon-16.png`
- Create: `images/favicon-32.png`

- [ ] **Step 1: Export the Figma master assets**

Use Figma file `x52kxyU32xd6y0zeWO3SeP` and these approved nodes:

```text
48:17  Compact Emblem master, positive, 210×210
48:22  Compact Emblem navigation mark, reverse, 37×37
45:25  Compact Emblem favicon optical master, positive, 16×16
```

Download each as PNG. Export `45:25` once at 1× for `favicon-16.png` and once at 2× for `favicon-32.png`. Save every file at the exact path above without recompressing or adding a background.

- [ ] **Step 2: Verify deterministic asset properties**

Run:

```bash
file images/zhu-logo.png images/zhu-logo-nav.png images/favicon-16.png images/favicon-32.png
```

Expected: four PNG files at 210×210, 37×37, 16×16, and 32×32, all retaining transparency.

### Task 3: Integrate the logo into the static site

**Files:**
- Modify: `index.html`
- Modify: `css/style.css`

- [ ] **Step 1: Add favicon metadata**

Insert immediately after the canonical link in `<head>`:

```html
<link rel="icon" type="image/png" sizes="16x16" href="images/favicon-16.png">
<link rel="icon" type="image/png" sizes="32x32" href="images/favicon-32.png">
```

- [ ] **Step 2: Replace the HZ text badge with the approved identity lockup**

Replace the existing `span.brand-mark` with:

```html
<span class="brand-lockup" aria-hidden="true">
    <img class="brand-mark" src="images/zhu-logo-nav.png" width="37" height="37" alt="">
    <span class="brand-divider"></span>
    <img class="brand-institution-mark" src="images/tamu.png" width="248" height="203" alt="">
</span>
```

Keep the existing accessible name on `a.brand` and keep the visible `Research Index` label.

- [ ] **Step 3: Replace the text-badge CSS with image-lockup CSS**

Use these rules in place of the existing `.brand-mark` text badge:

```css
.brand-lockup {
    display: inline-flex;
    align-items: center;
    gap: .65rem;
    flex: none;
}

.brand-mark {
    width: 2.35rem;
    height: 2.35rem;
    object-fit: contain;
}

.brand-divider {
    width: 1px;
    height: 1.75rem;
    background: rgb(255 255 255 / .28);
}

.brand-institution-mark {
    width: 2.2rem;
    height: auto;
    object-fit: contain;
}
```

- [ ] **Step 4: Run the focused test and verify GREEN**

Run:

```bash
python3 -m unittest tests.test_site.SiteContractTests.test_compact_zhu_brand_lockup_and_favicons -v
```

Expected: PASS.

- [ ] **Step 5: Run the full contract suite**

Run:

```bash
python3 -m unittest discover -s tests -v
```

Expected: 32 tests pass with 0 failures.

### Task 4: Visual QA, commit, and deploy

**Files:**
- Verify: `index.html`
- Verify: `css/style.css`
- Verify: `images/zhu-logo.png`
- Verify: `images/zhu-logo-nav.png`
- Verify: `images/favicon-16.png`
- Verify: `images/favicon-32.png`

- [ ] **Step 1: Run a local static server and inspect desktop/mobile**

Run:

```bash
python3 -m http.server 4173
```

Verify at `http://127.0.0.1:4173/` that the warm-white personal mark, official-color TAMU mark, divider, and `Research Index` label are aligned on desktop and do not overflow at 320px. Verify that the tab displays the compact black favicon.

- [ ] **Step 2: Commit the complete change**

Run:

```bash
git add docs/superpowers/plans/2026-09-01-compact-zhu-logo-deployment.md tests/test_site.py index.html css/style.css images/zhu-logo.png images/zhu-logo-nav.png images/favicon-16.png images/favicon-32.png
git commit -m "feat: add compact Zhu personal logo"
```

- [ ] **Step 3: Merge the verified branch and push GitHub Pages**

Fast-forward `feat/compact-zhu-logo` into `main`, then run:

```bash
git push origin main
```

Expected: GitHub accepts the push and starts the Pages deployment from `main`.

- [ ] **Step 4: Verify the public deployment**

Poll `https://flypig23.github.io/` until the HTML references `images/zhu-logo-nav.png` and both favicon links. Confirm each PNG URL returns HTTP 200 with `Content-Type: image/png`, and capture a final public-page screenshot.
