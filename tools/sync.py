#!/usr/bin/env python3
"""The one-way copy from the project, now `tools/hub.py sync`, which also brings the hub's changes back.

Kept so that the schedules and notes that still name tools/sync.py keep working: it says in one
line that hub.py replaced it, then runs `hub.py sync` with the same flags.

    python3 tools/sync.py [--source DIR] [--memory DIR] [--commit] [--push] [--trailer 'Key: value']...
"""
import os
import sys

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import hub  # noqa: E402


if __name__ == "__main__":
    print("tools/sync.py is replaced by tools/hub.py: running `hub.py sync` with the same flags", flush=True)
    sys.exit(hub.main(["sync"] + sys.argv[1:]))
