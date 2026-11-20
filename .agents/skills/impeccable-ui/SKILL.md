---
name: impeccable-ui
description: >-
  Enforces the pbakaus/impeccable craft standard: pixel alignment, contrast ratios,
  responsive tap targets, optical optical centering, and layout stability.
---

# 💎 Impeccable UI Craft Standard

Based on `pbakaus / impeccable`.

## Checklist:
1. **Contrast & Hardcopy Readability:** WCAG AAA compliance; pure high-contrast foregrounds (`#0F172A`) against crisp backgrounds (`#FFFFFF`).
2. **Optical Balance:** Compensate visually for geometric quirks (e.g. play button icons offset by +2px).
3. **No Cumulative Layout Shift (CLS):** Explicit width/height on all images, skeleton loaders, and containers.
4. **Touch Target Sizing:** Minimum 44x44px interactive bounding box for mobile accessibility.
