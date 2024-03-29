#!/usr/bin/env python

# =============================================================================================
# DeepFinder - a deep learning approach to localize macromolecules in cryo electron tomograms
# =============================================================================================
# Copyright (C) Inria,  Emmanuel Moebel, Charles Kervrann, All Rights Reserved, 2015-2021, v1.0
# License: GPL v3.0. See <https://www.gnu.org/licenses/>
# =============================================================================================

import os
import sys
from os.path import dirname, abspath, join, basename
import argparse


def main():
    # Set deepfindHome to the location of this file
    deepfindHome = dirname(abspath(__file__))
    deepfindHome = os.path.split(deepfindHome)[0] + '/'
    sys.path.append(deepfindHome)

    # Define arguments:
    parser = argparse.ArgumentParser(description='Segment a tomogram.')
    parser.add_argument('-t', action='store', dest='path_tomo', help='path to tomogram')
    parser.add_argument('-w', action='store', dest='path_weights', help='path to network weights')
    parser.add_argument('-c', action='store', dest='nclass', type=int, help='number of classes')
    parser.add_argument('-p', action='store', dest='psize', type=int, help='patch size, must be multiple of 4')
    parser.add_argument('-o', action='store', dest='path_output', help='output path')
    parser.add_argument('-bin', action='store_true', help='bin resulting segmentation')
    args = parser.parse_args()

    no_args = args.path_tomo == None and args.path_weights == None and args.nclass == None and args.psize == None and args.path_output == None
    incomplete_args = args.path_tomo == None or args.path_weights == None or args.nclass == None or args.psize == None or args.path_output == None

    if no_args:  # if no args are passed, then open GUI
        gui_folder = 'pyqt.segment.'
        gui_script = 'gui_segment'

        cmd = 'python -m ' + 'deepfinder.' + gui_folder+gui_script
        os.system(cmd)
    elif incomplete_args:
        print('DeepFinder message: an argument is missing. All arguments need to be addressed: -t, -w, -c, -p, -o')
    else:
        from deepfinder.utils import smap as sm
        from deepfinder.inference import Segment
        import deepfinder.utils.common as cm

        # Load data:
        tomo = cm.read_array(args.path_tomo)

        # Initialize segmentation task:
        seg = Segment(Ncl=args.nclass, path_weights=args.path_weights, patch_size=args.psize)

        # Segment tomogram:
        scoremaps = seg.launch(tomo)

        # Get labelmap from scoremaps:
        labelmap = sm.to_labelmap(scoremaps)

        # Save labelmap:
        cm.write_array(labelmap, args.path_output)

        # Get binned labelmap and save:
        if args.bin:
            s = os.path.splitext(args.path_output)
            scoremapsB = sm.bin(scoremaps)
            labelmapB = sm.to_labelmap(scoremapsB)
            cm.write_array(labelmapB, s[0] + '_binned' + s[1])


if __name__ == "__main__":
    main()
