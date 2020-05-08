#!/bin/bash
# -*- mode: Bash; tab-width: 2; indent-tabs-mode: t; -*-
# SPDX-License-Indentifier: MPL-2.0

main="sense-hat-single-thing.py"
dir=$(readlink -f $(dirname "$0"))
cd "${dir}"
libdir="lib"

declare -a opts=(
 "--install-option=--prefix="\
 "--target="${libdir}""\
 "--requirement=requirements.txt"
)

[ ! -f /etc/debian_version ] || opts+=("--system")
[ -d lib ] ||  pip3 install "${opts[@]}"

PYTHONPATH=./lib \
          python3 "${main}"
