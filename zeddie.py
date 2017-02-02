import rprocess
import heapq
import sys
from cr import ShiftAssignment

# Detects overlapping shifts between consultants and supervisors
# Returns a tuple containing 
# 1. a LIST of cons objects that contain: (netid of cons, [list of sups that overlap at some point])
# 2. a LIST of sup assignment objects: (netid of sup, [list of cons that are assigned to this sups])
def populateoverlapshift(allshifts):
    sups, cons = allshifts

    # list of cons(netid, {sups that overlap}) objects
    consoverlaps = createshiftassignments(cons)
    supassignments = createshiftassignments(sups, maxassignments = 8)

    # populating consoverlaps with the sup netIDs that overlap with their shifts
    for conshift in cons:
        # get the tuple from the consoverlaps list with the netid of this cons
        consassign = [c for c in consoverlaps if c.netID == conshift.netID][0]
        for supshift in sups:
            # If the cons shift overlaps with the sup shift
            if conshift.overlaps(supshift):
                consassign.addassignment(supshift.netID)
    return (supassignments, consoverlaps)

# Given an input list of Shift objects,
# returns a list of unique ShiftAssignment objects.
# So, given a bunch of Shift objects, the returned list will have one ShiftAssignment per unique netID
def createshiftassignments(shiftlist, maxassignments = 0):
    tuplelist = []
    for shift in shiftlist:
        if not shift.netID in [t.netID for t in tuplelist]:
            tuplelist.append(ShiftAssignment(shift.netID, maxassignments = maxassignments))
    return tuplelist

# Returns a sup ShiftAssignment for the next available sup in possibleassign for the given ShiftAssignment ascons.
# Returns None if ascons does not have any overlapping sups
# If this finds that a 'popped' sup has the max assignments, it will remove it from the consoverlaps heap
def selectnextsup(ascons, possibleassign, consoverlaps):
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

# Assigns consultants to supervisors for their CRs, based on the given sup shift report data and cons report data.
# These reports should have been already processed by rprocess.processcsv().
# Returns a tuple containing 1. the assignments of cons to sups and 2. the list of unassigned consultant netIDs
def assigncrs(supreport, consreport):
    allshifts = rprocess.loadreports(supreport, consreport)

    # possibleassign is the list of sups that CAN have more consultants scheduled for. Once the sup reaches the max number
    # of assignments, it's removed from possibleassign.
    # consoverlaps is just the priority queue (heap) of consultants, sorted by the number of sups they have overlapping shifts with.
    possibleassign, consoverlaps = populateoverlapshift(allshifts)

    # Turn consoverlaps into a priority queue/heap
    # This way, the consultants with the least amount of overlapping sups are prioritized
    heapq.heapify(consoverlaps)

    # The suggested CR assignments that will be returned once this function finishes.
    supassignments = list(possibleassign)

    # Populate the unassignedcons list.
    # As a consultant is assigned a supervisor, they are removed from unassignedcons. However, if a consultant does not
    # have any overlapping shifts with any sup, their netIDs remain in this list.
    unassignedcons = []
    for c in consoverlaps:
        unassignedcons.append(c.netID)

    # Loop while there are still consultants that have overlapping shifts with sups
    while len(consoverlaps) > 0:
        # selectNextCons()
        nextcons = heapq.heappop(consoverlaps)
        
        # find the ShiftAssignment object that corresponds to the FIRST sup on ascons
        # aka selectNextSup()
        nextsup = selectnextsup(nextcons, possibleassign, consoverlaps)

        if nextsup == None:
            continue
        
        # The next supervisor was selected successfully; record the assignment and remove the cons from unassigned cons
        nextsup.addassignment(nextcons.netID)
        unassignedcons.remove(nextcons.netID)
    return (supassignments, unassignedcons)
    

if __name__ == "__main__":
    if len(sys.argv) == 3:
        supreport = sys.argv[1]
        consreport = sys.argv[2]
    elif len(sys.argv) == 1:
        supreport = 'data/sups.csv'
        consreport = 'data/cons.csv'
    else:
        print "Usage: python zeddie.py [sup report] [cons report]"
        print "OR python zeddie.py (defaults above to 'data/sups.csv' and 'data/cons.csv')"
        print "[sup report] = A ZED report containing all of the supervisors' shifts in csv format, which has ALREADY been processed by rprocess.py"
        print "[cons report] = A ZED report containing all of the consultants' shifts in csv format, which has ALREADY been processed by rprocess.py"
        sys.exit()
    assignments, unassigned = assigncrs(supreport, consreport)

    # Print out results
    for a in assignments:
        print a
    print "Unassigned cons: " + str(unassigned)