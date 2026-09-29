#!/usr/bin/env bash
set -e

pip list --outdated --format=json \ # gather the list of outdated packages
  | python3 -c 'import json, sys; print(*[p["name"] for p in json.load(sys.stdin)])' \ # get 'name'
  | xargs -r pip install -U # hand the names over to the update command

