# Workshop site

The Jekyll source is `workshop/`. The public home is
https://www.julien-dubois.com/github-copilot-app-java-workshop/; chapters such as
`setup/` sit directly below it. `_config.yml` supplies the project base URL.
The minimal header links to the workshop home; chapter navigation includes a
**View on GitHub** button for the source repository. Site assets and chapter
links use the project prefix. Do not add a CNAME: this project inherits the
owner's Pages domain. The main website owns redirects from the former handbook URLs.

`.github/workflows/workshop-pages.yml` builds and validates the handbook on
relevant canonical-repository PRs and publishes verified `main` builds using
GitHub Actions Pages. Set repository **Settings → Pages → Source** to
**GitHub Actions**. The `github-pages` environment must permit `main` deployment.
No default-branch publication or Pages configuration should happen without
maintainer approval.
The build runner is pinned to Ubuntu 24.04, supported by the existing pinned
Playwright release; do not silently follow `ubuntu-latest` to unsupported images.

The workflow is explicitly gated to `jdubois/github-copilot-app-java-workshop`.
Learner repositories created with **Use this template** retain their own Java CI
without needing Pages permissions or settings. Publishing handbook copies is not
supported by this workflow: keep using the official handbook, whose template
links name the upstream repository while exercises explicitly use the learner's
repository and its own `main`.

## Validate locally

From the repository root:

```sh
cd workshop
bundle check
bundle exec jekyll build --destination tools/copilot-workshop/.build/site
python3 -m unittest discover -s tools/copilot-workshop -p 'test_*.py'
python3 tools/copilot-workshop/check-site.py --remote
node --test tools/test-analytics.mjs
npm --prefix tools/copilot-workshop ci
npm --prefix tools/copilot-workshop exec -- playwright install chromium
node tools/copilot-workshop/test-site.mjs
```

Run `bundle install` if the locked gems are missing. Generated output is ignored
and excluded from Pages. The browser check owns only a temporary static-file
server, never the human's shop on port 18765. It blocks analytics network traffic.
Run `./mvnw test` separately from the repository root for the Java starter.

## Source and evidence

The initial migration comes from tracked source at
[`jdubois/jdubois.github.com@98ed7f0`](https://github.com/jdubois/jdubois.github.com/commit/98ed7f008192ef9ab497e299e7df2adb5b399f3d).
Its chapter navigation, prompt-copy behavior, consent UI and analytics
implementation are retained, with standalone route
adaptations. The personal-site header and conference return link have been
replaced with workshop navigation and the repository button.
The reading layout follows
[GitHub Docs](https://docs.github.com/en/get-started/using-github/hello-world)
and [Primer navigation](https://primer.style/product/components/nav-list/):
a white structural rail, neutral selected rows with green active markers,
compact typography and blue reading links. Colors and fonts draw on the
[GitHub brand foundations](https://brand.github.com/foundations/color).
The overview's conceptual artwork is deliberately smaller and unframed;
genuine application captures retain their contents and provenance.
This remains an independently authored workshop; the
GitHub mark identifies only the repository link, not the site's own identity.

[Mona Sans](https://brand.github.com/foundations/typography) and its mono companion
are self-hosted under `assets/fonts/`, with the SIL Open Font License alongside.
The unmodified normal-width variable WOFF2 files come from
[`github/mona-sans@4bc6ba8`](https://github.com/github/mona-sans/tree/4bc6ba8b354c36b4fb66d32cd67b4c1f2beb0a06/fonts/webfonts/variable):
`MonaSansVF[opsz,wght].woff2` and `MonaSansMonoVF[wght].woff2`.
Use optical sizing without manual letterspacing or ligatures for reading text.
Do not introduce a GitHub-logo site lockup or deprecated Copilot mascot imagery.

The shared analytics property remains `G-92TRR0HJMQ` and the origin-wide
localStorage key remains `jdubois-analytics-consent`. No analytics loads before
acceptance; the footer's Cookie settings control supports live revocation.

`assets/*.json` and the four PNG captures are unchanged historical evidence,
including the former repository name in their recorded source identity.
GitHub redirects that repository URL to the renamed upstream. Do not rewrite
receipt identities or hashes to imply a new capture. The checker verifies
internal consistency, image hashes, cart data, MCP receipts and live pinned
tag SHAs. New capture runs require their own real evidence and JVM metadata.

The three Java reference contracts under `tools/copilot-workshop/reference-tests/`
are preserved byte-for-byte maintainer resources, excluded from the site and
Maven's test source tree. They must never substitute for reviewed,
learner-generated exercise tests.

The root `tools/verify-checkpoints.py` loads `tools/checkpoint-pins.json`,
checks every published tag/reference tip against its full SHA, and reads original
contracts from pinned commit `c0ac24920dc16812e2c7187cc95245faffc84316`.
Fetch full history and reference branches before running it:

```sh
git fetch origin main 'refs/heads/reference/*:refs/remotes/origin/reference/*' --tags
python3 tools/verify-checkpoints.py
```

Run these commands from the repository root in a current maintainer checkout.
The verifier uses temporary worktrees, preserves published refs and writes
receipts under `target/checkpoint-checks/`. Missing/moved refs are errors, not a
reason to update pins. Skills are independently pinned in
`.github/skills/provenance.json`; `tools/vendor-skills.py` intentionally refreshes
their complete sources. Do not copy reference answers into `src/test/`.
