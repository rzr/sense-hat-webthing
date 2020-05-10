#!/bin/make -f
# -*- makefile -*-
# SPDX-License-Identifier: MPL-2.0

default: help all

project ?= sense-hat-adapter
addons_url ?= https://github.com/mozilla-iot/addon-list
addons_dir ?= tmp/addon-list
addons_json ?= ${addons_dir}/addons/sense-hat-adapter.json


help:
	@echo "## Usage: "
	@echo "# make prep # To install dev deps"
	@echo "# make start # To start adapter"
	@echo "# make unprep # To remove dev deps"
	@echo "# make rule/version/X.Y.Z # To update manifest"
	@echo "# make rule/version/X.Y.Z # To update addon-list"

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


rule/release/%: ${addons_json} rule/version/%
	sed -e "s|\(\"version\":\) .*|\1 \"${@F}\"|g" -i $<
	sed -e "s|\(.*/${project}-\)\([0-9.]*\)\(-.*\)|\1${@F}\3|g" -i $<
	cd ${<D} \
&& git --no-pager diff \
&& git commit -am "${project}: Update to ${@F}"

${addons_json}:
	mkdir -p "${addons_dir}"
	git clone --depth 1 ${addons_url} "${addons_dir}"
