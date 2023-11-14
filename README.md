# MINC and OBJ File Format Converter

[![Version](https://img.shields.io/docker/v/fnndsc/pl-mni2common?sort=semver)](https://hub.docker.com/r/fnndsc/pl-mni2common)
[![MIT License](https://img.shields.io/github/license/fnndsc/pl-mni2common)](https://github.com/FNNDSC/pl-mni2common/blob/main/LICENSE)
[![ci](https://github.com/FNNDSC/pl-mni2common/actions/workflows/ci.yml/badge.svg)](https://github.com/FNNDSC/pl-mni2common/actions/workflows/ci.yml)

`pl-mni2common` is a [_ChRIS_](https://chrisproject.org/)
_ds_ plugin wrapper around the programs
[mnc2nii](https://bic-mni.github.io/man-pages/man/mnc2nii.html)
and [mni2mz3](https://github.com/FNNDSC/mni2mz3).
It converts MINC volumes to NIFTI, surfaces to MZ3, and surface data to MZ3.
The output file formats NIFTI and MZ3 are convenient for visualization by [niivue](https://github.com/niivue/niivue).

## Local Usage

```shell
apptainer exec docker://ghcr.io/fnndsc/pl-mni2common:latest mni2common input/ output/
```
