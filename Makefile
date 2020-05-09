#!/bin/make -f
# -*- makefile -*-
# SPDX-License-Identifier: MPL-2.0

default: help all

project ?= sense-hat-adapter

help:
	@echo "## Usage: "
	@echo "# make rule/version/X.Y.Z"

rule/version/%: manifest.json package.json setup.py
	-git describe --tags
	sed -e "s|\(\"version\":\) .*|\1 \"${@F}\"|g" -i $<
	sed -e "s|\(\"version\":\) .*|\1 \"${@F}\",|g" -i package.json
	sed -e "s|\(.*version='\).*\('.*\)|\1${@F}\2|g" -i setup.py
	-git commit -sm "Release ${@F}" $^
	-git tag -sam "${project}-${@F}" "v${@F}" \
|| git tag -am "${project}-${@F}" "v${@F}"
