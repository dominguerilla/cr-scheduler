# Holds all data structures we use for CR scheduling.
from datetime import datetime

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

    # http://stackoverflow.com/questions/9044084/efficient-date-range-overlap-calculation-in-python
    # Will return True if the shift times overlap AND the overlap time is greater than or equal to 30 minutes
    def overlaps(self, shiftB):
        if self.start <= shiftB.end and self.end >= shiftB.end:
            latest_start = max(self.start, shiftB.start)
            earliest_end = min(self.end, shiftB.end)
            overlaptime = (earliest_end - latest_start).seconds + 1

            # Get the minutes of overlap
            minuteoverlap = overlaptime // 60 % 60
            if minuteoverlap >= 30:
                return True
        return False

# Meant to be a smarter version of the tuple <netID, []>.
# Used in zeddie and scheduler to:
#   1. Track the sups that each cons has an overlapping shift with
#   2. Track the sups that each cons is assigned to
class ShiftAssignment:
    
    # netID = the netID of the assignment to use. 
    # maxassignments = the max number of assignments to allow this ShiftAssignment to have.
    def __init__(self, netID, assignments = [], maxassignments = 0):
        self.netID = netID
        self.assignments = assignments
        # if maxassignments is 0, then there is no max assignment limit
        self.maxassignments = maxassignments

    # Adds a netID to the assignments field. 
    # Returns true if the length of the list of assignments is less than maxassignments 
    # or if netID is already in the assignments list, false if at max 
    def addassignment(self, netID):
        if not netID in self.assignments:
            self.assignments.append(netID)
            if self.atMax():
                return True
            else:
                return False
        return True
    
    # Removes a netID from this ShiftAssignment's assignments, if it exists
    def removeassignment(self, netID):
        if netID in self.assignments:
            self.assignments.remove(netID)

    def __str__(self):
        return "{ " + self.netID + ", " + str(self.assignments) + " }"
    
    def atMax(self):
        return (not self.maxassignments == 0) and len(self.assignments) >= self.maxassignments

    # A ShiftAssignment is 'less' than another if it has less assignments than the other.
    # This is defined so that a list of ShiftAssignments works with heapq
    def __lt__(self, other):
        return len(self.assignments) < len(other.assignments)
    
    def __gt__(self, other):
        return len(self.assignments) > len(other.assignments)