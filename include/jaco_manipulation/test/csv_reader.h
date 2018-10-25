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

#ifndef PROJECT_CSV_READER_H
#define PROJECT_CSV_READER_H

#include <vector>
#include <fstream>
#include <string>
#include <jaco_manipulation/BoundingBox.h>

namespace jaco_manipulation {
namespace test {

class CSVReader {
 public:
  /// deleted default constructor
  CSVReader() = delete;

  /// destructor
  virtual ~CSVReader();

  /**
   * Get bounding boxes that were generated from random poses in file
   * @return vector of bounding boxes
   */
  const std::vector<jaco_manipulation::BoundingBox>& getData() const;

  /// Saves poses from single csv line as bounding boxes
  virtual void saveVec(const std::vector<std::string> &line) = 0;

  /// processes file
  virtual void processFile(const std::string &filename) = 0;

 protected:
  /**
   * Constructor
   * @param filename ro read from: ABSOLUTE PATH
   * @param delim that seperated the csv columns
   */
  explicit CSVReader(const std::string filename, std::string delim = ";");

  // vector of bounding boxes generated from poses in file
  std::vector<jaco_manipulation::BoundingBox> data;

  /// filestream of opened file
  std::ifstream file;

  /// delimiter of csv column
  std::string delimiter;
};

} // namespace test
} // namespace jaco_manipulation

#endif //PROJECT_CSV_READER_H
