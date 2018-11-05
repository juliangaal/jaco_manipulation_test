#!/usr/bin/env python
from analyse import ResultPlotter
import os


def analyse_dir(path):
    for dirpath, dirs, files in os.walk(path):
        for fname in os.listdir(dirpath):
            if fname.endswith('recording.csv') and not "obstacle_anchoring" in dirpath:
                if "baseline" in dirpath:
                    plotter = ResultPlotter(dirpath, fname, ['Time', 'Type', 'CurrentPose', 'TargetPose', 'Result'], delimiter=';')
                    plotter.save_3d_result('TargetPose', force=True)
                else:
                    plotter = ResultPlotter(dirpath, fname, ['Time', 'Type', 'CurrentPose', 'TargetPose', 'Result', 'Gripped'], delimiter=';')
                    plotter.save_3d_result('TargetPose', 'Gripped', force=True)
                    plotter.save_2d_result('TargetPose', 'Gripped', force=True)
                print "\nAnalysing", os.path.join(dirpath, fname)


if __name__ == "__main__":
    analyse_dir("../results")