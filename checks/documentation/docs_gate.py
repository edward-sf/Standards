"""Check documentation and ADRs in an immutable client Git revision."""
import argparse
import fnmatch
import re
import subprocess
import sys
from pathlib import PurePosixPath


def git(*args):
    return subprocess.check_output(["git", *args])


def paths(*args):
    return [p.decode("utf-8", "surrogateescape") for p in git(*args).split(b"\0") if p]


def contents(head, path):
    entry = git("ls-tree", "-z", head, "--", ":(literal)" + path)
    if not entry.startswith((b"100644 blob ", b"100755 blob ")):
        raise ValueError(f"{path}: expected a tracked regular file")
    data = git("show", f"{head}:{path}").decode("utf-8")
    if not data.strip():
        raise ValueError(f"{path}: empty document")
    return data


def sections(document):
    result = {}
    section = None
    fence = ""
    for line in document.splitlines():
        marker = re.match(r"^ {0,3}(`{3,}|~{3,})(.*)$", line)
        if fence:
            if marker and marker[1].startswith(fence) and not marker[2].strip():
                fence = ""
            continue
        if marker:
            fence = marker[1]
        elif line.startswith("## "):
            section = line[3:].strip()
            if section in result:
                raise ValueError(f"duplicate heading: {section}")
            result[section] = []
        elif section is not None:
            result[section].append(line)
    return {key: "\n".join(value).strip() for key, value in result.items()}


def check_adrs(head, directory):
    records = {}
    for path in paths("ls-tree", "-r", "-z", "--name-only", head, "--", directory):
        file = PurePosixPath(path)
        if str(file.parent) != directory or file.suffix != ".md":
            continue
        fields = sections(contents(head, path))
        for label in ("Status", "Context", "Alternatives", "Decision", "Consequences"):
            if not fields.get(label):
                raise ValueError(f"{path}: missing or empty {label}")
        if fields["Status"] not in {"Proposed", "Accepted", "Rejected", "Superseded"}:
            raise ValueError(f"{path}: unexpected status")
        records[file.name] = fields
    for origin, fields in records.items():
        if fields["Status"] != "Superseded":
            continue
        seen = {origin}
        while fields["Status"] == "Superseded":
            target = fields.get("Superseded by", "")
            if target not in records or target in seen:
                raise ValueError(f"{origin}: missing or cyclic successor")
            seen.add(target)
            fields = records[target]
        if fields["Status"] != "Accepted":
            raise ValueError(f"{origin}: successor chain must end at an accepted record")


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("base")
    parser.add_argument("candidate")
    for option in ("readme", "api-doc", "changelog", "adr-dir"):
        parser.add_argument("--" + option, required=True)
    parser.add_argument("--api-pattern", action="append", required=True)
    args = parser.parse_args()
    try:
        base, head = [git("rev-parse", "--verify", "--end-of-options", rev + "^{commit}").decode().strip()
                      for rev in (args.base, args.candidate)]
        documents = (args.readme, args.api_doc, args.changelog)
        if len(set(documents)) != len(documents):
            raise ValueError("configure distinct README, reference and changelog files")
        for path in documents:
            contents(head, path)
        ancestor = git("merge-base", base, head).decode().strip()
        changed = set(paths("diff", "--no-renames", "--name-only", "-z", ancestor, head, "--"))
        if any(fnmatch.fnmatchcase(p, pattern) for p in changed for pattern in args.api_pattern):
            missing = set()
            for path in (args.api_doc, args.changelog):
                old = git("ls-tree", ancestor, "--", ":(literal)" + path).split(b"\t", 1)[0].split()
                if old and old[2].decode() == git("rev-parse", f"{head}:{path}").decode().strip():
                    missing.add(path)
            if missing:
                raise ValueError("public contract changed: update " + ", ".join(sorted(missing)))
        directory = str(PurePosixPath(args.adr_dir))
        old_records = paths("ls-tree", "-r", "-z", "--name-only", ancestor, "--", directory)
        for path in old_records:
            file = PurePosixPath(path)
            if file.suffix == ".md" and str(file.parent) == directory:
                contents(head, path)
        check_adrs(head, directory)
    except (OSError, ValueError, subprocess.CalledProcessError) as error:
        sys.exit(f"documentation rejected: {error}")


if __name__ == "__main__":
    main()
