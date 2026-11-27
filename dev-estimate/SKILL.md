---
name: dev-estimate
description: Estimate dev + testing hours for a client quote from a BRD and/or feature-list CSV, producing two tracks in one CSV - a lean MVP and a full production-ready app, both AI-assisted. Starts by discussing and locking the tech stack. Use when the user asks for an estimate, quote, effort, hours, or timeline for a project/BRD/feature list.
---

# Dev Estimate (MVP vs Production)

Output = **hours only** (dev + testing), no dates, no team size, no cost. User adds rates.
Team always builds with AI (Claude Code etc.) - every hour here is AI-assisted. Never produce a no-AI estimate.

## Inputs
- BRD (pdf/docx/md) and/or features CSV (any column layout - map it, don't demand a format).
- Read both fully before saying anything. Note features in BRD missing from CSV and vice versa.

## Step 1 - Stack discussion (STOP and wait)
Stack changes hours a lot (e.g. BaaS gives auth/storage for free), so lock it first.
1. Pull drivers from BRD: platforms (web/iOS/Android/admin), users & scale, integrations
   (payment, SMS, maps, ERP), realtime, offline, compliance/data residency, hosting constraints.
2. Propose 2-3 stack options as a short table: frontend, backend, DB, auth, hosting,
   with pros/cons tied to *this* BRD and the hour impact ("saves ~X h on auth/admin").
3. Recommend one. Ask the user to confirm or pick. **Do not estimate until confirmed.**

## Step 2 - Gaps (one round, max 5 questions)
Ask only what moves hours: number of roles, integrations' API availability, design provided
or not, languages/i18n, report/export count, data migration. Everything else -> assumption.

## Step 3 - Work breakdown
Write `<project>-work.csv` next to the inputs with columns:
`module,feature,moscow,complexity,dev_o,dev_m,dev_p,test_o,test_m,test_p,mvp_scope,notes`

Rules:
- One row per feature from CSV/BRD; split anything with `dev_m` > 24h into sub-features.
- Hours = **mid-level dev using AI coding agents, on the confirmed stack, building the
  production-quality version** of the feature. Script derives MVP from it.
  O/M/P = optimistic / most likely / pessimistic. Typically O ≈ 0.7·M, P ≈ 1.5-2·M (wider for
  integrations, unclear BRD items).
- Test hours = manual + automated testing for that feature (typically 30-40% of dev).
- `moscow`: Must = core flow needed for MVP; Should/Could = production only; Wont = out of scope.
- `mvp_scope`: what MVP cuts for Must items (e.g. "email only, no SMS; no bulk import").
- `notes`: assumptions and exclusions per row - these protect the quote.
- Always add `_Cross-cutting` rows with `moscow=Prod` (production only), sized to the project:
  project setup & CI/CD, environments (dev/stage/prod), security hardening (OWASP, rate limits,
  secrets), logging & monitoring, performance/load testing, accessibility, regression test
  automation, UAT bug-fix support, deployment & go-live. And one `Must` row for basic MVP
  setup + deploy.

Reference (AI-assisted, production quality, likely hours, adjust per stack):
| Item | Dev | Test |
|---|---|---|
| Auth (login/signup/reset/OTP) | 8-12 | 4-6 |
| Role/permission system | 8-12 | 5-6 |
| CRUD screen + API per entity | 3-5 | 2-3 |
| Complex form w/ validation | 3-5 | 2 |
| List w/ search/filter/sort/paging | 3-4 | 1.5-2 |
| Dashboard (per 4-6 widgets) | 8-12 | 4-5 |
| Report + PDF/Excel export | 4-6 | 2-3 |
| Third-party integration (per) | 10-20 | 5-8 |
| Payment gateway | 16-28 | 8-12 |
| Notifications (email/SMS/push, per channel) | 3-5 | 2 |
| File upload + storage | 3-4 | 1.5-2 |
| Realtime (chat/live updates) | 14-24 | 8 |
| Mobile app screen (RN/Flutter) | 4-6 | 2-3 |
| Admin panel (basic) | 12-20 | 6-8 |

## Step 4 - Compute
```
python3 ~/.claude/skills/dev-estimate/estimate.py <project>-work.csv <project>-estimate.csv
```
Scope multipliers (edit top of script): MVP dev ×0.7, test ×0.5, buffer ×1.15 (Must only -
lean scope, happy-path testing); Production dev ×1.0, test ×1.0, buffer ×1.3 (all except Wont).
Integrations, payments and unclear BRD items gain least from AI - keep their P wide, since
review, third-party sandboxes and QA stay human-bound.

## Step 5 - Report
In chat, give: stack chosen, MVP total vs Production total (dev / test / total), top 5
cost drivers, key assumptions & exclusions, and the path to `<project>-estimate.csv`.
Never quote a number without its assumptions.
