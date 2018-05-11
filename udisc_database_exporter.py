# Script to load in all of the scorecards

import csv
import os
import pprint


def main():
    # FIXME: make this path less absolute
    csv_dir = './workspace/'

    # FIXME: inefficient doing join twice...
    files = [os.path.join(csv_dir, file) for file in os.listdir(
        csv_dir) if os.path.isfile(os.path.join(csv_dir, file))]

    database = Database()

    for file in files:
        with open(file) as f:
            # this magic turns csv into dict
            # from https://stackoverflow.com/questions/21572175/convert-csv-file-to-list-of-dictionaries
            rows = [{k: v for k, v in row.items()}
                    for row in csv.DictReader(f, skipinitialspace=True)]

            if rows == []:
                continue

            # this is safe because we are guarenteed one (actually two) row
            num_holes = get_num_holes(rows[0])

            # first row is the course info
            course_info_row = rows[0]
            pars = get_hole_vals(course_info_row, num_holes)
            course_name = course_info_row['CourseName']
            layout_name = course_info_row['LayoutName']
            notes = course_info_row['Notes']

            date = course_info_row['Date']

            scores = {}
            for row in rows[2:]:
                player = row['PlayerName']
                score = get_hole_vals(row, num_holes)
                scores[player] = score

            database.add_scorecard(scores, date, course_name, layout_name, pars, notes)

    print(vars(database))


def get_num_holes(label_row):
    return max([int(label.replace('Hole', '')) for label in label_row.keys() if 'Hole' in label])


def get_hole_vals(row, num_holes):
    return [row['Hole' + str(hole_num)] for hole_num in range(1, num_holes-1)]


class Database:
    def __init__(self):
        self.courses = []

    def __contains__(self, course):
        return course in self.courses

    def add_scorecard(self, scores, date, name, layout, pars, notes):
        course = self._get_course(name, layout, pars, notes)
        course.add_scorecard(scores, date)

    def _get_course(self, name, layout, pars, notes):
        new_course = Course(name, layout, pars, notes)

        course = None
        if new_course not in self.courses:
            self.courses.append(new_course)
            course = new_course
        else:
            # if here, then course that is identical
            course = next((c for c in self.courses if new_course == c), None)

        assert course is not None, 'We messed up and there is no course'

        return course

    def __repr__(self):
        return pprint.pformat(vars(self))


# this is a glorified dictionary with user names as keys to the scores
# includes some meta data
class Scorecard:
    def __init__(self, scores, date):
        self.scores = scores
        # TODO: parse the date into a date object
        self.date = date

    def __repr__(self):
        return pprint.pformat(vars(self))

# this is used to uniquely identify scorecards
class Course:
    def __init__(self, name, layout, pars, notes):
        self.name = name
        self.layout = layout
        self.pars = pars
        self.notes = notes

        self.scorecards = []

    def __eq__(self, other):
        result = self.name == other.name and self.layout == other.layout and self.pars == other.pars and self.notes == other.notes

        return result

    def add_scorecard(self, scores, date):
        # TODO: only adds if there is no duplicate (just same date)
        self.scorecards.append(
            Scorecard(scores, date))

    def __repr__(self):
        return pprint.pformat(vars(self))


if __name__ == '__main__':
    main()
