# Vercel Research Portal

## Purpose

The repository includes a publication-grade Next.js research portal that presents the Part 2 study without inventing empirical results. It is designed for Vercel deployment and lives at the repository root alongside the Python reproducibility package.

## Scientific presentation contract

The portal may present:

- the research question and novelty;
- benchmark roles and provenance rules;
- model tiers and evaluation dimensions;
- the deterministic execution pipeline;
- reproducibility commands and repository structure;
- research-readiness / evidence status.

The portal must not present unexecuted metrics as findings. Empirical cards, plots, tables, model-download links, and numeric claims remain locked until an accepted run passes `scripts/research_gate.py`.

## Architecture

- Framework: Next.js App Router + TypeScript
- Rendering: static/server-first content; no client data dependency
- Styling: repository-local CSS; no external font dependency
- Metadata: scholarly title, description, keywords, Open Graph, Twitter card, JSON-LD
- Security: no powered-by header plus Vercel response headers for MIME sniffing, framing, referrer policy, and browser permissions
- CI: typecheck + production build on portal changes
- Runtime secrets: none required for the current pre-results portal

## Local development

```bash
npm install
npm run dev
```

Then open `http://localhost:3000`.

## Validation

```bash
npm run typecheck
npm run build
```

## Vercel deployment

1. In Vercel, create a new project and import:
   `Arungharami/Customer-Behavior-Prediction-in-Banking-and-Insurance-2`
2. Keep the repository root as the project root.
3. Framework preset should resolve to Next.js.
4. Build command: `npm run build`.
5. Install command: `npm install`.
6. No environment variables are required for the initial portal.
7. Deploy a preview first, inspect desktop/mobile rendering, then promote or deploy the `main` branch to production.

Vercel Git integration can then create previews for pull requests and production deployments from the configured production branch.

## Recommended Vercel project name

`beyond-static-accuracy`

Alternative:

`customer-behavior-prediction-part2`

## Post-results upgrade path

After an accepted experiment run is frozen, the site can be extended with generated JSON under a public-safe directory such as `public/results/`. A publication export script should copy only verified, non-restricted aggregate artifacts into that directory. The website should then render:

- held-out discrimination with confidence intervals;
- calibration curves and summary metrics;
- time-window degradation and PSI alerts;
- explanation-stability summaries;
- accuracy/stability/efficiency Pareto comparisons;
- fixed-capacity and cost-sensitivity views;
- ablation results;
- model-card link for the accepted compact model.

Restricted competition data and private manuscript drafts must never be copied into the Vercel output.

## Release gate

A production research-results release should require all of the following:

- accepted run ID is frozen;
- research gate passes;
- all public numbers are traceable to machine-readable artifacts;
- every displayed figure/table matches the manuscript registry;
- no restricted raw dataset is included;
- no blind-review identity policy is violated;
- the deployed commit SHA is recorded in the research release notes.
