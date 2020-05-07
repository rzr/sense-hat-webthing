#!/bin/echo docker build . -f
# -*- coding: utf-8 -*-
# SPDX-License-Identifier: MPL-2.0

FROM python:3.7-buster
LABEL maintainer="Philippe Coval (rzr@users.sf.net)"

ENV DEBIAN_FRONTEND noninteractive
ENV LC_ALL en_US.UTF-8
ENV LANG ${LC_ALL}

ENV project sense-hat-adapter
ENV workdir /root/.mozilla-iot/addons/${project}
ADD . ${workdir}

WORKDIR ${workdir}

RUN echo "# log: ${project}: Setup system" \
  && set -x \
  && apt-get clean \
  && apt-get update \
  && apt-get install -y \
    libjpeg-dev \
  && sync

RUN echo "# log: ${project}: Building package" \
  && set -x \
  && ./package.sh \
  && sync

WORKDIR ${workdir}
RUN echo "# log: ${project}: Distribute package" \
  && set -x \
  && install -d /usr/local/opt/${project}/dist \
  && install ${project}-*.tgz /usr/local/opt/${project}/dist \
  && tar tvfz /usr/local/opt/${project}/dist/${project}-*.tgz \
  && sha256sum /usr/local/opt/${project}/dist/* \
  && sync
