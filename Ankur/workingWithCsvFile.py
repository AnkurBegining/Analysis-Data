from datetime import datetime as dt

from unicodecsv import *


# open csv file
def openCsvFile(file):
    with open(file, 'rb') as f:
        reader = DictReader(f)
        return (list(reader))


# make object of every file
enrollments = openCsvFile('enrollments.csv')
daily_engagement = openCsvFile('daily_engagement.csv')
submissions = openCsvFile('project_submissions.csv')

# print first of all three
print(enrollments[0])
print(daily_engagement[0])
print(submissions[0])


# clean of code by reformatting data type


# for parsing date into another data type
def parse_date(date):
    if date == '':
        return None
    else:
        return dt.strptime(date, '%Y-%m-%d')


# checking any string and convert it into the integer.
def parse_in_int(i):
    if i == '':
        return None
    else:
        return int(i)
