#!/usr/bin/env python
from analyse import ResultPlotter
import os


def analyse_dir(path):
    for dirpath, dirs, files in os.walk(path):
        for fname in os.listdir(dirpath):
            if fname.endswith('recording.csv'):
                if "baseline" in dirpath:
                    plotter = ResultPlotter(dirpath, fname, ['Time', 'Type', 'CurrentPose', 'TargetPose', 'Result'], delimiter=';')
                    plotter.save_2d_result('TargetPose', force=False)
                    plotter.save_3d_result('TargetPose', force=False)
                elif "obstacle_anchoring" in dirpath:
                    plotter = ResultPlotter(dirpath, fname, ['Time','Type','CurrentPose','TargetPose','Obstacles','Result','Gripped','Percent'], delimiter=';')
                    plotter.save_3d_result('TargetPose', 'Gripped', force=False)
                    plotter.save_2d_result('TargetPose', 'Gripped', force=False)
                    plotter.save_surface_coverage_result()
                else:
                    plotter = ResultPlotter(dirpath, fname, ['Time', 'Type', 'CurrentPose', 'TargetPose', 'Result', 'Gripped'], delimiter=';')
                    plotter.save_3d_result('TargetPose', 'Gripped', force=False)
                    plotter.save_2d_result('TargetPose', 'Gripped', force=False)

                print "\nAnalysing", os.path.join(dirpath, fname)


if __name__ == "__main__":
    analyse_dir("../results/baseline")