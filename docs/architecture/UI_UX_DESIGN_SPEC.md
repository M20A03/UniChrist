# UI/UX Design System Specification (Anti-Vibe-Coded Intentional Design)
## Based on Emil Kowalski Design, Impeccable Standards & Taste Skill

### 1. Design Direction: Academic Editorial & Neo-Functionalism
- **Philosophy:** Content-first, high information density, intentional micro-interactions, robust typographical hierarchy. Zero marketing fluff, zero cliché decorative artifacts.
- **Palette Foundation:**
  - Canvas Deep: `#090D14` (Christ Deep Indigo Black)
  - Surface Elevated: `#111827` (Card Surface)
  - Border Subdued: `#1F2937` (1px clean geometric dividers)
  - Primary Accent: `#D4AF37` (Imperial University Gold - Matte, non-glowing)
  - Secondary Accent: `#2563EB` (Cobalt Blue - Crisp, zero purple tint)
  - Text Primary: `#F9FAFB` (High contrast legibility)
  - Text Secondary: `#9CA3AF` (Muted functional meta-information)
  - Functional Alerts: `#059669` (Success Emerald), `#D97706` (Amber Notice), `#DC2626` (Red Flag)

### 2. Forbidden Anti-Patterns (Strictly Enforced)
- ❌ **No Purple Gradients:** Gradient backgrounds and purple-to-pink CTA buttons are prohibited.
- ❌ **No Lucide Default Icons:** Replaced by custom SVG monoline glyphs crafted specifically for academic operations.
- ❌ **No Sparkle Icons:** Sparkles (`✨`) or AI hype icons are banned.
- ❌ **No Generic Bento Grids:** Grid layouts follow rigorous tabular editorial systems with explicit cell ratios.
- ❌ **No Glassmorphism:** No blurred translucent glass panels or backdrops with `backdrop-filter: blur(20px)`. Solid high-contrast surfaces only.
- ❌ **No Emojis in Headings:** Headings must be clean, professional, and semantic without emoji prefixes.
- ❌ **No Glowing Borders:** Strict 1px solid borders (`#1F2937` or `#E5E7EB`).
- ❌ **No Inter Default Typography:** Utilizing authentic editorial typography:
  - Display & Headings: `Cinzel` (Classical Roman Serif with geometric precision)
  - Data & Operational Interface: `JetBrains Mono` and `Space Grotesk` for dense tabular readouts.

### 3. Motion & Animation Principles (Emil Kowalski Spec)
- **Physics-driven Springs:** Transitions utilize spring parameters with dampening `stiffness: 400, damping: 30`.
- **Purposeful Micro-Interactions:** Animations exist solely to convey state changes (e.g., ticket state transition, parking slot vacancy shift). No decorative floating elements.
- **Transitions.dev & React Bits Layout:** Tab changes trigger linear directional slide-and-settle with 0.18s cubic-bezier ease (`cubic-bezier(0.16, 1, 0.3, 1)`).

