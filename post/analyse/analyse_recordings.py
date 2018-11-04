#!/usr/bin/env python
import os
from analyse import ResultPlotter
from analyse import FileReader

path = "../results"

import os
for dirpath, dirs, files in os.walk(path):
    for fname in os.listdir(dirpath):
        if fname.endswith('recording.csv') and not "obstacle_anchoring" in dirpath:
            if "baseline" in dirpath:
                plotter = ResultPlotter(dirpath, fname, ['Time', 'Type', 'CurrentPose', 'TargetPose', 'Result'], delimiter=';')
                plotter.save3DResultFrom('TargetPose', force=False)
            else:
                plotter = ResultPlotter(dirpath, fname, ['Time', 'Type', 'CurrentPose', 'TargetPose', 'Result', 'Gripped'], delimiter=';')
                plotter.save3DResultFrom('TargetPose','Gripped', force=False)
                plotter.save2DResultFrom('TargetPose','Gripped', force=False)
            print "\nAnalysing", os.path.join(dirpath, fname)
