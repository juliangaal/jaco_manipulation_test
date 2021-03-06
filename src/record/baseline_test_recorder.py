#!/usr/bin/env python
# Copyright (C) 2018  Julian Gaal
# This program is free software: you can redistribute it and/or modify
# it under the terms of the GNU General Public License as published by
# the Free Software Foundation, either version 3 of the License, or
# (at your option) any later version.
# This program is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU General Public License for more details.
#     You should have received a copy of the GNU General Public License
# along with this program.  If not, see <http://www.gnu.org/licenses/>
import rospy
from jaco_manipulation.msg import JacoDebug
from record.test_recorder import Test
from conversions import Conversions


class BaseLineTest(Test):
    def __init__(self, filename, labels='baseline labels', delimiter=';'):
        Test.__init__(self, filename, labels)
        self.delimiter = delimiter
        self.num_data_points = 0
        rospy.init_node('base_line_tester', anonymous=True)
        rospy.Subscriber("jaco_manipulation/debug", JacoDebug, self.__callback)
        rospy.spin()

    def __callback(self, msg):
        line = self.__msg_to_string(msg)
        self.num_data_points += 1
        self.__write(line)

    def __msg_to_string(self, msg):
        type_ = msg.goal.description
        time = msg.timestamp.strip('\n')
        current_pose = Conversions.pose_to_string(msg.goal.current_pose).strip('\n')
        target_pose  = Conversions.pose_to_string(msg.goal.target_pose).strip('\n')
        result = msg.result.strip('\n')
        return time + self.delimiter + type_ + self.delimiter + current_pose + self.delimiter + target_pose + self.delimiter + result

    def __write(self, line):
        Test.write(self, line)


if __name__ == "__main__":
    test = BaseLineTest("baseline_test_recording.csv", "Time;Type;CurrentPose;TargetPose;Result")