---
layout: default
title: Workshop worksheet
description: "Keep enough evidence to explain your result without copying your entire history."
permalink: /worksheet/
workshop: true
---

## A small record for each ticket

Copy this once per ticket into your own notes, then use the exercise records
below in workshop order:

| Field | Your observation |
|---|---|
| Ticket and acceptance criteria | |
| App session, source directory and handoff branch | |
| Mode, model and effort | |
| Repository/file-access and MCP approvals, denials or unresolved permissions | |
| Skill loaded and guidance used | |
| Generated test assertions reviewed before implementation | |
| Initial failing tests and assertion messages | |
| Reviewed production/test/UI changes | |
| Test command and results (tests, failures, errors, skipped) | |
| Commit and preview outcome | |
| PR link, actual Merged status, verified main commit and merged-revision checks | |
| Worked alone, with a partner, or from a demonstration/reference? | |
| Unfinished work or results not yet checked | |

Do not include API tokens, passwords, cookies or unrelated personal work.
If you use a reference solution or watch a demonstration, note which steps
you also ran yourself.

## Three task handoffs

| Session | Reviewed PR | Verified main commit and checks |
|---|---|---|
| Cart: quantity bug | | |
| Cart: item removal, including Canvas | | |
| Cart: query optimization | | |

Merge and verify each PR before creating the next session from updated `main`.
Name each session only after sending its first prompt.

## Canvas: one observed improvement

| Field | Your observation |
|---|---|
| Active session/directory and server owner | |
| Browser canvas URL and selected element | |
| Observed UI issue and accepted scope | |
| impeccable guidance actually used, or unavailable | |
| Before/after keyboard and narrow-screen observations | |
| Regression results and reviewed feature handoff | |
| Native picker used, browser fallback or demonstration | |

## MCP before and after

| Field | Before | After |
|---|---|---|
| Reviewed source directory/branch | | |
| Workload: eight distinct products, GET `/api/cart` | | |
| Request ID, method/path and time | | |
| Tool names and actual arguments | | |
| Observed SELECT count | | |
| Product fields, count and total preserved? | | |
| Source: MCP call in the App, saved reference or demonstration | | |

Wait for DevTools to load the fix, then capture a fresh request profile.
Reusing the baseline profile does not show whether the optimization worked.

Also record query-contract test results for **8 and 16 distinct products**:
exactly **1 SELECT** per completed HTTP GET `/api/cart`, excluding setup queries
and preserving response values. The eight-product MCP capture is separate evidence.

## Parallel handoff

Keep all three task PR links and verified merge results. The MCP handoff PR
establishes the published `origin/main` commit used to start both workers.
Then keep each worker's handoff: its branch/commit, changed files, executed checks
and limitations. Both must start from that same updated `main` commit; let
Copilot capture the commit details. If the MCP handoff used local recovery, record
the accepted local starting branch/commit and **main not updated: local recovery used**.
Only record a preview or runtime result if that worker ran the
matching application. Mark integration checks **pending** until you test the
merged result.

If a boundary case exposed a bug, record the failing regression, approved fix
and passing rerun in that session. For overlapping files, record any conflict
resolutions and checks that both contributions still work; no conflict is also
a valid outcome.

## Agent Merge and integration

| Field | Your observation |
|---|---|
| Own repository and both worker PRs targeting `main` | |
| UI PR link, linked in Cart: empty-state UX, head and CI results | |
| UI PR merge authorization and actual status | |
| UI merged-main revision and its passing tests CI job | |
| Boundary-test PR link, linked in Cart: boundary tests, head/updated commit and fresh CI results | |
| Boundary-test PR merge authorization and actual status | |
| Agent Merge corrections or conflicts reviewed | |
| Merged main commit checked in Cart: boundary tests before checkout, both contributions and full-suite results | |
| Combined preview from the verified directory: quantities, removal, empty-cart link, keyboard and narrow screen | |
| Recovery used, open PRs and unfinished work | |

Keep the PRs sequential. A running agent, local test pass or enabled merge
permission is not confirmation that GitHub merged the PR. If using local
recovery, record **Agent Merge not completed: local recovery used**.

## Rubber duck: critique and decision

| Field | Your observation |
|---|---|
| Checked result and comparison starting point | |
| Actual critic invocation/model if exposed, or unavailable | |
| Finding, code/evidence and impact | |
| Accepted, rejected or deferred, with reason | |
| Follow-up branch/PR, merge status and verified main result if corrected | |

## Five subagents: mock-checkout implementation

| Field | Your observation |
|---|---|
| Shared goal, reviewed base and checkout feature branch | |
| Cart: mock checkout session, new worktree directory and verified starting commit | |
| Approved HTTP contract, test setup/probes and exclusive file/fixture ownership | |
| Common starting commit verified in all five child worktrees | |
| Five actual assignments/contributions; concurrency observed | |
| Load check, five-way concurrency approval and observed execution overlap or limitation | |
| Reviewer's findings, reviewed PR head at merge authorization and fix/defer decisions | |
| Later Agent Merge repair commits, checks and review coverage or limitation | |
| Questions/answers exchanged, directly or through the orchestrator | |
| Implemented API, order snapshot, atomic clearing and duplicate handling | |
| Conflicting proposals resolved or decisions still open | |
| Full-suite counts, including baseline, generated cart/removal/query, boundary, CheckoutContractTest and CheckoutResilienceTest | |
| Rollback, snapshot and concurrent/later-retry evidence | |
| Browser canvas receipt, cleared cart, keyboard and narrow-screen observations | |
| Final diff accepted, checkout publication approved, Agent Merge repairs reviewed and merge separately authorized | |
| Checkout PR URL, repository, feature head and base `main` checked | |
| Actual merge status/commit and checks for that merged revision | |
| Verified main commit, local full-suite results and running directory/URL | |
| Place order and receipt verified with the app serving the verified merged-main code | |
| Delegation or messaging unavailable, or demonstration | |

Record four writers' local handoffs and the read-only review:

| Child session | Session link, worktree and branch | Integrated handoff commit or reviewed commit/findings |
|---|---|---|
| Checkout: backend | | |
| Checkout: UI | | |
| Checkout: HTTP tests | | |
| Checkout: resilience tests | | |
| Checkout: review | | No code commit; record findings |

Mark checkout **merged and verified on main**, **unfinished**, or **demonstrated**
according to the evidence. Use **verified locally; delivery blocked** or
**merged; post-merge verification blocked** when appropriate.
Record actual contributions. Write **none exchanged** if there were no questions/answers, and
**unknown** for concurrency you did not observe. Local checkout code is not on
`main` until its checkout PR actually merges. Keep the approved plan and agent
activity available for Chronicle.

## Chronicle: one better habit

| Field | Your observation |
|---|---|
| Privacy choice and scope controls checked before running | |
| Cart: Chronicle analysis session, excluded from source sessions | |
| Current repository, reported seven-day range/timezone and actual source sessions | |
| Returned scope and coverage | |
| Reported input/output/cache/usage values **with units**, or unavailable | |
| Observed turnaround/rework and quality evidence, or unavailable | |
| Token/time/quality trade-off and supporting session/example | |
| One prompt/workflow change | |
| Suggested repository instruction (proposal only, not applied) | |
| Expected token/time/quality benefit (prediction until measured) | |
| Acceptance and review checks retained | |
| Result observed, or improvement not yet checked | |

There is no required savings percentage. Different tasks are not controlled
trials. Do not convert a usage multiplier or byte count into dollars/tokens.
Keep your full Chronicle output private; share only the relevant, reviewed excerpt.

## Final review and handoff

Return to **Cart: mock checkout** for the
[read-only final review]({{ site.baseurl }}/finish/#final-review).
Record the verified result separately from unfinished local work.

| Field | Your observation |
|---|---|
| Read-only review session/worktree and verified result commit | |
| Comparison starting point and result commit, reported by Copilot | |
| Local edits/untracked files, excluded from the verified result | |
| Final full-suite counts and per-class reports, including both checkout suites | |
| Findings/decisions and separately approved correction PRs | |
| Actual PR/CI status, verified revision and running directory/URL | |
| Completed, demonstrated, unfinished or blocked status, with reason | |
| Handoff: what changed, checked, still unknown and one reusable habit | |

Keep the handoff concise; do not attach private Chronicle output or unrelated history.
