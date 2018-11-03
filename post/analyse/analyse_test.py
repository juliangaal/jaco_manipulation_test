#!/usr/bin/env python
import os
from analyse import ResultPlotter
from analyse import FileReader

path = "../results"

import os
for dirpath, dirs, files in os.walk(path):
    for fname in os.listdir(dirpath):
        if fname.endswith('recording.csv'):
            if "baseline" in dirpath:
                plotter = ResultPlotter(dirpath, fname, ['Time', 'Type', 'CurrentPose', 'TargetPose', 'Result'], delimiter=';')
                plotter.save3DResultFrom('TargetPose')
            else:
                plotter = ResultPlotter(dirpath, fname, ['Time', 'Type', 'CurrentPose', 'TargetPose', 'Result', 'Gripped'], delimiter=';')
                plotter.save3DResultFrom('TargetPose','Gripped')
                plotter.save2DResultFrom('TargetPose','Gripped')
