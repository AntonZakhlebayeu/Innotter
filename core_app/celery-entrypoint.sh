#!/bin/bash

set -o errexit
set -o nounset

celery -A core_app worker --loglevel=INFO