"""Check attribution and public Git metadata before publishing."""
import argparse
import json
import re
import subprocess
import sys
from pathlib import Path


PROHIBITED_NAMES = (
    "cla" "ude", "anthro" "pic", "co" "dex", "open" "ai",
    "chat" "gpt", "co" "pilot", "gem" "ini",
)
NAME_PATTERN = re.compile("|".join(PROHIBITED_NAMES), re.IGNORECASE)


def prohibited(value):
    return NAME_PATTERN.search(value) or re.search(r"(?<![a-zA-Z])AI(?![a-zA-Z])", value)


def check(label, value):
    if prohibited(value):
        print(f"Publication policy violation in {label}.", file=sys.stderr)
        return False
    return True


def git(*args):
    return subprocess.check_output(["git", *args], encoding="utf-8", errors="replace")


def history(revision):
    records = git("log", "-z", "--format=%H%x00%an%x00%ae%x00%cn%x00%ce%x00%B", revision).split("\0")
    results = [check(f"commit {records[i][:12]}", "\n".join(records[i + 1:i + 6]))
               for i in range(0, len(records) - 1, 6)]
    return all(results)


def push_history(before, after):
    # A new ref or a force push can have no locally available previous tip.
    found = subprocess.run(["git", "cat-file", "-e", before], stderr=subprocess.DEVNULL)
    return history(f"{before}..{after}" if found.returncode == 0 else after)


def check_push():
    valid = True
    for line in sys.stdin:
        _, local, remote_ref, remote = line.split()
        if set(local) == {"0"}:
            continue
        valid &= check("destination ref", remote_ref)
        valid &= push_history(remote, local)
    return valid


def check_event(path):
    event = json.loads(path.read_text(encoding="utf-8"))
    if "pull_request" in event:
        pr = event["pull_request"]
        values = {"PR title": pr["title"], "PR body": pr.get("body") or "",
                  "source branch": pr["head"]["ref"], "target branch": pr["base"]["ref"]}
        valid = all([check(label, value) for label, value in values.items()])
        return history(f"{pr['base']['sha']}..{pr['head']['sha']}") and valid
    after, before = event["after"], event["before"]
    if set(after) == {"0"}:
        return True
    valid = check("destination ref", event["ref"])
    return push_history(before, after) and valid


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    checks = parser.add_mutually_exclusive_group(required=True)
    checks.add_argument("--message", type=Path)
    checks.add_argument("--event", type=Path)
    checks.add_argument("--history")
    checks.add_argument("--text")
    checks.add_argument("--pre-push", action="store_true")
    args = parser.parse_args()
    if args.message is not None:
        valid = check("commit message", args.message.read_text(encoding="utf-8"))
        valid &= check("local branch", git("rev-parse", "--abbrev-ref", "HEAD"))
        for identity in ("GIT_AUTHOR_IDENT", "GIT_COMMITTER_IDENT"):
            valid &= check(identity, git("var", identity))
    elif args.event is not None:
        valid = check_event(args.event)
    elif args.history is not None:
        valid = history(args.history)
    elif args.text is not None:
        valid = check("supplied text", args.text)
    else:
        valid = check_push()
    return 0 if valid else 1


if __name__ == "__main__":
    sys.exit(main())
