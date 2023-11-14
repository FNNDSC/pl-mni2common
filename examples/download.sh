#!/bin/bash

HERE="$(dirname "$(readlink -f "$0")")"

urls=(
  https://github.com/aces/CIVET/raw/9818b3cbe8308249e7c373ef1a2a53956512143e/models/colin/colin_white_mc_mask_left.txt
  https://github.com/aces/CIVET/raw/9818b3cbe8308249e7c373ef1a2a53956512143e/models/colin/colin_white_mc_mask_right.txt
  https://github.com/aces/CIVET/raw/9818b3cbe8308249e7c373ef1a2a53956512143e/models/colin/colin_white_mc_left.obj
  https://github.com/aces/CIVET/raw/9818b3cbe8308249e7c373ef1a2a53956512143e/models/colin/colin_white_mc_right.obj
  https://github.com/aces/mni-models_colin27-lin/raw/60787485e2ed4e012bda4da8fc2b163384fc3431/colin27_t1_tal_lin.mnc.gz
  https://github.com/aces/mni-models_colin27-lin/raw/60787485e2ed4e012bda4da8fc2b163384fc3431/colin27_t1_tal_lin_headmask.mnc.gz
  https://github.com/aces/mni-models_colin27-lin/raw/60787485e2ed4e012bda4da8fc2b163384fc3431/colin27_t1_tal_lin_mask.mnc.gz
)

set -ex

cd "$HERE"
mkdir -v incoming
cd incoming

parallel wget -q ::: ${urls[@]}
find -type f -name '*.gz' | parallel gzip -d
