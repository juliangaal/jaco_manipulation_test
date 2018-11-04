import os
import sys
from mpl_toolkits.mplot3d import Axes3D
import matplotlib.pyplot as plt
import pandas as pd


class Point:
    def __init__(self, x, y, z, result):
        self.x = x
        self.y = y
        self.z = z
        self.success = result

    def __str__(self):
        return "({} {} {})".format(self.x, self.y, self.z)

class AnchorPoint:
    def __init__(self, x, y, z, result):
        self.x = x
        self.y = y
        self.z = z
        self.result = result

    def __str__(self):
        return "({} {} {} {})".format(self.x, self.y, self.z, self.result)

class Color:
    success = 'limegreen'
    failure = 'r'
    kinda = 'yellow'

class FileReader:
    def __init__(self, file):
        self.file = open(os.path.abspath(file), 'r')
        if not self.file:
            print 'Filereader: Cant open file', file
            exit()

        self.files = [os.path.abspath(line).rstrip() for line in self.file]

    def __str__(self):
        return ''.join(str(s) for s in self.files)

    def __del__(self):
        self.file.close()

class ResultPlotter:
    def __init__(self, target_dir, file, labels, delimiter=',', template=False):
        self.target_dir = target_dir
        self.file = os.path.join(self.target_dir, file)
        self.figure_path_3d = os.path.join(self.target_dir, '3d_fig.png')
        self.figure_path_2d = os.path.join(self.target_dir, '2d_fig.png')
        self.labels = labels
        self.delimiter = delimiter
        self.points = []
        self.df = pd.read_csv(self.file, names=self.labels, sep=self.delimiter)

    def __extract_point(self, result_key, grip_result_key):
        data = self.df[result_key]
        results = self.df[grip_result_key]

        for d, r in zip(data, results):
            if d == result_key or r == grip_result_key:
                continue

            try:
                point, _ = d.split('/')
                point = point.replace('(', '').replace(')', '')
                x, y, z = point.split(',')
                if grip_result_key == 'Result':
                    self.points.append(Point(x, y, z, True if r == 'success' else False))
                else:
                    self.points.append(AnchorPoint(x,y,z,r))
            except ValueError:
                print "!!", ".csv data malformed: ", d
                pass

    def save3DResultFrom(self, result_key, grip_result_key='Result', force=False):
        if not force:
            for fname in os.listdir(self.target_dir):
                if fname.endswith('.png'):
                    print "Skipping existing plot"
                    return

        fig = plt.figure()
        fig.suptitle(self.file)
        ax = fig.add_subplot(111, projection='3d')

        self.__extract_point(result_key, grip_result_key)

        print "Attempting to generate 3d plot"

        if grip_result_key == 'Result':
            X = [float(p.x) for p in self.points if p.success]
            Y = [float(p.y) for p in self.points if p.success]
            Z = [float(p.z) for p in self.points if p.success]
            ax.scatter(X, Y, Z, c=Color.success, marker='o')

            X = [float(p.x) for p in self.points if not p.success]
            Y = [float(p.y) for p in self.points if not p.success]
            Z = [float(p.z) for p in self.points if not p.success]
            ax.scatter(X, Y, Z, c=Color.failure, marker='o')

            plt.savefig(self.figure_path_3d, dpi=300)
            print " ==> Generated figure with", len(self.points), "data points saved to:", self.figure_path_3d
        else:
            X = [float(p.x) for p in self.points if p.result == 'success']
            Y = [float(p.y) for p in self.points if p.result == 'success']
            Z = [float(p.z) for p in self.points if p.result == 'success']
            ax.scatter(X, Y, Z, c=Color.success, marker='o')

            X = [float(p.x) for p in self.points if p.result == 'failure']
            Y = [float(p.y) for p in self.points if p.result == 'failure']
            Z = [float(p.z) for p in self.points if p.result == 'failure']
            ax.scatter(X, Y, Z, c=Color.failure, marker='o')

            X = [float(p.x) for p in self.points if p.result == 'kinda']
            Y = [float(p.y) for p in self.points if p.result == 'kinda']
            Z = [float(p.z) for p in self.points if p.result == 'kinda']
            ax.scatter(X, Y, Z, c=Color.kinda, marker='o')

            X = [float(p.x) for p in self.points if p.result == 'Default']
            if len(X) == len(self.points):
                print '!! NO default values were changed. Adjust them to the recorded gripping status in column "Gripped" !!'
                print '!! Plot will not be saved !!'
            elif X:
                print '!! Some default values were NOT changed. Adjust them to the recorded gripping status in column "Gripped" !!'
            else:
                ax.set_xlim3d(0.2, 0.7)
                ax.set_ylim3d(0.0, 0.58)
                ax.set_zlim3d(0.15, 0.3)
                ax.set_xlabel('robotic arm          <- X ->          kinect')
                ax.set_ylabel('Y')
                ax.set_zlabel('Z')

                plt.savefig(self.figure_path_3d, dpi=300)
                print " ==> Generated figure with", len(self.points), "data points saved to:", self.figure_path_3d

    def save2DResultFrom(self, result_key, grip_result_key='Result', force=False):
        if not force:
            for fname in os.listdir(self.target_dir):
                if fname.endswith('.png'):
                    print "Skipping existing plot"
                    return

        plt.figure()
        plt.title(self.file)
        plt.ylabel('Y')
        plt.xlabel('robotic arm          <- X ->          kinect')

        if not self.points:
            self.__extract_point(result_key, grip_result_key)

        print "Attempting to generate 2d plot"

        if grip_result_key == 'Result':
            X = [float(p.x) for p in self.points if p.success]
            Y = [float(p.y) for p in self.points if p.success]
            plt.scatter(X, Y, marker='o', c=Color.success)

            X = [float(p.x) for p in self.points if not p.success]
            Y = [float(p.y) for p in self.points if not p.success]
            plt.scatter(X, Y, marker='o', c=Color.failure)

            plt.savefig(self.figure_path_2d, dpi=300)
            print " ==> Generated figure with", len(self.points), "data points saved to:", self.figure_path_2d
        else:
            X = [float(p.x) for p in self.points if p.result == 'success']
            Y = [float(p.y) for p in self.points if p.result == 'success']
            plt.scatter(X, Y, marker='o', c=Color.success)

            X = [float(p.x) for p in self.points if p.result == 'failure']
            Y = [float(p.y) for p in self.points if p.result == 'failure']
            plt.scatter(X, Y, marker='o', c=Color.failure)

            X = [float(p.x) for p in self.points if p.result == 'kinda']
            Y = [float(p.y) for p in self.points if p.result == 'kinda']
            plt.scatter(X, Y, marker='o', c=Color.kinda)

            X = [float(p.x) for p in self.points if p.result == 'Default']
            if len(X) == len(self.points):
                print '!! NO default values were changed. Adjust them to the recorded gripping status in column "Gripped" !!'
                print '!! Plot will not be saved !!'
            elif X:
                print '!! Some default values were NOT changed. Adjust them to the recorded gripping status in column "Gripped" !!'
                print '!! Plot will not be saved !!'
            else:
                plt.savefig(self.figure_path_2d, dpi=300)
                print " ==> Generated figure with", len(self.points), "data points saved to:", self.figure_path_2d
