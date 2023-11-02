FROM docker.io/fnndsc/pl-mni2common:base-1

LABEL org.opencontainers.image.authors="FNNDSC <dev@babyMRI.org>" \
      org.opencontainers.image.title="pl-mnc2common" \
      org.opencontainers.image.description="A ChRIS plugin to convert MINC volume and MNI .obj surface file formats to NIFTI and Wavefront OBJ respectively."

# use micromamba to install binary python dependencies for multiarch build
RUN \
    --mount=type=cache,sharing=private,target=/home/mambauser/.mamba/pkgs,uid=57439,gid=57439 \
    --mount=type=cache,sharing=private,target=/opt/conda/pkgs,uid=57439,gid=57439 \
    micromamba install -y -n base -c conda-forge python=3.11.5 numpy=1.26.0

ARG SRCDIR=/usr/local/src/pl-mni2common
WORKDIR ${SRCDIR}

COPY --chown=57439:57439 requirements.txt .
RUN --mount=type=cache,sharing=private,target=/home/mambauser/.cache/pip,uid=57439,gid=57439 \
    pip install -r requirements.txt

COPY --chown=mambauser:mambauser . .
ARG extras_require=none
RUN pip install ".[${extras_require}]" \
    && cd / && rm -rf ${SRCDIR}/*
WORKDIR /

CMD ["mni2common"]
