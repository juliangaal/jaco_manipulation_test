from analyse import ResultPlotter
import os

if __name__ == "__main__":
    file = '../anchoring_test_recording.csv'
    print '\nAnalysing', os.path.basename(file)
    plotter = ResultPlotter(file, ['Time', 'Type', 'CurrentPose', 'TargetPose', 'Result', 'Gripped'], delimiter=';', template=True)
    plotter.save_3d_result('TargetPose', 'Gripped')
    plotter.save_2d_result('TargetPose', 'Gripped')