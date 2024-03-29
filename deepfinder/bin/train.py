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
    parser = argparse.ArgumentParser(description='Train network.')
    parser.add_argument('-p', action='store', dest='path_params', help='path to params file')
    args = parser.parse_args()

    if args.path_params == None:  # if no args are passed, then open GUI
        gui_folder = 'pyqt.train.'
        gui_script = 'gui_train'

        cmd = 'python -m ' + 'deepfinder.' + gui_folder+gui_script
        os.system(cmd)

    else:
        from deepfinder.utils.params import ParamsTrain
        from deepfinder.training import Train
        import deepfinder.utils.objl as ol

        # Import parameters:
        params = ParamsTrain()
        params.read(args.path_params)

        # Initialize training task:
        trainer = Train(Ncl=params.Ncl, dim_in=params.psize)
        trainer.path_out = params.path_out
        trainer.h5_dset_name = 'dataset'  # if training data is stored as h5, you can specify the h5 dataset
        trainer.batch_size = params.bsize
        trainer.epochs = params.nepochs
        trainer.steps_per_epoch = params.steps_per_e
        trainer.Nvalid = params.steps_per_v
        trainer.flag_direct_read = params.flag_direct_read
        trainer.flag_batch_bootstrap = params.flag_bootstrap
        trainer.Lrnd = params.rnd_shift
        trainer.class_weights = None  # TODO

        # Use following line if you want to resume a previous training session:
        # trainer.net.load_weights('out/round1/net_weights_FINAL.h5') # TODO

        # Load object lists:
        objl_train = ol.read_xml(params.path_objl_train)
        objl_valid = ol.read_xml(params.path_objl_valid)

        # Finally, launch the training procedure:
        trainer.launch(params.path_tomo, params.path_target, objl_train, objl_valid)


if __name__ == "__main__":
    main()
