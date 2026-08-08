#!/usr/bin/python

import os, glob, re

SRC_PATTERN = re.compile(
    r'(<img\s+loading="lazy"\s+src="[^"]*?)(=w\d+(?:-[^"=]*)?)("\s+width="(\d+)"\s*/>)'
)
EXPECTED_SUFFIX = lambda w: f"=w{w}-no"

TARGET_DIR = "travels"

def process(path):
    with open(path, "r") as f:
        contents = f.read()

    changes = 0
    inspected = 0
    already_ok = 0

    def repl(m):
        nonlocal changes, inspected, already_ok
        inspected += 1
        prefix, current_suffix, tail, width = m.group(1), m.group(2), m.group(3), m.group(4)
        expected = EXPECTED_SUFFIX(width)
        if current_suffix == expected:
            already_ok += 1
            return m.group(0)
        changes += 1
        return f"{prefix}{expected}{tail}"

    new_contents = SRC_PATTERN.sub(repl, contents)

    print(f"\n=== {path} ===")
    print(f"  Inspected: {inspected}")
    print(f"  Already correct: {already_ok}")
    print(f"  Changes: {changes}")

    if changes == 0:
        return inspected, already_ok, 0

    with open(path, "w") as f:
        f.write(new_contents)
    print(f"  Wrote {changes} change(s) to {path}")
    return inspected, already_ok, changes

if __name__ == "__main__":
    total_files = 0
    total_changes = 0
    total_inspected = 0
    total_ok = 0
    for path in sorted(glob.glob(os.path.join(TARGET_DIR, "**", "*.md"), recursive=True)):
        inspected, already_ok, changes = process(path)
        total_files += 1
        total_changes += changes
        total_inspected += inspected
        total_ok += already_ok
    print(f"\n--- TOTAL across {total_files} files: inspected={total_inspected}, already_ok={total_ok}, changes={total_changes} ---")
