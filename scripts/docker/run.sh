#!/bin/sh


docker run --rm -it \
       -v $(pwd):/app/data \
       -w /app/data \
       wl/librarian \
       "$(basename "$0")" "$@" \
