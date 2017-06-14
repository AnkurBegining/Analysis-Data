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
def parse_maybe_int(i):
    if i == '':
        return None
    else:
        return int(i)


# Clean Date for enrollments
for enrollment in enrollments:
    enrollment['join_date'] = parse_date(enrollment['join_date'])
    enrollment['cancel_date'] = parse_date(enrollment['cancel_date'])
    enrollment['is_udacity'] = enrollment['is_udacity'] == 'True'
    enrollment['is_canceled'] = enrollment['is_canceled'] == 'True'
    enrollment['days_to_cancel'] = parse_maybe_int(enrollment['days_to_cancel'])

# Clean Data for dialy_engagement
for engagement_record in daily_engagement:
    engagement_record['lessons_completed'] = int(float(engagement_record['lessons_completed']))
    engagement_record['num_courses_visited'] = int(float(engagement_record['num_courses_visited']))
    engagement_record['projects_completed'] = int(float(engagement_record['projects_completed']))
    engagement_record['total_minutes_visited'] = float(engagement_record['total_minutes_visited'])
    engagement_record['utc_date'] = parse_date(engagement_record['utc_date'])

# Clean up the data types in the submissions table
for submission in submissions:
    submission['completion_date'] = parse_date(submission['completion_date'])
    submission['creation_date'] = parse_date(submission['creation_date'])

# Data after one clean up
print('\n\n')
print(enrollments[0])
print(daily_engagement[0])
print(submissions[0])


# fuction for conting number of row in all three table
def countNumberOfRow(filename):
    return (len(filename))


# function to convert 'acct' of daily engagement to 'account_key
for engagement in daily_engagement:
    engagement['account_key'] = engagement['acct']
    del [engagement['acct']]


# function for counting number of unique entry in table
def uniqueDataEntry(filename):
    uniqueDataset = set()
    for i in filename:
        uniqueDataset.add(i['account_key'])
    return uniqueDataset


# print number of row and unique entry
print('\n\n')
print("Number of row Enrollments: ", countNumberOfRow(enrollments))
print("Number of row Engagement: ", countNumberOfRow(daily_engagement))
print("Number of row Submissions: ", countNumberOfRow(submissions))
uniqueDataEntryEmployee = uniqueDataEntry(enrollments)
uniqueDataEntryEngagement = uniqueDataEntry(daily_engagement)
uniqueDataEntrySubmission = uniqueDataEntry(submissions)
print('\n\n')
print("Number of true Enrollment: ", len(uniqueDataEntryEmployee))
print("Number of true Engagement", len(uniqueDataEntryEngagement))
print("Number of true submission", len(uniqueDataEntrySubmission))

# code for seeing if some one is enrolled the is he or she has engagement of not
count = 0
for enrollment in enrollments:
    student = enrollment['account_key']
    if student not in uniqueDataEntryEngagement and enrollment['join_date'] != enrollment['cancel_date']:
        count += 1
print('\n\n')
print(count)

# count the account which was soley made for testing
count = 0
test_account = set()
for enrollment in enrollments:
    if (enrollment['is_udacity']):
        test_account.add(enrollment['account_key'])
print(len(test_account))


# function for deleting test account
def deleteTestAccountEntry(filename):
    non_udacity_data = []
    for i in filename:
        if i['account_key'] not in test_account:
            non_udacity_data.append(i)
    return non_udacity_data


non_udacity_enrollments = deleteTestAccountEntry(enrollments)
non_udacity_engagement = deleteTestAccountEntry(daily_engagement)
non_udacity_submission = deleteTestAccountEntry(submissions)

print('\n\n')
print("Non - Udacity Enrollment: ", len(non_udacity_enrollments))
print("Non - Udacity Engagement", len(non_udacity_engagement))
print("Non - Udacity submission", len(non_udacity_submission))

paid_student = {}


def countTrueStudent():
    for enrollment in non_udacity_enrollments:
        if not enrollment['is_canceled'] or enrollment['days_to_cancel'] > 7:
            account_key = enrollment['account_key']
            enrollment_date = enrollment['join_date']

            if account_key not in paid_student or enrollment_date > paid_student[account_key]:
                paid_student[account_key] = enrollment_date


countTrueStudent()
print("Paid_student ", len(paid_student))
'''from pprint import *
pprint(paid_student)'''


# remove free_trail user
def remove_free_trail_user(data):
    non_data = []
    for data_entry in data:
        if data_entry['account_key'] in paid_student:
            non_data.append(data_entry)

    return non_data


paid_enrollment = remove_free_trail_user(non_udacity_enrollments)
paid_engagement = remove_free_trail_user(non_udacity_engagement)
paid_submission = remove_free_trail_user(non_udacity_submission)
print("Paid Enrollment", paid_enrollment[0])
print("Paid Engagement", paid_engagement[0])
print("Paid submission", paid_submission[0])
print('\n\n')
print("Number of paid Enrollment ", len(paid_enrollment))
print("Number of paid Engagement ", len(paid_engagement))
print("Number of paid Submission ", len(paid_submission))


# Now we would analyse for first week

def with_in_one_week(join_date, engagement_date):
    days_delta = engagement_date - join_date
    return (days_delta.days < 7 and days_delta.days >= 0.0)


# create list of first week engagement of paid user
paid_engagement_in_first_week = []
for engagement in paid_engagement:
    account_key = engagement['account_key']
    join_date = paid_student[account_key]
    engagement_date = engagement['utc_date']
    if with_in_one_week(join_date, engagement_date):
        paid_engagement_in_first_week.append(engagement)
print("Paid Engagement in first week", len(paid_engagement_in_first_week))

# Group Engagement data by account key
from collections import *

engagement_by_account = defaultdict(list)

for engagement_record in paid_engagement_in_first_week:
    account_key = engagement_record['account_key']
    engagement_by_account[account_key].append(engagement_record)

# pprint(engagement_by_account)

# count total time spend by paid student in first week
total_minute_spend_by_account = {}


def analyseData(dataToanalyse):
    for account_key, engagement_by_student in engagement_by_account.items():
        total_minute = 0
        for engagement_record in engagement_by_student:
            total_minute += engagement_record[dataToanalyse]
        total_minute_spend_by_account[account_key] = total_minute

    total = total_minute_spend_by_account.values()

    return total


total_minutes_visited = analyseData('total_minutes_visited')
import numpy as np


def findmeanEtc(data_point):
    arr = np.array(list(map(float, data_point)))
    resultingList = []
    resultingList.append(arr.mean())
    resultingList.append(arr.std())
    resultingList.append(arr.min())
    resultingList.append(arr.max())
    return resultingList


meanEtcOfMinutesSpend = findmeanEtc(total_minutes_visited)
print('\n\n')
print("Mean of time spend by Paid student in first week: ", meanEtcOfMinutesSpend[0])
print("Standard deviation of time spend in first week: ", meanEtcOfMinutesSpend[1])
print("Minimum time spend by paid user in first week: ", meanEtcOfMinutesSpend[2])
print("Maximum time spend by paid user in first week: ", meanEtcOfMinutesSpend[3])

total_lesson_completed = analyseData('lessons_completed')

meanEtcOfLessonsCompleted = findmeanEtc(total_lesson_completed)
print("\n\n")
print("Mean of lesson completed by Paid student in first week: ", meanEtcOfLessonsCompleted[0])
print("Standard deviation of lesson completed in first week: ", meanEtcOfLessonsCompleted[1])
print("Minimum time spend by lesson completed in first week: ", meanEtcOfLessonsCompleted[2])
print("Maximum time spend by lesson completed in first week: ", meanEtcOfLessonsCompleted[3])
