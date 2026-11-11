"""Keep one workshop without duration labels, chapter timings or alternate routes."""
from pathlib import Path
import hashlib
import re
import unittest

ROOT = Path(__file__).resolve().parents[2]
HANDBOOK = ROOT
SEQUENCE = ["", "setup", "ticket", "modes", "skills", "generate",
            "canvas", "tools", "parallel", "integrate", "rubber-duck",
            "subagents", "tokens", "finish"]
EXERCISES = {"ticket", "modes", "skills", "generate",
             "canvas", "tools", "parallel", "integrate", "rubber-duck",
             "subagents", "tokens"}


def chapter(slug):
    return (HANDBOOK / (slug or "index")).with_suffix(".md").read_text()


class WorkshopScheduleTests(unittest.TestCase):
    def test_reference_tests_are_preserved_only_as_maintainer_resources(self):
        source_blobs = {
            "CartContractTest.java": "ba7918c297408c058721c6a653363ad374ebf6aa",
            "RemoveContractTest.java": "d58825a26eba0721f91e716a9ea6d7e2f6b79a15",
            "QueryContractTest.java": "198b27cdc3558a4a55441e67ecc8eaaa13a6a4b9",
        }
        directory = ROOT / "tools/copilot-workshop/reference-tests"
        self.assertEqual({path.name for path in directory.glob("*.java")},
                         set(source_blobs))
        for name, blob in source_blobs.items():
            with self.subTest(reference=name):
                content = (directory / name).read_bytes()
                header = f"blob {len(content)}\0".encode()
                self.assertEqual(hashlib.sha1(header + content).hexdigest(), blob)
        maintenance = (ROOT / "tools/copilot-workshop/README.md").read_text()
        self.assertIn("c0ac24920dc16812e2c7187cc95245faffc84316", maintenance)
        self.assertIn("excluded from the Jekyll", maintenance)

    def test_query_tests_are_generated_with_an_explicit_measurement_boundary(self):
        tools = re.sub(r"\s+", " ", chapter("tools"))
        section = tools.split("## Fix the N+1 query issue", 1)[1].split(
            "## Publish the reviewed result", 1)[0]
        self.assertEqual(section.count("```copilot "), 1)
        prompt = section.split(
            "```copilot ", 1)[1].split("```", 1)[0]
        for text in ["/java-hibernate-jpa", "spring-boot-testing",
                     "src/test/java/com/juliendubois/workshop/QueryContractTest.java",
                     "8 and 16 distinct products", "exactly 1 SELECT",
                     "completed HTTP GET /api/cart response",
                     "Seed each cart first, then clear the statistics",
                     "before any verification queries",
                     "product IDs, names, prices, quantities, line totals",
                     "Show the assertions; wait for my approval before running them or optimizing",
                     "real HTTP requests and database access",
                     "do not retrieve reference tests or solutions",
                     "query-budget assertions fail before fixing",
                     "No global eager loading, dependency changes or unrelated refactors",
                     "Keep earlier tests and assertions unchanged",
                     "./mvnw -Dtest=BaselineTest,CartContractTest,RemoveContractTest,QueryContractTest test",
                     "before/after query counts and actual test results",
                     "Do not commit yet"]:
            self.assertIn(text, prompt)
        self.assertLess(prompt.index("assertions fail before fixing"),
                        prompt.index("Then fix the N+1"))
        self.assertLess(prompt.index("wait for my approval"),
                        prompt.index("Run the tests and confirm"))
        self.assertLessEqual(len(prompt.split()), 190)
        self.assertIn("/tools/#fix-the-n1-query-issue", chapter("prompts"))
        self.assertIn("generated test count may vary", tools)
        self.assertNotIn("Expect **2 failures**", tools)
        self.assertIn("all generated cart, removal and query tests", tools)
        for path in HANDBOOK.glob("*.md"):
            if path.stem == "facilitator":
                continue
            with self.subTest(chapter=path.name):
                self.assertNotIn("teaching/", path.read_text())
                self.assertNotIn("teaching test", path.read_text())
                self.assertNotIn("supplied query", path.read_text())

    def test_three_sequential_tasks_have_dedicated_sessions_and_prs(self):
        setup = re.sub(r"\s+", " ", chapter("setup"))
        self.assertIn("one named session and one reviewed PR for each task", setup)
        self.assertIn("latest merged **`main`**", setup)
        self.assertIn("Send its first prompt before naming it", setup)
        for slug in ["setup", "skills", "generate", "canvas", "tools", "prompts"]:
            with self.subTest(chapter=slug):
                text = chapter(slug)
                self.assertNotIn("workshop-quantity", text)
                self.assertNotIn("workshop-feature", text)
                self.assertNotIn("Create a branch", text)
        for slug, name in [("setup", "Cart: quantity bug"),
                           ("generate", "Cart: item removal"),
                           ("tools", "Cart: query optimization")]:
            with self.subTest(session=name):
                source = chapter(slug)
                self.assertIn("**New worktree**", source)
                self.assertIn(name, setup)
                prompt = re.search(r"```copilot\n.*?```", source, re.DOTALL)
                rename = re.search(
                    rf"Once the session has started, name (?:the session|it) \*\*{re.escape(name)}\*\*",
                    source)
                self.assertIsNotNone(prompt)
                self.assertIsNotNone(rename)
                self.assertLess(prompt.end(), rename.start())
        for slug, heading, expected in [
                ("skills", "## Publish the quantity fix", "quantity-fix PR"),
                ("canvas", "## Publish removal and Canvas changes", "removal-and-Canvas PR"),
                ("tools", "## Publish the reviewed result", "reviewed PR")]:
            with self.subTest(delivery=slug):
                delivery = re.sub(r"\s+", " ", chapter(slug)).split(
                    heading, 1)[1].split("## What you have learned", 1)[0]
                for text in ["**Create PR**", "**`main`**", "own repository",
                             "If the PR already exists, open it instead",
                             expected, "all required checks and approvals pass",
                             "Do not bypass protections", "PR as Merged",
                             "merged-revision tests pass", "Fetch origin/main"]:
                    self.assertIn(text, delivery)
        self.assertIn("Do not start removal until this PR is merged and verified",
                      chapter("skills"))
        self.assertIn("Do not start MCP until this PR is merged and verified",
                      chapter("canvas"))
        for slug in ["generate", "tools"]:
            self.assertNotIn("Do not create a new session", chapter(slug))
            self.assertIn("must be merged and verified first", chapter(slug))

    def test_supporting_pages_follow_main_sessions_and_checkout_children(self):
        names = ["Cart: quantity bug", "Cart: item removal",
                 "Cart: query optimization", "Cart: empty-state UX",
                 "Cart: boundary tests", "Cart: mock checkout", "Cart: Chronicle"]
        for slug in ["prompts", "worksheet", "facilitator"]:
            for name in names:
                with self.subTest(surface=slug, session=name):
                    self.assertIn(name, chapter(slug))
        overview = re.sub(r"\s+", " ", chapter(""))
        for text in ["Each of the first three tickets has a named session and one reviewed PR",
                     "Removal and Canvas polish share a PR",
                     "UI first, then boundary tests",
                     "Delivery starts with the quantity-fix PR"]:
            self.assertIn(text, overview)
        tokens = re.sub(r"\s+", " ", chapter("tokens"))
        for text in ["**current repository**", "**past seven days**",
                     "do not need to enter dates or list session names or IDs",
                     "Exclude this Chronicle session"]:
            self.assertIn(text, tokens)
        worksheet = chapter("worksheet")
        for text in ["UI merged-main revision and its passing tests CI job",
                     "Combined preview from the verified directory",
                     "Current repository, reported seven-day range/timezone and actual source sessions"]:
            self.assertIn(text, worksheet)
        for path in HANDBOOK.glob("*.md"):
            for stale in ["preparation PR", "preparation handoff", "preparation recovery",
                          "If preparation used local recovery", "PR creation prompt",
                          "publication prompts", "run all currently activated tests"]:
                with self.subTest(surface=path.name, obsolete=stale):
                    self.assertNotIn(stale, path.read_text())

    def test_prompt_cards_connect_planning_implementation_and_runtime_evidence(self):
        cards = chapter("prompts")
        investigation = cards.split("## Investigate without editing", 1)[1].split(
            "## Use the test skill", 1)[0]
        self.assertIn("Stay in **Cart: quantity bug**", investigation)
        self.assertIn("not the session's first prompt", investigation)
        feature = cards.split("## Generate a feature", 1)[1].split(
            "## Canvas and UI feedback", 1)[0]
        self.assertIn("/generate/#generate-the-backend-and-ui", feature)
        self.assertIn("/generate/#preview-and-iterate", feature)
        self.assertIn("publish the feature and polish together afterward", feature)
        mcp = cards.split("## Investigate through MCP", 1)[1].split(
            "## Parallel worker cards", 1)[0]
        steps = ["/tools/#start-the-query-session", "/tools/#connect-runtime-tools",
                 "/tools/#reproduce-the-same-workload", "/tools/#ask-copilot-for-evidence",
                 "/tools/#fix-the-n1-query-issue", "/tools/#publish-the-reviewed-result"]
        positions = [mcp.index(step) for step in steps]
        self.assertEqual(positions, sorted(positions))

    def test_removal_feature_flows_from_plan_to_generated_tests_and_iteration(self):
        feature = re.sub(r"\s+", " ", chapter("generate"))
        steps = ["## Start from the reviewed fix",
                 "Send this prompt to start planning the feature:",
                 "Review the plan in the **plan canvas on the right**",
                 "## Generate the removal tests", "## Generate the backend and UI",
                 "## Preview and iterate", "## Save the feature and continue"]
        positions = [feature.index(text) for text in steps]
        self.assertEqual(positions, sorted(positions))
        planning = feature.split("```copilot ", 1)[1].split("```", 1)[0]
        for text in ["merged quantity fix", "CartContractTest.java", "Remove button",
                     "returns 200 with the updated cart",
                     "Remove deletes the entire product line and all its units, not just one unit",
                     "empty cart with zero count and total",
                     "Other products and their quantities stay unchanged",
                     "missing line returns 404",
                     "catalogue product that has never been added",
                     "Do not edit files yet"]:
            self.assertIn(text, planning)
        tests = feature.split("## Generate the removal tests", 1)[1].split(
            "```copilot ", 1)[1].split("```", 1)[0]
        for text in ["/spring-boot-testing",
                     "Generate src/test/java/com/juliendubois/workshop/RemoveContractTest.java",
                     "do not retrieve reference tests or solutions",
                     "subsequent GET /api/cart",
                     "quantity 3", "removal deletes all 3 units",
                     "Do not implement removal, change earlier tests",
                     "wait for my review"]:
            self.assertIn(text, tests)
        for text in ["must fail before implementation",
                     "no fixed test or failure count",
                     "Keep all reviewed tests and assertions unchanged",
                     "Report your actual observation",
                     "repeat the browser checks", "**this same session, Cart: item removal**"]:
            self.assertIn(text, feature)
        self.assertNotIn("Expect **3 tests, 2 failures**", feature)
        for slug in ["generate", "tools", "canvas", "parallel", "finish"]:
            with self.subTest(chapter=slug):
                self.assertNotIn("supplied removal", chapter(slug))
        self.assertIn("```copilot\n/spring-boot-testing", chapter("prompts"))
        self.assertIn("not decrement its quantity", feature)
        self.assertIn("Add **3 Notebooks**", feature)
        prompts = re.sub(r"\s+", " ", chapter("prompts"))
        self.assertIn("Remove deletes the entire product line and all its units", prompts)
        self.assertIn("removal deletes all 3 units", prompts)

    def test_quantity_fix_is_one_continuous_skill_exercise(self):
        skills = chapter("skills")
        steps = ["## Use the skill with /java-junit",
                 "## Generate the regression tests",
                 "must fail on the unfixed application",
                 "## Implement the agreed fix",
                 "## Review in the App", "## Verify the shop",
                 "## Publish the quantity fix",
                 "## What you have learned"]
        positions = [skills.index(text) for text in steps]
        self.assertEqual(positions, sorted(positions))
        self.assertIn("next: generate", skills)
        self.assertIn("Keep the reviewed regression assertions", skills)
        self.assertFalse((HANDBOOK / "verify.md").exists())
        for path in HANDBOOK.glob("*.md"):
            with self.subTest(chapter=path.name):
                self.assertNotIn("{{ site.baseurl }}/verify/", path.read_text())

    def test_quantity_regressions_are_generated_before_production_edits(self):
        skills = re.sub(r"\s+", " ", chapter("skills"))
        prompt = skills.split("## Generate the regression tests", 1)[1].split(
            "```copilot ", 1)[1].split("```", 1)[0]
        for text in ["Generate src/test/java/com/juliendubois/workshop/CartContractTest.java",
                     "acceptance criteria and test approach we just reviewed",
                     "existing JUnit and HTTP test fixtures",
                     "quantity limits and unchanged state after rejected input",
                     "Assert server-calculated totals",
                     "do not retrieve reference tests or solutions",
                     "Do not change production code",
                     "wait for my review before running or committing"]:
            self.assertIn(text, prompt)
        self.assertIn("must fail on the unfixed application", skills)
        self.assertIn("do not expect a fixed count", skills)
        self.assertNotIn("Expect **3 tests, 2 failures**", skills)
        self.assertIn("4 baseline tests and all generated cart tests", chapter("skills"))
        for slug in ["generate", "tools", "parallel", "integrate", "subagents", "finish"]:
            with self.subTest(chapter=slug):
                self.assertNotRegex(chapter(slug), r"\b12 (?:supplied )?tests\b")

    def test_learner_maven_commands_keep_test_output_visible(self):
        for path in HANDBOOK.glob("*.md"):
            with self.subTest(chapter=path.name):
                self.assertNotRegex(path.read_text(),
                                    r"(?:\./mvnw|\.\\mvnw\.cmd)[^\n]*\s-q\b")

    def test_modes_explain_same_session_and_test_first_handoff(self):
        modes = re.sub(r"\s+", " ", chapter("modes"))
        steps = ["## Match autonomy to the task", "## Choose effort deliberately",
                 "## Plan the quantity fix",
                 "Switch to **Plan** in this same session",
                 "## Review the plan, then prepare to write tests",
                 "return to **Interactive**"]
        positions = [modes.index(text) for text in steps]
        self.assertEqual(positions, sorted(positions))
        self.assertNotIn("## Check permissions", modes)
        for text in ["**No new session or worktree is needed.**",
                     "| **Plan** |", "| **Interactive** |", "| **Autopilot** |",
                     "**do not start the whole implementation yet**",
                     "without implementing the plan",
                     "Production code stays unchanged"]:
            self.assertIn(text, modes)
        self.assertIn("in **Interactive** mode", chapter("skills"))
        self.assertIn("Now authorize the production-fix", chapter("skills"))

    def test_setup_explains_repository_instructions_before_running_commands(self):
        setup = re.sub(r"\s+", " ", chapter("setup"))
        steps = ["review `AGENTS.md`", "## Understand AGENTS.md",
                 "## Check the starter", "## Start the application"]
        positions = [setup.index(text) for text in steps]
        self.assertEqual(positions, sorted(positions))
        for text in ["Copilot loads applicable instructions automatically",
                     "does not run commands or grant tool permissions",
                     "run the full suite as you add tests",
                     "exact, working build, run and test commands",
                     "random ports and isolated databases",
                     "Stay short and current",
                     "you don't need to edit them"]:
            self.assertIn(text, setup)

    def test_fix_requirements_are_introduced_when_planning(self):
        investigation = chapter("ticket")
        self.assertNotIn("## What the fix must achieve", investigation)
        self.assertIn("## Check the investigation", investigation)
        self.assertIn("No code should have changed yet.", investigation)
        modes = chapter("modes")
        steps = ["### Acceptance criteria",
                 "Switch to **Plan** in this same session", "```copilot"]
        positions = [modes.index(text) for text in steps]
        self.assertEqual(positions, sorted(positions))
        for text in ["quantity 2, total €20", "quantity 3 produces quantity 5",
                     "Quantities remain 1–99", "rejected input leaves state unchanged",
                     "Prices and totals come from the server",
                     "no checkout, stock management, accounts, new dependencies"]:
            self.assertIn(text, modes)
        self.assertIn("{{ site.baseurl }}/modes/#acceptance-criteria",
                      chapter("skills"))
        self.assertIn("permalink: /modes/", modes)
        self.assertNotIn("{{ site.baseurl }}/fusion/", modes)
        self.assertIn("Do not edit files yet; wait for my review.", modes)

    def test_workshop_amounts_use_euros_not_cent_amounts(self):
        for path in HANDBOOK.glob("*.md"):
            with self.subTest(chapter=path.name):
                text = path.read_text()
                self.assertNotRegex(text, r"\b\d+\s+cents\b")
                self.assertNotRegex(text, r"\$\d|\bUSD\b")
        for slug in ["ticket", "prompts", "skills", "subagents", "facilitator"]:
            with self.subTest(euro_examples=slug):
                self.assertIn("€20", chapter(slug))

    def test_chronicle_availability_is_checked_in_its_own_chapter(self):
        self.assertNotIn("/chronicle", chapter("setup"))
        tokens = chapter("tokens")
        steps = ["## Decide before analyzing history",
                 "## Open Chronicle if you opted in", "Create a **new App session**",
                 "```copilot\n/chronicle tips Review all workshop sessions",
                 "If Chronicle is unavailable in your build"]
        positions = [tokens.index(text) for text in steps]
        self.assertEqual(positions, sorted(positions))
        self.assertIn("Chronicle not available.", tokens)
        self.assertIn("**Cart: Chronicle**", tokens)
        self.assertIn("The App creates a new worktree, but this read-only analysis does not use it",
                      re.sub(r"\s+", " ", tokens))
        self.assertIn("no app restart is needed", tokens)
        self.assertIn("A fresh session does not restrict history access", tokens)
        self.assertNotIn("Stay in **Cart: mock checkout**", tokens)
        self.assertIn("Use **`tips`** for this broader workflow review", tokens)
        self.assertIn("**`cost-tips`** is an optional", tokens)
        self.assertIn("you do not need to run both", tokens)
        self.assertNotIn("/chronicle cost tips", tokens)
        self.assertNotIn("```copilot\n/chronicle cost-tips\n```", tokens)
        self.assertNotIn("```copilot\n/chronicle tips\n```", tokens)
        self.assertNotIn("```copilot\n/chronicle\n```", tokens)
        self.assertNotIn("Do not send `/chronicle` alone.", tokens)
        self.assertNotIn("Check that the picker appears", tokens)

    def test_chronicle_prompt_is_concise_repo_scoped_and_consistent(self):
        tokens = chapter("tokens")
        token_prompts = re.findall(r"```copilot\n(.*?)```", tokens, re.DOTALL)
        self.assertEqual(len(token_prompts), 1)
        prompt = token_prompts[0].strip()
        card = chapter("prompts").split("## Improve usage", 1)[1].split(
            "## Review the diff", 1)[0]
        card_prompts = re.findall(r"```copilot\n(.*?)```", card, re.DOTALL)
        self.assertEqual(len(card_prompts), 1)
        card_prompt = card_prompts[0].strip()
        self.assertEqual(prompt, card_prompt)
        self.assertTrue(prompt.startswith("/chronicle tips "))
        self.assertLessEqual(len(prompt.split()), 80)
        normalized = re.sub(r"\s+", " ", prompt)
        for text in ["all workshop sessions for the current repository",
                     "over the past seven days",
                     "excluding this Chronicle session and unrelated work",
                     "State the repository, resolved time range/timezone and sessions used",
                     "Suggest up to three improvements",
                     "token efficiency, agent turnaround time and output quality",
                     "grounded in observed examples", "Explain trade-offs",
                     "Preserve tests, review and permission boundaries",
                     "Report only available metrics", "units and coverage",
                     "mark missing data unknown",
                     "Do not infer currency or edit files"]:
            with self.subTest(chronicle_prompt_requirement=text):
                self.assertIn(text, normalized)
        self.assertNotIn("[session", prompt)
        self.assertNotIn("[repository]", prompt)
        self.assertNotRegex(prompt, r"\[[^\]]+\]")
        source = re.sub(r"\s+", " ", tokens)
        self.assertIn("a later workshop-only prompt **cannot undo prior access**", source)
        self.assertIn("Scope wording does not restrict history access", source)
        self.assertLess(source.index("send the command and request as **one message**"),
                        source.index("/chronicle tips"))
        self.assertIn("Cart: Chronicle analysis session, excluded from source sessions",
                      chapter("worksheet"))
        self.assertIn("Return to **Cart: mock checkout**",
                      re.sub(r"\s+", " ", chapter("finish")))

    def test_chronicle_balances_tokens_turnaround_and_quality_with_evidence(self):
        source = re.sub(r"\s+", " ", chapter("tokens"))
        for text in [
                "balance token economics, turnaround time and quality",
                "| Token economics |", "| Agent turnaround |", "| Output quality |",
                "**performance means completing tasks faster with fewer corrections**",
                "Check the application separately with tests and HTTP/SQL measurements",
                "not a performance benchmark or proof of code quality",
                "Use recorded agent execution time when available, excluding time spent waiting for human input",
                "use existing sessions rather than creating extra comparison runs",
                "Missing usage is **unknown, not zero**",
                "Credits, model-weighted usage and billed currency are different",
                "Do not infer complete Fusion accounting",
                "Different tasks are not controlled comparisons",
                "Describe expected benefits as predictions until you measure them",
                "**do not edit the verified main checkout**"]:
            with self.subTest(chronicle_evidence_requirement=text):
                self.assertIn(text, source)
        explanation = next(paragraph for paragraph in chapter("tokens").split("\n\n")
                           if paragraph.startswith("Here, **performance means"))
        self.assertLessEqual(len(explanation.split()), 45)
        self.assertIn("Observed turnaround/rework and quality evidence, or unavailable",
                      chapter("worksheet"))
        self.assertIn("Token/time/quality trade-off and supporting session/example",
                      chapter("worksheet"))
        self.assertIn("Reviewed workflow efficiency and quality", chapter("finish"))
        self.assertIn("Confirm `/chronicle tips` is available", chapter("facilitator"))
        self.assertNotIn("App docs show `cost tips`", chapter("facilitator"))

    def test_chronicle_learning_outcomes_are_aligned_and_concise(self):
        tokens = chapter("tokens")
        for heading in ["What you will learn", "What you have learned"]:
            section = tokens.split(f"## {heading}\n", 1)[1].split("\n## ", 1)[0]
            source = re.sub(r"\s+", " ", section)
            with self.subTest(heading=heading):
                for text in ["privacy", "token usage, task completion time and result quality",
                             "tests", "review"]:
                    self.assertIn(text, source)
        recap = tokens.split("## What you have learned\n", 1)[1]
        self.assertEqual(len(re.findall(r"^- ", recap, re.MULTILINE)), 3)
        self.assertIn("refine a prompt or propose a repository instruction", recap)
        self.assertIn("keeping tests and review unchanged", recap)
        self.assertNotIn("improve the next prompt or project instruction", recap)

    def test_mcp_connection_is_deferred_to_runtime_exercise(self):
        setup = chapter("setup")
        self.assertNotIn("## Connect runtime tools", setup)
        self.assertNotIn("get_live_activity", setup)
        self.assertIn("MCP setup comes later", setup)
        tools = chapter("tools")
        steps = ["## Connect runtime tools", "right-click your **cart-workshop** project",
                 "**Settings**", "**Repository customizations → MCP servers**",
                 'query: "/api/cart" and limit: 1',
                 "## Reproduce the same workload", "## Ask Copilot for evidence"]
        positions = [tools.index(text) for text in steps]
        self.assertEqual(positions, sorted(positions))
        self.assertNotIn("**Customize → MCP**", tools)
        self.assertIn("you do not need to\ninstall another one", tools)
        self.assertIn("customize-github-copilot-app#configuring-mcp-servers", tools)
        self.assertIn('"bootui-shopping-cart": {', tools)
        self.assertNotIn('"shopping-cart": {', tools)
        self.assertIn('"url": "http://127.0.0.1:18765/bootui/api/mcp"', tools)
        self.assertIn('"tools": ["get_live_activity", "get_request_profile"]', tools)
        prompt = tools.split("## Connect runtime tools", 1)[1].split(
            "```copilot\n", 1)[1].split("```", 1)[0]
        self.assertIn("bootui-shopping-cart MCP server", prompt)
        self.assertIn("get_live_activity", prompt)
        self.assertIn('query: "/api/cart" and limit: 1', prompt)
        self.assertIn("Show the tool response", prompt)
        self.assertIn("Do not change files or application data", prompt)

    def test_mcp_evidence_has_a_scoped_copyable_prompt(self):
        section = chapter("tools").split(
            "## Ask Copilot for evidence", 1)[1].split(
                "## Fix the N+1 query issue", 1)[0]
        prompt = re.sub(r"\s+", " ", section.split(
            "```copilot\n", 1)[1].split("```", 1)[0])
        for text in ["bootui-shopping-cart MCP server", "get_live_activity",
                     'query: "/api/cart" and limit: 8',
                     "GET /api/cart from our eight-distinct-product workload",
                     "not a POST",
                     "get_request_profile with its returned id",
                     "request ID, method/path, time and SELECT count",
                     "using the actual tool response",
                     "Do not change code or data",
                     "If no matching request is available, say so"]:
            with self.subTest(requirement=text):
                self.assertIn(text, prompt)
        self.assertLess(prompt.index("get_live_activity"),
                        prompt.index("get_request_profile"))
        self.assertLessEqual(len(prompt.split()), 100)

    def test_mcp_intro_continues_without_repeating_setup(self):
        tools = chapter("tools")
        heading = "## “Why does a full cart run so many queries?”"
        self.assertIn(heading, tools)
        intro = re.sub(r"\s+", " ", tools.split(
            heading, 1)[1].split(
                "## Start the query session", 1)[0])
        self.assertTrue(intro.strip().startswith("The cart works"))
        self.assertIn("classic **N+1 query problem**", intro)
        self.assertIn("one query loads the cart", intro)
        self.assertIn("one query per product", intro)
        self.assertIn("Static code can suggest the cause", intro)
        self.assertIn("runtime evidence shows which queries actually execute", intro)
        self.assertIn("BootUI captures these queries", intro)
        self.assertIn("Connecting its **MCP server** lets Copilot inspect them", intro)
        self.assertIn("without changing cart behavior", intro)
        self.assertIn("establish a baseline before changing code", intro)
        self.assertLessEqual(len(intro.split()), 110)
        self.assertNotIn("Ask Copilot to confirm", intro)
        self.assertNotIn("## Start the reviewed shop", tools)
        self.assertNotIn("./mvnw spring-boot:run", tools)
        self.assertIn("/setup/#move-running-shop", tools)

    def test_setup_starts_session_before_naming_and_opening_files(self):
        setup = re.sub(r"\s+", " ", chapter("setup"))
        prompt = setup.split("```copilot ", 1)[1].split("```", 1)[0]
        for text in ["Analyze this project's tech stack",
                     "backend, frontend, database and test tooling",
                     "Do not edit files, install dependencies, start the application or call MCP tools."]:
            self.assertIn(text, prompt)
        steps = [
            "**model picker below the prompt box**",
            "Send this first prompt to start the session:",
            "Once the session has started, name the session **Cart: quantity bug**.",
            "**Open in...** menu at the **top right**",
            "review `AGENTS.md`",
        ]
        positions = [setup.index(text) for text in steps]
        self.assertEqual(positions, sorted(positions))
        self.assertIn("open the session's working directory in your editor", setup)
        self.assertIn("under `.github/skills/` and `.github/mcp.json`", setup)

    def test_quantity_reproduction_waits_for_completed_requests(self):
        ticket = re.sub(r"\s+", " ", chapter("ticket"))
        for text in ["click **Reset cart**. Click", "button to re-enable",
                     "waiting for each request to finish"]:
            self.assertIn(text, ticket)
        self.assertIn("waiting for each response", chapter("prompts"))

    def test_manual_sessions_do_not_require_delegation_permissions(self):
        canvas = re.sub(r"\s+", " ", chapter("canvas"))
        prompt = canvas.split("```copilot ", 1)[1].split("```", 1)[0]
        for text in ["collaboration", "checkout", "subagents", "publish", "merge"]:
            self.assertNotIn(text, prompt)
        self.assertLessEqual(len(chapter("canvas").split("```copilot\n", 1)[1]
                                 .split("```", 1)[0].strip().splitlines()), 10)
        parallel = re.sub(r"\s+", " ", chapter("parallel"))
        for text in ["**Copilot App UI**", "**New worktree**",
                     "Both sessions may edit the same files",
                     "Both sessions will start from that same published version"]:
            self.assertIn(text, parallel)
        self.assertNotIn("AGENTS.md", parallel)
        self.assertNotIn("Update only the collaboration rule", parallel)
        self.assertNotIn("scoped collaboration", chapter("facilitator"))
        duck = re.sub(r"\s+", " ", chapter("rubber-duck"))
        self.assertIn("For this review only, I approve a read-only independent critic", duck)
        self.assertIn("Keep AGENTS.md and all other restrictions unchanged", duck)
        agents = re.sub(r"\s+", " ", chapter("subagents"))
        self.assertIn("Read AGENTS.md and keep it unchanged", agents)
        self.assertIn("Stop and report any conflicting instructions", agents)
        self.assertIn("Wait for my approval of the checkout contract, implementation plan "
                      "and file ownership", agents)
        self.assertNotIn("instruction diff", agents)
        self.assertNotIn("instruction update", agents)
        self.assertIn("The five specialists must not publish or merge", agents)

    def test_starter_allows_only_explicitly_approved_checkout_delegation(self):
        instructions = re.sub(r"\s+", " ", (ROOT.parent / "AGENTS.md").read_text())
        for text in [
                "Subagents and checkout are off by default",
                "Only in the five-subagent checkout chapter",
                "explicit user approval of the contract, implementation plan and file ownership",
                "exactly five coordinated child App sessions",
                "each in its own new worktree and branch with a bounded assignment",
                "approved delegation may authorize local handoff commits",
                "integration of reviewed commits into the orchestrator's checkout branch",
                "fresh Cart: mock checkout session and New worktree",
                "Only the orchestrator may publish and merge",
                "separate explicit approval of the integrated result",
                "specialists must not publish or merge",
                "does not authorize unrelated delegation",
                "additional App sessions beyond those five, nested agents, /fleet execution",
                "No Docker, dependencies, upgrades or authentication"]:
            with self.subTest(scoped_allowance=text):
                self.assertIn(text, instructions)
        self.assertNotIn("mock checkout in Cart: boundary tests", instructions)
        recovery = chapter("subagents").split(
            "<summary>If earlier work exists only in local recovery</summary>", 1)[1].split(
                "</details>", 1)[0]
        self.assertIn("stop and ask", recovery)
        self.assertIn("rather than editing them or proceeding", recovery)

    def test_boundary_regressions_require_approval_for_same_session_fixes(self):
        parallel = re.sub(r"\s+", " ", chapter("parallel"))
        worker = parallel.split("### Cart: boundary tests", 1)[1].split(
            "```copilot ", 1)[1].split("```", 1)[0]
        for text in ['numeric 1.5 and string "one"', "HTTP 400",
                     "GET /api/cart and persisted state are unchanged",
                     "add CartBoundaryTest.java and reuse existing fixtures",
                     "keep the failing test and propose the smallest fix",
                     "Wait for my approval before changing application behavior",
                     "Do not weaken an assertion"]:
            self.assertIn(text, worker)
        correction = parallel.split('id="boundary-fix"', 1)[1].split(
            "</details>", 1)[0]
        for text in ["**Cart: boundary tests**",
                     "approve the smallest correction in that same session",
                     "Preserve earlier tests and rerun the full suite",
                     "Do not weaken assertions or proceed while the regression still fails",
                     "Include the reviewed correction in this session's handoff and PR"]:
            self.assertIn(text, correction)
        self.assertNotIn("separate production-fix feature branch", correction)
        recovery = re.sub(r"\s+", " ", chapter("integrate").split(
            '<summary>Recovery:', 1)[1])
        self.assertIn("Preserve any approved bug fixes", recovery)
        self.assertIn("stop and propose a correction for review", recovery)

    def test_prompt_cards_follow_chapter_order_and_reference_bases_are_conditional(self):
        cards = chapter("prompts")
        self.assertEqual(re.findall(r"^## (.+)$", cards, re.MULTILINE), [
            "Investigate without editing", "Use the test skill", "Generate a feature",
            "Canvas and UI feedback", "Investigate through MCP", "Parallel worker cards",
            "Integrate with Agent Merge", "Rubber duck and subagent implementation",
            "Deliver checkout to main", "Improve usage", "Review the diff"])
        for slug in ["prompts", "finish"]:
            text = chapter(slug)
            self.assertIn("v2-start", text)
            for prompt in re.findall(r"```copilot\n(.*?)```", text, re.DOTALL):
                self.assertNotIn("v2-start", prompt)
        duck = chapter("rubber-duck")
        self.assertIn("Use `workshop-start`, the tag you created during setup", duck)
        self.assertNotIn("v2-start", duck)

    def test_cache_recovery_does_not_discard_design_records(self):
        recovery = re.sub(r"\s+", " ", chapter("facilitator"))
        for text in ["untracked `.impeccable/hook.cache.json`",
                     "local Git exclude", "review it before approval",
                     "delete the whole directory or ignore all `.impeccable/`",
                     "Keep intentional design records"]:
            self.assertIn(text, recovery)
        self.assertNotIn(".impeccable/hook.cache.json", chapter("canvas"))

    def test_agent_evidence_and_empty_checkout_do_not_require_invented_activity(self):
        agents = re.sub(r"\s+", " ", chapter("subagents"))
        for text in ["concurrency limit", "during follow-ups as well as launches",
                     "any interface change before affected work continues",
                     "**none exchanged**", "Do not manufacture dialogue",
                     "verify the required **409** through HTTP tests",
                     "do not enable it just for this demonstration"]:
            self.assertIn(text, agents)
        worksheet = chapter("worksheet")
        self.assertIn("none exchanged", worksheet)
        self.assertIn("**unknown** for concurrency", worksheet)
        self.assertIn("not an earlier PR", chapter("integrate"))

    def test_facilitator_keeps_visible_guidance_short_and_recovery_safe(self):
        facilitator = chapter("facilitator")
        body = facilitator.split("---", 2)[2]
        visible = re.sub(r"<details\b.*?</details>", "", body, flags=re.DOTALL)
        self.assertLess(len(re.findall(r"\b[\w'-]+\b", visible)), 900)
        self.assertEqual(body.count("<details"), 3)
        for text in ["## Before participants arrive",
                     "**before running Chronicle**",
                     "**two worker PRs targeting `main`**",
                     "**Cart: boundary tests**",
                     "checkout PR merged into `main`",
                     "## Recovery", "disable Agent Merge on open PRs",
                     "do not switch back to incomplete remote `main`",
                     "do not prove their generated checkout works"]:
            with self.subTest(visible_requirement=text):
                self.assertIn(text, visible)
        for text in ["restore any accepted Canvas UI changes",
                     "all 12 supplied tests pass before parallel work",
                     "participant's **own `main`**",
                     "changing\nthe remote alone does not make reference commits mergeable",
                     "Record that a reference solution was used",
                     "**not through the App**",
                     "{: #executable-checkpoints}",
                     "{: #recover-without-losing-work}"]:
            with self.subTest(recovery_requirement=text):
                self.assertIn(text, facilitator)

    def test_investigation_continues_setup_session_without_creating_an_issue(self):
        investigation = chapter("ticket")
        self.assertIn("name the session **Cart: quantity bug**", chapter("setup"))
        for text in ["## Continue in your existing session",
                     "**Copilot App project session** named **Cart: quantity bug**",
                     "{{ site.baseurl }}/setup/#open-it-in-copilot-app",
                     "**No new session or GitHub issue is needed.**",
                     "that session's composer"]:
            with self.subTest(session_guidance=text):
                self.assertIn(text, investigation)
        prompt = investigation.split("```copilot\n", 1)[1].split("```", 1)[0]
        for text in ["After resetting the cart", "quantity 1 and total €10",
                     "quantity 2\nand total €20", "Do not edit files yet"]:
            with self.subTest(investigation_prompt=text):
                self.assertIn(text, prompt)
        self.assertIn("exercise briefs, not GitHub issues", chapter(""))
        self.assertNotIn("## Give Copilot a useful ticket", investigation)

    def test_learning_focused_titles_match_menu_pages_and_next_links(self):
        navigation = (ROOT / "_data/copilot_workshop.yml").read_text()
        names = re.findall(r"^- title: (.+)$", navigation, re.MULTILINE)
        slugs = [value.strip('"').rstrip("/") for value in
                 re.findall(r"^  slug: (.*)$", navigation, re.MULTILINE)]
        titles = dict(zip(slugs, names))
        expected = {
            "setup": "Set up your App workspace",
            "ticket": "Investigate with Copilot",
            "modes": "Modes and effort",
            "skills": "Use a skill to fix the bug",
            "generate": "Generate and iterate",
            "canvas": "Canvas and Pick & polish",
            "tools": "Investigate runtime with MCP",
            "integrate": "Merge PRs with Agent Merge",
            "rubber-duck": "Review with rubber duck",
            "subagents": "Coordinate five subagents",
        }
        for slug, title in expected.items():
            with self.subTest(chapter=slug):
                self.assertEqual(titles[slug], title)
                metadata = chapter(slug).split("---", 2)[1]
                heading = re.search(r"^title: (.+)$", metadata, re.MULTILINE)
                self.assertEqual(heading.group(1), title)
        for index, slug in enumerate(SEQUENCE[:-1]):
            with self.subTest(next_link=slug or "index"):
                metadata = chapter(slug).split("---", 2)[1]
                following = re.search(r"^next_title: (.+)$", metadata, re.MULTILINE)
                self.assertEqual(following.group(1), titles[SEQUENCE[index + 1]])

    def test_skill_installation_is_visible_and_usage_has_a_copyable_prompt(self):
        skills = chapter("skills")
        self.assertIn("## What is a skill?", skills)
        self.assertIn("## Install skills in another project", skills)
        self.assertLess(skills.index("## Install skills in another project"),
                        skills.index("<details"))
        for text in ["No installation is needed for this workshop",
                     "Installation makes the skill available",
                     "Neither grants new tool permissions",
                     "keep its existing pinned copies unchanged",
                     "**Cart: quantity bug**", "```copilot\n/java-junit",
                     ".github/skills/java-junit/SKILL.md",
                     "report which guidance you loaded",
                     "gh skills install github/awesome-copilot java-junit --pin",
                     "{: #skills-are-already-installed}"]:
            with self.subTest(skills_requirement=text):
                self.assertIn(text, skills)
        for text in ["you don't need to paste them again",
                     "requirements to test assertions",
                     "propose regression",
                     "which assertions would check each requirement",
                     "Do not edit files or implement the fix yet."]:
            self.assertIn(text, skills)
        self.assertIn("```copilot\n/java-junit", chapter("prompts"))

    def test_exercises_have_app_learning_goals_and_recap(self):
        for path in HANDBOOK.glob("*.md"):
            if path.stem not in EXERCISES:
                continue
            body = path.read_text().split("---", 2)[2].strip()
            with self.subTest(chapter=path.name):
                self.assertTrue(body.startswith("## What you will learn\n"))
                self.assertEqual(body.count("## What you will learn\n"), 1)
                self.assertEqual(body.count("## What you have learned\n"), 1)
                goals = body.split("\n## ", 1)[0]
                self.assertRegex(goals, r"Copilot|Chronicle")
                recap = body.split("## What you have learned\n", 1)[1]
                self.assertNotIn("\n## ", recap)
                self.assertGreaterEqual(
                    len(re.findall(r"^- ", recap, re.MULTILINE)), 3)

    def test_preparation_and_reference_pages_have_no_learning_blocks(self):
        for path in HANDBOOK.glob("*.md"):
            if path.stem in EXERCISES:
                continue
            with self.subTest(page=path.name):
                text = path.read_text()
                self.assertNotIn("## What you will learn", text)
                self.assertNotIn("## What you have learned", text)
        self.assertIn("## The scenario", chapter(""))

    def test_one_workshop_flow_without_a_timetable(self):
        landing = chapter("")
        self.assertIn("hands-on workshop", landing)
        self.assertEqual(landing.count("## Workshop flow"), 1)
        self.assertNotIn("| Minutes |", landing)
        self.assertIn("Take a break before the parallel work", landing)

    def test_overview_and_site_metadata_cover_the_expanded_workshop(self):
        landing = chapter("")
        metadata = landing.split("---", 2)[1]
        layout = (ROOT / "_layouts/default.html").read_text()
        for text in ["Canvas", "rubber duck", "five subagents", "mock checkout"]:
            with self.subTest(summary_concept=text):
                self.assertIn(text, metadata)
        self.assertIn("page.description | default: site.description", layout)
        self.assertIn('property="og:description"', layout)
        self.assertIn("One shop, four tickets", landing)
        self.assertIn("Mock means no real payments", landing)
        flow = landing.split("## Workshop flow", 1)[1].split("\n## ", 1)[0]
        links = re.findall(r"\]\({{ site.baseurl }}/([^)]*)\)", flow)
        slugs = [link.split("#", 1)[0].rstrip("/") for link in links]
        self.assertEqual(slugs, SEQUENCE[1:])

    def test_worksheet_records_follow_workshop_order(self):
        headings = re.findall(r"^## (.+)$", chapter("worksheet"), re.MULTILINE)
        self.assertEqual(headings, [
            "A small record for each ticket", "Three task handoffs",
            "Canvas: one observed improvement",
            "MCP before and after", "Parallel handoff",
            "Agent Merge and integration", "Rubber duck: critique and decision",
            "Five subagents: mock-checkout implementation", "Chronicle: one better habit",
            "Final review and handoff"])
        finish = chapter("finish")
        self.assertIn("prices, removal, Canvas UI changes", finish)
        self.assertIn("independent critique and checkout branch/commit", finish)

    def test_final_handoff_reviews_the_verified_result_and_all_checkout_tests(self):
        finish = chapter("finish")
        source = re.sub(r"\s+", " ", finish)
        prompts = re.findall(r"```copilot\n(.*?)```", finish, re.DOTALL)
        self.assertEqual(len(prompts), 1)
        card = chapter("prompts").split("## Review the diff\n", 1)[1]
        self.assertEqual(prompts, re.findall(r"```copilot\n(.*?)```", card, re.DOTALL))
        for text in [
                "Return to **Cart: mock checkout**",
                "after the Chronicle exercise",
                "verified main commit", "recorded reviewed local commit",
                "State both compared commits",
                "If continuing from a separate reference checkout",
                "current edits and untracked files separately as unverified work",
                "Preserve reviewed acceptance criteria",
                "atomic clearing, rollback, concurrent duplicates, retry/reload recovery",
                "Do not infer that the running app uses this revision or that CI is green",
                "Do not edit files, switch or reset branches, or retarget PRs",
                "From an empty cart", "exactly 1 SELECT",
                "8 and 16 distinct products",
                "Keep private Chronicle output out of the handoff",
                "actual delivery status, unfinished work"]:
            with self.subTest(handoff_requirement=text):
                self.assertIn(text, source)
        for name in ["BaselineTest", "CartContractTest", "RemoveContractTest",
                     "QueryContractTest", "CartBoundaryTest", "CheckoutContractTest",
                     "CheckoutResilienceTest"]:
            with self.subTest(required_test_report=name):
                self.assertIn(f"`{name}`", finish)

    def test_supporting_pages_preserve_review_gates_and_recovery(self):
        requirements = {
            "index": ["On the completed normal path", "Return to **Cart: mock checkout**",
                      "unfinished work separate from the verified result",
                      "Chronicle or transcript review"],
            "prompts": ["Review the generated assertions before allowing optimization",
                        "recorded reviewed local base", "after the machine-load check",
                        "The same reviewer rechecks changed heads",
                        "coverage limits for later repairs",
                        "Its new worktree is not used for this read-only history review"],
            "facilitator": ["two worker PRs and the integrated checkout PR",
                            "matching URL is not enough",
                            "return to **Cart: mock checkout**",
                            "leave the verification checkout unchanged",
                            "Keep private Chronicle output out of the handoff",
                            "workshop/tools/copilot-workshop/reference-tests/",
                            "change into `workshop/` first"],
        }
        for slug, texts in requirements.items():
            source = re.sub(r"\s+", " ", chapter(slug))
            for text in texts:
                with self.subTest(surface=slug, requirement=text):
                    self.assertIn(text, source)
        self.assertNotIn("fix the issue in one step", chapter("prompts"))
        self.assertNotIn("website repository", chapter("facilitator"))
        self.assertIn("cd workshop\nCAPTURE_CHANNEL=chrome", chapter("facilitator"))
        navigation = (ROOT / "_data/copilot_workshop.yml").read_text()
        self.assertIn("- title: Improve usage with Chronicle\n  slug: tokens/", navigation)

    def test_worksheet_records_the_query_budget_and_final_verified_handoff(self):
        source = re.sub(r"\s+", " ", chapter("worksheet"))
        for text in ["Generated test assertions reviewed before implementation",
                     "**8 and 16 distinct products**", "exactly **1 SELECT**",
                     "completed HTTP GET `/api/cart`, excluding setup queries",
                     "eight-product MCP capture is separate evidence",
                     "Suggested repository instruction (proposal only, not applied)",
                     "Expected token/time/quality benefit (prediction until measured)",
                     "## Final review and handoff",
                     "Read-only review session/worktree and verified result commit",
                     "Local edits/untracked files, excluded from the verified result",
                     "Final full-suite counts and per-class reports, including both checkout suites",
                     "Actual PR/CI status, verified revision and running directory/URL",
                     "Completed, demonstrated, unfinished or blocked status",
                     "do not attach private Chronicle output"]:
            with self.subTest(worksheet_requirement=text):
                self.assertIn(text, source)

    def test_chapters_have_no_deadlines_or_timeboxes(self):
        timing = re.compile(r"^timebox:|\bminute \d+|\b\d{2,3}–\d{2,3}\b|\bcutoff\b",
                            re.MULTILINE | re.IGNORECASE)
        for path in HANDBOOK.glob("*.md"):
            with self.subTest(chapter=path.name):
                self.assertIsNone(timing.search(path.read_text()))

    def test_workshop_has_no_duration_labels(self):
        duration = re.compile(r"\b(?:three|3)[- ]hours?\b|\b180[- ]minutes?\b",
                              re.IGNORECASE)
        paths = list(HANDBOOK.glob("*.md")) + [
            ROOT / "_includes/copilot-workshop-nav.html"
        ]
        for path in paths:
            with self.subTest(path=path.name):
                self.assertIsNone(duration.search(path.read_text()))
        layout = (ROOT / "_layouts/default.html").read_text()
        self.assertIsNone(duration.search(layout))

    def test_learner_startup_needs_no_revision_argument(self):
        setup = chapter("setup")
        self.assertIn('annotated tag workshop-start', setup)
        self.assertNotIn("Record that SHA", setup)
        for slug in ["setup", "subagents"]:
            with self.subTest(startup_chapter=slug):
                self.assertIn("\n./mvnw spring-boot:run\n", chapter(slug))
        self.assertIn("/setup/#move-running-shop", chapter("integrate"))
        self.assertNotIn("./mvnw spring-boot:run", chapter("integrate"))
        for path in HANDBOOK.glob("*.md"):
            text = path.read_text()
            with self.subTest(chapter=path.name):
                self.assertIsNone(re.search(r"\b[A-Z][A-Z_]*_SHA\b", text))
                self.assertNotIn("workshop.revision", text)
                self.assertNotIn("runtime revision", text)
                for command in re.findall(r"^\./mvnw spring-boot:run[^\n]*$",
                                          text, re.MULTILINE):
                    self.assertEqual(command, "./mvnw spring-boot:run")
        self.assertNotIn("`workshop-start` SHA", chapter("worksheet"))

    def test_same_worktree_previews_use_devtools_after_compilation(self):
        setup = re.sub(r"\s+", " ", chapter("setup"))
        for text in ["compiled classpath", "not merely when Java source is saved",
                     "Maven test commands compile Java and copy resources",
                     "./mvnw compile", "DevTools does not switch worktrees",
                     "Static HTML, CSS and JavaScript"]:
            self.assertIn(text, setup.replace("**", ""))
        for slug in ["skills", "generate", "tools", "subagents"]:
            with self.subTest(chapter=slug):
                self.assertIn("DevTools", chapter(slug))
        for slug in ["skills", "generate", "tools"]:
            with self.subTest(same_worktree=slug):
                self.assertNotIn("./mvnw spring-boot:run", chapter(slug))
                self.assertIn("/setup/#start-the-application" if slug == "skills"
                              else "/setup/#move-running-shop", chapter(slug))
        canvas = re.sub(r"\s+", " ", chapter("canvas"))
        self.assertIn("server already running from this session's directory", canvas)
        self.assertIn("run ./mvnw compile", canvas)
        self.assertIn("Keep the shop running", canvas)
        tools = re.sub(r"\s+", " ", chapter("tools"))
        self.assertIn("Wait for DevTools before measuring again", tools)
        self.assertIn("Recreate the exact workload", tools)
        self.assertNotIn("Restart before measuring again", tools)
        self.assertIn("**switching worktrees**", chapter("integrate"))
        self.assertIn("Ctrl+C", chapter("integrate"))

    def test_checkout_and_git_bookkeeping_are_app_driven(self):
        setup = chapter("setup")
        self.assertIn("Add GitHub repository", setup)
        self.assertIn("New worktree", setup)
        self.assertIn("your new `cart-workshop` repository", setup)
        commands = re.compile(
            r"\bgit\s+(?:clone|--version|remote|tag|status|branch|rev-parse|"
            r"add|diff|commit|switch|checkout|merge)\b",
            re.IGNORECASE)
        for path in HANDBOOK.glob("*.md"):
            if path.stem == "facilitator":
                continue
            with self.subTest(chapter=path.name):
                self.assertIsNone(commands.search(path.read_text()))
        for slug in ["skills", "canvas", "tools"]:
            with self.subTest(delivery=slug):
                self.assertIn("**Create PR** in Copilot App", chapter(slug))
                self.assertIn("Review **Files changed**", chapter(slug))

    def test_preview_handoffs_follow_the_active_session_without_forced_restarts(self):
        for slug in ["skills", "generate", "canvas", "tools", "parallel",
                     "integrate", "prompts"]:
            with self.subTest(surface=slug):
                self.assertIn("/setup/#move-running-shop", chapter(slug))
        parallel = re.sub(r"\s+", " ", chapter("parallel")).split(
            "## Supervise without sharing a working directory", 1)[1]
        self.assertIn("to **Cart: empty-state UX**, then have Copilot reload", parallel)
        self.assertIn("**Cart: boundary tests** does not need another persistent shop", parallel)
        delivery = re.sub(r"\s+", " ", chapter("prompts")).split(
            "## Deliver checkout to main", 1)[1].split("## Improve usage", 1)[0]
        for text in ["Reuse the shop if it already runs from that directory",
                     "waiting for DevTools", "otherwise use the",
                     "Reload the Browser canvas"]:
            self.assertIn(text, delivery)
        self.assertNotIn("Restart the one shop", delivery)

    def test_canvas_preserves_preview_scope_and_same_session_progress(self):
        canvas = re.sub(r"\s+", " ", chapter("canvas"))
        for text in [
                "Stay in **Cart: item removal**, on its current branch",
                "human-owned server",
                "Only change src/main/resources/static/",
                "`/impeccable`", "**Pick & polish**",
                "If it already meets these criteria",
                "The removal feature and any accepted Canvas polish belong to **one PR**",
                "preserving the quantity fix and earlier tests"]:
            with self.subTest(requirement=text):
                self.assertIn(text, canvas)
        self.assertNotIn("Create a branch workshop-feature", chapter("generate"))
        self.assertIn("**new session from that updated `main`**", canvas)
        self.assertIn("**Cart: query optimization**", chapter("tools"))
        self.assertIn("canvas-recovery", chapter("canvas"))
        self.assertIn("```copilot\n/impeccable\n", chapter("canvas"))
        self.assertNotIn("Use the bundled impeccable skill", chapter("canvas"))

    def test_canvas_opens_preview_without_an_instruction_editing_exercise(self):
        canvas = chapter("canvas")
        for text in ["AGENTS.md", "project-instructions", "instruction and UI changes"]:
            self.assertNotIn(text, canvas)
        self.assertLess(canvas.index("## Open the running shop"),
                        canvas.index("## Pick one interaction to improve"))
        self.assertIn("Confirm which source directory owns the running shop", canvas)
        self.assertIn("Do not start a second server", canvas)
        self.assertIn("## Publish removal and Canvas changes", canvas)
        self.assertIn("/canvas/#browser-preview", chapter("prompts"))
        for slug in ["prompts", "parallel", "facilitator", "finish", "worksheet", "index"]:
            with self.subTest(surface=slug):
                self.assertNotIn("/canvas/#project-instructions", chapter(slug))
                self.assertNotIn("Canvas AGENTS.md", chapter(slug))
                self.assertNotIn("Canvas instruction/UI changes", chapter(slug))

    def test_canvas_refresh_is_agent_driven_after_approved_edits(self):
        canvas = re.sub(r"\s+", " ", chapter("canvas"))
        prompt = canvas.split("## Pick one interaction to improve", 1)[1].split(
            "```copilot ", 1)[1].split("```", 1)[0]
        for text in ["wait for my approval",
                     "After approval, apply it and run ./mvnw compile",
                     "in this session's directory",
                     "Reload this existing Browser canvas and verify the result",
                     "Keep the shop running",
                     "report compilation or refresh failures"]:
            self.assertIn(text, prompt)
        self.assertLess(prompt.index("wait for my approval"),
                        prompt.index("After approval"))
        self.assertIn("reload the same Browser canvas automatically", canvas)
        self.assertNotIn("In a second terminal", canvas)
        self.assertIn("Keep the shop running", prompt)

    def test_canvas_style_request_uses_compact_secondary_button(self):
        canvas = re.sub(r"\s+", " ", chapter("canvas"))
        prompt = canvas.split("## Pick one interaction to improve", 1)[1].split(
            "```copilot ", 1)[1].split("```", 1)[0]
        for text in ["Make this Remove button more compact",
                     "use the existing secondary theme color",
                     "not Add to cart's primary styling",
                     'Use a real <button type="button"> with secondary button styling, not a link',
                     "Keep its label, accessibility and whole-line DELETE behavior",
                     "visible keyboard focus", "usable click/tap target",
                     "If it already meets these criteria",
                     "say no change is needed"]:
            self.assertIn(text, prompt)
        self.assertIn("Compare **Remove** with **Add to cart**", canvas)
        self.assertIn("Remove should be compact and secondary", canvas)
        self.assertNotIn("same visual treatment as Add to cart", canvas)
        self.assertIn("removal still deletes the whole product line", canvas)
        self.assertLessEqual(len(prompt.split()), 110)

    def test_canvas_postprompt_guidance_stays_concise(self):
        section = chapter("canvas").split("## Pick one interaction to improve", 1)[1]
        guidance = section.split("```copilot\n", 1)[1].split("```", 1)[1].split(
            "<details", 1)[0]
        self.assertLessEqual(len(guidance.split()), 140)
        self.assertIn("keyboard focus remains fully visible",
                      re.sub(r"\s+", " ", guidance))
        self.assertIn("All tests must pass without weakening assertions", guidance)
        self.assertEqual(section.count("<details"), 1)

    def test_rubber_duck_is_read_only_and_corrections_need_a_branch(self):
        duck = re.sub(r"\s+", " ", chapter("rubber-duck"))
        for text in [
                "**Cart: boundary tests**", "/rubber-duck Review",
                "Do not edit files", "suggested correction",
                "actual critic", "normal follow-up feature branch",
                "before editing", "Any follow-up PR needs its own review and merge approval",
                "On the normal path, use **Create PR** for the correction",
                "preserving the correction branch",
                "starting the fresh checkout session from verified `main`",
                "If you used local recovery, keep the corrected local branch",
                "do not switch to incomplete remote `main`",
                "If you defer a finding", "without applying that correction"]:
            with self.subTest(requirement=text):
                self.assertIn(text, duck)
        self.assertIn("not a completed five-agent run", chapter("subagents"))
        self.assertIn("do not commit", chapter("finish"))

    def test_child_sessions_implement_checkout_with_owned_files_and_one_integrated_pr(self):
        agents = re.sub(r"\s+", " ", chapter("subagents"))
        for text in [
                "**Mock means no real payment processing**", "**Cart: mock checkout**",
                "exactly five coordinated child App sessions", "Checkout: backend",
                "Checkout: UI", "Checkout: HTTP tests", "Checkout: resilience tests",
                "Checkout: review",
                "/orchestrate I approve", "Read AGENTS.md",
                "**New worktree**", "**`main` as the base branch**",
                "on the App-created feature branch, not main or a detached checkout",
                "Report this session's directory, actual branch and starting commit",
                "new worktree from **that reviewed local branch**",
                "The four writers edit only assigned files", "Workers must not run Maven",
                "launch nested agents", "relay questions through the orchestrator",
                "five actual contributions", "Wait for my review before publishing or merging",
                "failed checkout must leave the cart intact", "Concurrent submissions",
                "No payments, authentication", "Record actual questions, answers and decisions",
                "scheduled in smaller batches"]:
            with self.subTest(requirement=text):
                self.assertIn(text, agents)
        for slug in ["worksheet", "finish"]:
            with self.subTest(handoff_page=slug):
                self.assertNotIn("planned, not implemented", chapter(slug))
                self.assertIn("checkout feature branch", chapter(slug))
        self.assertLess(agents.index("Start a fresh checkout session"),
                        agents.index("/orchestrate I approve"))
        self.assertNotIn("Create and switch to a new branch workshop-checkout", agents)
        self.assertNotIn("Stay in **Cart: boundary tests**", agents)
        for slug in ["index", "prompts", "tokens", "finish", "facilitator", "worksheet"]:
            with self.subTest(checkout_session_page=slug):
                self.assertIn("Cart: mock checkout", chapter(slug))
        self.assertLess(agents.index("Show the plan and wait for my approval"),
                        agents.index("/orchestrate I approve"))
        self.assertLess(SEQUENCE.index("parallel"), SEQUENCE.index("rubber-duck"))
        self.assertLess(SEQUENCE.index("rubber-duck"), SEQUENCE.index("subagents"))

    def test_checkout_contract_verification_and_recovery_are_explicit(self):
        contract = chapter("subagents").split("## Agree on the contract first", 1)[1].split(
            "## Give each subagent a bounded job", 1)[0]
        overview, details = contract.split('<details markdown="1">', 1)
        self.assertIn("before approving", overview)
        self.assertIn("one-SELECT", overview)
        self.assertNotIn("| Case |", overview)
        self.assertIn("<summary>Detailed checkout contract and edge cases</summary>", details)
        self.assertIn("| Case | Required result |", details)
        self.assertIn("Concurrent submissions", details)
        self.assertIn("</details>", details)
        agents = re.sub(r"\s+", " ", chapter("subagents"))
        prompt = agents.split("Read this branch's cart implementation", 1)[1].split("```", 1)[0]
        for text in ["POST /api/orders", "UUID requestId", "201", "200",
                     "400", "409", "orderId, requestId, items, itemCount and totalCents",
                     "productId, name, priceCents, quantity and lineTotalCents",
                     "clear the cart atomically", "failure/rollback",
                     "Retries, including concurrent ones",
                     "Validate requestId first", "return a stored order before",
                     "one-SELECT GET /api/cart budget"]:
            with self.subTest(copyable_contract=text):
                self.assertIn(text, prompt)
        implementation = agents.split("/orchestrate I approve", 1)[1].split("```", 1)[0]
        self.assertIn("Preserve the approved contract", implementation)
        self.assertIn("CheckoutContractTest", implementation)
        self.assertIn("CheckoutResilienceTest", implementation)
        self.assertNotIn("POST /api/orders", implementation)
        for text in ["rollback", "snapshots", "concurrent duplicate",
                     "**€20**", "confirm the App's authorization prompt",
                     "published reference checkpoints do not include checkout",
                     "record checkout as unfinished"]:
            with self.subTest(verification=text):
                self.assertIn(text, agents)
        for path in HANDBOOK.glob("*.md"):
            with self.subTest(page=path.name):
                self.assertNotIn("planning-only exercise", path.read_text())

    def test_checkout_planning_does_not_authorize_implementation(self):
        agents = re.sub(r"\s+", " ", chapter("subagents"))
        for text in [
                "switch this session to **Plan**",
                "**before sending the prompt below**",
                "**Plan mode is important here:**",
                "Do not rely on the prompt's wording alone",
                "Planning only: do not modify source, tests, configuration or AGENTS.md",
                "Do not implement any part of checkout or launch agents",
                "Review the contract, file ownership, local handoffs and concurrency limit before approving delegation",
                "The orchestrator will launch the five child sessions together and integrate four code handoffs plus review findings",
                "**Do not choose an action that implements the plan.**",
                "return to **Interactive**",
                "without implementing it",
                "This is the step that authorizes the five child sessions, four writers' local handoff commits and the read-only review",
                "do not reset or discard them without explicit approval",
                "Do not count existing main-agent implementation as five specialists' work"]:
            with self.subTest(planning_boundary=text):
                self.assertIn(text, agents)
        self.assertLess(agents.index("switch this session to **Plan**"),
                        agents.index("Read this branch's cart implementation"))
        self.assertLess(agents.index("return to **Interactive**"),
                        agents.index("/orchestrate I approve"))

    def test_checkout_copyable_plan_includes_ui_recovery_contract(self):
        agents = re.sub(r"\s+", " ", chapter("subagents"))
        plan = agents.split("Read this branch's cart implementation", 1)[1].split("```", 1)[0]
        for text in [
                "keyboard-accessible UI with Place order, pending/error feedback",
                "receipt and return to shopping",
                "Retain the same unresolved requestId after a lost response and across reloads",
                "Make storage failure visible; never silently replace the ID",
                "Retire a definitive 400/409 attempt",
                "keep new checkout locked until an authoritative cart refresh succeeds",
                "GET-only recovery when refresh fails",
                "a known receipt must never trigger another order POST",
                "Keep cart totals/count/status authoritative and receipt totals separate",
                "Asynchronous completion must respect focus the user moved elsewhere"]:
            with self.subTest(copyable_ui_requirement=text):
                self.assertIn(text, plan)

    def test_checkout_previews_start_with_an_empty_cart(self):
        source = re.sub(r"\s+", " ", chapter("subagents"))
        for start, end in [
                ("## Review and run the integrated feature", "## Deliver checkout into main"),
                ("## Verify the merged application", "**Done when:**")]:
            preview = source.split(start, 1)[1].split(end, 1)[0]
            with self.subTest(preview_section=start):
                self.assertIn("Start with an empty cart, add the €10 Notebook twice", preview)
                self.assertLess(preview.index("Start with an empty cart"),
                                preview.index("add the €10 Notebook twice"))

    def test_checkout_repairs_refresh_review_and_record_coverage_limits(self):
        source = re.sub(r"\s+", " ", chapter("subagents"))
        delivery = source.split("## Deliver checkout into main", 1)[1].split(
            "## Verify the merged application", 1)[0]
        for text in [
                "Any changed PR head needs the same reviewer's read-only recheck and resolved findings",
                "the orchestrator reruns the full suite and refreshes affected previews",
                "Record the reviewed head",
                "Record any later repair commits and checks separately",
                "without a new review, they are outside the recorded reviewer coverage"]:
            with self.subTest(repair_review_requirement=text):
                self.assertIn(text, delivery)
        for text in ["same reviewer's read-only recheck", "Record the reviewed head"]:
            self.assertLess(delivery.index(text), delivery.index("Then enable **Merge pull request**"))
        worksheet = chapter("worksheet")
        self.assertIn("reviewed PR head at merge authorization", worksheet)
        self.assertIn("Later Agent Merge repair commits, checks and review coverage or limitation",
                      worksheet)
        finish = chapter("finish")
        self.assertIn("read-only findings for the PR head at merge authorization", finish)
        self.assertIn("coverage limits for later repairs", finish)

    def test_checkout_review_keeps_main_path_short_and_checks_in_existing_drawer(self):
        source = chapter("subagents")
        communication = source.split("## Watch how they communicate", 1)[1].split(
            "## Review and run the integrated feature", 1)[0]
        self.assertLessEqual(len(re.findall(r"\b[\w'-]+\b", communication)), 80)
        self.assertNotIn("**example exchange**", communication)
        for text in ["four writers' handoffs", "reviewer's findings",
                     "Record actual questions, answers and decisions",
                     "**none exchanged**", "messages do not copy code",
                     "Report missing contributions", "Do not manufacture dialogue"]:
            self.assertIn(text, communication)

        review = source.split("## Review and run the integrated feature", 1)[1].split(
            "## Deliver checkout into main", 1)[0]
        self.assertEqual(review.count("<details"), 1)
        visible = re.sub(r"<details\b.*?</details>", "", review, flags=re.DOTALL)
        self.assertLessEqual(len(re.findall(r"\b[\w'-]+\b", visible)), 240)
        self.assertEqual(re.findall(r"^\d\. \*\*(.*?)\*\*", visible, re.MULTILINE),
                         ["Review the combined changes.", "Check the full suite.",
                          "Preview checkout."])
        visible = re.sub(r"\s+", " ", visible)
        for text in ["**orchestrator's integration worktree**",
                     "all four writer handoffs are included once",
                     "reviewer findings have recorded decisions for this commit",
                     "accepted critique corrections", "./mvnw test",
                     "must execute with no failures/errors/skips",
                     "http://127.0.0.1:18765", "quantity **2** and total **€20**",
                     "empty cart", "Return to shopping",
                     "**You own the server, not the agents.**", "**DevTools**",
                     "**Ctrl+C in its owning terminal**",
                     "Only if no shop is running", "./mvnw spring-boot:run",
                     "before authorizing delivery", "only the orchestrator"]:
            with self.subTest(visible_review_requirement=text):
                self.assertIn(text, visible)

        details = re.sub(r"\s+", " ", review.split('<details markdown="1">', 1)[1].split(
            "</details>", 1)[0])
        for text in ["Detailed failure, concurrency and accessibility checks",
                     "same fields and errors", "snapshots, concurrent duplicate submissions",
                     "replay after new items have been added",
                     "not a new supplied reference checkpoint",
                     "visible error feedback", "**409**", "a narrow viewport",
                     "keyboard access", "must respect that choice", "live status",
                     "complete focus ring", "physical commit", "after a real write",
                     "both order and cart roll back",
                     "two client futures alone are not proof", "parsed wire JSON",
                     "same ID after reload", "never fabricate a successful backend response",
                     "close each owned helper", "An incomplete probe is not a pass"]:
            with self.subTest(detailed_review_requirement=text):
                self.assertIn(text, details)

    def test_checkout_children_share_one_base_and_run_four_writers_plus_reviewer(self):
        agents = re.sub(r"\s+", " ", chapter("subagents"))
        prompt = agents.split("/orchestrate I approve", 1)[1].split("```", 1)[0]
        expected_names = ["Checkout: backend", "Checkout: UI",
                          "Checkout: HTTP tests", "Checkout: resilience tests",
                          "Checkout: review"]
        actual_names = re.findall(
            r"Checkout: (?:backend|UI|HTTP tests|resilience tests|review)", prompt)
        self.assertEqual(actual_names, expected_names)
        for name in expected_names:
            self.assertIn(name, chapter("worksheet"))
        for text in [
                "Coordinate implementation; do not implement it yourself",
                "each with its own New worktree and branch",
                "Do not substitute /fleet or in-session subagents",
                "Do not create extra sessions",
                "five concurrent children subject to a safe load check",
                "Check machine load, available resources and active sessions before launching",
                "If five concurrent children are unsafe or unavailable, stop and ask",
                "Record one reviewed starting commit on this integration branch, not default main",
                "verify all five child worktrees have that same base",
                "separate directories/branches and the approved assignments",
                "Start all five in Interactive mode without waiting for any writer's handoff",
                "Do not serialize backend, UI or test implementation",
                "monitor load and ask if it becomes unsafe",
                "Check active workers before starting or waking another child",
                "The four writers edit only assigned files and may commit those files locally for handoff",
                "The reviewer is read-only: no file edits, commits, cherry-picks or branch changes",
                "Assign each shared fixture/helper file to one writer",
                "do not invent placeholder implementations or claim unexecuted tests pass",
                "Give the reviewer exact handoff commits to inspect read-only from its own worktree",
                "it begins with the design/existing cart code while writers implement",
                "reviewed commit IDs, actionable findings and coverage gaps, not a code handoff",
                "Workers must not run Maven, start/stop the shop",
                "push, open PRs, merge, launch nested agents",
                "review and cherry-pick only the accepted handoff commits",
                "clean integration worktree",
                "Check whether each handoff is already included",
                "do not apply it twice or overwrite unfinished work",
                "Do not move or reset child branches",
                "ask before resolving integration conflicts",
                "Route implementation fixes back to the owning child",
                "After all four writer handoffs are integrated",
                "You own the Maven run and final shop preview",
                "Have the reviewer check the final integrated commit and test results",
                "any deferral needs my review",
                "Track which final commit was reviewed and tested",
                "observed execution overlap, four code handoffs, review findings",
                "Missing overlap is not a parallel run",
                "Preserve all child sessions, branches and unfinished work"]:
            with self.subTest(child_handoff_requirement=text):
                self.assertIn(text, prompt)
        self.assertLess(prompt.index("After all four writer handoffs are integrated"),
                        prompt.index("./mvnw test"))
        self.assertLess(prompt.index("./mvnw test"),
                        prompt.index("Have the reviewer check the final integrated commit"))
        for stale in ["Stage model, service and API work in dependency order",
                      "UI and tests may run in parallel after their interfaces are integrated",
                      "After all five contributions are integrated"]:
            self.assertNotIn(stale, agents)

    def test_parallel_checkout_roles_and_review_evidence_are_consistent(self):
        source = chapter("subagents")
        role_section = source.split("## Give each subagent a bounded job", 1)[1]
        roles = re.findall(r"^\| (Checkout: [^|]+?) \|", role_section, re.MULTILINE)
        self.assertEqual(roles, ["Checkout: backend", "Checkout: UI",
                                 "Checkout: HTTP tests", "Checkout: resilience tests",
                                 "Checkout: review"])
        plan = re.sub(r"\s+", " ", source).split(
            "Read this branch's cart implementation", 1)[1].split("```", 1)[0]
        for text in ["complete checkout backend, static UI, HTTP contract tests and resilience tests",
                     "one read-only reviewer", "it must not edit files or commit",
                     "test setup/reset and controlled rollback/concurrency probes",
                     "each shared fixture/helper file to one writer",
                     "settle any test-facing Java interface before launch",
                     "same reviewed commit and working in parallel",
                     "stop and ask rather than silently scheduling sequential implementation"]:
            with self.subTest(parallel_plan_requirement=text):
                self.assertIn(text, plan)
        for slug in ["index", "prompts", "rubber-duck", "facilitator"]:
            with self.subTest(parallel_supporting_page=slug):
                self.assertIn("read-only reviewer", chapter(slug))
                self.assertNotIn("Review and integrate model, then service", chapter(slug))
        worksheet = chapter("worksheet")
        for text in ["Common starting commit verified in all five child worktrees",
                     "observed execution overlap or limitation", "No code commit; record findings",
                     "CheckoutResilienceTest", "reviewed PR head at merge authorization"]:
            self.assertIn(text, worksheet)
        delivery = re.sub(r"\s+", " ", source).split(
            "## Deliver checkout into main", 1)[1].split("## Verify the merged application", 1)[0]
        self.assertIn("read-only review covers the current head", delivery)
        self.assertIn("every finding has a recorded decision", delivery)
        illustration = (ROOT / "assets/illustration-five-specialists.svg").read_text()
        for text in ["Checkout backend", "Checkout UI", "HTTP contract tests",
                     "Resilience tests", "Read-only reviewer",
                     "Four parallel writers + one read-only reviewer"]:
            self.assertIn(text, illustration)
        self.assertNotIn('class="link"', illustration)
        self.assertNotIn("Model precedes service", illustration)

    def test_fleet_is_explained_in_an_information_box_not_used_for_execution(self):
        source = chapter("subagents")
        box = re.sub(r"\s+", " ", " ".join(
            line[2:] for line in source.splitlines() if line.startswith("> ")))
        for text in [
                "**How is this different from `/fleet`?**",
                "within its current App session",
                "Each subagent has its own context",
                "five persistent App sessions and worktrees",
                "exactly five workers",
                "their commits need integration",
                "increase model usage",
                "do not run `/fleet` for this exercise"]:
            with self.subTest(comparison=text):
                self.assertIn(text, box)
        prompts = re.findall(r"```copilot\n(.*?)```", source, re.DOTALL)
        self.assertEqual(sum(p.startswith("/orchestrate ") for p in prompts), 1)
        self.assertFalse(any(p.startswith("/fleet") for p in prompts))
        illustration = (ROOT / "assets/illustration-five-specialists.svg").read_text()
        self.assertIn("Five parallel child sessions / five worktrees / one reviewed base",
                      illustration)
        self.assertNotIn("not five worktrees", illustration)

    def test_next_links_and_navigation_have_one_linear_sequence(self):
        for index, slug in enumerate(SEQUENCE):
            with self.subTest(chapter=slug or "index"):
                metadata = chapter(slug).split("---", 2)[1]
                following = re.search(r"^next: (\S+)$", metadata, re.MULTILINE)
                if index == len(SEQUENCE) - 1:
                    self.assertIsNone(following)
                else:
                    self.assertIsNotNone(following)
                    self.assertEqual(following.group(1), SEQUENCE[index + 1])
                self.assertNotIn("next_anchor:", metadata)
        navigation = (ROOT / "_data/copilot_workshop.yml").read_text()
        slugs = [value.strip('"').rstrip("/") for value in
                 re.findall(r"^  slug: (.*)$", navigation, re.MULTILINE)]
        self.assertEqual(slugs[:len(SEQUENCE)], SEQUENCE)

    def test_parallel_prompts_are_inline_and_assigned_to_named_sessions(self):
        parallel = chapter("parallel")
        self.assertNotIn("{{ site.baseurl }}/prompts/#parallel", parallel)
        self.assertIn("**Copilot App UI**", parallel)
        self.assertIn("Both prompts are below", parallel)
        self.assertIn("Both sessions may edit the same files", parallel)
        self.assertNotIn("Only change src/main/resources/static/", parallel)
        self.assertNotIn("Only add CartBoundaryTest.java", parallel)
        for heading, prompt, name in [
                ("### Cart: empty-state UX", "Improve the empty-cart state",
                 "Cart: empty-state UX"),
                ("### Cart: boundary tests", "add CartBoundaryTest.java",
                 "Cart: boundary tests")]:
            section = parallel.split(heading, 1)[1].split("\n##", 1)[0]
            with self.subTest(session=heading):
                self.assertIn("Send this prompt to start it",
                              re.sub(r"\s+", " ", section))
                rename = f"Once the session has started, rename it **{name}**"
                self.assertIn(rename, section)
                self.assertLess(section.index("\n```\n"),
                                section.index(rename))
                self.assertNotIn(f"Select **{name}** in the App sidebar", section)
                self.assertIn(prompt, section)
                task = section.split("```copilot\n", 1)[1].split("```", 1)[0]
                self.assertNotIn("Fetch origin", task)
                self.assertNotIn("shared updated origin/main", task)
                self.assertTrue(task.startswith("Improve the empty-cart state")
                                if "UX" in heading else task.startswith("Use spring-boot-testing"))
                self.assertIn("Do not open or merge a PR yet", section)
        self.assertIn("Do not weaken an assertion", parallel)
        cards = chapter("prompts")
        for anchor in ["ui-worker", "test-worker"]:
            self.assertIn("{{ site.baseurl }}/parallel/#" + anchor, cards)

    def test_parallel_starts_from_merged_tasks_without_repeating_publication(self):
        parallel = chapter("parallel")
        prose = re.sub(r"\s+", " ", parallel)
        for text in [
                "The quantity, removal-and-Canvas and MCP PRs must be merged before continuing",
                "/tools/#publish-the-reviewed-result",
                "Use the updated **`main`** verified at the end",
                "**`main` as the base branch** for both",
                "Each session will work in its own worktree on a separate branch",
                "**`main` unchanged until its PR is merged**",
                "main not updated: local recovery used"]:
            with self.subTest(requirement=text):
                self.assertIn(text, prose)
        self.assertNotIn("If you already created the sessions from an older baseline", prose)
        self.assertNotIn("open one PR targeting main for the three completed tickets", prose)
        self.assertNotIn("push the reviewed changes to main", prose)
        introduction = parallel.split("## Create two sessions from main", 1)[1].split(
            "<figure>", 1)[0]
        self.assertNotIn("```copilot", introduction)
        self.assertNotIn("original workshop session", parallel)
        self.assertLessEqual(len(introduction.split()), 160)
        for path in HANDBOOK.glob("*.md"):
            with self.subTest(page=path.name):
                self.assertNotIn("workshop-complete", path.read_text())

    def test_mcp_publishes_and_verifies_a_pr_before_parallel_work(self):
        tools = re.sub(r"\s+", " ", chapter("tools"))
        publication = tools.split("## Publish the reviewed result", 1)[1].split(
            "## What you have learned", 1)[0]
        prompts = re.findall(r"```copilot (.*?)```", publication)
        self.assertEqual(len(prompts), 1)
        merge = prompts[0]
        for text in ["Before starting the next section",
                     "**New worktree** created a separate branch",
                     "Review **Changes**, then use **Create PR** in Copilot App",
                     "targeting **`main`** in **your own repository**",
                     "If the PR already exists, open it instead"]:
            with self.subTest(publication_instruction=text):
                self.assertIn(text, publication)
        setup = re.sub(r"\s+", " ", chapter("setup"))
        self.assertIn("separate branch starting from `main`; you are not editing `main` directly",
                      setup)
        for text in ["Merge this reviewed PR into main",
                     "only after all required checks and approvals pass",
                     "Do not bypass protections",
                     "PR as Merged and its merged-revision tests pass",
                     "Fetch origin/main", "QueryContractTest.java and all earlier tests",
                     "merged PR link and shared starting commit"]:
            with self.subTest(merge_requirement=text):
                self.assertIn(text, merge)
        self.assertIn("Review **Files changed**", publication)
        self.assertIn("**Do not create the parallel sessions until this handoff is verified.**",
                      publication)
        self.assertLess(tools.index("## Fix the N+1 query issue"),
                        tools.index("## Publish the reviewed result"))
        for slug in ["prompts", "worksheet", "facilitator", "finish"]:
            with self.subTest(surface=slug):
                self.assertIn("MCP handoff PR" if slug != "prompts"
                              else "/tools/#publish-the-reviewed-result", chapter(slug))

    def test_integration_uses_sequential_agent_merge_with_correct_target(self):
        integration = chapter("integrate")
        prose = re.sub(r"\s+", " ", integration)
        for text in [
                "**Both worker PRs target `main`.**",
                "## Open the two worker PRs",
                "## Merge the UI PR first",
                "{: #check-ui-merge}",
                "## Update and merge the test PR",
                "## Verify the combined application",
                "repairs and CI can run in parallel",
                "Keep merging disabled on both PRs during parallel preparation.",
                "**Done when:** the UI PR's status is **Merged**",
                "**all earlier reviewed tests plus the new boundary",
                "all required checks and approvals pass",
                "Do not reset main or this branch"]:
            with self.subTest(requirement=text):
                self.assertIn(text, prose)
        stages = ["## Open the two worker PRs", "## Merge the UI PR first",
                  "{: #check-ui-merge}", "## Update and merge the test PR",
                  "## Verify the combined application"]
        positions = [integration.index(stage) for stage in stages]
        self.assertEqual(positions, sorted(positions))
        self.assertNotIn("--no-ff", integration)

    def test_integration_explains_sessions_review_gates_and_remote_state(self):
        prose = re.sub(r"\s+", " ", chapter("integrate"))
        for text in [
                "Stay in **Cart: boundary tests**.",
                "**`base: main` ← `head: this session's branch`**",
                "review **Changes**, its preview or test results",
                "Leave **Merge pull request** unchecked",
                "check out the exact latest origin/main commit for verification",
                "Confirm the checked-out commit equals origin/main",
                "actual merged results, including squash merges",
                "fresh CI for its new revision",
                "may make further permitted repairs and merge without another review pause",
                "A denied permission",
                "If remote status is unavailable, mark it unknown"]:
            with self.subTest(requirement=text):
                self.assertIn(text, prose)
        ui = prose.split("## Merge the UI PR first", 1)[1].split(
            "## Update and merge the test PR", 1)[0]
        self.assertLess(ui.index("Leave **Merge pull request** unchecked"),
                        ui.index("enable **Merge pull request**"))
        self.assertLess(ui.index("Review **Files changed**, including repairs"),
                        ui.index("enable **Merge pull request**"))
        self.assertIn("authorization prompt for this PR only", ui)
        test = prose.split("## Update and merge the test PR", 1)[1].split(
            "## Verify the combined application", 1)[0]
        self.assertLess(test.index("**Merge pull request** still off"),
                        test.index("enable **Merge pull request**"))
        self.assertIn("**separate authorization for this PR**", test)
        self.assertIn("Authorize each PR separately", chapter("prompts"))
        self.assertIn("comparison starting point only", chapter("finish"))

    def test_integration_uses_app_actions_and_keeps_only_task_prompts(self):
        integration = chapter("integrate")
        normal = integration.split(
            '<details markdown="1" id="local-recovery">', 1)[0]
        visible = re.sub(r"<details\b.*?</details>", "", normal, flags=re.DOTALL)
        visible = visible.replace("{{ site.baseurl }}", "/github-copilot-app-java-workshop")
        self.assertLessEqual(len(visible.split()), 750)
        prompts = re.findall(r"```copilot\n(.*?)```", normal, re.DOTALL)
        self.assertEqual(len(prompts), 2)
        self.assertTrue(prompts[0].startswith("Update this boundary-test PR"))
        self.assertTrue(prompts[1].startswith("Confirm both worker PRs are Merged"))
        opening = normal.split("## Open the two worker PRs", 1)[1].split(
            "## Merge the UI PR first", 1)[0]
        for text in ["**Create PR** in Copilot App",
                     "**`main` in your own repository**",
                     "If the PR already exists, open it",
                     "the three earlier task PRs are already merged"]:
            self.assertIn(text, opening)
        self.assertNotIn("```copilot", opening)
        self.assertNotIn("PR creation prompt", chapter("prompts"))

    def test_agent_merge_reconciles_overlapping_changes_before_merge_approval(self):
        integration = re.sub(r"\s+", " ", chapter("integrate"))
        self.assertIn("sessions may have changed the same files", integration)
        self.assertNotIn("changed only their assigned files", integration)
        section = integration.split(
            "## Update and merge the test PR", 1)[1].split(
                "## Verify the combined application", 1)[0]
        for text in ["Keep repair-only Agent Merge running",
                     "**Merge pull request** still off",
                     "After the UI merge is verified",
                     "Earlier green checks do not verify the combined result",
                     "Resolve merge conflicts",
                     "preserving both workers' intended changes and tests",
                     "merging disabled while I review the conflict resolution",
                     "fresh CI for its new revision",
                     "Even conflict-free changes can interact incorrectly"]:
            with self.subTest(requirement=text):
                self.assertIn(text, section)
        self.assertLess(section.index("Review any conflict resolutions"),
                        section.index("enable **Merge pull request**"))

    def test_verification_and_recovery_reuse_the_test_worker_session(self):
        for path in HANDBOOK.glob("*.md"):
            with self.subTest(page=path.name):
                self.assertNotIn("Cart: integration", path.read_text())
        integration = chapter("integrate")
        self.assertNotIn("## Open a session", integration)
        recovery = re.sub(r"\s+", " ", integration.split(
            '<summary>Recovery:', 1)[1])
        for text in [
                "Stay in **Cart: boundary tests**",
                "merge origin/main into this test worker branch",
                "keeping its boundary tests",
                "do not replace it with starter main",
                "mark it unknown",
                "accounting for squash merges",
                "Do not merge the test branch into itself",
                "Skip the normal-path checkout of `origin/main`"]:
            with self.subTest(requirement=text):
                self.assertIn(text, recovery)

    def test_agent_merge_prerequisites_recovery_and_handoff_are_consistent(self):
        setup = chapter("setup")
        for text in ["GitHub Actions", "PRs", "Agent Merge",
                     "default settings", "ask the facilitator"]:
            self.assertIn(text, setup)
        self.assertIn("Agent Merge", chapter(""))
        self.assertIn("Do not let the workers open or merge PRs yet", chapter("parallel"))
        self.assertIn("## Integrate with Agent Merge", chapter("prompts"))
        for slug in ["integrate", "worksheet"]:
            with self.subTest(chapter=slug):
                self.assertIn("Agent Merge not completed: local recovery used", chapter(slug))
        recovery = chapter("integrate").split('<summary>Recovery:', 1)[1]
        self.assertIn("Disable Agent Merge in each worker session", recovery)
        self.assertIn("Do not push, merge remote PRs or enable Agent Merge", recovery)
        self.assertIn("**two worker PRs targeting `main`**", chapter("facilitator"))
        finish = chapter("finish")
        self.assertIn("both worker PR links", finish)
        self.assertIn("both worker PRs landed on **`main`**", finish)
        self.assertNotIn("## Optional GitHub delivery", finish)
        self.assertNotIn("No remote PR is required", finish)

    def test_checkout_delivery_reuses_agent_merge_under_scoped_approval(self):
        agents = re.sub(r"\s+", " ", chapter("subagents"))
        delivery = agents.split("## Deliver checkout into main", 1)[1].split(
            "## Verify the merged application", 1)[0]
        for text in [
                "one checkout PR", "not five specialist PRs or a new delivery session",
                "all five workers have finished and all reviewed handoffs are integrated",
                "The three task PRs, both worker PRs and any accepted critique corrections",
                "already be on your own `main`",
                "**Create PR**", "**Create PR → Agent Merge**",
                "**`base: main` ← `head: this session's branch`**",
                "repository, head and base match",
                "not the earlier merged boundary-test PR",
                "do not reopen earlier worker PRs or create duplicates",
                "Leave **Merge pull request** off",
                "Preserve all earlier and checkout tests",
                "ask before out-of-scope corrections or conflict resolutions",
                "review the integration and rerun the full suite",
                "**current PR head**", "Missing, skipped, queued or failed checks",
                "all required checks and approvals",
                "confirm the App's authorization prompt **for this checkout PR only**",
                "merge without another review pause",
                "If PR identity, review or check status cannot be verified",
                "stop with merging disabled",
                "checkout PR's actual status is **Merged**"]:
            with self.subTest(delivery_requirement=text):
                self.assertIn(text, delivery)
        self.assertLess(agents.index("Wait for my review before publishing or merging"),
                        agents.index("Select **Create PR**"))
        self.assertNotIn("```copilot", delivery)
        self.assertLess(delivery.index("Leave **Merge pull request** off"),
                        delivery.index("Then enable **Merge pull request**"))
        self.assertLess(delivery.index("**current PR head**"),
                        delivery.index("Then enable **Merge pull request**"))
        for slug in ["index", "finish", "worksheet", "facilitator", "prompts"]:
            with self.subTest(surface=slug):
                self.assertIn("checkout PR", chapter(slug))
                self.assertIn("Agent Merge", chapter(slug))
                self.assertNotIn("checkout PR is optional", chapter(slug))
        self.assertNotIn("checkout delivery prompt", chapter("prompts"))
        self.assertIn("Only the orchestrator may publish and merge", agents)
        self.assertIn("after separate explicit approval", agents)

    def test_checkout_verification_uses_merged_main_and_correct_running_copy(self):
        agents = re.sub(r"\s+", " ", chapter("subagents"))
        verification = agents.split("## Verify the merged application", 1)[1]
        for text in [
                "checkout PR is Merged", "exact merged revision on main",
                "latest origin/main commit", "accounting for squash merges",
                "stop without overwriting unfinished work",
                "detached verification checkout",
                "Do not move another worktree, reset branches, delete refs or edit",
                "checked-out commit equals origin/main",
                "If main has advanced", "passing checks for this revision too",
                "all earlier reviewed tests, boundary tests and new checkout tests",
                "absolute directory and shop URL",
                "Ctrl+C in its owning terminal", "Opening a canvas",
                "does not replace a running server",
                "app running from the verified main revision demonstrates checkout"]:
            with self.subTest(verification_requirement=text):
                self.assertIn(text, verification)
        self.assertLess(verification.index("stop without overwriting unfinished work"),
                        verification.index("Check out the exact latest origin/main"))
        self.assertIn("/subagents/#verify-merged-checkout", chapter("prompts"))

    def test_checkout_blockers_and_postdelivery_edits_are_not_silent_success(self):
        for slug in ["subagents", "finish", "worksheet", "facilitator"]:
            text = re.sub(r"\s+", " ", chapter(slug))
            for state in ["verified locally; delivery blocked",
                          "merged; post-merge verification blocked"]:
                with self.subTest(surface=slug, state=state):
                    self.assertIn(state, text)
        agents = re.sub(r"\s+", " ", chapter("subagents"))
        self.assertIn("Do not publish a recovered combined branch", agents)
        self.assertIn("Do not substitute a direct push or local merge", agents)
        self.assertIn("Turn off Agent Merge while blocked or before local recovery", agents)
        self.assertIn("bypass protections, force-push, broaden permissions or delete branches",
                      agents)
        tokens = re.sub(r"\s+", " ", chapter("tokens"))
        for text in ["Record it as a suggestion", "do not edit the verified main checkout",
                     "new follow-up feature branch",
                     "own review, publishing/merge approval, PR and verification"]:
            self.assertIn(text, tokens)
        finish = re.sub(r"\s+", " ", chapter("finish"))
        self.assertIn("new follow-up feature branch", finish)
        self.assertIn("reuse the merged checkout PR", finish)
        self.assertIn("do not create another commit just to finish", finish)

    def test_alternative_route_instructions_are_removed(self):
        paths = list(HANDBOOK.glob("*.md")) + [
            ROOT / "_layouts/default.html", ROOT / "_includes/copilot-workshop-nav.html"
        ]
        obsolete = re.compile(
            r"\b(?:one|two)[- ]hour\b|\b[12]h\b|one-hour-demo|extended-clinic|choose your route",
            re.IGNORECASE)
        for path in paths:
            with self.subTest(path=path.name):
                self.assertIsNone(obsolete.search(path.read_text()))


if __name__ == "__main__":
    unittest.main()
