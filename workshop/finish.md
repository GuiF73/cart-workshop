---
layout: default
title: Review and hand off
description: "Review the complete change, check your results and record what remains unfinished."
permalink: /finish/
workshop: true
---

## Final review
{: #final-review}

The checkout chapter already reviewed and delivered the code. Return to
**Cart: mock checkout** after the Chronicle exercise for this **read-only**
final review of the verified merged-main revision. If delivery was blocked,
review the recorded reviewed local result and state that limitation instead.
Inspect **Changes** in the App, then ask Copilot to compare your original starter
with that verified commit, including all committed tickets.
Report current edits and untracked files separately as unverified work;
preserve them rather than treating them as part of the verified result.
If continuing from a separate reference checkout, compare from **`v2-start`**
instead and note that your work is based on the reference.

The comparison starts at the **`workshop-start` tag**, not the PR's integration
target. This is the comparison starting point only; it does not move your code
or change where a PR merges.
Ask for a review without edits:

```copilot
Review the full change from workshop-start to the verified main commit,
or the recorded reviewed local commit if delivery is blocked.
State both compared commits. Check cart behavior, validation, server
prices, removal, Canvas UI changes, the query change, both parallel workers'
contributions and mock checkout: order snapshots, atomic clearing, rollback,
concurrent duplicates, retry/reload recovery and receipt UI.
Preserve reviewed acceptance criteria.
Report current edits and untracked files separately as unverified work.
Identify concrete regressions or missing evidence, not style preferences.
Cite specific code and evidence; mark unverified assumptions.
Do not infer that the running app uses this revision or that CI is green.
Do not edit files, switch or reset branches, or retarget PRs.
```

Inspect findings yourself. If corrections are needed after delivery, ask Copilot
to create a new follow-up feature branch from the verified result before editing;
do not commit on the verification checkout, reuse the merged checkout PR or push
directly to `main`. Review the corrections and rerun the suite below. A follow-up
PR needs its own publishing and merge approval, passing checks and post-merge
verification. Do not leave accepted corrections unmerged while claiming a
completed main-branch result.

## Check your results

| Outcome | Evidence |
|---|---|
| Fixed repeated additions | From an empty cart, Notebook added twice → quantity 2 / €20, persists after reload; regression tests pass |
| Generated removal | Correct DELETE response, working button, other products and totals preserved |
| Used a Canvas | Running shop preview, selected UI issue and checked correction, or an explicit fallback record |
| Investigated N+1 | Matched MCP before/after profiles for the same eight-product workload; query tests confirm exactly 1 SELECT per completed GET `/api/cart` at 8 and 16 distinct products, with response values preserved |
| Delivered three task PRs | Quantity fix, removal plus Canvas, and query fix each merged and verified before the next task |
| Coordinated parallel work | Reviewed starting point published on `main`, two isolated sessions from that version, two worker PRs merged sequentially with Agent Merge, and a tested combined result; or an explicit local-recovery record |
| Requested an independent critique | Actual rubber duck findings, decisions and evidence for corrections; or a recorded unavailable critic |
| Delivered mock checkout with five subagents | Five child-session links/worktrees and observed overlap, four code handoffs plus read-only findings for the PR head at merge authorization and coverage limits for later repairs, one checkout PR merged into `main`, passing merged-revision checks and receipt/cart preview; or an explicit incomplete/demonstration record |
| Reviewed workflow efficiency and quality | Fresh Cart: Chronicle session, scoped tips report and one evidence-backed improvement balancing tokens, turnaround and quality; or a note that Chronicle was unavailable/not run |
| Used Copilot App effectively | Reviewed plan, loaded skills, inspected changed files and checked test output |

Use the [worksheet]({{ site.baseurl }}/worksheet/); mark demos, reference
solutions and unavailable features. Use tool responses and test output to
support the results, not just Copilot's final summary.

## Verify before handing off

On the merged-main revision verified in the checkout chapter, run the **full
suite**, including generated boundary and checkout tests. For local recovery,
use the preserved result and explicitly record that it is not merged:

```sh
./mvnw test
```

All baseline, generated cart/removal/query, boundary and checkout
tests must execute with no failures/errors/skips. Report actual counts and
check the reports for `BaselineTest`, `CartContractTest`, `RemoveContractTest`,
`QueryContractTest`, `CartBoundaryTest`, `CheckoutContractTest` and
`CheckoutResilienceTest`; no reviewed case may be removed or weakened.
If checkout was blocked, mark its cases as not completed rather than treating
an earlier passing suite as checkout evidence.
If a ticket or worker remains unfinished, record that explicitly rather than
presenting partial work as the complete workshop result.

Ask Copilot to show the file list and diff between the recorded comparison
commits. Review them in **Changes**, keeping any local edits and untracked files
separate as unfinished work. On the normal path the accepted workshop work is
already merged; do not create another commit just to finish. If you made corrections
on a follow-up feature branch, deliver them through their own reviewed PR before
claiming they are on `main`.
Ask Copilot for a concise handoff:
what changed, what was checked, what is still unknown.
Include the independent critique and checkout branch/commit, actual PR/CI
status and verified revision. Keep private Chronicle output out of the handoff.

## Where your result lives

On the completed normal path, the three task PRs and both worker PRs landed on **`main`**,
followed by the orchestrator's **checkout PR**. Stay in **Cart: mock checkout**
on the verified main revision, not the old worker or checkout feature branch.
Retain the quantity-fix, removal-and-Canvas and MCP handoff PR links,
both worker PR links and CI results, plus the checkout PR,
feature head, merge commit, verified main commit, checks and running directory/URL.
If any additional delivery or correction PRs were needed, retain their
review, checks and actual merge status too.

**Checkout merged and verified on `main` is required for the completed normal path.**
Use Agent Merge under the checkout chapter's explicit approval, then let the
orchestrator verify the merged result; no fixed PR number is required.
Do not claim checkout is on `main`
merely because the earlier PRs merged.
If checkout remains unfinished, preserve its branch and hand off the earlier
reviewed result with that limitation, not a fictional successful order.
Keep the five child sessions, worktrees and local commits until their work is
accounted for; do not delete them merely because the integrated PR merged.

If you used local recovery, keep the local combined branch and record the
GitHub, CI or Agent Merge blocker. Do not describe open PRs as merged or local
results as completed CI checks. Record **verified locally; delivery blocked**
or **merged; post-merge verification blocked**, as appropriate.

## Keep one useful habit

Leave with the reviewed result, actual delivery status, unfinished work,
independent review decisions and one workflow habit based on your session review.

The transferable loop is **reproduce → plan → implement → inspect → verify**.
Skills provide procedure, Canvas grounds UI feedback, and MCP provides runtime
evidence. Rubber duck challenges your reasoning; subagents coordinate focused
work. Chronicle helps you improve the workflow. None replaces your judgment.
