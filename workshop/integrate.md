---
layout: default
title: Merge PRs with Agent Merge
description: "Prepare PRs in parallel, merge UI first, and verify the combined application."
permalink: /integrate/
workshop: true
next: rubber-duck
next_title: Review with rubber duck
---

## What you will learn

In Copilot App, prepare both PRs with repair-only **Agent Merge** in parallel, authorize their
merges separately, then verify the combined result.

## Open the two worker PRs

Keep **Cart: empty-state UX** and **Cart: boundary tests**;
do not create another session or integration branch.

In each session, review **Changes**, its preview or test results, and any
[approved boundary fix]({{ site.baseurl }}/parallel/#boundary-fix).
Keep earlier tests and resolve any failing regression before continuing.

Select **Create PR** in Copilot App, targeting **`main` in your own repository**.
If the PR already exists, open it.
**Both worker PRs target `main`.** Limit each diff to its session's work:
the three earlier task PRs are already merged.
Check **`base: main` ← `head: this session's branch`** in the PR overview.

## Merge the UI PR first

**Agent Merge** can address review feedback, fix CI failures and resolve
conflicts. It does not replace your review or bypass repository protections.
See the <a href="https://docs.github.com/en/copilot/how-tos/github-copilot-app/managing-issues-and-pull-requests#merging-a-pull-request" target="_blank">Agent Merge guide</a>.

In **Cart: empty-state UX**, follow these steps. Optionally run steps 1–2 in
**Cart: boundary tests** too: repairs and CI can run in parallel; authorize
merges separately, **UI first**.

1. Open the **Create PR** dropdown and choose **Agent Merge**. Verify its linked PR, repository and head branch match this session, not an earlier PR. If not linked, ask the facilitator; do not create a duplicate.
2. Leave **Merge pull request** unchecked and start **Agent Merge** with the reviewed repair options. Preserve acceptance tests; ask before out-of-scope corrections. Keep merging disabled on both PRs during parallel preparation.
3. Review **Files changed**, including repairs. Once you accept the result and the **tests** job and all required checks and approvals pass for the current PR revision, enable **Merge pull request** and confirm the App's authorization prompt for this PR only.

After authorization, Agent Merge may make further permitted repairs and merge
without another review pause. Keep merging off to review corrections first.

**Done when:** the UI PR's status is **Merged** and the **tests** job passes
for its merged revision on `main`.
{: #check-ui-merge}

<details markdown="1">
<summary>If checks or merging do not progress</summary>

A queued or running **tests** job means wait; a failed job needs a correction.
A missing or skipped job is not a pass: check **Actions** and ask the facilitator.
A denied permission, disallowed Agent Merge or missing approval is a blocker,
not permission to bypass protections. If blocked, turn off Agent Merge and use
[local recovery](#local-recovery).

</details>

## Update and merge the test PR

After the UI merge is verified, return to **Cart: boundary tests** with
**Merge pull request** still off. Keep repair-only Agent Merge running, or start
it now. The sessions may have changed the same files; ask:

```copilot
Update this boundary-test PR against the latest origin/main.
Resolve merge conflicts, preserving both workers' intended changes and tests.
Do not reset main or this branch, discard either worker's changes
or force-push. Keep the PR base main and merging disabled while I review
the conflict resolution and updated diff.
Ask before changes outside the reviewed tasks.
Run ./mvnw test and show the results; stop on failures or skipped tests.
Do not merge the PR yet.
```

Review any conflict resolutions, the complete updated diff and **fresh CI for
its new revision** against the updated `main`. Earlier green checks do not verify
the combined result. Even conflict-free changes can interact incorrectly.
Once you accept the result and all required checks and approvals pass,
enable **Merge pull request** and confirm a **separate authorization for this PR**.
**Done when:** this second PR is also **Merged**.

## Verify the combined application

Stay in **Cart: boundary tests**. Verify merged `main`, not an old worker version.
Ask Copilot:

```copilot
Confirm both worker PRs are Merged in my own repository. Fetch origin.
Stop if this session's working tree is not clean.
Preserve both worker branches and their commits. In this session's worktree,
check out the exact latest origin/main commit for verification without moving
main or another session's checkout. Do not create a branch, reset or push.
Confirm the checked-out commit equals origin/main and contains both PRs'
actual merged results, including squash merges.
Require passing tests CI for this exact main revision before reporting success.
Run ./mvnw test and report the executed counts and any failures or skips.
```

Confirm **all earlier reviewed tests plus the new boundary cases** actually
ran, with no failures/errors/skips.

You are **switching worktrees**: stop the old shop with **Ctrl+C** in its owning
terminal, then [move the running shop]({{ site.baseurl }}/setup/#move-running-shop)
to this session's checked-out main version. DevTools cannot switch worktrees.
Confirm repeated adds, removal and the empty-cart catalogue link still work,
including keyboard navigation and a narrow viewport.

Record both PR links, CI results and combined checks on the
[worksheet]({{ site.baseurl }}/worksheet/#agent-merge-and-integration).

<details markdown="1" id="local-recovery">
<summary>Recovery: GitHub, CI or Agent Merge is unavailable</summary>

Preserve the worker branches and any open PRs. Record the blocker and which
PRs, if any, actually merged. Disable Agent Merge in each worker session with
an open PR before integrating locally, so it cannot merge in the background.
Do not bypass protections,
invent CI results or report a local merge as Agent Merge completion.

Stay in **Cart: boundary tests** and give Copilot both reviewed handoffs.
This worker already has the boundary tests; it only needs any missing accepted
UI changes. Ask:

```copilot
Confirm the working tree is clean and this is the reviewed boundary-test
worker branch with its accepted tests. If not, stop and ask before switching.
Preserve both worker branches, their commits and any unfinished work.
If the shared starting point is published on main and GitHub is reachable, fetch origin and merge
origin/main into this test worker branch, keeping its boundary tests.
If the MCP handoff used local recovery, keep the accepted local starting point;
do not replace it with starter main. If remote status is unavailable, mark
it unknown and use only the recorded reviewed local results.
Check whether the accepted UI result is already included, accounting for
squash merges. Merge the reviewed UI handoff commit only if its changes
are missing. Do not merge the test branch into itself or apply changes twice.
Preserve any approved bug fixes in the reviewed boundary-test handoff.
If a new regression appears, stop and propose a correction for review.
Ask before resolving a conflict, or if a reviewed handoff cannot be found.
Run ./mvnw test and report all counts, failures and skips.
Do not push, merge remote PRs or enable Agent Merge.
```

Perform the same combined tests and preview described above. If a conflict
occurs, review both contributions rather than automatically choosing one side.
Continue in **Cart: boundary tests** using this checked local result, not a
remote `main` that may still be incomplete. Skip the normal-path checkout of
`origin/main`: it could discard the recovered result from your preview.
Mark **Agent Merge not completed: local recovery used** and record whether
remote `main` actually contains the work.

</details>

Record whether the result is ready, needs correction or remains unfinished.
Then [get a second opinion]({{ site.baseurl }}/rubber-duck/) on this
checked result before building the next feature on its own branch.

## What you have learned

- Use **Changes** and each session's handoff to check its scope, committed code and reported results.
- Use **Agent Merge** as a PR-maintenance agent: it can address review feedback, fix CI failures and resolve merge conflicts. With **Merge pull request** off, it prepares the PR without merging; enabling that option authorizes it to merge when required checks and approvals allow it, without another review pause.
- Prepare both PRs with repair-only Agent Merge in parallel, but authorize merges separately: UI first, then the test PR after review and fresh checks against updated `main`.
- Verify the merged application, rather than assuming that two individually passing branches will work together.
