#!/usr/bin/env python3
"""Verify exact red/green contracts in immutable Git checkpoint worktrees."""
import hashlib
import json
from pathlib import Path
import re
import subprocess
import tempfile
import xml.etree.ElementTree as ET

ROOT = Path(__file__).resolve().parents[1]
OUTPUT = ROOT / "target/checkpoint-checks"
TESTS = Path("src/test/java/com/juliendubois/workshop")
STAGES = ("start", "bugfix", "feature", "performance")
CONTRACTS = ("CartContractTest", "RemoveContractTest", "QueryContractTest")


def activate(project, name, contracts):
    (project / TESTS / f"{name}.java").write_bytes(contracts[name])


def load_contracts(revision):
    verify_revision(revision, revision)
    contracts = {}
    for name in CONTRACTS:
        path = f"teaching/{name}.java"
        result = subprocess.run(
            ["git", "-C", str(ROOT), "show", f"{revision}:{path}"],
            capture_output=True, check=False)
        if result.returncode:
            raise RuntimeError(f"Cannot read pinned reference contract {revision}:{path}: "
                               f"{result.stderr.decode().strip()}")
        contracts[name] = result.stdout
    return contracts


def check(project, names, expected_tests, expected_failures=None):
    expected_failures = expected_failures or {}
    log = OUTPUT / f"{project.name}-{'-'.join(names)}.log"
    with log.open("w") as stream:
        result = subprocess.run(
            ["./mvnw", "-q", f"-Dtest={','.join(names)}", "test"],
            cwd=project, stdout=stream, stderr=subprocess.STDOUT, check=False)
    tests = errors = skipped = 0
    failures = {}
    for name in names:
        report = project / "target/surefire-reports" / f"TEST-com.juliendubois.workshop.{name}.xml"
        if not report.exists():
            raise RuntimeError(f"Missing test report; see {log}")
        suite = ET.parse(report).getroot()
        tests += int(suite.attrib["tests"])
        errors += int(suite.attrib["errors"])
        skipped += int(suite.attrib["skipped"])
        for case in suite.findall("testcase"):
            failure = case.find("failure")
            if failure is not None:
                if failure.attrib.get("type") != "org.opentest4j.AssertionFailedError":
                    raise RuntimeError(f"Not an intended assertion failure; see {log}")
                failures[f"{name}.{case.attrib['name']}"] = failure.attrib.get("message", "")
    if (tests, errors, skipped) != (expected_tests, 0, 0) or failures.keys() != expected_failures.keys():
        raise RuntimeError(f"{project.name}: unexpected result; see {log}")
    for name, fragments in expected_failures.items():
        if not all(fragment in failures[name] for fragment in fragments):
            raise RuntimeError(f"{name}: wrong assertion failed; see {log}")
    if (result.returncode == 0) != (len(expected_failures) == 0):
        raise RuntimeError(f"{project.name}: unexpected Maven exit; see {log}")
    print(f"{project.name}: {tests} executed, {len(failures)} intended assertion failures, no errors/skips", flush=True)
    return {"checkpoint": project.name, "tests": tests, "expectedAssertionFailures": list(failures)}


def git(*args):
    return subprocess.check_output(["git", "-C", str(ROOT), *args], text=True).strip()


def verify_revision(ref, expected):
    if not isinstance(expected, str) or re.fullmatch(r"[0-9a-f]{40}", expected) is None:
        raise RuntimeError(f"Invalid expected commit SHA in checkpoint pins: {ref}")
    result = subprocess.run(
        ["git", "-C", str(ROOT), "rev-parse", "--verify", f"{ref}^{{commit}}"],
        text=True, capture_output=True, check=False)
    if result.returncode:
        raise RuntimeError(f"Missing published ref {ref}; fetch all checkpoint tags and reference branches")
    actual = result.stdout.strip()
    if actual != expected:
        raise RuntimeError(f"Published ref moved: {ref}: expected {expected}, found {actual}")


def verify_pins():
    pins = json.loads((ROOT / "tools/checkpoint-pins.json").read_text())
    for tag, expected in pins["checkpoints"].items():
        verify_revision(f"refs/tags/{tag}", expected)
    for branch, expected in pins["references"].items():
        refs = [ref for ref in (f"refs/heads/{branch}", f"refs/remotes/origin/{branch}")
                if subprocess.run(["git", "-C", str(ROOT), "show-ref", "--verify", "--quiet", ref],
                                  check=False).returncode == 0]
        if not refs:
            raise RuntimeError(f"Missing published reference branch {branch}; fetch reference branches")
        for ref in refs:
            verify_revision(ref, expected)
    for stage in STAGES:
        tag = f"{pins['edition']}-{stage}"
        if tag not in pins["checkpoints"]:
            raise RuntimeError(f"Missing active checkpoint pin: {tag}")
    return pins


def main():
    OUTPUT.mkdir(parents=True, exist_ok=True)
    (OUTPUT / "manifest.json").unlink(missing_ok=True)
    pins = verify_pins()
    contracts = load_contracts(pins["contractSourceRevision"])
    checks = []
    revisions = {}
    with tempfile.TemporaryDirectory(prefix="cart-checkpoints-") as directory:
        projects = {}
        try:
            for stage in STAGES:
                tag = f"{pins['edition']}-{stage}"
                revision = pins["checkpoints"][tag]
                project = Path(directory) / tag
                subprocess.run(["git", "-C", str(ROOT), "worktree", "add", "--detach",
                                str(project), revision], check=True, stdout=subprocess.DEVNULL)
                projects[stage] = project
                revisions[tag] = revision
                provenance = json.loads((project / ".github/skills/provenance.json").read_text())
                for name, digest in provenance["sha256"].items():
                    if hashlib.sha256((project / ".github/skills" / name).read_bytes()).hexdigest() != digest:
                        raise RuntimeError(f"Skill provenance mismatch: {tag}/{name}")
                for name in CONTRACTS:
                    teaching = project / "teaching" / f"{name}.java"
                    if teaching.read_bytes() != contracts[name]:
                        raise RuntimeError(f"Teaching test changed between checkpoints: {tag}/{name}")
                    activated = project / TESTS / f"{name}.java"
                    if activated.exists() and activated.read_bytes() != teaching.read_bytes():
                        raise RuntimeError(f"Acceptance test changed: {tag}/{name}")

            start, fixed, feature, optimized = (projects[stage] for stage in STAGES)
            checks.append(check(start, ["BaselineTest"], 4))
            activate(start, "CartContractTest", contracts)
            checks.append(check(start, ["CartContractTest"], 3, {
                "CartContractTest.repeatedAddIncrementsQuantityAndTotal": ("expected: 2", "but was: 1"),
                "CartContractTest.addingSeveralUnitsKeepsOneLine": ("expected: 5000", "but was: 2000"),
            }))
            checks.append(check(fixed, ["BaselineTest", "CartContractTest"], 7))
            activate(fixed, "RemoveContractTest", contracts)
            checks.append(check(fixed, ["RemoveContractTest"], 3, {
                "RemoveContractTest.removingTheLastItemReturnsAnEmptyCart": ("expected: 200", "but was: 404"),
                "RemoveContractTest.removingOneProductPreservesOtherLinesAndTotals": ("expected: 200", "but was: 404"),
            }))
            combined = ["BaselineTest", "CartContractTest", "RemoveContractTest"]
            checks.append(check(feature, combined, 10))
            activate(feature, "QueryContractTest", contracts)
            checks.append(check(feature, ["QueryContractTest"], 2, {
                "QueryContractTest.eightDistinctProductsUseOneSelect": ("expected: 1", "but was: 9"),
                "QueryContractTest.doublingTheCartDoesNotGrowTheSelectBudget": ("expected: 1", "but was: 17"),
            }))
            checks.append(check(optimized, combined + ["QueryContractTest"], 12))
        finally:
            for project in projects.values():
                subprocess.run(["git", "-C", str(ROOT), "worktree", "remove", "--force", str(project)], check=True)
    (OUTPUT / "manifest.json").write_text(json.dumps({
        "edition": pins["edition"], "verifierRevision": git("rev-parse", "HEAD"),
        "pins": pins, "revisions": revisions, "checks": checks
    }, indent=2) + "\n")


if __name__ == "__main__":
    main()
