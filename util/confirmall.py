# I used this to confirm that all names on the Busch roster were present in the assignments.txt file that I kept the assignments in.
# The only names that WEREN'T on the assignments.txt and WERE on the Busch roster were Albert and those who did not have a permanent shift on Busch.
import csv
import sys

# load the netIDs from the Busch consultant roster; it's a CSV file with the first column being a netID.
def loadusernames(filename):
    fo = open(filename, 'r')
    csvreader = csv.reader(fo)
    netids = []

    # gets rid of title row
    titlerow = csvreader.next()
    for row in csvreader:
        netids.append(row[0])
    fo.close()
    print "NetIDs found in roster name: "
    for n in netids:
        print n
    return netids

# Checks to see if all netIDs found in the roster report are found in 
# the Assignment file, and prints the ones that are not found.
def checkassignments(assignmentfilename, rosterfilename):
    with open(assignmentfilename) as assignments:
        netids = loadusernames(rosterfilename)
        fulltext = assignments.read()
        for netID in netids:
            if not netID in fulltext:
                print "NetID " + netID + " not in assignment file."

if __name__ == "__main__":
    if len(sys.argv) == 3:
        checkassignments(sys.argv[1], sys.argv[2])
    else:
        print "Usage: python confirmall.py [text file containing assignments] [roster downloaded from Zed]"
        print "Open this script in a text editor for more information."