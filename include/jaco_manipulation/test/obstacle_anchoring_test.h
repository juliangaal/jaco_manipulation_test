/*
  Copyright (C) 2018  Julian Gaal
  This program is free software: you can redistribute it and/or modify
  it under the terms of the GNU General Public License as published by
  the Free Software Foundation, either version 3 of the License, or
  (at your option) any later version.
  This program is distributed in the hope that it will be useful,
  but WITHOUT ANY WARRANTY; without even the implied warranty of
  MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
  GNU General Public License for more details.
  You should have received a copy of the GNU General Public License
  along with this program.  If not, see <http://www.gnu.org/licenses/>
*/

#ifndef PROJECT_OBSTACLE_ANCHORING_TEST_H
#define PROJECT_OBSTACLE_ANCHORING_TEST_H

#include <jaco_manipulation/test/anchoring_base_test.h>
#include <tuple>

namespace jaco_manipulation {
namespace test {

struct Seconds {
  Seconds(size_t duration) : duration(duration) {}
  ~Seconds() = default;
  size_t duration;
};

using SeparatedObstacles = std::tuple<std::vector<jaco_manipulation::BoundingBox>, jaco_manipulation::BoundingBox, bool>;

class ObstacleAnchorTest : public AnchorBaseTest {
 public:
  /// deleted default constructor
  ObstacleAnchorTest() = delete;

  /**
   * constructor
   * @param data vector of bounding boxes generated with csv_reader
   */
  explicit ObstacleAnchorTest(const std::vector<jaco_manipulation::BoundingBox> &data);

  /// default destructor
  ~ObstacleAnchorTest() final = default;

  /**
   * callback for subscriber
   * @param msg anchor array from vision system
   */
  void anchorArrayCallback(const anchor_msgs::AnchorArray::ConstPtr &msg);

  /// checks if anchors are published
  bool anchors_published() const;

 private:
  /// node handle
  ros::NodeHandle nh_;
  /// subscriber
  ros::Subscriber sub_;
  /// whether or not target anchor was found, skips callback if not found
  bool found_anchor_;
  /// helper for debug messages
  bool time_to_add_obstacles_;
  /// describes how much of surface is covered
  double surface_coverage;
  /// how many surface obstacles are necessary for current test
  int surface_obstacles_necessary;
  /// how many grasps per coverage step
  const int grasps_per_obstacle_coverage;

  /**
   * Function to do countdown to give time to rearrange obstacles
   * @param seconds how many seconds to stop
   * @param target_found whether target was found or not
   */
  void countdown(struct Seconds seconds, bool target_found = true) const;

  /**
   * Separates target anchor from the rest in acnhor array msg
   * @param msg anchor array from vision system
   * @return vector of bounding box of obstacles, boundign box of target obstacle, target found or not
   */
  SeparatedObstacles extractObstacles(const anchor_msgs::AnchorArray::ConstPtr &msg) const;
};
} // namespace test
} // namespace jaco_manipulation

#endif //PROJECT_OBSTACLE_ANCHORING_TEST_H
