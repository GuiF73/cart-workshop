---
layout: default
title: Coordinate five subagents
description: "Run four writers and one read-only reviewer in parallel child sessions, then deliver mock checkout through one reviewed PR."
permalink: /subagents/
workshop: true
next: tokens
next_title: Improve usage with Chronicle
---

## What you will learn

Use Copilot App to delegate a shared goal to **five specialist agents in child
App sessions**: **four writers and one read-only reviewer working in parallel**.
Coordinate through a shared HTTP contract, then deliver the integrated feature
into **`main`**.
Keep delivery in the orchestrator's session, use Agent Merge for the checkout PR
and verify the application actually merged.

## One goal, five perspectives

**Customer request:** “Let me place a mock order, see a receipt and start
shopping again with an empty cart.”

**Mock means no real payment processing**, not an unimplemented feature.
Build a working local checkout after the three earlier tickets and parallel
improvements. Keep Spring Boot, H2, vanilla JavaScript and server-owned integer-cent prices.
No payments, authentication, customer personal data or external services.

The **orchestrator** is the main Copilot agent in your new
**Cart: mock checkout** session. In this exercise, each specialist runs in a
**visible child App session with its own worktree and branch**. You can open
each conversation in the sidebar and inspect its changes independently.
Four children write the backend, UI and two test suites; the fifth reviews.
The orchestrator integrates the writers' reviewed local commits and resolves
review findings for **one integrated PR**, not five specialist PRs.

Earlier, two worktree sessions built independent changes. Rubber ducking
challenged the result. Here, children work on one feature at the same time,
using the same contract and separate files rather than waiting for each other's code.
See <a href="https://docs.github.com/en/copilot/concepts/agent-capabilities/choosing-and-delegating-agent-work/delegating-and-parallelizing-work-with-agents" target="_blank">how delegation works</a>.

<figure>
  <a href="{{ site.baseurl }}/assets/illustration-five-specialists.svg" target="_blank"><img src="{{ site.baseurl }}/assets/illustration-five-specialists.svg" alt="Five child App sessions start from one reviewed commit: backend, UI, HTTP tests and resilience tests write separate files while a read-only reviewer checks the design and incoming commits. The orchestrator integrates four code handoffs and review findings into one checkout PR." width="1440" height="1080" loading="lazy"></a>
  <figcaption>Four parallel writers, one read-only reviewer, one delivery owner. This is a conceptual workflow, not evidence that agents have run.</figcaption>
</figure>

> **How is this different from `/fleet`?**
>
> `/fleet` lets the main agent delegate suitable work to subagents within its
> current App session. Each subagent has its own context, but the command does
> not itself create five persistent App sessions and worktrees or guarantee
> exactly five workers.
>
> Here, `/orchestrate` creates five named child App sessions with separate
> working copies and branches. They are easier to inspect and steer individually,
> but their commits need integration. This exercise uses four writers and one
> read-only reviewer. Both approaches can parallelize independent
> work and increase model usage; neither guarantees a speedup.
> **Use the child-session approach below; do not run `/fleet` for this exercise.**

## Start a fresh checkout session
{: #prepare-checkout}

After integration and rubber duck review, create a **new session** in your own
repository using the **Copilot App UI**. Choose **This computer**, **New worktree**
and **Interactive**, with the latest verified **`main` as the base branch**,
including any merged critique corrections. The App will create a separate
worktree and feature branch; keep **Cart: boundary tests** for its history.

<details markdown="1">
<summary>If earlier work exists only in local recovery</summary>

Preserve the checked local result and record its branch and commit. Create the
new worktree from **that reviewed local branch**, not incomplete remote `main`,
and verify the starting commit before editing. Keep delivery marked as blocked
until the earlier work and accepted critique corrections are merged and verified.
If the recovered instructions lack the scoped checkout allowance, stop and ask
the facilitator rather than editing them or proceeding.

</details>

Send this first prompt in the new session:

```copilot
Confirm this new worktree is in my own workshop repository, on the App-created
feature branch, not main or a detached checkout.
Fetch origin and verify this worktree starts at the latest verified origin/main,
including all three earlier tickets and accepted UI/boundary-test changes.
Confirm any accepted critique corrections are included.
If local recovery was used, verify the recorded reviewed starting commit instead;
keep that checked result, not incomplete remote main, and report delivery blocked.
Confirm the working tree is clean; stop if there is unfinished work.
Report this session's directory, actual branch and starting commit.
Preserve worker branches, main and other session checkouts.
Read AGENTS.md and keep it unchanged. Stop and report any conflicting instructions.
Wait for my approval of the checkout contract, implementation plan and file ownership.
Only the orchestrator may publish and merge checkout
after separate explicit approval of the integrated result.
The five specialists must not publish or merge.
Preserve existing tests, stack, privacy and approvals.
Do not implement checkout,
spawn subagents, push, open PRs or merge yet.
```

Once the conversation has started, name the session **Cart: mock checkout**.
The starter instructions already allow this exercise after explicit approval;
you do not need to edit `AGENTS.md`. This session will own the checkout plan,
integration branch and delivery; four children write code and the fifth reviews it.

## Agree on the contract first
{: #checkout-contract}

Give all five specialists the same rules: **Place order** saves a receipt and
clears the cart together. Retrying must not create another order; a failed
checkout must leave the cart intact. The UI shows progress, errors and a way
back to shopping.

Review Copilot's plan against the detailed contract below before approving
implementation. Keep earlier behavior, tests and the one-SELECT cart query budget.

<details markdown="1">
<summary>Detailed checkout contract and edge cases</summary>

| Case | Required result |
|---|---|
| Submit a nonempty cart | `POST /api/orders` with a client-generated UUID `requestId`; first success returns **201** and a receipt |
| Receipt | `orderId`, `requestId`, `items`, `itemCount`, `totalCents`; each item snapshots `productId`, `name`, `priceCents`, `quantity`, `lineTotalCents` |
| Successful creation | Store the order snapshot in H2 and clear the cart in the same transaction |
| Missing or invalid request ID | **400**, with no order or cart mutation |
| Empty cart with a new request ID | **409**, with no order |
| Retry the same request ID | **200**, returning the same stored order; never create another order or clear a later cart |
| Failure while creating the order | Roll back both order creation and cart clearing; report an error, not success |
| UI | Place order, visible pending/error states, receipt and return to shopping; retain the request ID when retrying after a lost response |
| Cart refresh fails | Show uncertain cart state and offer a GET-only refresh; a known receipt must not trigger another order POST |
| Asynchronous completion | Cart totals, count and status agree with the authoritative cart; receipt totals stay separate; do not steal focus the user moved elsewhere |

The server reads the cart and its prices; the browser does not submit trusted
line items or totals. Receipt data must not change when the catalogue or cart
changes later. Concurrent submissions of the same request ID must also produce
one order, not two successes with different IDs.
Validate `requestId` first: invalid or missing IDs return 400 even when the
cart is empty. For a valid ID, check for an existing order before checking
the cart; a successful retry must not become an empty-cart error.
Keep an unresolved request ID across reloads. A definitive 400 or 409 retires
that attempt, but new checkout stays locked until an authoritative cart refresh
succeeds. Storage failure must be visible, not silently replaced by a new ID.

The current template has `CartService`, `CartRepository` and `CartController`,
not a separate cart entity. Ask Copilot to inspect your actual implementation
before choosing transaction and concurrency boundaries.
Keep the existing one-SELECT **GET `/api/cart`** budget and reviewed query
tests unchanged when adding checkout reads.

</details>

## Give each subagent a bounded job

| Child session | Owns and delivers |
|---|---|
| Checkout: backend | Production Java: order storage, atomic checkout, retries and REST endpoint, including necessary cart changes |
| Checkout: UI | Approved static files: pending/error states, receipt and return to shopping |
| Checkout: HTTP tests | `CheckoutContractTest.java`: creation, validation, receipt fields/totals and cart clearing |
| Checkout: resilience tests | `CheckoutResilienceTest.java` and assigned test helpers: retries, concurrency, rollback and immutable receipts |
| Checkout: review | Read-only design, cart compatibility and incoming-commit review. Findings with reviewed commit IDs; no file edits or commits |

Keep the backend together so other writers depend on the **HTTP contract**,
not unfinished Java classes. Agree on test setup/reset, shared fixture ownership
and controlled rollback/concurrency probes before launch. Each shared helper
file has one writer. Tests may be written before the endpoint exists; that is
not evidence they pass.

**First, plan:** switch this session to **Plan** using the mode control beside
the composer **before sending the prompt below**.

**Plan mode is important here:** the main agent should investigate and propose
the plan, not build checkout itself. Do not rely on the prompt's wording alone.
Save implementation for the four writers in the later delegation step.
The API requirements below describe the design to propose, not permission to code.

```copilot
Read this branch's cart implementation and propose a mock-checkout plan.
Planning only: do not modify source, tests, configuration or AGENTS.md.
Do not implement any part of checkout or launch agents.
Treat the following as requirements for the plan:
Use POST /api/orders with a UUID requestId, 201 for a new order,
200 with the same receipt for a retry, 400 for an invalid requestId,
and 409 for an empty cart with a new requestId.
Validate requestId first; return a stored order before checking whether
the cart is empty. Preserve the one-SELECT GET /api/cart budget.
Receipt fields are orderId, requestId, items, itemCount and totalCents;
item fields are productId, name, priceCents, quantity and lineTotalCents.
Plan how to snapshot server data, create the order and clear the cart atomically.
Retries, including concurrent ones, must not duplicate orders or clear a later cart.
Plan a keyboard-accessible UI with Place order, pending/error feedback,
receipt and return to shopping. Retain the same unresolved requestId after
a lost response and across reloads. Make storage failure visible; never silently
replace the ID. Retire a definitive 400/409 attempt, but keep new checkout locked
until an authoritative cart refresh succeeds. Offer GET-only recovery when
refresh fails; a known receipt must never trigger another order POST.
Keep cart totals/count/status authoritative and receipt totals separate.
Asynchronous completion must respect focus the user moved elsewhere.
Keep all earlier behavior and reviewed tests unchanged. No new dependencies,
payments, authentication, personal data or external services.
Plan four writers with exact, non-overlapping files: the complete checkout
backend, static UI, HTTP contract tests and resilience tests.
Add one read-only reviewer for the design, existing cart compatibility and
incoming commits; it must not edit files or commit.
Agree on HTTP behavior, test setup/reset and controlled rollback/concurrency
probes. Assign each shared fixture/helper file to one writer and settle any
test-facing Java interface before launch. Explain transaction and concurrency safety.
Plan five coordinated child App sessions, each with a separate new worktree
and branch, all starting from the same reviewed commit and working in parallel.
Name them Checkout: backend, Checkout: UI, Checkout: HTTP tests,
Checkout: resilience tests and Checkout: review.
You will integrate four reviewed code handoffs and the reviewer's findings
into this checkout branch. The children must not publish or merge.
Plan a machine-load check and concurrency limit of five. If unsafe or unavailable,
stop and ask rather than silently scheduling sequential implementation.
Plan meaningful failure/rollback and immutable-receipt tests, not only happy paths.
Do not edit code or launch agents yet. Show the plan and wait for my approval.
```

Review the contract, file ownership, local handoffs and concurrency limit before
approving delegation. The orchestrator will launch the five child sessions
together and integrate four code handoffs plus review findings.

**Do not choose an action that implements the plan.** Leave planning without
launching implementation and return to **Interactive**, as in
[Modes and effort]({{ site.baseurl }}/modes/#review-the-plan-then-prepare-to-write-tests).
If a plan-approval screen appears, choose the option that returns to the session
without implementing it.

**Then, delegate:** send **`/orchestrate`** below in the same session's composer.
This is the step that authorizes the five child sessions, four writers' local
handoff commits and the read-only review.

If planning already changed code, stop and review the diff before continuing.
Preserve the changes; do not reset or discard them without explicit approval.
Do not count existing main-agent implementation as five specialists' work.

```copilot
/orchestrate I approve the checkout contract, implementation plan, file ownership
and local handoffs, including five concurrent children subject to a safe load check.
Coordinate implementation; do not implement it yourself.
Check machine load, available resources and active sessions before launching.
If five concurrent children are unsafe or unavailable, stop and ask.
Create exactly five coordinated child App sessions in this repository,
each with its own New worktree and branch: Checkout: backend, Checkout: UI,
Checkout: HTTP tests, Checkout: resilience tests and Checkout: review.
Do not substitute /fleet or in-session subagents. Do not create extra sessions.
Keep this session's checkout feature branch as the integration branch, not main.
Record one reviewed starting commit on this integration branch, not default main.
Before starting work, verify all five child worktrees have that same base,
separate directories/branches and the approved assignments.
Start all five in Interactive mode without waiting for any writer's handoff.
Do not serialize backend, UI or test implementation. Respect the concurrency limit
during follow-ups as well as launches; monitor load and ask if it becomes unsafe.
Check active workers before starting or waking another child.
Give every child the complete approved contract, role, file ownership,
test setup/probe agreements, relevant source and AGENTS.md. Do not assume shared context.
Preserve the approved contract, stack, response fields and all earlier tests.
The four writers edit only assigned files and may commit those files locally for handoff.
The reviewer is read-only: no file edits, commits, cherry-picks or branch changes.
Workers must not run Maven, start/stop the shop, change other branches, push,
open PRs, merge, launch nested agents or add agent profiles.
Assign each shared fixture/helper file to one writer. Relay questions and coordinate
any interface change before affected work continues; do not invent placeholder
implementations or claim unexecuted tests pass.
Have writers report their branch, handoff commits, files and incomplete work.
Give the reviewer exact handoff commits to inspect read-only from its own worktree;
it begins with the design/existing cart code while writers implement.
It reports reviewed commit IDs, actionable findings and coverage gaps, not a code handoff.
You may review and cherry-pick only the accepted handoff commits into your clean
integration worktree. Check whether each handoff is already included; do not apply
it twice or overwrite unfinished work. Do not move or reset child branches.
Stop and ask before expanding scope or resolving conflicting ownership.
Stop and ask before resolving integration conflicts. Route implementation fixes
back to the owning child and review each new handoff.
After all four writer handoffs are integrated, review the combined diff and run
./mvnw test here. You own the Maven run and final shop preview, not five workers.
Confirm BaselineTest, CartContractTest, RemoveContractTest, QueryContractTest,
CartBoundaryTest, new CheckoutContractTest and CheckoutResilienceTest execute
without failures, errors or skips. Never weaken tests.
Have the reviewer check the final integrated commit and test results. Resolve
actionable findings through the owning writers and rerun checks after changes;
any deferral needs my review. Track which final commit was reviewed and tested.
Report the five actual contributions and child-session links, common base,
observed execution overlap, four code handoffs, review findings, final diff,
executed test counts and anything incomplete. Missing overlap is not a parallel run.
Preserve all child sessions, branches and unfinished work.
Wait for my review before publishing or merging. Only this orchestrator may
deliver the one integrated checkout PR after separate explicit approval.
If child sessions or worktrees cannot be created, stop and report the blocker.
```

Open the five child sessions from the sidebar as they are created. Check each
assignment, starting commit and owned-file diff. A name in a plan is not a
running child session, and an idle session is not proof its work is complete.
Local handoff commits are not permission to push or open five PRs.

## Watch how they communicate
{: #communication}

Open the five child sessions and inspect the four writers' handoffs and the
reviewer's findings. Record actual questions, answers and decisions, or **none exchanged**.
If direct messaging is unavailable, relay questions through the orchestrator;
messages do not copy code between worktrees. Report missing contributions or
unavailable messaging. Do not manufacture dialogue.

## Review and run the integrated feature
{: #verify-checkout}

Stay in the **orchestrator's integration worktree**, not a child's checkout.

1. **Review the combined changes.** Confirm all four writer handoffs are included once, the UI and API agree, accepted critique corrections are present and reviewer findings have recorded decisions for this commit.
2. **Check the full suite.** The orchestrator runs `./mvnw test`. All **earlier reviewed tests**, boundary tests and **new checkout tests** must execute with no failures/errors/skips.
3. **Preview checkout.** Once the shop is running here, ask Copilot to open or reload **http://127.0.0.1:18765** in the Browser canvas. Start with an empty cart, add the €10 Notebook twice and place an order: the receipt must show quantity **2** and total **€20**, followed by an empty cart. Return to shopping.

**You own the server, not the agents.** If the shop runs from this worktree,
reuse it and wait for **DevTools** to finish reloading the compiled changes.
If it runs elsewhere, stop it with **Ctrl+C in its owning terminal**.
Only if no shop is running, start it from this integration worktree:

```sh
./mvnw spring-boot:run
```

<details markdown="1">
<summary>Detailed failure, concurrency and accessibility checks</summary>

**Contract and regressions.** Check that the UI and API use the same fields
and errors, data transactions match the clearing rule, and tests cover failure,
snapshots, concurrent duplicate submissions and replay after new items have
been added. The generated checkout tests are additional cases, not a new
supplied reference checkpoint. A disabled button alone does not prove server-side
duplicate prevention; use the HTTP regression results for retry, rollback and
concurrency evidence.

**Browser checks.** Check visible error feedback for a failed request.
If Place order is disabled on an empty
cart, verify the required **409** through HTTP tests; do not enable it just
for this demonstration. Confirm keyboard access and a narrow viewport.
Move focus to the catalogue while a real response is pending: completion
must respect that choice. Check the cart's live status as well as its visible
total, and inspect the complete focus ring during natural Tab scrolling.

**Failure and concurrency probes.** The transaction boundary must include
physical commit, not just the body of an annotated Java method. Inject failure
after a real write and verify both order and cart roll back. For overlap, hold
an uncommitted write and establish that a second request entered the server;
two client futures alone are not proof. Compare receipts as parsed wire JSON
so Java UUID or numeric node types do not create a test-harness mismatch.

If simulating a lost response, let the real server commit, record its response,
then discard delivery and retry the same ID after reload. Label fault injection;
never fabricate a successful backend response. Save raw outcomes and viewport
screenshots before assertions or cleanup, bound the probe, and close each owned
helper even when another cleanup fails. An incomplete probe is not a pass.

</details>

Review **Changes**, the full starter-to-current result, tests and the running
checkout before authorizing delivery. Writers own their local handoff commits;
only the orchestrator integrates, publishes and manages the checkout PR.

## Deliver checkout into main
{: #deliver-checkout}

Stay in **Cart: mock checkout** and reuse
[Agent Merge]({{ site.baseurl }}/integrate/#merge-the-ui-pr-first).
Deliver **one checkout PR**, not five specialist PRs or a new delivery session.
The three task PRs, both worker PRs and any accepted critique corrections must
already be on your own `main`; if local recovery was used,
resolve those delivery blockers first or keep the result explicitly incomplete.
Do not publish a recovered combined branch against incomplete remote `main`
as though the earlier PRs had merged.

Confirm all five workers have finished and all reviewed handoffs are integrated.
Check the read-only review covers the current head and every finding has a recorded decision.
Resolve any pending child changes before freezing the reviewed checkout result.
After accepting the final diff, tests and preview:

1. Select **Create PR** and approve publishing only the reviewed checkout changes to your own repository. Check **`base: main` ← `head: this session's branch`**. Reuse an existing checkout PR only if its repository, head and base match; do not reopen earlier worker PRs or create duplicates.
2. Open **Create PR → Agent Merge** for this checkout PR, not the earlier merged boundary-test PR. Leave **Merge pull request** off and start with the reviewed repair options. Preserve all earlier and checkout tests; ask before out-of-scope corrections or conflict resolutions.
3. Review **Files changed**, including repairs. If `main` advanced, review the integration and rerun the full suite. Any changed PR head needs the same reviewer's read-only recheck and resolved findings; the orchestrator reruns the full suite and refreshes affected previews. Require the **tests** job and all required checks and approvals to pass for the **current PR head**. Record the reviewed head. Then enable **Merge pull request** and confirm the App's authorization prompt **for this checkout PR only**.

As before, authorization lets Agent Merge make further permitted repairs and
merge without another review pause. Keep merging off until you accept the result.
Record any later repair commits and checks separately; without a new review,
they are outside the recorded reviewer coverage.
Missing, skipped, queued or failed checks are not a pass. If PR identity, review
or check status cannot be verified, stop with merging disabled.
Continue below only when the checkout PR's actual status is **Merged**.

## Verify the merged application
{: #verify-merged-checkout}

A green feature branch or a merged PR alone is not the final result. Ask the
same orchestrator:

```copilot
Confirm the checkout PR is Merged in my own repository and record its merge commit.
Check the tests job and all required checks for that exact merged revision on main.
Fetch origin and show the latest origin/main commit. Confirm it includes checkout
and all earlier accepted work, accounting for squash merges rather than requiring
the feature commit to be an ancestor.
Confirm this worktree is clean; stop without overwriting unfinished work.
Check out the exact latest origin/main commit for verification in this same worktree.
If main is checked out elsewhere, use a detached verification checkout here.
Do not move another worktree, reset branches, delete refs or edit this checkout.
Confirm the checked-out commit equals origin/main. If main has advanced since the
merge, require passing checks for this revision too, then run ./mvnw test here.
Confirm all earlier reviewed tests, boundary tests and new checkout tests
execute without failures, errors or skips.
Show the absolute directory and shop URL for previewing this verified application.
Record the checkout PR, merge commit, verified main commit, checks and any blocker.
```

The human still owns the one persistent server. If it already runs from the
absolute directory the orchestrator just verified, let **DevTools** reload
the compiled merged-main changes and wait for startup to finish.
If it belongs to another worktree, stop it with **Ctrl+C in its owning terminal**.
Only if it is not running from the verified directory, start it there:

```sh
./mvnw spring-boot:run
```

Reload **http://127.0.0.1:18765** in the Browser canvas. Confirm **Place order**
is present. Start with an empty cart, add the €10 Notebook twice and check the receipt shows quantity **2**
and **€20**, the cart clears, and returning to shopping works.
Opening a canvas or selecting another repository does not replace a running
server. Check its owning directory if you still see an older application.

**Done when:** the checkout PR is merged into your own `main`, merged-revision
checks and local verification pass, and the app running from the verified main
revision demonstrates checkout. Record the PR, commits, actual five contributions
and preview evidence on the [worksheet]({{ site.baseurl }}/worksheet/).
Then continue with Chronicle and the final handoff.

<details markdown="1">
<summary>Availability, cost and recovery</summary>

Five agents are a teaching example, not automatically the most efficient
choice for a small app. Each consumes model usage. Check the `/` picker and
permissions; do not broaden account access to create child sessions.
Concurrency depends on your build and machine. If five concurrent children are
unsafe or unavailable, stop and agree on a fallback. Work scheduled in smaller
batches is a limited-concurrency run, not the five-way parallel exercise.
If child sessions or worktrees are unavailable, use a facilitator's demonstration
or an explicitly approved single-agent implementation.
Mark it as **not a completed five-agent run**.
If coding or tests fail, preserve the integration branch, five child worktrees,
local commits and earlier worker refs; record checkout as unfinished and continue
the handoff with the earlier reviewed result.
Do not discard work, weaken assertions or invent a successful receipt.
If GitHub, CI, Agent Merge or required approval blocks publication or merging, preserve the
branch and any open checkout PR. Mark **verified locally; delivery blocked**,
not complete. Turn off Agent Merge while blocked or before local recovery.
Do not substitute a direct push or local merge into `main`, bypass protections,
force-push, broaden permissions or delete branches.
If the PR merged but post-merge checks or preview fail, record **merged;
post-merge verification blocked**. Any repair needs a separately approved
follow-up feature branch and reviewed PR; never edit the verification checkout.
The published reference checkpoints do not include checkout.

</details>

## What you have learned

- Distinguish five visible child App sessions from `/fleet` subagents within one session.
- Run four writers and one read-only reviewer from a common base, using HTTP contracts and exclusive file ownership rather than serial backend handoffs.
- Distinguish four code handoffs from review findings and verify actual execution overlap.
- Verify atomic checkout, immutable receipts and retry behavior alongside all earlier tests and the running UI.
- Reuse Agent Merge for the integrated checkout PR under explicit authorization, then verify the exact merged-main application rather than an older running copy.
- Distinguish locally verified work, merged and verified delivery, and blocked or unavailable capabilities.
