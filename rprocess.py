# Preprocesses the reports from ZED, so that we can get it ready for use for
# the scheduler
import csv
import sys

# DATA PREPROCESSING NEEDS TO
# 1. Renames the title rows in the input csv
#   Day Of Week -> weekday
# 2. Removes the Requests, Location, Total Requests, and Total Hours column
# 3. Turn each row of the preprocessed report into an object for use in the
# scheduler

# renames the columns, as well as removes the last three unnecessary rows
# from the report (requests, total requests, and total hours)
def processreport(filename, newfilename):
    with open(filename, "r") as csvFile, open(newfilename, "w") as newFile:
        reader = csv.reader(csvFile)
        writer = csv.writer(newFile)

        # get rid of default title row from report
        titlerow = reader.next()

        # adds title columns & remove the last few
        writer.writerow(("owner", "schedule", "weekday", "start", "end"))

        # remove the rest of the unnecessary rows from the file
        for row in reader:
            writer.writerow((row[0], row[1], row[3], row[4], row[5]))
