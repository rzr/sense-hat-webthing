#!/bin/echo docker build . -f
# -*- coding: utf-8 -*-
# SPDX-License-Identifier: MPL-2.0

FROM mozillaiot/gateway:latest
LABEL maintainer="Philippe Coval (rzr@users.sf.net)"

ENV DEBIAN_FRONTEND noninteractive
ENV LC_ALL en_US.UTF-8
ENV LANG ${LC_ALL}

ENV project sense-hat-webthing

ADD . /root/.mozilla-iot/addons/${project}
WORKDIR /root/.mozilla-iot/addons/${project}

RUN echo "#log: ${project}: Building package" \
  && set -x \
  && ./package.sh \
  && sync

WORKDIR /root/.mozilla-iot/addons/${project}
RUN echo "#log: ${project}: Installing sources" \
  && set -x \
  && install -d /usr/local/opt/${project}/dist \
  && install ${project}-*.tgz /usr/local/opt/${project}/dist \
  && sha256sum /usr/local/opt/${project}/dist/* \
  && sync
