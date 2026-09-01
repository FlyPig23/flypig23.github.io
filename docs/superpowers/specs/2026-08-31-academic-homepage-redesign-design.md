# Hangxiao Zhu Academic Homepage Redesign

Date: 2026-08-31  
Status: Approved

## Summary

Redesign the existing GitHub Pages homepage as a single-page research index. The new site should feel academically credible and technically distinctive without becoming a dark cyberpunk interface. It will preserve the existing identity, school, contact, and personal assets while improving information hierarchy, publication accuracy, responsiveness, accessibility, and maintainability.

The selected visual direction is **Signal & Structure**: a deep charcoal opening section followed by a very light cool-gray reading surface. Texas A&M maroon is a controlled accent color. It must never be used for Hangxiao Zhu's name.

## Goals

- Make Hangxiao's research identity legible within the first viewport to both academic and industry-research visitors.
- Preserve the existing portrait, school logos/mascots, academic history, advisors, contact links, CV, and personal interests.
- Present all works with equal visual weight in a compact, reverse-chronological bibliography.
- Add only SciImpact and MemeBridge to News.
- Correctly distinguish peer-reviewed papers, preprints, and the master's thesis.
- Keep the site fast, accessible, responsive, and easy to maintain on GitHub Pages.

## Non-goals

- No framework, CMS, database, analytics, search, filtering, blog, or additional route.
- No featured-paper or featured-project treatment.
- No replacement of the portrait or school imagery.
- No change to the public domain, GitHub Pages deployment source, CV URL, or existing section anchors where they remain applicable.
- Do not add the externally discovered “Synergizing Embedding and Generative Language Models…” manuscript until its current title and submission status are confirmed; it is not present on the linked Scholar profile and public sources conflict.

## Audience and success criteria

The homepage should balance two audiences: faculty/collaborators and industry research teams. Academic credibility takes priority, with a strong but restrained technical character.

A successful result lets a visitor quickly answer:

1. Who is Hangxiao Zhu and where does he work?
2. What areas does he research?
3. What has he published most recently?
4. How can the visitor read the work or make contact?

## Information architecture

The site remains one continuous page with this order:

1. **Hero**
2. **About / Education**
3. **Research Interests**
4. **News**
5. **Publications**
6. **Footer**

The top navigation links to the relevant page anchors. On narrow screens, it remains compact and does not become a complex menu.

### 1. Hero

The hero uses a deep charcoal background and contains:

- Texas A&M logo in its original maroon color on a light neutral tile.
- Hangxiao Zhu's portrait.
- Hangxiao Zhu's name in warm white, never maroon/red.
- Ph.D. identity and Texas A&M Computer Science affiliation.
- A concise research statement centered on intelligent agents, data-driven systems, and scientific discovery.
- Visible Email, Google Scholar, and CV links with text labels, not icon-only controls.

### 2. About / Education

This section appears immediately after the hero. It preserves the current personal story and reorganizes it into two readable parts:

- A concise About paragraph covering current Ph.D. study, mentors, earlier education, and research-intern experience.
- An Education / Mentorship timeline containing Texas A&M, Washington University in St. Louis, Ohio State, and Purdue-related mentorship.

The existing Reveille, WashU Bears, and Buckeye imagery moves out of inline prose and into the structured education area. The current sports interests remain as a short “Beyond Research” note.

### 3. Research Interests

Display exactly these three areas, in this order:

1. Agent System
2. Data Mining
3. AI for Science

They appear as equal-weight typographic blocks rather than interactive cards.

### 4. News

News contains exactly two entries:

- 2026 — SciImpact accepted to Findings of ACL 2026.
- 2026 — MemeBridge accepted to KDD 2026, Datasets and Benchmarks Track.

Do not include the former CHI 2025 or Ph.D.-start items. Do not invent month/day dates that have not been supplied or verified.

### 5. Publications

Use one compact bibliography, newest first. No work receives a larger card, thumbnail, or “featured” label. Each row includes:

- Year and accurate venue/status label.
- Linked title.
- Full author list when available, with **Hangxiao Zhu** emphasized.
- Venue or status description.
- Available primary links such as Paper, Project, DOI, or Thesis.

The linked Google Scholar profile currently contains these nine works:

- **2026 — MemeBridge: A Dataset for Benchmarking and Mitigating the Bidirectional Cultural Gap in Meme Interpretation.** Hangxiao Zhu, Suliu Qin, Zhuoyan Li, Ming Jiang, Yu Zhang, Meng Xia. KDD 2026, Datasets and Benchmarks Track.
- **2026 — SciImpact: A Multi-Dimensional, Multi-Field Benchmark for Scientific Impact Prediction.** Hangxiao Zhu, Yuyu Zhang, Ping Nie, Yu Zhang. Findings of ACL 2026.
- **2026 — Inference-Time Control for Trustworthy Large Language Models.** Multi-author working paper/preprint; Hangxiao Zhu is a coauthor. It must not be shown as conference-accepted.
- **2026 — Beyond Semantic Similarity: Rethinking Retrieval for Agentic Search via Direct Corpus Interaction.** Multi-author arXiv preprint; Hangxiao Zhu is a coauthor.
- **2025 — Survivors, Complainers, and Borderliners: Upward Bias in Online Discussions of Academic Conference Reviews.** Hangxiao Zhu, Yian Yin, Yu Zhang. arXiv preprint.
- **2025 — TutorUp: What If Your Students Were Simulated? Training Tutors to Address Engagement Challenges in Online Learning.** Sitong Pan, Robin Schmucker, Bernardo Garcia Bulle Bueno, Salome Aguilar Llanes, Fernanda Albo Alarcón, Hangxiao Zhu, Adam Teo, Meng Xia. CHI 2025.
- **2025 — From Text to Trust: Empowering AI-assisted Decision Making with Adaptive LLM-powered Analysis.** Zhuoyan Li, Hangxiao Zhu, Zhuoran Lu, Ziang Xiao, Ming Yin. CHI 2025.
- **2024 — Mending Trust in AI: Trust Repair Policy Interventions for Large Language Models in Visual Data Journalism.** Hangxiao Zhu. Washington University in St. Louis master's thesis.
- **2023 — Synthetic Data Generation with Large Language Models for Text Classification: Potential and Limitations.** Zhuoyan Li, Hangxiao Zhu, Zhuoran Lu, Ming Yin. EMNLP 2023.

Within the same year, use the latest verifiable release/publication date. The verified 2026 order is MemeBridge (August), SciImpact (July), Inference-Time Control (May 15), then Beyond Semantic Similarity (May 3). When precise dates are unavailable, display only the year rather than inventing a day or month.

The existing three publication thumbnail files remain in the repository for compatibility but do not appear in the new bibliography, because showing them for only three works would violate the equal-weight requirement.

### 6. Footer

Use a normal document-flow footer so it cannot cover content. Show a current copyright year and a restrained “Last updated” value if it can be maintained accurately.

## Visual system

### Color

- Hero: deep charcoal, approximately `#171A1F`.
- Main reading surface: very light cool gray, approximately `#F5F7F8`.
- Primary text: near-black charcoal.
- Secondary text and rules: cool neutral grays.
- Brand/accent: Texas A&M maroon `#500000`.
- Name: warm white in the hero and near-black on light surfaces; never maroon/red.

Maroon is reserved for the TAMU mark, year/venue labels, link/focus states, and fine structural accents.

### Typography

- A restrained serif display face or system serif for the name and major section titles.
- A highly readable system sans-serif for paragraphs, authors, and navigation.
- A system monospace face for small year, venue, and section-index labels.

The hierarchy should remain compact: publication titles must not expand into oversized multi-line headings on mobile.

### Layout and motifs

- Full-width dark hero followed by a centered editorial reading column.
- Subtle grid/orbit geometry in the hero using CSS only; it remains decorative and non-interactive.
- Thin rules, numbered labels, and generous horizontal rhythm provide the technical character.
- Corner radii are small and deliberate; the site should not look like a generic card dashboard.

## Responsive behavior

- Desktop uses an editorial grid with a readable maximum content width.
- Tablet reduces gaps and column widths without forcing a fixed sidebar.
- Mobile becomes a single left-aligned flow; the portrait, identity, education items, and publication metadata stack cleanly.
- Contact targets are at least approximately 44px high on touch screens.
- No fixed footer or absolute-positioned reading column.

## Interaction and motion

- Smooth anchor navigation may be used when reduced motion is not requested.
- Links and publication rows receive subtle hover/focus feedback.
- No cursor effects, parallax, auto-playing animation, or decorative interaction that competes with reading.
- Respect `prefers-reduced-motion`.
- A minimal script may update the copyright year; the content remains fully usable without JavaScript.

## Accessibility and metadata

- Use semantic `header`, `nav`, `main`, `section`, `article`, and `footer` landmarks.
- Add a keyboard-visible skip link and focus styles.
- Preserve or improve descriptive alt text for the portrait and school imagery; mark purely decorative motifs as hidden.
- Add a clear page description, canonical URL, Open Graph text metadata, and Person/ScholarlyArticle structured data where accurate.
- External links opened in new tabs use safe relationship attributes.
- Maintain sufficient contrast for text, maroon accents, and controls.

## Technical constraints

- Preserve the existing static HTML/CSS architecture and GitHub Pages root deployment.
- Preserve existing public asset paths, especially the portrait, school assets, and CV URL.
- Keep `#about-me`, `#news`, and `#publications` anchors compatible; add a research-interest anchor without breaking old links.
- Optimize with explicit image dimensions, lazy loading below the fold, and a derived responsive portrait format without overwriting the original source image.
- Do not add a build step or third-party framework.

## Verification and acceptance criteria

Before publishing:

- Verify all nine Scholar works appear exactly once and in reverse chronological order.
- Verify SciImpact says **Findings of ACL 2026**, not ACL main.
- Verify MemeBridge says **KDD 2026, Datasets and Benchmarks Track**.
- Verify the three preprints are not presented as accepted conference papers.
- Verify News contains only SciImpact and MemeBridge.
- Verify the name is not red anywhere.
- Verify the TAMU logo uses its original maroon color.
- Verify the About / Education section immediately follows the hero.
- Check desktop, tablet, and mobile widths for overflow and readability.
- Check keyboard navigation, visible focus, reduced-motion behavior, image loading, and external links.
- Run HTML/CSS validation and a local link/asset check.
- Ensure the GitHub Pages deployment path remains the repository root.
