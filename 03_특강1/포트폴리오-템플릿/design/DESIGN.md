# Najmi Portfolio — Deep Purple and Gold

Based on the supplied `DESIGN-pinterest.md`: rounded card geometry, clear heading hierarchy, a responsive project grid, and pill-shaped actions. The supplied analysis remains unchanged. The user's card-news screenshot informs information hierarchy only; its imagery, branding, and wording are not copied.

## User-approved direction

- Canvas: deep purple `#100a1c`.
- Panels: `#211431` and `#1c112a`.
- Headings: warm ivory `#fff6df`.
- Body: `#e1d6e9`.
- Secondary text: `#bdb0ca`.
- Accent: muted gold `#e7c779`.
- Borders: `#493552`; stronger borders on the featured project.
- Restrained gold metallic highlights on primary actions and the featured-project panel.
- Typography: Pretendard Variable with system fallbacks for Korean and English. Do not use proprietary Pin Sans.
- Cards: 16px corners; featured panel and video frame: 32px; actions: pill shape.
- Maximum content width: 1160px; mobile layouts stack into one column.
- Shared layout for both languages. Korean is the default; a small inline script switches language, document title, description, and Person metadata.

## Preserved assignment structure

Profile → work inventory → CakGo case study with all five required parts → five-card Korean personal-introduction gallery. Following the user's clarification of the lecturer's brief, the cards introduce the person, with projects as evidence. Keep Person JSON-LD and omit missing/private project links.

## Implementation notes

- `portfolio/index.html` opens directly in a browser. It does not require Python, Node, dependencies, or a build step.
- `portfolio/styles.css` contains the shared design.
- `build-portfolio.py` is the authoring source for the initial page. It overwrites `index.html` when run; preserve any later manual additions before regenerating.
- `verify-portfolio.mjs` runs local QA through an installed Chrome browser and writes screenshots to a temporary folder. It is not included in the public website.
- The original HTML template is retained as `portfolio/index_이전.html`. It is a local backup, not a finished public page; exclude it when preparing the final submission/deployment folder.
- The demo poster is a frame from the user's actual recording, not a generated interface or fabricated result.

## Previous palette

The blue-and-silver HTML, CSS, design notes, and authoring source are preserved in `design/blue-silver-backup/`. The current user-approved palette is purple and gold.
