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

#ifndef PROJECT_ANCHORING_BASE_TEST_H
#define PROJECT_ANCHORING_BASE_TEST_H

#include <jaco_manipulation/client/jaco_manipulation_client.h>
#include <jaco_manipulation/BoundingBox.h>
#include <anchor_msgs/AnchorArray.h>

namespace jaco_manipulation {
namespace test {

class AnchorBaseTest {
 public:
  /**
   * Deleted default constructor
   */
  AnchorBaseTest() = delete;

  /**
   * Default destructor
   */
  virtual ~AnchorBaseTest() = default;

 protected:
  /**
   * AnchorBaseTest constructor
   * @param datapoints datapoints from generated poses file
   */
  explicit AnchorBaseTest(const std::vector<jaco_manipulation::BoundingBox> &datapoints);

  /**
   * Holds default bounding boxes from generated poses file
   */
  const std::vector<jaco_manipulation::BoundingBox> &data_;

  /**
   * Counts numer of trials
   */
  size_t trial_counter_;

  /**
   * Count number of grasps
   */
  size_t grip_counter_;

  /**
   * topic to subscribe to
   */
  const std::string topic_;

  /**
   * Holds anchor array that arrives at subscriber
   */
  anchor_msgs::AnchorArray anchors_;

  /**
   * Jaco manipulation client to interact with jaco manipulation server/ jaco arm
   */
  client::JacoManipulationClient jmc_;

  /**
   * Box to be dropped at
   */
  jaco_manipulation::BoundingBox drop_box_;

  /**
   * Iterator that points to current drop pose and bounding box
   */
  std::vector<jaco_manipulation::BoundingBox>::const_iterator current_drop_box_it_;

  /**
   * Holds current target anchor
   */
  jaco_manipulation::BoundingBox current_anchor_box_;

  /**
   * Adapts default box generated from random drop poses (generate in pose/generate with appropriate script)
   * @param current_drop_box_it current drop pose and it's default bounding box
   * @return
   */
  jaco_manipulation::BoundingBox
  adaptDropBoxToAnchorDims(std::vector<jaco_manipulation::BoundingBox>::const_iterator current_drop_box_it) const;

  /**
   * Creates bounding box for target anchor
   * @param anchor target anchor
   * @param const_label whether or not to choose separate label
   * @return
   */
  jaco_manipulation::BoundingBox
  createBoundingBoxFromAnchor(const anchor_msgs::Anchor &anchor, bool const_label=true) const;

  /**
   * Iterator to next random drop box
   * @return iterator to next drop box. If reached end-1, it return end, so the test stops
   */
  std::vector<jaco_manipulation::BoundingBox>::const_iterator next_drop_box();

  /**
   * Shows summary of anchors found, test number etc
   * @param labels
   */
  void show_summary(const std::vector<std::string> &labels) const;

  /**
   * Shows info about current test
   * @param name target object name
   */
  void show_test_info(std::string name = "Anchor");
};
} // namespace test
} // namespace jaco_manipulation

#endif //PROJECT_ANCHORING_BASE_TEST_H
