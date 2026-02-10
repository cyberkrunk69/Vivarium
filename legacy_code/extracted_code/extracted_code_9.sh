#!/bin/sh
pytest || { echo "Tests failed – aborting push"; exit 1; }