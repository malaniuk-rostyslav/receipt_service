#!/usr/bin/env bash

set -e
set -x

pytest --cov=/server/backend/ --cov-report=term-missing /server/backend/tests/ "${@}"
