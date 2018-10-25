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

#ifndef PROJECT_ANCHORING_TEST_H
#define PROJECT_ANCHORING_TEST_H

#include <jaco_manipulation/test/anchoring_base_test.h>

namespace jaco_manipulation {
namespace test {

class AnchorTest : public AnchorBaseTest {
 public:
  /// deleted default constructor
  AnchorTest() = delete;

  /// constructor
  explicit AnchorTest(const std::vector<jaco_manipulation::BoundingBox> &datapoints);

  /// destructor
  ~AnchorTest() final= default;

  /**
   * Callback fro subscriber
   * @param msg anchorarray
   */
  void anchorArrayCallback(const anchor_msgs::AnchorArray::ConstPtr &msg);

  /**
   * Checks whether or not anchors are published
   * @return true if published
   */
  bool anchors_published() const;

 private:
  /// nodehandle
  ros::NodeHandle nh_;
  /// subscriber
  ros::Subscriber sub_;
  /// whether or not target anchor was found
  bool found_anchor_;
  /// creates bounding box from anchor array (size 1 in this test specifically)
  jaco_manipulation::BoundingBox createBoundingBoxFromAnchors() const;
};
} // namespace tes
} // namespace jaco_manipulation

#endif //PROJECT_ANCHORING_TEST_H
