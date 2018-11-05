from analyse import ResultPlotter
from analyse import FileReader
import os

if __name__ == "__main__":
    reader = FileReader('anchoring_recordings.txt')
    for file in reader.files:
        print '\nAnalysing', os.path.basename(file)
        plotter = ResultPlotter(file, ['Time', 'Type', 'CurrentPose', 'TargetPose', 'Result', 'Gripped'], delimiter=';')
        plotter.save_3d_result('TargetPose', 'Gripped')
        plotter.save_2d_result('TargetPose', 'Gripped')