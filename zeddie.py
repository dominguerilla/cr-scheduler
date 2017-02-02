import scheduler
import rprocess
import cr
import heapq

# Returns a sup ShiftAssignment for the next available sup for the given ShiftAssignment ascons.
# Returns None if ascons does not have any overlapping sups
def selectnextsup(ascons):
    # if this cons has no overlaps
    if len(ascons.assignments) == 0:
        return None
    while True:
        nextsup = ascons.assignments.pop()
        assup = [s for s in possibleassign if s.netID == nextsup]
        sup = assup[0]
        
        # if sup assignment is at max, remove sup netID from all the other consultants and pop again
        if sup.atMax():
            for c in consoverlaps:
                c.removeassignment(sup.netID)
            # remove sup assignment from possibleassign
            possibleassign.remove(sup)
        else:
            return sup

allshifts = rprocess.loadreports('data/sups.csv', 'data/cons.csv')
possibleassign, consoverlaps = scheduler.populateoverlapshift(allshifts)

# The sup-cons assignments
supassignments = list(possibleassign)

# Populate the unassignedcons list
unassignedcons = []
for c in consoverlaps:
    unassignedcons.append(c.netID)

print "len(consoverlaps): " + str(len(consoverlaps))
while len(consoverlaps) > 0:
    # selectNextCons()
    ascons = heapq.heappop(consoverlaps)
    
    # find the ShiftAssignment object that corresponds to the FIRST sup on ascons
    # aka selectNextSup()
    assup = selectnextsup(ascons)

    if assup == None:
        continue

    assup.addassignment(ascons.netID)
    unassignedcons.remove(ascons.netID)

for a in supassignments:
    print a
print "Unassigned cons: " + str(unassignedcons)