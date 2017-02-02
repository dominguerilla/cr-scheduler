from cr import ShiftAssignment
import heapq

# Detects overlapping shifts between consultants and supervisors
# Returns a tuple containing 
# 1. a HEAP of cons objects that contain: (netid of cons, [list of sups that overlap at some point])
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
    heapq.heapify(consoverlaps)
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