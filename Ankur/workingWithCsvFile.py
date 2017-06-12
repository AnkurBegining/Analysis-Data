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
