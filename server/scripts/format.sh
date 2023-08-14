#!/bin/sh -e
set -x

autoflake --remove-all-unused-imports --recursive --remove-unused-variables --in-place /server/backend/ --exclude=__init__.py
black /server/backend/
isort /server/backend/
