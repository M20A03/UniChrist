---
name: anti-ai-auditor
description: >-
  Audits scripts, content, code, and media assets against the 17 Absolute Anti-AI Prohibitions.
  Checks for forbidden buzzwords, unmastered audio, linear transitions, and static frames.
---

# Sector 3 Tool: Anti-AI Standards Auditor & Linter

This skill enforces zero-tolerance quality gates across all generated assets.

## The 17 Prohibitions Linter Checklist

1. **Buzzword Audit:**
   Scan text for forbidden words: `delve`, `tapestry`, `game-changer`, `testament`, `revolutionize`, `in conclusion`, `furthermore`, `realm`, `beacon`, `pinnacle`.
   *Action:* Flag and replace with direct, plain factual statements.

2. **Emoji Audit:**
   Scan for `🚀`, `✨`, `🔥`, `🧠`, `💡`, `🤖`.
   *Action:* Strip immediately.

3. **Audio Mastering Audit:**
   Verify loudness against EBU R128: `-13.6 ± 0.5 LUFS`, True Peak `≤ -1.0 dBFS`.
   Verify background music ducking: `-20dB` under narration.

4. **Visual & Motion Audit:**
   Verify frame hold `<= 2.0s`.
   Verify spring physics: `damping: 14`, `stiffness: 180` (no linear transitions).
   Verify caption vertical safe zone: bottom `250px–300px`.

5. **Recursive Loop Exit Condition:**
   Calculate score `[1–10]`. If `< 9.0/10`, trigger automated revision. Proceed only when score `>= 9.0/10`.
