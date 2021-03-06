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

#ifndef PROJECT_ANCHORING_EDGE_CASE_TEST_H
#define PROJECT_ANCHORING_EDGE_CASE_TEST_H

#include <jaco_manipulation/test/anchoring_base_test.h>

namespace jaco_manipulation {
namespace test {

class AnchorEdgeCaseTest : public AnchorBaseTest {
 public:
  /**
   * Deleted default construcot
   */
  AnchorEdgeCaseTest() = delete;

  /**
   * Constructor of AnchorEdgeCaseTest
   * @param datapoints datapoints from randomly generated drop poses
   */
  explicit AnchorEdgeCaseTest(const std::vector<jaco_manipulation::BoundingBox> &datapoints);

  /**
   * Destructor
   */
  ~AnchorEdgeCaseTest() final= default;

  /**
   * Callback fro anchorarry subscriber
   * @param msg anchor array from vision system
   */
  void anchorArrayCallback(const anchor_msgs::AnchorArray::ConstPtr &msg);
  bool anchors_published() const;

 private:
  /// Nodehandle
  ros::NodeHandle nh_;
  /// subscriber
  ros::Subscriber sub_;
  /// whether or not target anchor was found, used to skip test, if not found
  bool found_anchor_;

  /// Creates boundinbox from anchors
  jaco_manipulation::BoundingBox createBoundingBoxFromAnchors() const;
};
} // namespace tes
} // namespace jaco_manipulation

#endif //PROJECT_ANCHORING_EDGE_CASE_TEST_H
