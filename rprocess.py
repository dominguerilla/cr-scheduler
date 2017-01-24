<<<<<<< HEAD
# Preprocesses the reports from Zed, so that we can get it ready for use for the scheduler
# 1. Renames the title rows in the input csv
#   Day Of Week -> weekday
# 2. Removes the Requests, Location, Total Requests, and Total Hours column
# And can turn each row of the preprocessed report into an object for use in the scheduler
import csv

# Represents a single shift in Zed. 
# You can use 'print([shift variable])' to print out a handy representation of that individual shift.
class Shift:

    # 'row' should be a list of strings. Meant to be used in conjunction with the default python csv.reader object.
    def __init__(self, row):
        self.netID = row[0]
        self.location = row[1]
        self.start = row[2]
        self.end = row[3]
    
    def __str__(self):
        return self.netID + "," + self.location + "," + self.start + "," + self.end


# Renames the columns, as well as removes the last three unnecessary rows from the report (requests, total requests, and total hours)
def processreport(filename, newfilename):
    with open(filename, "r") as csvFile, open(newfilename, "w") as newFile:
        reader = csv.reader(csvFile)
        writer = csv.writer(newFile)

        # get rid of default title row from report
        titlerow = reader.next()

        # adds title columns & remove the last few
        writer.writerow(("netID", "location", "start", "end"))

        # remove the rest of the unnecessary rows from the file
        for row in reader:
<<<<<<< HEAD
            writer.writerow((row[0], row[1], row[4], row[5]))

# Returns a list of Shift objects based on an individual report created by processreport
def loadshifts(filename):
    shifts = []
    with open(filename, 'r') as report:
        reader = csv.reader(report)

        # remove title row
        titlerow = reader.next()

        # each row in reader is a list of strings
        for row in reader:
            shift = Shift(row)
            shifts.append(shift)
    return shifts

# Returns a tuple of two lists of Shift objects based on reports that has been processed by processreport()
# 'supreport' should be the report that comes out after processing the shifts of sups
# 'consreport' should be the report that comes out after processing the shifts of cons
# USAGE:    allshifts = rprocess.loadreports('data/[sup report filename]', 'data/[cons report filename]')
#           allshifts[0] # The list of all supervisor Shift objects
#           allshifts[1] # The list of all consultant Shift objects
#           allshifts[0][0] # The first Shift in the sup Shift list
#           len(allshifts[1]) # Length of the list of cons Shifts.
def loadreports(supreport, consreport):
    sups = loadshifts(supreport)
    cons = loadshifts(consreport)
    return (sups, cons)
