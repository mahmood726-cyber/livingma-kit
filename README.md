# livingma-kit

Canonical source of the **shared front-end assets** vendored by the ~41
`*_LivingMeta` GitHub-Pages dashboards (AntiAmyloid-AD, Antiplatelet-NMA,
AttrCM, …).

Each LivingMeta repo is its own GitHub-Pages site and must ship **fully
offline** — so it vendors a copy of `assets/` (Plotly, the Paper Studio
bundle, the advanced-stats / vendor JS, Tailwind, …) and `configs/`. Those
files were **byte-identical across all 41 repos** (86 asset files + configs),
i.e. one logical bundle copied 41×.

This repo holds that bundle **once**. Edit it here, then propagate with the
sync script — instead of hand-editing dozens of copies.

## Layout

```
assets/    plotly.min.js, paper-studio.* , vendor/*.js, stats-ext.js, ...  (86 files)
configs/   shared dashboard config templates
sync_repos.py   copy this kit into every *_LivingMeta repo (idempotent)
```

## Usage

```bash
# Preview what would change across all sibling *_LivingMeta repos:
python sync_repos.py --dry-run

# Propagate the kit (only writes files that differ; never touches each
# repo's unique *_REVIEW.html):
python sync_repos.py
```

The sync **never** modifies a repo's topic-specific `*_REVIEW.html` — it only
refreshes the shared `assets/` and `configs/`. After syncing, commit/push each
changed repo as usual.

## Why a kit (not removing the vendored copies)

GitHub Pages serves each repo independently and cross-repo references don't
resolve, so the assets must stay vendored per repo for offline use. The kit is
therefore a **single source of truth + propagation tool** (same pattern as
`aact-kit` and the e156 `chart-kit`), not a runtime dependency.
