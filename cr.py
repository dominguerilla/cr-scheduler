# Holds the data structures we use for CR scheduling.
from datetime import datetime

# Represents a single shift in Zed. 
# You can use 'print([shift variable])' to print out a handy representation of that individual shift.
class Shift:

    # 'row' should be a list of strings. Meant to be used in conjunction with the default python csv.reader object.
    def __init__(self, row):
        self.netID = row[0]
        self.location = row[1]
        self.start = datetime.strptime(row[2], "%Y-%m-%d %H:%M")
        self.end = datetime.strptime(row[3], "%Y-%m-%d %H:%M")
    
    def __str__(self):
        return self.netID + "," + self.location + "," + self.start + "," + self.end

