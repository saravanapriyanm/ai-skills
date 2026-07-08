---
name: aggressive-dry-kiss-docs
description: >-
  Use this skill whenever writing, reviewing, or editing documentation for the organisation
  — READMEs, wikis, runbooks, onboarding docs, design docs, Slack-thread-turned-doc
  write-ups, or any internal reference material. Also use when a user asks to
  "document" something they did, asks whether something should be written up, or
  asks for feedback/review on existing docs. Applies the org's documentation
  standard — Aggressive (document everything, don't skip it), DRY (single source
  of truth, no duplication), KISS (no fluff, omit the obvious). Trigger even if
  the user doesn't name the standard explicitly; any documentation task in this
  org should follow it.
---

# Aggressive DRY KISS Documentation

The org's documentation principle, in three lines:

- **Aggressive** — Document everything you do. No exceptions, no "later."
- **DRY** — Don't say the same thing twice. Keep a single source of truth.
- **KISS** — Don't add fluff. If something is obvious, omit it.

Use this skill both when **writing new documentation** and when **reviewing/editing existing documentation**.

## When writing documentation

1. **Check for an existing source first.** Before writing anything, search for whether this already has a home (another doc, a README, a wiki page). If it exists but is stale or wrong, edit it in place rather than creating a parallel doc.
2. **If it doesn't exist, write it now.** Don't defer "obvious" or "small" things — those are exactly what the aggressive principle is meant to catch. If the user did something noteworthy (shipped a feature, made a decision, changed a process, debugged something non-trivial), default to writing it up rather than asking if it's worth it.
3. **Write once, link elsewhere.** State each fact, config value, or decision in exactly one place. If it needs to be referenced from another doc, add a short pointer line and a link — don't restate the content.
4. **Cut anything obvious to the intended reader.** No throat-clearing, no restating what the reader already knows, no hedging language, no speculative edge cases that haven't happened yet.
5. **One idea per sentence, one topic per paragraph.** Optimize for a teammate skimming this in under a minute.

## When reviewing existing documentation

Walk through this checklist and flag violations directly — don't just describe the principle, point at the specific line/section:

**Aggressive**
- [ ] Is there anything this doc *should* cover but doesn't? (undocumented steps, unstated assumptions, tribal knowledge)
- [ ] Would a new hire be able to do this without pinging someone directly?

**DRY**
- [ ] Is any fact, value, or explanation repeated in more than one place? Flag it and point to which instance should become the canonical one (usually the most detailed/most recently updated).
- [ ] Are there paragraphs duplicated across docs that should instead be a link back to one canonical doc?
- [ ] Is a short pointer line before a link acceptable here, or has it drifted into re-explaining the linked content?

**KISS**
- [ ] Is anything stated that would be obvious to the intended reader? Suggest cutting it.
- [ ] Are there sentences doing more than one job? Split them.
- [ ] Is there hedging, throat-clearing, or "as you may know" language? Cut it.
- [ ] Are there speculative edge cases with no evidence they've occurred? Cut or move to a "known limitations" section rather than inline.

## Output format for reviews

When reviewing a doc against this standard, structure feedback as:

```
**Aggressive gaps:** [missing content, or "none found"]
**DRY violations:** [duplicated content + where the single source of truth should live]
**KISS violations:** [specific lines/sections that are obvious or fluffy, with a suggested cut or rewrite]
```

Keep the review itself KISS-compliant: point at the problem, don't over-explain the principle behind it — the person already knows the standard.

## Quick gut check (use while drafting)

| Ask yourself | If yes |
|---|---|
| Am I about to explain something twice? | Delete one, link instead |
| Am I about to explain something obvious? | Delete it |
| Am I skipping this because it feels like too much effort? | Write it anyway - that's the aggressive principle talking you out of it |
