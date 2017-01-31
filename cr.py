# Holds the data structures we use for CR scheduling.
from datetime import datetime
import heapq

# Represents a single shift in Zed.
# You can use 'print([shift variable])' to print out a handy representation
# of that individual shift.
class Shift:

    # 'row' should be a list of strings. Meant to be used in conjunction with
    # the default python csv.reader object.
    def __init__(self, row):
        self.netID = row[0]
        self.location = row[1]
        self.start = datetime.strptime(row[2], "%Y-%m-%d %H:%M:%S")
        self.end = datetime.strptime(row[3], "%Y-%m-%d %H:%M:%S")

    def __str__(self):
        return self.netID + "," + self.location + "," + self.start + "," + self.end

    def overlaps(self, shiftB):
        if self.start <= shiftB.end and self.end >= shiftB.end:
            return True
        return False

class ShiftAssignment:
    
    def __init__(self, netID):
        self.netID = netID
        self.assignments = []

    def addassignment(self, netID):
        if not netID in self.assignments:
            self.assignments.append(netID)
    
    def removeassignment(self, netID):
        if netID in self.assignments:
            self.assignments.remove(netID)

    def __str__(self):
        return "{ " + self.netID + ", " + str(self.assignments) + " }"

    # A ShiftAssignment is 'less' than another if it has less assignments than the other.
    def __lt__(self, other):
        return len(self.assignments) < len(other.assignments)
    
    def __gt__(self, other):
        return len(self.assignments) > len(other.assignments)

    def __eq__(self, other):
        return len(self.assignments) == len(other.assignments)