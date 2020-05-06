#!/bin/bash -e
# -*- mode: Bash; tab-width: 2; indent-tabs-mode: t; -*-
# SPDX-License-Indentifier: MPL-2.0

package="sense-hat-adapter"
version=$(grep '"version":' manifest.json | cut -d: -f2 | cut -d\" -f2)
date=$(git log -1 --date=short --pretty=format:%cd || date -u)

if [ -z "${ADDON_ARCH}" ]; then
  TARFILE_SUFFIX=
else
  PYTHON_VERSION="$(python3 --version 2>&1 | cut -d' ' -f2 | cut -d. -f 1-2)"
  TARFILE_SUFFIX="-${ADDON_ARCH}-v${PYTHON_VERSION}"
fi

# Clean up from previous releases
rm -rf *.tgz package SHA256SUMS lib

# Prep new package
mkdir package lib

# Pull down Python dependencies
pip3 install -r requirements.txt -t lib --no-binary :all: --prefix ""

# Put package together
cp -r \
	 lib pkg LICENSE *.json *.py *.sh README.md \
	 package/
find package -type f -name '*.pyc' -delete
find package -type d -empty -delete

# Generate checksums
cd package
find . -type f \! -name SHA256SUMS -exec shasum --algorithm 256 {} \; >> SHA256SUMS
cd -

# Make the tarball
TARFILE="${package}-${version}${TARFILE_SUFFIX}.tgz"
GZIP="-n" tar czf "${TARFILE}" --mtime="${date}" package

shasum --algorithm 256 "${TARFILE}" > "${TARFILE}.sha256sum"

rm -rf SHA256SUMS package
