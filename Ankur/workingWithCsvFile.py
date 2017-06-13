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

# print number of row and unique entry
print('\n\n')
print("Number of row Enrollments: ", countNumberOfRow(non_udacity_enrollments))
print("Number of row Engagement: ", countNumberOfRow(non_udacity_engagement))
print("Number of row Submissions: ", countNumberOfRow(non_udacity_submission))
uniqueDataEntryEmployee = uniqueDataEntry(non_udacity_enrollments)
uniqueDataEntryEngagement = uniqueDataEntry(non_udacity_engagement)
uniqueDataEntrySubmission = uniqueDataEntry(non_udacity_submission)
print('\n\n')
print("Number of true Enrollment: ", len(uniqueDataEntryEmployee))
print("Number of true Engagement", len(uniqueDataEntryEngagement))
print("Number of true submission", len(uniqueDataEntrySubmission))

paid_student = {}


def countTrueStudent():
    for enrollment in non_udacity_enrollments:
        if not enrollment['is_canceled'] or enrollment['days_to_cancel'] > 7:
            account_key = enrollment['account_key']
            enrollment_date = enrollment['join_date']

            if account_key not in paid_student or enrollment_date > paid_student[account_key]:
                paid_student[account_key] = enrollment_date


countTrueStudent()
print(len(paid_student))
'''from pprint import *
pprint(paid_student)'''


# remove free_trail user
def remove_free_trail_user(data):
    non_data = []
    for enrollment in data:
        if enrollment['account_key'] in paid_student:
            non_data.append(enrollment)
    return non_data


paid_enrollment = remove_free_trail_user(non_udacity_enrollments)
paid_engagement = remove_free_trail_user(non_udacity_engagement)
paid_submission = remove_free_trail_user(non_udacity_submission)
print('\n\n')
print("Number of paid Enrollment ", len(paid_enrollment))
print("Number of paid Engagement ", len(paid_engagement))
print("Number of paid Submission ", len(paid_submission))
