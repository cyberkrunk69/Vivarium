#!/usr/bin/env python3
import sys, re

pattern = r'^(feat|fix|docs|style|refactor|test|chore)(\([^\)]+\))?: .{10,}$'
msg = open(sys.argv[1]).read().strip()

if not re.match(pattern, msg):
    sys.stderr.write("ERROR: Commit message does not follow Conventional Commits format.\n")
    sys.exit(1)