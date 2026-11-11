---
layout: default
title: Prompt cards
description: "Small prompts for the task you are doing now. Do not paste the whole workshop into one request."
permalink: /prompts/
workshop: true
---

## Investigate without editing
{: #investigate}

Stay in **Cart: quantity bug**, created in Setup. This prompt continues that
session; it is not the session's first prompt.

```copilot
In this shopping-cart repository, reproduce the repeated-add bug:
reset the cart, then add one €10 Notebook twice, waiting for each response
before the next click; expect quantity 2 / €20, actual 1 / €10.
Trace the UI, POST /api/cart/items and persistence path.
Do not edit yet. Explain the cause, relevant files and smallest testable plan.
Keep removal and query optimization out of this ticket.
```

## Use the test skill

Stay in **Cart: quantity bug**, in **Interactive**, with the reviewed plan.
The [skills chapter]({{ site.baseurl }}/skills/) distinguishes installation
from loading. Its [installation section]({{ site.baseurl }}/skills/#install-skills)
is for another project; the workshop's pinned skills are already installed.

```copilot
/java-junit
Generate src/test/java/com/juliendubois/workshop/CartContractTest.java
from the acceptance criteria in our plan, using the existing test fixtures.
Cover quantity accumulation, totals, new products and rejected input.
Do not retrieve reference tests or solutions, or change production code
or dependencies.
Explain how you used the skill and show me the diff for review.
After my approval, run the tests and confirm they expose the quantity bug.
No new dependencies, Docker, skipped tests or unrelated refactors.
```

Complete the quantity fix and
[merge its reviewed PR]({{ site.baseurl }}/skills/#publish-the-quantity-fix)
before starting removal.

## Generate a feature

Prepare a **New worktree** session from the updated `main`, using **Plan**.
Send this first prompt:

```copilot
Plan removal from the merged quantity fix in this new worktree.
DELETE /api/cart/items/{productId} returns 200 with the updated cart;
a missing line returns 404 without changing the cart, including a catalogue
product never added. Add a Remove button per line.
Remove deletes the entire product line and all its units, not just one unit.
Removing the last line leaves zero count/total.
Preserve other items, quantities, server prices/totals.
No new dependencies, checkout or query changes. Do not edit yet.
```

Once the session has started, name it **Cart: item removal**.
After reviewing the plan, return to **Interactive** and generate tests first:

```copilot
/spring-boot-testing
Generate src/test/java/com/juliendubois/workshop/RemoveContractTest.java
from our reviewed removal criteria using the existing HTTP test fixtures.
Cover removal of one of two product lines, the last line and missing lines,
checking returned and stored state. Include a line with quantity 3:
removal deletes all 3 units and preserves the other product and its quantity.
Do not retrieve reference tests or solutions, implement removal or change
earlier tests.
Show me the assertions for review; after approval, run the tests and confirm
they demonstrate missing removal behavior before implementing the feature.
```

Then [implement the backend and UI]({{ site.baseurl }}/generate/#generate-the-backend-and-ui)
and [preview the feature]({{ site.baseurl }}/generate/#preview-and-iterate),
moving the running shop to this worktree. Continue to Canvas in this same
session; publish the feature and polish together afterward.

## Canvas and UI feedback

Stay in **Cart: item removal**, on its current branch.
[Open the running shop]({{ site.baseurl }}/canvas/#browser-preview),
then invoke **`/impeccable`** with the
[Pick & polish prompt]({{ site.baseurl }}/canvas/#pick-and-polish)
on a selected UI element. Then
[publish removal and Canvas changes together]({{ site.baseurl }}/canvas/#publish-removal-and-canvas-changes).
Merge that PR before creating the query session.

## Investigate through MCP

Use the [first query prompt]({{ site.baseurl }}/tools/#start-the-query-session)
to start a new worktree from merged `main`, then name it **Cart: query optimization**.
Follow the server handoff, [connect the MCP tools]({{ site.baseurl }}/tools/#connect-runtime-tools)
and [create the eight-product workload]({{ site.baseurl }}/tools/#reproduce-the-same-workload).
Use the [evidence prompt]({{ site.baseurl }}/tools/#ask-copilot-for-evidence)
to inspect the matching request through `bootui-shopping-cart`.
Then use the [N+1 fix prompt]({{ site.baseurl }}/tools/#fix-the-n1-query-issue)
to generate query-budget tests. Review the generated assertions before allowing
optimization, then repeat the workload to verify the runtime queries. Finish with the
[publication step]({{ site.baseurl }}/tools/#publish-the-reviewed-result):
review the PR, merge it into your own `main` and verify the shared starting point.

## Parallel worker cards
{: #parallel}

Both prompts are included directly in the
[parallel-sessions chapter]({{ site.baseurl }}/parallel/), beside the
App instructions for creating both worktrees from the `main` already verified
after the three task PRs merged. No separate preparation prompt is needed.

- [UI prompt]({{ site.baseurl }}/parallel/#ui-worker): start the first session, then name it **Cart: empty-state UX**.
- [Test prompt]({{ site.baseurl }}/parallel/#test-worker): start the second session, then name it **Cart: boundary tests**.

The UI session improves the empty-cart screen; the second adds boundary tests
and proposes fixes for any exposed bugs. Both may edit the same files;
Agent Merge helps reconcile their changes during integration.

## Integrate with Agent Merge

In each existing worker session, review the result and use **Create PR**,
[targeting `main` in your own repository]({{ site.baseurl }}/integrate/#open-the-two-worker-prs).
Use the chapter's [UI PR steps]({{ site.baseurl }}/integrate/#merge-the-ui-pr-first)
first: allow repairs with **Merge pull request** off, review the result,
then authorize merging in the App.
After the UI merge and its main-branch CI pass, use the
[test PR conflict-resolution prompt]({{ site.baseurl }}/integrate/#update-and-merge-the-test-pr).
Authorize each PR separately. Stay in **Cart: boundary tests** for
[verification of merged `main`]({{ site.baseurl }}/integrate/#verify-the-combined-application).

## Rubber duck and subagent implementation

Stay in **Cart: boundary tests**, on the checked combined result.
Use the [rubber duck prompt]({{ site.baseurl }}/rubber-duck/#review-prompt)
for a read-only critique. On the normal path, deliver and verify any accepted
correction's follow-up PR before checkout; for local recovery, keep the checked
local result. Record deferred findings without applying them. Then follow the
[fresh checkout session steps]({{ site.baseurl }}/subagents/#prepare-checkout):
choose **New worktree** from verified `main`, or the recorded reviewed local base
if delivery is blocked. Send the first prompt and name the new session
**Cart: mock checkout**. Use **Plan** for the checkout plan,
review the contract, file ownership and local handoffs, then return to
**Interactive** without implementing. Only then send the chapter's
**`/orchestrate`** prompt to create **five visible child sessions**, each with
its own worktree at the same reviewed commit. Four writers **implement mock checkout**
and its tests while a read-only reviewer checks the design and incoming commits.
Approve safe five-way concurrency after the machine-load check; if unsafe or
unavailable, stop and agree on a fallback. The parent integrates four code
handoffs and review findings into one checkout feature branch.
Each prompt names its scope and approval boundaries;
do not paste critique and implementation together. Do not create five specialist PRs.

## Deliver checkout to main

After reviewing the integrated code, tests and preview in **Cart: mock checkout**,
follow the [checkout delivery steps]({{ site.baseurl }}/subagents/#deliver-checkout):
use **Create PR** for one checkout PR, then **Agent Merge** with
**Merge pull request** off while reviewing repairs. The same reviewer rechecks
changed heads; the orchestrator reruns the full suite and affected previews
before authorization. Once you accept the result and required checks and approvals
pass, enable merging and confirm authorization for this PR only. Record coverage
limits for later repairs. The five specialists do not publish or merge.
Do not reuse the earlier worker PR; no extra delivery prompt is needed.

Then use [merged-main verification]({{ site.baseurl }}/subagents/#verify-merged-checkout).
Record the actual merge commit and verified main revision.
Reuse the shop if it already runs from that directory, waiting for DevTools;
otherwise use the [server handoff]({{ site.baseurl }}/setup/#move-running-shop).
Reload the Browser canvas before checking Place order and the receipt.
Local-only or blocked delivery is not the completed normal path.

## Improve usage

Before running Chronicle tips, follow the
[Chronicle privacy decision]({{ site.baseurl }}/tokens/#decide-before-analyzing-history).
The command may immediately access history beyond this workshop; a later scope
prompt cannot undo that. Opt out and use your local workshop transcript if that
access is unsuitable.

If you opt in, start a fresh **Cart: Chronicle** session in your workshop repository.
Its new worktree is not used for this read-only history review.
Leave the verified checkout unchanged and exclude the analysis session itself.
Send the command and request as one message; no dates need filling in:

```copilot
/chronicle tips Review all workshop sessions for the current repository
over the past seven days, excluding this Chronicle session and unrelated work.
State the repository, resolved time range/timezone and sessions used.
Suggest up to three improvements covering token efficiency, agent turnaround
time and output quality, grounded in observed examples. Explain trade-offs.
Preserve tests, review and permission boundaries. Report only available metrics
with units and coverage; mark missing data unknown. Do not infer currency or edit files.
```

## Review the diff

Return to **Cart: mock checkout** for the
[read-only final review]({{ site.baseurl }}/finish/#final-review) of the verified result.
For a separate reference checkout, replace `workshop-start` with `v2-start`.
Otherwise keep the personal starter tag:

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
