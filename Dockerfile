FROM docker.io/fnndsc/pl-mni2common:base-2 AS base

FROM base AS mni2mz3-installer

RUN apt-get update \
    && apt-get install -y curl

RUN curl --proto '=https' --tlsv1.2 -LsSf 'https://github.com/FNNDSC/mni2mz3/releases/download/v1.0.0-rc.5/installer.sh' | bash

FROM base

LABEL org.opencontainers.image.authors="Jennings.Zhang <jennings.zhang@childrens.harvard.edu>" \
      org.opencontainers.image.title="pl-mnc2common" \
      org.opencontainers.image.description="A ChRIS plugin to convert MINC volume, .txt surface data, and MNI .obj surface file formats to NIFTI and MZ3."

ARG SRCDIR=/usr/local/src/pl-mni2common
WORKDIR ${SRCDIR}

COPY . .
ARG extras_require=none
RUN pip install ".[${extras_require}]" \
    && cd / && rm -rf ${SRCDIR}/*
WORKDIR /

COPY --from=mni2mz3-installer /usr/local/bin/mni2mz3 /usr/local/bin/mni2mz3

CMD ["mni2common"]
