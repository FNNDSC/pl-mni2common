#!/usr/bin/env python
import os
import shutil
import sys
import logging
import shlex
import subprocess as sp
from pathlib import Path
from argparse import ArgumentParser, Namespace, ArgumentDefaultsHelpFormatter
from tqdm.contrib.concurrent import thread_map
from tqdm.contrib.logging import logging_redirect_tqdm
from bicpl import PolygonObj, WavefrontObj

from chris_plugin import chris_plugin, PathMapper

__version__ = '1.0.0'

DISPLAY_TITLE = r"""
       _                        _  _____                                           
      | |                      (_)/ __  \                                          
 _ __ | |______ _ __ ___  _ __  _ `' / /' ___ ___  _ __ ___  _ __ ___   ___  _ __  
| '_ \| |______| '_ ` _ \| '_ \| |  / /  / __/ _ \| '_ ` _ \| '_ ` _ \ / _ \| '_ \ 
| |_) | |      | | | | | | | | | |./ /__| (_| (_) | | | | | | | | | | | (_) | | | |
| .__/|_|      |_| |_| |_|_| |_|_|\_____/\___\___/|_| |_| |_|_| |_| |_|\___/|_| |_|
| |                                                                                
|_|                                                                                
"""


parser = ArgumentParser(description='Convert MINC and .obj to NIFTI and Wavefront respectively',
                        formatter_class=ArgumentDefaultsHelpFormatter)
parser.add_argument('-p', '--pattern', default='**/*', type=str,
                    help='Path filter')
parser.add_argument('-J', '--threads', type=int,
                    help='Number of threads to use')
parser.add_argument('-V', '--version', action='version',
                    version=f'%(prog)s {__version__}')

LOG = logging.getLogger(__name__)


@chris_plugin(
    parser=parser,
    title='MINC and OBJ File Format Converter',
    category='MRI',              # ref. https://chrisstore.co/plugins
    min_memory_limit='512Mi',    # supported units: Mi, Gi
    min_cpu_limit='1000m',       # millicores, e.g. "1000m" = 1 CPU core
    min_gpu_limit=0              # set min_gpu_limit=1 to enable GPU
)
def main(options: Namespace, inputdir: Path, outputdir: Path):
    print(DISPLAY_TITLE, flush=True)

    mapper = PathMapper.file_mapper(inputdir, outputdir, glob=options.pattern)
    nproc = options.threads if options.threads else len(os.sched_getaffinity(0))
    with logging_redirect_tqdm():
        results = thread_map(convert_file, mapper, max_workers=nproc, total=mapper.count(), maxinterval=0.1)
    if not all(results):
        sys.exit(1)


def convert_file(file_pair: tuple[Path, Path]) -> bool:
    input_file, output_file = file_pair
    if input_file.suffix == '.mnc':
        return convert_minc(input_file, output_file.with_suffix('.nii'))
    elif input_file.suffix == '.obj':
        return convert_obj(input_file, output_file.with_suffix('.wf.obj'))
    shutil.copy2(input_file, output_file)
    return True


def convert_minc(mnc, nii) -> bool:
    log_file = nii.with_suffix('.mnc2nii.log')
    cmd = ('mnc2nii', str(mnc), str(nii))
    with log_file.open('wb') as log_handle:
        proc = sp.run(cmd, stderr=log_handle, stdout=log_handle)
    if proc.returncode == 0:
        return True
    LOG.error(f'Command failed: {shlex.join(cmd)} > {log_file}')
    return False


def convert_obj(mniobj_path, wavefront_path) -> bool:
    try:
        obj = PolygonObj.from_file(mniobj_path)
        wf = WavefrontObj.from_mni(obj)
        with wavefront_path.open('w') as f:
            wf.write_to(f)
        return True
    except Exception as e:
        LOG.error(str(e))
        return False


if __name__ == '__main__':
    logging.basicConfig(level=logging.WARNING)
    main()
