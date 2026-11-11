---
layout: default
title: Improve usage with Chronicle
description: "Review token efficiency, agent turnaround and output quality, then choose one evidence-backed workflow change."
permalink: /tokens/
workshop: true
next: finish
next_title: Review and hand off
---

## What you will learn

Review workshop history with Chronicle while respecting privacy. Balance token
usage, task completion time and result quality, then choose one evidence-backed
workflow improvement without weakening tests or review.

## Review your workshop sessions

You have fixed a bug, generated a feature, polished the UI, investigated a query
problem, coordinated parallel work, requested a critique and delegated checkout
implementation. Use **Chronicle in GitHub Copilot App** to find patterns across
those sessions: what helped, what caused rework and what you could improve.

**Goal:** balance token economics, turnaround time and quality, not simply use
fewer tokens. Preserve tests, review and permission boundaries.

<figure>
  <a href="{{ site.baseurl }}/assets/illustration-chronicle-history-insights.svg" target="_blank"><img src="{{ site.baseurl }}/assets/illustration-chronicle-history-insights.svg" alt="Chronicle analyzes Copilot session history to summarize and search past work, explain reported usage patterns, provide workflow tips and suggest project-instruction improvements. This chapter focuses on token efficiency, agent turnaround and output quality." width="1440" height="880" loading="lazy"></a>
  <figcaption>Use workflow tips to balance token efficiency, turnaround time and quality.</figcaption>
</figure>

## Decide before analyzing history

Chronicle can access history across repositories. Running usage tips may start
that analysis immediately: a later workshop-only prompt **cannot undo prior
access**. Before running it, decide whether you are comfortable with the
history it may use. A repository name or a request to filter the report does not restrict which
history the command can access.

**You may opt out.** If the accessible history is unsuitable, or you cannot
verify an offered pre-execution scope control, do not launch the analysis.
Review your workshop transcript locally instead, choose one better prompt,
and record **"Chronicle not run: privacy choice."** You can complete this
exercise by reviewing the transcript instead. Do not project personal history
on a classroom screen.

## Open Chronicle if you opted in

Create a **new App session** in your workshop repository and name it
**Cart: Chronicle**. The App creates a new worktree, but this read-only analysis
does not use it. Leave **Cart: mock checkout** and its verified worktree unchanged;
no app restart is needed. A fresh session does not restrict history access.

Review the **current repository** over the **past seven days**;
you do not need to enter dates or list session names or IDs.
Exclude this Chronicle session.

In the new session's **App composer, not a terminal**, send the command and
request as **one message**:

```copilot
/chronicle tips Review all workshop sessions for the current repository
over the past seven days, excluding this Chronicle session and unrelated work.
State the repository, resolved time range/timezone and sessions used.
Suggest up to three improvements covering token efficiency, agent turnaround
time and output quality, grounded in observed examples. Explain trade-offs.
Preserve tests, review and permission boundaries. Report only available metrics
with units and coverage; mark missing data unknown. Do not infer currency or edit files.
```

Use **`tips`** for this broader workflow review. **`cost-tips`** is an optional
token-spend drill-down; you do not need to run both.

If Chronicle is unavailable in your build, review your workshop transcript
locally instead and record **"Chronicle not available."**
Scope wording does not restrict history access. Check the returned scope;
if unrelated work appears, stop and do not share it.

## Understand the recommendations

| Lens | Evidence to look for |
|---|---|
| Token economics | Repeated broad reads, oversized logs or unnecessary skill loading. Narrow the investigation and load guidance on demand. |
| Agent turnaround | Repeated corrections, duplicate investigation or avoidable serial handoffs. Improve the brief or agree on interfaces before delegating. |
| Output quality | Missing acceptance cases, UI/API mismatch or stale review evidence. Strengthen the contract and verification. |

These are patterns to look for, not findings every report must contain.
A longer initial brief or an additional review may use more tokens but reduce
rework and improve the result. Choose model and effort for the task, not on the
assumption that more effort always improves quality.

Here, **performance means completing tasks faster with fewer corrections**.
Chronicle reviews how you work with Copilot, not how fast the shopping cart
responds. Check the application separately with tests and HTTP/SQL measurements.

Use recorded agent execution time when available, excluding time spent waiting
for human input.

### Distinguish tokens, credits and cost

Input/output/cache counts, when available, describe token usage for the reported
scope. `/context`, where exposed, describes the active window—not total workflow
consumption. Credits, model-weighted usage and billed currency are different
quantities. Preserve Chronicle's labels and units; do not turn an unexplained
cost field into dollars.

Fusion can make additional calls. Do not infer complete Fusion accounting from
the main conversation alone. Missing usage is **unknown, not zero**.
The same applies to the rubber duck and five-subagent exercise: include their
usage only if exposed, and distinguish five assignments from five simultaneous
agents. More agents are not proof of lower cost or better quality.
Caching can change cost without changing task quality or raw token counts.

## Change one habit

On the [worksheet]({{ site.baseurl }}/worksheet/), record:
**observation → supporting session/example → next action → checks retained**.
For example, replace “fix the cart” with the reproduction, relevant endpoint,
acceptance criteria and exact regression command.

Choose one recommendation and record the expected token, time or quality
benefit and its trade-off. Use that improved brief for the final review, keeping
the same tests and evidence requirements. Different tasks are not controlled
comparisons; usage or timing differences do not prove an improvement.
For this exercise, use existing sessions rather than creating extra comparison runs.

If history is not available yet, use the actual workshop transcript to identify
a repeated read or unclear prompt and mark Chronicle “not observed.”
A new account may not have enough history; record usage as unavailable rather
than guessing figures. Run the analysis once, not after every message, because
the analysis itself also consumes resources.

Ask Copilot to suggest **one short repository instruction** for a recurring
problem you identified. Record it as a suggestion for now; **do not edit the
verified main checkout** or silently add commits after checkout delivery.
If you explicitly choose to apply it, use a new follow-up feature branch.
That change needs its own review, publishing/merge approval, PR and verification.
For local recovery, preserve the checked result and create a normal branch before
any separately approved edits.
Describe expected benefits as predictions until you measure them. Session-history
advice is not a performance benchmark or proof of code quality.

Continue with the [final review and handoff]({{ site.baseurl }}/finish/).

## What you have learned

- Review workshop history with Chronicle or a local transcript, respecting privacy.
- Balance token usage, task completion time and result quality rather than assuming fewer tokens means better work.
- Choose one improvement supported by session examples: refine a prompt or propose a repository instruction, keeping tests and review unchanged.
