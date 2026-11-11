#!/usr/bin/env python3
"""Refresh complete skill directories from the workshop's immutable source."""
import hashlib
import io
import json
from pathlib import Path
import tarfile
from urllib.request import urlopen

ROOT = Path(__file__).resolve().parents[1]
PIN = "7e408815ddcb64889a3683799a85399331cfd4ef"
NAMES = ("java-junit", "java-hibernate-jpa", "spring-boot-testing")
DEST = ROOT / ".github/skills"


def main():
    url = f"https://codeload.github.com/github/awesome-copilot/tar.gz/{PIN}"
    with urlopen(url, timeout=60) as response:
        archive = response.read()
    files = {}
    with tarfile.open(fileobj=io.BytesIO(archive), mode="r:gz") as source:
        for member in source.getmembers():
            relative = Path(*Path(member.name).parts[1:])
            if not member.isfile():
                continue
            if relative == Path("LICENSE"):
                destination = DEST / "UPSTREAM-LICENSE"
            elif len(relative.parts) > 2 and relative.parts[0] == "skills" and relative.parts[1] in NAMES:
                destination = DEST / Path(*relative.parts[1:])
            else:
                continue
            data = source.extractfile(member).read()
            destination.parent.mkdir(parents=True, exist_ok=True)
            destination.write_bytes(data)
            files[str(destination.relative_to(DEST))] = hashlib.sha256(data).hexdigest()
    for name in NAMES:
        if not (DEST / name / "SKILL.md").is_file():
            raise RuntimeError(f"Missing skill {name}")
    manifest = {"repository": "github/awesome-copilot", "revision": PIN, "sha256": files}
    (DEST / "provenance.json").write_text(json.dumps(manifest, indent=2) + "\n")
    print(f"Vendored {len(files)} licensed files from {PIN}")


if __name__ == "__main__":
    main()
