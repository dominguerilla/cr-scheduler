# REPORT PROCESS: Preprocesses the reports from Zed, so that we can get it ready for use for
# the scheduler
# 1. Renames the title rows in the input csv
#   Day Of Week -> weekday
# 2. Removes the Requests, Location, Total Requests, and Total Hours column
# And can turn each row of the preprocessed report into an object for use in
# the scheduler
import csv
import cr
import sys
import os

# Renames the columns, as well as removes the last three unnecessary rows from
# the report (requests, total requests, and total hours). If a list of netIDs is specified,
# will create a report containing only the requested netID's shifts.
def processcsv(filename, newfilename, netIDs = None):
    with open(filename, "r") as csvFile, open(newfilename, "w") as newFile:
        reader = csv.reader(csvFile)
        writer = csv.writer(newFile)

        # get rid of default title row from report
        titlerow = reader.next()

        # adds title columns & remove the last few
        writer.writerow(("netID", "location", "start", "end"))

        # remove the rest of the unnecessary rows from the file
        if netIDs == None:
            for row in reader:
                writer.writerow((row[0], row[1], row[4], row[5]))
        else:
            for row in reader:
                if row[0] in netIDs:
                    writer.writerow((row[0], row[1], row[4], row[5]))

# Returns a list of Shift objects based on an individual report created by
# processcsv.
def loadshifts(filename):
    shifts = []
    with open(filename, 'r') as report:
        reader = csv.reader(report)

        # remove title row
        titlerow = reader.next()

        # each row in reader is a list of strings
        for row in reader:
            shift = cr.Shift(row)
            shifts.append(shift)
    return shifts

# Returns a tuple of two lists of Shift objects based on reports that has been
# processed by processcsv()
# 'supreport' should be the report that comes out after processing the shifts
# of sups
# 'consreport' should be the report that comes out after processing the shifts
# of cons
# USAGE:    allshifts = rprocess.loadreports('data/[sup report filename]',
# 'data/[cons report filename]')
#           allshifts[0] # The list of all supervisor Shift objects
#           allshifts[1] # The list of all consultant Shift objects
#           allshifts[0][0] # The first Shift in the sup Shift list
#           len(allshifts[1]) # Length of the list of cons Shifts.
def loadreports(supreport, consreport):
    sups = loadshifts(supreport)
    cons = loadshifts(consreport)
    return (sups, cons)

if __name__ == "__main__":
    if len(sys.argv) == 3:
        if not os.path.exists('data/'):
            os.makedirs('data/')
        processcsv(sys.argv[1], 'data/sups.csv')
        processcsv(sys.argv[2], 'data/cons.csv')
        print "Reports processed to data/sups.csv and data/cons.csv."
        sys.exit()
    else:
        print "Usage: python rprocess.py [SUP SHIFTS REPORT] [CONS SHIFTS REPORT]"
        print "Will process the input files into data/sups.csv and data/cons.csv, respectively."
        print "The reports should be downloaded directly from Zed."