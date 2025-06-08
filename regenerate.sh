#!/usr/bin/env bash
count=1
until yes '' | ~/.python/bin/python Generate.py --skip_prog_balancing; do
  count=$((count + 1))
  echo Restarting, attempt $count
  sleep 1
done
echo Successfully Generated after $count tries
