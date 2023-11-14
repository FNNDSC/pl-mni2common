FROM docker.io/fnndsc/microminc-builder:latest as builder

RUN microminc.sh mnc2nii /microminc

FROM python:3.12.0-slim-bullseye
COPY --from=builder /microminc /opt/microminc
ENV PATH=/opt/microminc/bin:$PATH \
    LD_LIBRARY_PATH=/opt/microminc/lib:$LD_LIBRARY_PATH \
    MINC_FORCE_V2=1 MINC_COMPRESS=4 VOLUME_CACHE_THRESHOLD=-1 \
    MNI_DATAPATH=/opt/microminc/share
