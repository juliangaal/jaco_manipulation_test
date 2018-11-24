import os
import sys
from mpl_toolkits.mplot3d import Axes3D
import matplotlib.patches as mpatches
import matplotlib.pyplot as plt
import pandas as pd
import numpy as np


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
    kinda = 'orange'


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
    
    def __point_rate(self, points, all_points):
        return (len(points)/float(len(all_points))) * 100.0
    
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

    def save_surface_coverage_result(self, key="Percent"):
        frame = pd.DataFrame()

        frame['11success'] = np.where((self.df[key] == '11') & (self.df['Gripped'] == 'success'), self.df["Gripped"], np.nan)
        frame['11kinda'] = np.where((self.df[key] == '11') & (self.df['Gripped'] == 'kinda'), self.df["Gripped"], np.nan)
        frame['11failure'] = np.where((self.df[key] == '11') & (self.df['Gripped'] == 'failure'), self.df["Gripped"], np.nan)
        print frame

    def save_3d_result(self, result_key, grip_result_key='Result', force=False):
        if not force:
            for fname in os.listdir(self.target_dir):
                if fname.endswith('.png'):
                    print "Skipping existing plot"
                    return

        fig = plt.figure()
        ax = fig.add_subplot(111, projection='3d')
        ax.set_xlim3d(0.2, 0.7)
        ax.set_ylim3d(0.0, 0.58)
        ax.set_zlim3d(0.15, 0.3)
        ax.set_xlabel('robotic arm          <- X ->          kinect')
        ax.set_ylabel('Y')
        ax.set_zlabel('Z')

        self.__extract_point(result_key, grip_result_key)

        print "Attempting to generate 3d plot"

        if grip_result_key == 'Result':
            X = [float(p.x) for p in self.points if p.success]
            Y = [float(p.y) for p in self.points if p.success]
            Z = [float(p.z) for p in self.points if p.success]
            success_rate = self.__point_rate(X, self.points)
            success_patch = mpatches.Patch(color=Color.success, label='Success ' + str(success_rate) + '%')
            ax.scatter(X, Y, Z, c=Color.success, marker='o')

            X = [float(p.x) for p in self.points if not p.success]
            Y = [float(p.y) for p in self.points if not p.success]
            Z = [float(p.z) for p in self.points if not p.success]
            failure_rate = self.__point_rate(X, self.points)
            failure_patch = mpatches.Patch(color=Color.failure, label='Failure ' + str(failure_rate) + '%')
            ax.scatter(X, Y, Z, c=Color.failure, marker='o')

            plt.legend(handles=[success_patch, failure_patch], loc=0, fontsize=10)

            plt.savefig(self.figure_path_3d, dpi=300)
            print " ==> Generated figure with", len(self.points), "data points saved to:", self.figure_path_3d
        else:
            X = [float(p.x) for p in self.points if p.result == 'success']
            Y = [float(p.y) for p in self.points if p.result == 'success']
            Z = [float(p.z) for p in self.points if p.result == 'success']
            success_rate = self.__point_rate(X, self.points)
            success_patch = mpatches.Patch(color=Color.success, label='Success ' + str(success_rate) + '%')
            ax.scatter(X, Y, Z, c=Color.success, marker='o')

            X = [float(p.x) for p in self.points if p.result == 'failure']
            Y = [float(p.y) for p in self.points if p.result == 'failure']
            Z = [float(p.z) for p in self.points if p.result == 'failure']
            failure_rate = self.__point_rate(X, self.points)
            failure_patch = mpatches.Patch(color=Color.failure, label='Failure ' + str(failure_rate) + '%')
            ax.scatter(X, Y, Z, c=Color.failure, marker='o')

            X = [float(p.x) for p in self.points if p.result == 'kinda']
            Y = [float(p.y) for p in self.points if p.result == 'kinda']
            Z = [float(p.z) for p in self.points if p.result == 'kinda']
            kinda_rate = self.__point_rate(X, self.points)
            kinda_patch = mpatches.Patch(color=Color.kinda, label='Kinda ' + str(kinda_rate) + '%')
            ax.scatter(X, Y, Z, c=Color.kinda, marker='o')

            plt.legend(handles=[success_patch, failure_patch, kinda_patch], loc=0, fontsize=10)

            X = [float(p.x) for p in self.points if p.result == 'Default']
            if len(X) == len(self.points):
                print '!! NO default values were changed. Adjust them to the recorded gripping status in column "Gripped" !!'
                print '!! Plot will not be saved !!'
            elif X:
                print '!! Some default values were NOT changed. Adjust them to the recorded gripping status in column "Gripped" !!'
            else:
                plt.savefig(self.figure_path_3d, dpi=300)
                print " ==> Generated figure with", len(self.points), "data points saved to:", self.figure_path_3d

    def save_2d_result(self, result_key, grip_result_key='Result', force=False):
        if not force:
            for fname in os.listdir(self.target_dir):
                if fname.endswith('.png'):
                    print "Skipping existing plot"
                    return

        plt.figure()
        plt.ylabel('Y')
        plt.xlabel('robotic arm          <- X ->          kinect')

        if not self.points:
            self.__extract_point(result_key, grip_result_key)

        print "Attempting to generate 2d plot"

        if grip_result_key == 'Result':
            X = [float(p.x) for p in self.points if p.success]
            Y = [float(p.y) for p in self.points if p.success]
            success_rate = self.__point_rate(X, self.points)
            success_patch = mpatches.Patch(color=Color.success, label='Success ' + str(success_rate) + '%')
            plt.scatter(X, Y, marker='o', c=Color.success)

            X = [float(p.x) for p in self.points if not p.success]
            Y = [float(p.y) for p in self.points if not p.success]
            failure_rate = self.__point_rate(X, self.points)
            failure_patch = mpatches.Patch(color=Color.failure, label='Failure ' + str(failure_rate) + '%')
            plt.scatter(X, Y, marker='o', c=Color.failure)

            plt.legend(handles=[success_patch, failure_patch], loc=0, fontsize=10)

            plt.savefig(self.figure_path_2d, dpi=300)
            print " ==> Generated figure with", len(self.points), "data points saved to:", self.figure_path_2d
        else:
            X = [float(p.x) for p in self.points if p.result == 'success']
            Y = [float(p.y) for p in self.points if p.result == 'success']
            success_rate = self.__point_rate(X, self.points)
            success_patch = mpatches.Patch(color=Color.success, label='Success ' + str(success_rate) + '%')
            plt.scatter(X, Y, marker='o', c=Color.success)

            X = [float(p.x) for p in self.points if p.result == 'failure']
            Y = [float(p.y) for p in self.points if p.result == 'failure']
            failure_rate = self.__point_rate(X, self.points)
            failure_patch = mpatches.Patch(color=Color.failure, label='Failure ' + str(failure_rate) + '%')
            plt.scatter(X, Y, marker='o', c=Color.failure)

            X = [float(p.x) for p in self.points if p.result == 'kinda']
            Y = [float(p.y) for p in self.points if p.result == 'kinda']
            kinda_rate = self.__point_rate(X, self.points)
            kinda_patch = mpatches.Patch(color=Color.kinda, label='Kinda ' + str(kinda_rate) + '%')
            plt.scatter(X, Y, marker='o', c=Color.kinda)

            plt.legend(handles=[success_patch, failure_patch, kinda_patch], loc=0, fontsize=10)

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
