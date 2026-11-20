---
name: emil-kowalski-design
description: >-
  Implements Emil Kowalski interaction design standards: physical spring animations,
  tactile feedback, micro-interactions, and fluid gesture physics.
---

# 🌀 Emil Kowalski Design & Micro-Interaction Engine

## Spring Physics Specification:
- **Never use linear or robotic CSS transitions (`transition: all 0.3s ease`).**
- Use physical spring curves calibrated for human perception:
  ```js
  // High-performance spring physics
  damping: 14,
  stiffness: 180,
  mass: 0.8
  ```
- **Exit Velocity & Layout Transitions:**
  - Fast responsive entry (< 200ms), smooth decelerating settling.
  - Scale transforms should never exceed `1.02` on hover; keep tactile and grounded.
