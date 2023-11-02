FROM docker.io/fnndsc/microminc-builder:latest as builder

RUN microminc.sh mnc2nii /microminc

FROM ghcr.io/mamba-org/micromamba:1.5.1-bookworm-slim
COPY --from=builder /microminc /opt/microminc
ENV PATH=/opt/conda/bin:/opt/microminc/bin:$PATH \
    LD_LIBRARY_PATH=/opt/microminc/lib:$LD_LIBRARY_PATH \
    MINC_FORCE_V2=1 MINC_COMPRESS=4 VOLUME_CACHE_THRESHOLD=-1 \
    MNI_DATAPATH=/opt/microminc/share
