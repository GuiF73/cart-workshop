---
layout: default
title: Facilitate and recover
description: "Prepare the workshop, check key handoffs and help participants recover without losing work."
permalink: /facilitator/
workshop: true
---

Copilot App is the subject; the shop is the example.
Follow the [workshop flow]({{ site.baseurl }}/#workshop-flow), with a break before
parallel work and no chapter deadlines.

## Before participants arrive
{: #rehearse-with-the-app}

Rehearse with the App build and accounts you will use.

| Check | Ready when |
|---|---|
| Environment | The participant's own repository opens in a worktree; the 4 baseline tests pass; one owned shop runs on port 18765 |
| App controls | Plan, Interactive, effort and permissions are understood; Fusion Standard or the [setup alternative]({{ site.baseurl }}/setup/#open-it-in-copilot-app) is available |
| Skills and tools | Bundled Java skills load; Browser canvas, Pick & polish, impeccable and the two MCP tools have been tried |
| GitHub delivery | Actions is enabled; **Shopping-cart checks / tests** runs; PR delivery works from the quantity fix onward; Agent Merge is allowed for the two worker PRs and the integrated checkout PR |
| History privacy | Participants decide **before running Chronicle** whether its history access is acceptable; [transcript review]({{ site.baseurl }}/tokens/#decide-before-analyzing-history) is an equal alternative |

<details markdown="1">
<summary>App rehearsal checklist</summary>

### Skills and Canvas

- The three Java skills are repository-bundled; **impeccable** is App-bundled. Invoke it with **`/impeccable`**. Demonstrate loading guidance, not reinstalling the workshop's pinned copies.
- Follow the [Canvas chapter]({{ site.baseurl }}/canvas/): open the running shop and focus on one observed UI issue with Pick & polish. No instruction-file editing exercise is needed.
- Use three named task sessions: **Cart: quantity bug**, **Cart: item removal** (including Canvas) and **Cart: query optimization**. Merge and verify each task's PR before starting the next from updated `main`; name sessions only after their first prompt. Participants create sessions in the App UI, without changing agent instructions.
- Confirm this worktree owns the running shop before refreshing UI edits; a matching URL is not enough. If ownership is unknown or different, use the [human-run server handoff]({{ site.baseurl }}/setup/#move-running-shop) rather than touching another checkout's app.
- Keep the shop running during same-worktree edits. DevTools reloads compiled backend changes; Maven tests compile Java and copy resources. After approved UI edits, Copilot runs `./mvnw compile`, reloads the existing Browser canvas and verifies the visible change; no manual refresh is needed. An automatic restart resets cart data; static-resource updates normally do not. Stop/start manually when switching the running app to another worktree or for recovery.

### Review and five-subagent checkout

- Approve a read-only independent critic for [rubber ducking]({{ site.baseurl }}/rubber-duck/) without editing the verification checkout's `AGENTS.md`. Use an actual critic, not a main-agent reread. On the normal path, merge and verify accepted corrections through a follow-up PR before checkout; local recovery keeps the checked local branch.
- Start a fresh **Cart: mock checkout** session using **New worktree** from verified `main`, including merged critique corrections. The App creates the feature branch. If using local recovery, explicitly select and verify the recorded reviewed local base instead.
- Prepare the checkout plan in **Plan** mode. Approve the [contract, plan, file ownership and local handoffs]({{ site.baseurl }}/subagents/#checkout-contract), then return to **Interactive** without implementing. The `/orchestrate` prompt creates exactly five coordinated child sessions, each with its own worktree and branch. No `/fleet`, nested agents or custom profiles. The starter instructions already provide this scoped allowance; no `AGENTS.md` edit is needed.
- Approve five-way concurrency after a machine-load check. Start backend, UI, HTTP tests, resilience tests and a read-only reviewer together from the same reviewed commit. Agree on HTTP behavior, test setup/probes and exclusive fixture ownership first. Do not wait for backend implementation before starting the others; record actual overlap or the concurrency limitation.
- Four writers provide local commits; the reviewer provides findings tied to commits, including the final integrated head. The orchestrator owns integration, Maven and preview. Preserve all worktrees; no child publishing, merging, shops, Maven runs or nested agents.
- Check all earlier reviewed tests, boundary cases and **new checkout tests**, including `CheckoutContractTest` and `CheckoutResilienceTest`. Verify rollback, immutable receipts, concurrent duplicate requests and replay after new cart items. Wait for DevTools to load compiled changes, then place an order in the Browser canvas.
- After final review, use **Create PR** in **Cart: mock checkout**, then reuse **Agent Merge**. Keep **Merge pull request** off while reviewing repairs; authorize this checkout PR's merge separately once checks and approvals pass. Have the same reviewer recheck repairs before merge approval; record later repair/review limitations. Workers never publish or merge. Verify exact merged main and that the shop serves its compiled code from the verified directory; change the running server's worktree only if needed.

### Evidence and privacy

Confirm `/chronicle tips` is available in your build. Focus on token efficiency,
agent turnaround and output quality; `cost-tips` is an optional drill-down.
History may span repositories or still be indexing. Never project unrelated
private work, invent missing usage figures or treat a later filter as undoing
earlier access.

For the final review, compare the recorded starter and verified result commits,
keeping unfinished edits separate. Corrections need a new approved feature branch
and reviewed PR; leave the verification checkout unchanged.
Keep private Chronicle output out of the handoff.

Record App actions only when their actual responses are available.
Shop screenshots and saved HTTP captures do not prove an App interaction.
Run newcomer and experienced pilots, including navigation and recovery.

### Interrupted sessions

Read the actual partial handoff first: source directory/revision, unfinished
files, executed outcomes and owned helpers. Confirm cleanup before starting
another preview. A query error with no detailed cause is not proof of an
authentication failure. After a bounded retry following recovery, stop if the
same failure repeats; do not create a retry or replacement-agent loop.

If the participant approves a facilitator or single-agent takeover, record the
execution-method change. Preserve earlier failures and coverage gaps; delivered
code is not proof that the original independent or native App exercise completed.

</details>

## Check the delivery handoffs
{: #one-workshop}

The three task PRs precede **two worker PRs targeting `main`**:

| Order | Required handoff |
|---|---|
| Quantity-fix PR | Merge and verify at the end of Skills before creating **Cart: item removal** from updated `main` |
| Removal-and-Canvas PR | Keep both chapters in **Cart: item removal**; merge and verify after Canvas before creating the query session |
| MCP handoff PR | Merge and verify the query fix before creating both parallel sessions from updated `main` |
| UI worker PR | Use **Create PR** in **Cart: empty-state UX**. Review Agent Merge repairs with **Merge pull request** off; authorize this PR only, then confirm **Merged** and passing checks on `main` |
| Boundary-test PR | Use **Create PR** in **Cart: boundary tests**. Reconcile updated `main` with merging off; review resolutions and fresh CI, then separately authorize its merge |

Verify merged `origin/main` in the clean **Cart: boundary tests** worktree.
Preserve worker branches and other checkouts; account for squash merges.
No extra integration session is needed.

After rubber duck, start **Cart: mock checkout**:
**build and review checkout → Create PR → Agent Merge →
checkout PR merged into `main` → verify merged app → Chronicle → handoff**.
If participants opt in, run Chronicle in a fresh **Cart: Chronicle** session; scope its report to this
repository over the past seven days, excluding the analysis session itself.
Keep the checkout PR in the orchestrator's session, not the earlier boundary-test PR.
Authorize its merge separately and record actual PR links.
The template's `main` remains the unsolved starter, not a completed demo.

After Chronicle or transcript review, return to **Cart: mock checkout** for the
[read-only final handoff]({{ site.baseurl }}/finish/#final-review).

## Recovery
{: #recovery}

Preserve the participant's work first. Record what they actually completed;
a fallback or reference demonstration is not a successful native App exercise.

| Blocker | What to do |
|---|---|
| Setup or skill loading | Help or pair with a working participant. Compilation errors are not the expected regression failures |
| Quantity, removal or query fix | Use a separate pinned copy; see [reference recovery](#reference-recovery) below |
| Browser, Pick & polish or impeccable | Use the [Canvas fallback]({{ site.baseurl }}/canvas/#canvas-recovery); record which interaction was unavailable |
| MCP connection or baseline | Use [matched reference evidence]({{ site.baseurl }}/assets/mcp-evidence.json), clearly labelled as reference, not the participant's App tool calls |
| MCP handoff cannot be published | Follow [MCP handoff recovery]({{ site.baseurl }}/parallel/#local-recovery) only from an accepted local copy with all earlier reviewed tests passing; record `main` as not updated |
| Worker, CI or Agent Merge blocked | Preserve both branches, disable Agent Merge on open PRs and follow [integration recovery]({{ site.baseurl }}/integrate/#local-recovery) in **Cart: boundary tests** |
| Boundary test reveals a production bug | Keep the regression, approve the [smallest correction in that session]({{ site.baseurl }}/parallel/#boundary-fix), and rerun the full suite before integration |
| Independent critic or five child sessions unavailable | Use the relevant chapter's demonstration/review fallback; explicitly record the missing independent critique or five-agent run |
| Checkout coding or tests fail | Keep the integration branch, child worktrees and local handoff commits; mark checkout unfinished and retain the earlier reviewed result. No checkout reference solution is supplied |
| Checkout publishing or merge blocked | Preserve branch/open PR; mark **verified locally; delivery blocked**. No direct push or substitute local merge into `main` |
| Checkout merged but checks or preview fail | Record **merged; post-merge verification blocked**. Repairs need a new approved feature branch and PR |
| Session query error or interruption | Preserve source, branches and partial evidence; an idle session is not completion. Resume only missing work, not the entire rehearsal |
| Chronicle unavailable or privacy opt-out | Use the workshop transcript; record **Chronicle not available** or **Chronicle not run: privacy choice**. Missing usage is unknown |

**CI:** queued/running means wait; absent, skipped or failed is not a pass.
Check Actions and the current PR revision. Keep the second PR's Agent Merge
off until the UI merge is verified. Never bypass policies, required approvals
or failing checks.

**Local recovery:** remote status may be unknown. Keep the checked recovered
result for preview and handoff; do not switch back to incomplete remote `main`
or report local integration as Agent Merge completion.

**Generated Impeccable state:** for an untracked `.impeccable/hook.cache.json`,
request a narrowly scoped local Git exclude and review it before approval.
Do not commit the cache, delete the whole directory or ignore all `.impeccable/`
files. Keep intentional design records; review source changes separately.

<details markdown="1" id="reference-recovery">
<summary>Reference checkpoints and safe Git recovery</summary>

### Expected reference results
{: #executable-checkpoints}

The [pinned revisions]({{ site.baseurl }}/assets/references.json) and
[recorded checks]({{ site.baseurl }}/assets/checkpoint-checks.json)
cover the three earlier tickets, **not checkout**.
These historical pins also predate current-starter input and keyboard hardening;
their counts and captures describe those exact revisions, not today's `main`.
The table uses historical reference tests. In the normal workshop, participants
generate `CartContractTest`, `RemoveContractTest` and `QueryContractTest`;
their counts and failures vary. The current learner starter contains no
ready-made exercise tests.

| Check | Tests | Expected result |
|---|---:|---|
| Start, `BaselineTest` | 4 | Pass; repeated addition is not covered |
| Start, activate `CartContractTest` | 3 | Two failures: quantity 2 vs 1, total €50 vs €20 |
| After bug fix, baseline + cart | 7 | Pass |
| After bug fix, activate `RemoveContractTest` | 3 | Two failures: expected 200, actual 404 |
| After feature, baseline + cart + removal | 10 | Pass |
| After feature, activate `QueryContractTest` | 2 | Two failures: 9/17 SELECTs, expected 1 |
| After performance, all four classes | 12 | Pass |

Maintainer test snapshots live at
`workshop/tools/copilot-workshop/reference-tests/` in this repository,
excluded from the published site.
The pinned historical checkpoints below retain their own `teaching/` classes
for reproducing these recorded counts. Use those files only in a separate
reference checkout; never replace reviewed learner tests. Boundary and
checkout tests add cases beyond the historical 12.

### Recover without losing work
{: #recover-without-losing-work}

Use a **new directory**, never the participant's project. This quantity-fix
example checks out the full pinned commit, not a movable tag:

```sh
git clone --no-checkout https://github.com/jdubois/github-copilot-app-java-workshop.git cart-reference-bugfix
cd cart-reference-bugfix
git switch -c reference-work 8291261524b5e20ce86c111abe909877d8510776
git rev-parse HEAD
```

Confirm the printed SHA matches. For another checkpoint, use its full SHA
below and a fresh directory name. If the commit is unavailable, stop.

1. Connect a new App session to the reference copy. Check its directory and starting commit; activate any required teaching tests there and run the matching checks.
2. Use that reference session only for the blocked task, committing reviewed results. For removal recovery, complete Canvas there too. Do not use the reference clone as the next task's base.
3. For performance recovery, restore any accepted Canvas UI changes, check startup paths for this copy, and activate all three teaching classes unchanged. Confirm all 12 supplied tests pass before parallel work.
4. To resume GitHub delivery, apply the reviewed reference changes and any accepted Canvas work in a new worktree based on the participant's **own `main`**. Review the complete diff and rerun tests, then deliver those recovery changes through a reviewed PR. If GitHub is blocked, use the linked local recovery instead.

**Do not push this clone:** its `origin` is the template, not the personal
repository. Template-created repositories have independent history; changing
the remote alone does not make reference commits mergeable. Never merge
unrelated histories, overwrite personal `main` or replace an existing handoff
branch.

Stop the old shop in its owning terminal before starting the reference copy.
Record that a reference solution was used. Reference copies do not include
the participant's Canvas changes, new boundary tests or checkout.

| Git checkpoint | Reference | Pinned commit |
|---|---|---|
| `v2-start` | <a href="https://github.com/jdubois/github-copilot-app-java-workshop/tree/v2-start" target="_blank">Starter</a> | `326f95840e3d42dcbb83d1bb182091cdda38382e` |
| `v2-bugfix` | <a href="https://github.com/jdubois/github-copilot-app-java-workshop/tree/v2-bugfix" target="_blank">Quantity fix</a> | `8291261524b5e20ce86c111abe909877d8510776` |
| `v2-feature` | <a href="https://github.com/jdubois/github-copilot-app-java-workshop/tree/v2-feature" target="_blank">Removal feature</a> | `f1b8d4104a3415c5568ea4f7fb15e1294aa3ad3f` |
| `v2-performance` | <a href="https://github.com/jdubois/github-copilot-app-java-workshop/tree/v2-performance" target="_blank">Query fix</a> | `0a7d9dd3962929c7909ecfee64f72b2f03f43970` |

These are one reference history in the template repository, not separate
repositories or archives. Earlier v1 checkpoints remain unchanged.

</details>

## Evidence and maintenance

Use participants' actual test reports, previews and App responses.
The published reference checks do not prove their generated checkout works.

<details markdown="1">
<summary>Capture provenance and maintainer commands</summary>

The [capture manifest]({{ site.baseurl }}/assets/capture-manifest.json)
pins source revisions, image/response hashes, runtime identities and the
capture JVM version, which differs from the Java 21 compilation target.
[Saved MCP responses]({{ site.baseurl }}/assets/mcp-evidence.json)
were captured using HTTP JSON-RPC, **not through the App**.

Code, skills, test CI and this handbook live in
<a href="https://github.com/jdubois/github-copilot-app-java-workshop" target="_blank">this repository</a>.
Run its maintainer gate, `python3 tools/verify-checkpoints.py`, from the repository root.
For handbook builds and reference captures, change into `workshop/` first:

```sh
cd workshop
CAPTURE_CHANNEL=chrome python3 tools/copilot-workshop/capture-all.py --port 18767
bundle exec jekyll build --destination tools/copilot-workshop/.build/site
python3 -m unittest discover -s tools/copilot-workshop -p 'test_*.py'
python3 tools/copilot-workshop/check-site.py --remote
```

The local gate checks matched request IDs/runtime identities, eight distinct
products, €115 totals and the 9-to-1 SELECT change. `--remote` also checks live
annotated tags against the pins; local success does not establish remote state
or a successful website workflow. Checkpoint tags are protected against updates
and deletion.

</details>
