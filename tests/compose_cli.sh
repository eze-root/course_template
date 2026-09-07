#!/bin/sh
# Let the regression test invoke real Compose after clearing COURSE_* variables.
exec sudo docker compose "$@"
