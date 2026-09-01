# Academic Homepage Redesign Implementation Plan

> **For agentic workers:** REQUIRED SUB-SKILL: Use superpowers:subagent-driven-development (recommended) or superpowers:executing-plans to implement this plan task-by-task. Steps use checkbox (`- [ ]`) syntax for tracking.

**Goal:** Replace the current fixed-sidebar homepage with the approved single-page Research Index, accurately list all nine works newest-first, and preserve the existing identity and school assets.

**Architecture:** Keep the repository as a no-build GitHub Pages site. Rewrite `index.html` as semantic, source-of-truth content; replace `css/style.css` with a mobile-first editorial design; add one dependency-free script for the current year and one dependency-free Python contract suite for content, accessibility, metadata, assets, and publication ordering.

**Tech Stack:** HTML5, CSS3, vanilla JavaScript, Python 3 standard-library `unittest`, GitHub Pages.

**2026-09-01 design revision:** Keep Agent System, Data Mining, and AI for Science in one ordinary sentence inside the About self-introduction. Do not render a separate Research Interests section or navigation item. The section order is About / Education, News, then Publications, numbered 01–03.

---

## File map

- Modify: `index.html` — semantic page structure, all copy, news, all nine works, metadata, and JSON-LD.
- Replace: `css/style.css` — selected Signal & Structure visual system and responsive behavior.
- Create: `js/site.js` — current-year enhancement only.
- Create: `tests/test_site.py` — static-site content and accessibility contract.
- Create: `images/prof_pic-720.jpg` — optimized portrait derivative; preserve `images/prof_pic.jpg` unchanged.
- Create: `.gitignore` — exclude local brainstorm and Python cache artifacts.
- Preserve unchanged: `assets/CV_Hangxiao Zhu_2024.pdf`, all existing school images, and all legacy publication thumbnails.

## Data contract

The bibliography must use this exact display order:

1. MemeBridge — 2026 — `peer-reviewed` — KDD 2026, Datasets and Benchmarks Track.
2. SciImpact — 2026 — `peer-reviewed` — Findings of ACL 2026.
3. Inference-Time Control — 2026 — `preprint` — Working paper / preprint.
4. Beyond Semantic Similarity — 2026 — `preprint` — arXiv preprint.
5. Survivors, Complainers, and Borderliners — 2025 — `preprint` — arXiv preprint.
6. TutorUp — 2025 — `peer-reviewed` — CHI 2025.
7. From Text to Trust — 2025 — `peer-reviewed` — CHI 2025.
8. Mending Trust in AI — 2024 — `thesis` — Washington University in St. Louis master's thesis.
9. Synthetic Data Generation — 2023 — `peer-reviewed` — EMNLP 2023.

The News section contains exactly these two visible sentences:

```text
2026 — SciImpact accepted to Findings of ACL 2026.
2026 — MemeBridge accepted to KDD 2026, Datasets and Benchmarks Track.
```

## Task 1: Add the failing site contract

**Files:**

- Create: `.gitignore`
- Create: `tests/test_site.py`
- Test: `tests/test_site.py`

- [ ] **Step 1: Ignore local-only artifacts**

Create `.gitignore` with exactly:

```gitignore
.superpowers/
__pycache__/
*.py[cod]
```

Do not remove the already tracked `.idea` or `.DS_Store` files during this feature.

- [ ] **Step 2: Write the structural contract**

Create `tests/test_site.py` using only `html.parser`, `json`, `pathlib`, `re`, `unittest`, and `urllib.parse`. The parser must expose element tag, attributes, class set, normalized text, children, and descendant iteration.

Define these exact expectations:

```python
EXPECTED_SECTIONS = [
    "about-me",
    "news",
    "publications",
]

EXPECTED_INTERESTS = [
    "Agent System",
    "Data Mining",
    "AI for Science",
]

EXPECTED_NEWS = [
    "2026 — SciImpact accepted to Findings of ACL 2026.",
    "2026 — MemeBridge accepted to KDD 2026, Datasets and Benchmarks Track.",
]

EXPECTED_PUBLICATIONS = [
    ("2026", "peer-reviewed", "MemeBridge: A Dataset for Benchmarking and Mitigating the Bidirectional Cultural Gap in Meme Interpretation.", "KDD 2026, Datasets and Benchmarks Track"),
    ("2026", "peer-reviewed", "SciImpact: A Multi-Dimensional, Multi-Field Benchmark for Scientific Impact Prediction.", "Findings of ACL 2026"),
    ("2026", "preprint", "Inference-Time Control for Trustworthy Large Language Models.", "Working paper / preprint"),
    ("2026", "preprint", "Beyond Semantic Similarity: Rethinking Retrieval for Agentic Search via Direct Corpus Interaction.", "arXiv preprint"),
    ("2025", "preprint", "Survivors, Complainers, and Borderliners: Upward Bias in Online Discussions of Academic Conference Reviews.", "arXiv preprint"),
    ("2025", "peer-reviewed", "TutorUp: What If Your Students Were Simulated? Training Tutors to Address Engagement Challenges in Online Learning.", "CHI 2025"),
    ("2025", "peer-reviewed", "From Text to Trust: Empowering AI-assisted Decision Making with Adaptive LLM-powered Analysis.", "CHI 2025"),
    ("2024", "thesis", "Mending Trust in AI: Trust Repair Policy Interventions for Large Language Models in Visual Data Journalism.", "Washington University in St. Louis master's thesis"),
    ("2023", "peer-reviewed", "Synthetic Data Generation with Large Language Models for Text Classification: Potential and Limitations.", "EMNLP 2023"),
]
```

Implement test methods that assert all of the following:

```text
header#hero exists and precedes main#main-content
main's top-level section ids equal EXPECTED_SECTIONS in order
the primary nav links to those three section ids in order
the About copy contains Agent System, Data Mining, and AI for Science in one paragraph
no #research-interests section, Research navigation item, or .research-interest-title exists
the About, News, and Publications section indices equal 01, 02, and 03
li.news-item text equals EXPECTED_NEWS and there are exactly two
article.publication count is nine and each has data-status
each publication exposes .publication-year, .publication-title, .publication-authors, and .publication-status
publication tuples equal EXPECTED_PUBLICATIONS exactly
each publication author line contains <strong>Hangxiao Zhu</strong>
exactly three rows have data-status="preprint" and none says accepted
portrait, TAMU, Reveille, Bears, Buckeye, and CV are referenced and exist
the three legacy publication thumbnails exist but are not referenced
every local href/src/srcset/CSS url() resolves inside the repository
there is one h1, every top-level section begins with h2, and heading levels do not jump
all img elements have alt, numeric width, numeric height; below-fold images use loading="lazy"
Email, Google Scholar, and CV links have visible text
all target="_blank" external links use rel="noopener noreferrer"
meta description is 50–170 characters; canonical and Open Graph URL equal https://flypig23.github.io/
JSON-LD contains a Person named Hangxiao Zhu and a ScholarlyArticle for every non-thesis work
the skip link targets #main-content and every internal fragment resolves
CSS contains a visible :focus-visible rule and a prefers-reduced-motion rule
footer CSS never uses position: fixed or position: absolute
```

Use the following entry point:

```python
if __name__ == "__main__":
    unittest.main()
```

- [ ] **Step 3: Run the suite to prove the current page is RED**

Run:

```bash
python3 -m unittest discover -s tests -p 'test_*.py' -v
```

Expected: failures for missing `#hero`, `#main-content`, the integrated About research sentence, the approved News, nine publications, semantic metadata, and accessibility hooks. Parser/import errors are not acceptable; fix the test harness until it runs and fails only on the old page.

- [ ] **Step 4: Keep the failing contract uncommitted**

Run:

```bash
git status --short
```

Expected: only `.gitignore` and `tests/test_site.py` are newly visible; `.superpowers/` is ignored. Do not commit the deliberately failing state.

## Task 2: Rebuild semantic content and metadata

**Files:**

- Modify: `index.html`
- Create: `js/site.js`
- Test: `tests/test_site.py`

- [ ] **Step 1: Replace the document head**

Use this metadata contract in `index.html`:

```html
<!doctype html>
<html lang="en">
<head>
  <meta charset="utf-8">
  <meta name="viewport" content="width=device-width, initial-scale=1">
  <meta name="description" content="Hangxiao Zhu is a Computer Science Ph.D. student at Texas A&amp;M University researching agent systems, data mining, and AI for science.">
  <meta name="theme-color" content="#171a1f">
  <link rel="canonical" href="https://flypig23.github.io/">
  <meta property="og:type" content="profile">
  <meta property="og:title" content="Hangxiao Zhu — Research Index">
  <meta property="og:description" content="Hangxiao Zhu is a Computer Science Ph.D. student at Texas A&amp;M University researching agent systems, data mining, and AI for science.">
  <meta property="og:url" content="https://flypig23.github.io/">
  <title>Hangxiao Zhu — Research Index</title>
  <link rel="stylesheet" href="css/style.css">
  <script defer src="js/site.js"></script>
</head>
```

Add one `application/ld+json` script containing an `@graph` with:

- one `Person` node for Hangxiao Zhu, URL `https://flypig23.github.io/`, Texas A&M affiliation, email, Scholar URL, and the three research areas;
- eight `ScholarlyArticle` nodes, one for every work except the thesis, using the exact visible title and a `datePublished` beginning with the displayed year.

- [ ] **Step 2: Replace the old fixed-column body with semantic landmarks**

Use this exact outer structure:

```html
<body>
  <a class="skip-link" href="#main-content">Skip to content</a>
  <header class="hero" id="hero">
    <nav class="site-nav site-shell" aria-label="Primary navigation">
      <a class="site-nav-brand" href="#hero">HZ / Research Index</a>
      <ul class="site-nav-links">
        <li><a href="#about-me">About</a></li>
        <li><a href="#news">News</a></li>
        <li><a href="#publications">Publications</a></li>
      </ul>
    </nav>
    <div class="hero-body site-shell">
      <picture class="hero-portrait-frame">
        <source media="(max-width: 48rem)" srcset="images/prof_pic-720.jpg">
        <img class="hero-portrait" src="images/prof_pic.jpg" width="2587" height="2678" alt="Portrait of Hangxiao Zhu" fetchpriority="high">
      </picture>
      <div class="hero-content">
        <div class="hero-affiliation">
          <span class="hero-institution-mark"><img src="images/tamu.png" width="248" height="203" alt="Texas A&amp;M University"></span>
          <p>Ph.D. Student · Computer Science &amp; Engineering<br>Texas A&amp;M University</p>
        </div>
        <p class="hero-kicker">Research Index · 2026</p>
        <h1 class="hero-name">Hangxiao Zhu</h1>
        <p class="hero-lede">Building intelligent agents and data-driven systems for scientific discovery.</p>
        <ul class="contact-list" aria-label="Contact and profiles">
          <li><a class="contact-link" href="mailto:hangxiao@tamu.edu">Email</a></li>
          <li><a class="contact-link" href="https://scholar.google.com/citations?user=fmDa4U4AAAAJ&amp;hl=en" target="_blank" rel="noopener noreferrer">Google Scholar</a></li>
          <li><a class="contact-link" href="assets/CV_Hangxiao%20Zhu_2024.pdf" target="_blank" rel="noopener noreferrer">CV</a></li>
        </ul>
      </div>
    </div>
  </header>
  <main id="main-content">
    <section id="about-me" class="section section-about"></section>
    <section id="news" class="section"></section>
    <section id="publications" class="section"></section>
  </main>
  <footer class="site-footer">
    <div class="site-shell"><p>© <span data-current-year>2026</span> Hangxiao Zhu.</p><p><time datetime="2026-08-31">Last updated August 2026</time></p></div>
  </footer>
</body>
```

Populate these initially empty section elements with the exact content defined in the next three steps before running the contract.

- [ ] **Step 3: Implement About / Education first**

The first section must use a `section-inner` wrapper, an `h2` titled `About & Education`, and an `about-layout` containing:

- a concise About paragraph naming Prof. Yu Zhang, Prof. Alvitta Ottley, and Prof. Ming Yin with their existing links;
- the ordinary sentence `My research interests center on Agent System, Data Mining, and AI for Science.` inside that About paragraph;
- a `Beyond Research` paragraph preserving the Ohio State football, Lakers, and Texans links;
- an `ol.education-list` with Texas A&M, Washington University in St. Louis, Ohio State University, and Purdue research mentorship in that order;
- `images/rev.jpg` (`642×630`), `images/bears.png` (`1024×847`), and `images/buckeye.png` (`764×901`) inside their matching education rows with `loading="lazy"`;
- a text-only Purdue row because the repository has no Purdue asset.

- [ ] **Step 4: Implement News without a separate interests section**

Do not add a `#research-interests` section or Research navigation item. The exact interests belong only in the About sentence from Step 3. Number News `02` and Publications `03`.

```html
<ol class="news-list">
  <li class="news-item"><time datetime="2026">2026</time><span aria-hidden="true">—</span><span>SciImpact accepted to Findings of ACL 2026.</span></li>
  <li class="news-item"><time datetime="2026">2026</time><span aria-hidden="true">—</span><span>MemeBridge accepted to KDD 2026, Datasets and Benchmarks Track.</span></li>
</ol>
```

- [ ] **Step 5: Implement all nine equal-weight publication rows**

Every row must use this schema and no featured modifier or image:

```html
<li>
  <article class="publication" data-status="peer-reviewed">
    <div class="publication-meta">
      <time class="publication-year" datetime="2026">2026</time>
      <span class="publication-status">KDD 2026, Datasets and Benchmarks Track</span>
    </div>
    <div class="publication-body">
      <h3 class="publication-title"><a href="https://doi.org/10.1145/3770854.3785691" target="_blank" rel="noopener noreferrer">MemeBridge: A Dataset for Benchmarking and Mitigating the Bidirectional Cultural Gap in Meme Interpretation.</a></h3>
      <p class="publication-authors"><strong>Hangxiao Zhu</strong>, Suliu Qin, Zhuoyan Li, Ming Jiang, Yu Zhang, Meng Xia</p>
      <p class="publication-venue">Proceedings of KDD 2026 · Datasets and Benchmarks Track</p>
      <ul class="publication-links"><li><a href="https://doi.org/10.1145/3770854.3785691" target="_blank" rel="noopener noreferrer" aria-label="MemeBridge DOI">DOI</a></li><li><a href="https://www.xiameng.org/KDD_Meme_Bridge.pdf" target="_blank" rel="noopener noreferrer" aria-label="MemeBridge paper PDF">Paper</a></li><li><a href="https://drive.google.com/drive/folders/152AN3iREfi71WThArmr8OcUWM5cV8YZy" target="_blank" rel="noopener noreferrer" aria-label="MemeBridge dataset">Dataset</a></li></ul>
    </div>
  </article>
</li>
```

Repeat that exact schema for the other eight works, using these primary links and complete author lists:

| Work | Title link | Additional links | Complete author list |
|---|---|---|---|
| SciImpact | `https://aclanthology.org/2026.findings-acl.1445/` | Project `https://flypig23.github.io/sciimpact-homepage/`; Code `https://github.com/FlyPig23/SciImpact` | **Hangxiao Zhu**, Yuyu Zhang, Ping Nie, Yu Zhang |
| Inference-Time Control | `https://www.preprints.org/manuscript/202605.1041` | Project `https://leopoldwhite.github.io/Awesome-Inference-Time-Trustworthiness/`; Code `https://github.com/leopoldwhite/Awesome-Inference-Time-Trustworthiness` | Yuyang Bai, Zheyuan Liu, Han Yan, Zhangchen Xu, Yixin Wan, Canyu Chen, Zehong Wang, Xiangchi Yuan, Yue Huang, Guangyao Dou, Yuji Zhang, **Hangxiao Zhu**, Zhuofeng Li, Manling Li, Xiangliang Zhang, Mohit Bansal, Sanmi Koyejo, Kai-Wei Chang, Yu Zhang, Meng Jiang |
| Beyond Semantic Similarity | `https://arxiv.org/abs/2605.05242` | Code `https://github.com/vvjohn/DCI` | Zhuofeng Li, Haoxiang Zhang, Cong Wei, Pan Lu, Ping Nie, Yi Lu, Yuyang Bai, Shangbin Feng, **Hangxiao Zhu**, Ming Zhong, Yuyu Zhang, Jianwen Xie, Yejin Choi, James Zou, Jiawei Han, Wenhu Chen, Jimmy Lin, Dongfu Jiang, Yu Zhang |
| Survivors | `https://arxiv.org/abs/2509.16831` | none | **Hangxiao Zhu**, Yian Yin, Yu Zhang |
| TutorUp | `https://doi.org/10.1145/3706598.3713589` | arXiv `https://arxiv.org/abs/2502.16178` | Sitong Pan, Robin Schmucker, Bernardo Garcia Bulle Bueno, Salome Aguilar Llanes, Fernanda Albo Alarcón, **Hangxiao Zhu**, Adam Teo, Meng Xia |
| From Text to Trust | `https://doi.org/10.1145/3706598.3713133` | arXiv `https://arxiv.org/abs/2502.11919` | Zhuoyan Li, **Hangxiao Zhu**, Zhuoran Lu, Ziang Xiao, Ming Yin |
| Mending Trust in AI | `https://openscholarship.wustl.edu/eng_etds/1013/` | none; do not use the broken DOI resolver | **Hangxiao Zhu** |
| Synthetic Data Generation | `https://aclanthology.org/2023.emnlp-main.647/` | DOI `https://doi.org/10.18653/v1/2023.emnlp-main.647` | Zhuoyan Li, **Hangxiao Zhu**, Zhuoran Lu, Ming Yin |

Use `data-status="preprint"` and the exact status text from the Data contract for Inference-Time Control, Beyond Semantic Similarity, and Survivors. Use `data-status="thesis"` for Mending Trust in AI. All remaining rows use `data-status="peer-reviewed"`.

- [ ] **Step 6: Add the current-year enhancement**

Create `js/site.js`:

```javascript
const currentYear = document.querySelector("[data-current-year]");

if (currentYear) {
  currentYear.textContent = String(new Date().getFullYear());
}
```

- [ ] **Step 7: Run the content contract**

Run:

```bash
python3 -m unittest discover -s tests -p 'test_*.py' -v
```

Expected: content, metadata, asset, publication, and link-safety tests pass. CSS-specific focus/reduced-motion tests may still fail until Task 3.

- [ ] **Step 8: Commit the semantic rebuild once its tests are green**

```bash
git add .gitignore tests/test_site.py index.html js/site.js
git commit -m "feat: rebuild homepage content and structure"
```

Expected: commit succeeds without staging `.superpowers/`.

## Task 3: Apply the Signal & Structure visual system

**Files:**

- Replace: `css/style.css`
- Create: `images/prof_pic-720.jpg`
- Test: `tests/test_site.py`

- [ ] **Step 1: Generate an optimized portrait derivative**

Run:

```bash
sips -Z 720 -s format jpeg -s formatOptions 82 images/prof_pic.jpg --out images/prof_pic-720.jpg
```

Expected: `images/prof_pic-720.jpg` exists, is at most 720px on its longest edge, and the original file remains byte-for-byte unchanged.

Record the original checksum before and after:

```bash
shasum -a 256 images/prof_pic.jpg
sips -g pixelWidth -g pixelHeight images/prof_pic-720.jpg
```

- [ ] **Step 2: Replace the stylesheet tokens and base rules**

Start `css/style.css` with:

```css
:root {
  --color-hero: #171a1f;
  --color-hero-text: #f7f3ec;
  --color-hero-muted: #c8cdd2;
  --color-page: #f5f7f8;
  --color-surface: #ffffff;
  --color-text: #20262e;
  --color-muted: #59636f;
  --color-rule: #d6dde2;
  --color-accent: #500000;
  --color-accent-soft: #ede3e3;
  --font-display: ui-serif, Georgia, Cambria, "Times New Roman", Times, serif;
  --font-body: ui-sans-serif, -apple-system, BlinkMacSystemFont, "Segoe UI", sans-serif;
  --font-mono: ui-monospace, "SFMono-Regular", Consolas, "Liberation Mono", monospace;
  --shell-max: 72rem;
  --text-measure: 68ch;
  --page-gutter: clamp(1.125rem, 4vw, 3rem);
  --section-space: clamp(3.75rem, 7vw, 6.5rem);
  --radius-sm: .25rem;
}

*, *::before, *::after { box-sizing: border-box; }
html { scroll-behavior: smooth; }
body { margin: 0; color: var(--color-text); background: var(--color-page); font-family: var(--font-body); line-height: 1.65; }
img { display: block; max-width: 100%; height: auto; }
a { color: inherit; text-decoration-thickness: .08em; text-underline-offset: .22em; }
.site-shell { width: min(100% - (2 * var(--page-gutter)), var(--shell-max)); margin-inline: auto; }
.skip-link { position: fixed; z-index: 100; top: 1rem; left: 1rem; transform: translateY(-180%); padding: .75rem 1rem; color: #fff; background: var(--color-accent); }
.skip-link:focus { transform: translateY(0); }
:focus-visible { outline: 3px solid var(--color-accent); outline-offset: 4px; }
```

- [ ] **Step 3: Implement the selected hero**

Use `.hero` with `background: var(--color-hero)` and warm-white text. Add a low-opacity 40px CSS grid through `.hero::before` and one non-animated orbital circle through `.hero::after`; both must use `pointer-events: none`.

Implement these exact layout behaviors:

```css
.hero { position: relative; isolation: isolate; overflow: hidden; min-height: min(48rem, 92vh); color: var(--color-hero-text); background: var(--color-hero); }
.site-nav { display: flex; align-items: center; justify-content: space-between; gap: 1.5rem; padding-block: 1.25rem; }
.hero-body { display: grid; gap: 2.25rem; align-items: end; padding-block: clamp(3rem, 8vw, 7rem); }
.hero-portrait-frame { width: min(11rem, 48vw); aspect-ratio: 4 / 5; overflow: hidden; border: 1px solid rgb(255 255 255 / .25); border-radius: var(--radius-sm); }
.hero-portrait { width: 100%; height: 100%; object-fit: cover; object-position: 50% 38%; }
.hero-institution-mark { display: grid; place-items: center; width: 5.5rem; aspect-ratio: 1; padding: .75rem; background: #fff; border-radius: var(--radius-sm); }
.hero-name { margin: .5rem 0 0; color: var(--color-hero-text); font: 500 clamp(3rem, 9vw, 6.5rem)/.9 var(--font-display); letter-spacing: -.055em; }
.hero-lede { max-width: 38rem; color: var(--color-hero-muted); font-size: clamp(1.05rem, 2vw, 1.35rem); }
.contact-link { display: inline-flex; align-items: center; min-height: 44px; padding: .55rem .9rem; border: 1px solid rgb(255 255 255 / .35); border-radius: var(--radius-sm); }
```

The name must never inherit `--color-accent`.

- [ ] **Step 4: Implement the light reading surface and compact bibliography**

Use the following rules as the structural contract:

```css
.section { padding-block: var(--section-space); border-top: 1px solid var(--color-rule); scroll-margin-top: 3rem; }
.section-about { padding-top: clamp(3rem, 5vw, 4.5rem); }
.section-inner { display: grid; gap: 2rem; }
.section-index, .publication-year, .publication-status { color: var(--color-accent); font-family: var(--font-mono); font-size: .75rem; font-weight: 700; letter-spacing: .06em; text-transform: uppercase; }
.about-copy { max-width: var(--text-measure); }
.education-list, .news-list, .publication-list, .publication-links, .contact-list, .site-nav-links { margin: 0; padding: 0; list-style: none; }
.education-item, .news-item, .publication { border-top: 1px solid var(--color-rule); }
.news-item { display: grid; grid-template-columns: 4rem auto 1fr; gap: .75rem; padding-block: 1rem; }
.publication { display: grid; gap: .85rem; padding-block: clamp(1.35rem, 3vw, 2rem); }
.publication-title { margin: 0; max-width: 62rem; font: 600 clamp(1.05rem, .35vw + 1rem, 1.25rem)/1.35 var(--font-body); }
.publication-authors, .publication-venue { max-width: 72ch; margin: .45rem 0 0; color: var(--color-muted); font-size: .94rem; }
.publication-authors strong { color: var(--color-text); font-weight: 750; }
.publication-links { display: flex; flex-wrap: wrap; gap: .75rem; margin-top: .7rem; }
.publication-links a { color: var(--color-accent); font-family: var(--font-mono); font-size: .76rem; font-weight: 700; text-transform: uppercase; }
.site-footer { padding-block: 2rem; border-top: 1px solid var(--color-rule); }
```

Do not create publication cards, shadows, large radii, thumbnails, a fixed footer, or fixed/absolute content columns.

- [ ] **Step 5: Add responsive and reduced-motion rules**

Use these breakpoints:

```css
@media (min-width: 48rem) {
  .hero-body { grid-template-columns: 12rem minmax(0, 1fr); }
  .about-layout { grid-template-columns: minmax(0, 1fr) minmax(17rem, .9fr); }
  .publication { grid-template-columns: 7rem minmax(0, 1fr); }
}

@media (min-width: 64rem) {
  .hero-body { grid-template-columns: 15rem minmax(0, 1fr); gap: 4.5rem; }
  .section-inner { grid-template-columns: 10.5rem minmax(0, 1fr); gap: 3rem; }
}

@media (max-width: 47.999rem) {
  .site-nav { align-items: flex-start; flex-direction: column; }
  .site-nav-links { flex-wrap: wrap; }
  .news-item { grid-template-columns: 3.5rem auto 1fr; }
}

@media (prefers-reduced-motion: reduce) {
  html { scroll-behavior: auto; }
  *, *::before, *::after { animation-duration: .01ms !important; animation-iteration-count: 1 !important; transition-duration: .01ms !important; }
}
```

Supply the missing `display: grid/flex`, gaps, type sizes, hover states, and education-logo sizing in the same stylesheet so every named selector is functional at all widths.

- [ ] **Step 6: Run the complete contract and CSS parser checks**

Run:

```bash
python3 -m unittest discover -s tests -p 'test_*.py' -v
tidy -quiet -errors index.html
git diff --check
```

Expected: all unit tests pass; `tidy` reports no structural HTML errors; `git diff --check` prints nothing.

- [ ] **Step 7: Commit the visual implementation**

```bash
git add css/style.css images/prof_pic-720.jpg
git commit -m "style: apply research index visual system"
```

## Task 4: Runtime and responsive verification

**Files:**

- Modify only if verification finds a defect: `index.html`, `css/style.css`, `js/site.js`, `tests/test_site.py`
- Test: rendered homepage and all local assets

- [ ] **Step 1: Start the static site in a retained terminal**

Run:

```bash
python3 -m http.server 4173 --bind 127.0.0.1
```

Expected: retained server reports `Serving HTTP on 127.0.0.1 port 4173`.

- [ ] **Step 2: Prove the exact route and key assets respond**

Run in another terminal:

```bash
curl --fail --silent --show-error http://127.0.0.1:4173/ >/dev/null
curl --fail --silent --show-error http://127.0.0.1:4173/css/style.css >/dev/null
curl --fail --silent --show-error http://127.0.0.1:4173/js/site.js >/dev/null
curl --fail --silent --show-error http://127.0.0.1:4173/images/prof_pic-720.jpg >/dev/null
```

Expected: all four commands exit zero.

- [ ] **Step 3: Inspect five target viewports**

Open `http://127.0.0.1:4173/` in the in-app browser and inspect:

```text
1440 × 900
1024 × 768
768 × 1024
390 × 844
320 × 568
```

At each width verify no horizontal scroll, clipped name, overlapping footer, centered mobile bibliography, distorted logo, or publication-card emphasis. Confirm About / Education immediately follows the hero and all nine works remain visibly equal-weight.

- [ ] **Step 4: Verify keyboard and reduced motion**

Use keyboard-only navigation to confirm the first Tab reveals the skip link and every contact/publication link has a visible focus outline. Emulate `prefers-reduced-motion: reduce` and confirm anchor navigation has no smooth animation.

- [ ] **Step 5: Verify externally hosted primary links**

Check the final `href` values for the nine title links plus Scholar, advisor pages, and project/code links. A remote `403` or bot challenge is acceptable only when the URL is known authoritative and loads in a normal browser; broken/404 URLs must be replaced with the verified alternatives in the design spec.

- [ ] **Step 6: Fix only observed defects and rerun validation**

For each defect, add or tighten a regression assertion in `tests/test_site.py` when it can be tested statically, apply the smallest source change, then rerun:

```bash
python3 -m unittest discover -s tests -p 'test_*.py' -v
tidy -quiet -errors index.html
git diff --check
```

Expected: all checks pass after every fix.

- [ ] **Step 7: Commit verification fixes if any**

```bash
git add index.html css/style.css js/site.js tests/test_site.py
git diff --cached --quiet || git commit -m "fix: polish responsive homepage behavior"
```

## Task 5: Final review and safe publication handoff

**Files:**

- Review: all changed files against `docs/superpowers/specs/2026-08-31-academic-homepage-redesign-design.md`

- [ ] **Step 1: Run the final evidence bundle**

```bash
python3 -m unittest discover -s tests -p 'test_*.py' -v
tidy -quiet -errors index.html
git diff --check origin/main...HEAD
git status --short --branch
```

Expected: tests pass, HTML has no structural errors, diff check is clean, and only intentional branch changes remain.

- [ ] **Step 2: Review the exact branch diff**

```bash
git diff --stat origin/main...HEAD
git diff --name-status origin/main...HEAD
```

Expected changed product files: `.gitignore`, `index.html`, `css/style.css`, `js/site.js`, `tests/test_site.py`, `images/prof_pic-720.jpg`, plus the approved design and plan documents. No legacy image or CV is deleted or renamed.

- [ ] **Step 3: Obtain code review**

Use the requesting-code-review workflow against `origin/main...HEAD`. Resolve every correctness, accessibility, metadata, content, and responsive issue before publication.

- [ ] **Step 4: Push the feature branch**

```bash
git push -u origin codex/homepage-redesign-2026
```

Expected: the branch is available on GitHub without changing the live GitHub Pages site.

- [ ] **Step 5: Present the verified local preview and publication choice**

Show the user the final local preview and summarize content/visual verification. Because `main` deploys directly to GitHub Pages and is unprotected, merge/push to `main` only after the user confirms the coded preview. After confirmation, fast-forward `main`, push it, and verify `https://flypig23.github.io/` serves the new version.
