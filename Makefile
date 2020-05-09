#!/bin/make -f
# -*- makefile -*-
# SPDX-License-Identifier: MPL-2.0

default: help all

project ?= sense-hat-adapter

help:
	@echo "## Usage: "
	@echo "# make prep # To install dev deps"
	@echo "# make start # To start adapter"
	@echo "# make unprep # To remove dev deps"
	@echo "# make rule/version/X.Y.Z"

start: main.py
	${<D}/${<F}

prep: setup.sh
	${<D}/${<F}

unprep: /etc/debian_version
	sudo apt-get remove -y \
  libblas3 libgfortran5 libimagequant0 liblapack3 liblcms2-2 librtimulib-utils \
  librtimulib7 libwebpdemux2 \
  python3-numpy python3-olefile python3-pil  python3-rtimulib python3-sense-hat


rule/version/%: manifest.json package.json setup.py
	-git describe --tags
	sed -e "s|\(\"version\":\) .*|\1 \"${@F}\"|g" -i $<
	sed -e "s|\(\"version\":\) .*|\1 \"${@F}\",|g" -i package.json
	sed -e "s|\(.*version='\).*\('.*\)|\1${@F}\2|g" -i setup.py
	-git commit -sm "Release ${@F}" $^
	-git tag -sam "${project}-${@F}" "v${@F}" \
|| git tag -am "${project}-${@F}" "v${@F}"
