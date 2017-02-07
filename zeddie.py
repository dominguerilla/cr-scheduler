# Main scheduling module for the CR-scheduler.
# If you'd like to change how selectNextCons() or selectNextSup() works, just change initializecons() and initializesups(), as well as
# selectnextcons() and selectnextsup().
# The current implementation uses a priority queue for getting the next consultant based on the number of supervisors they work with, 
# and just grabbing a supervisor from that consultant's list.
#
# Another possible implementation would be the reverse; get the next supervisor based on the number of unique consultants they work with,
# and then assigning them a consultant from their list.

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
    supassignments = createshiftassignments(sups, maxassignments = 10)

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
            tuplelist.append(ShiftAssignment(shift.netID, assignments = [], maxassignments = maxassignments))
    return tuplelist

# Loads saved assignments from file, and then removes assignments that have already existed from both the sup assignments list and the consoverlap list.
# Call this AFTER calling rprocess.loadreports().
def loadsavedassignments(filename, possibleassign, consoverlaps):
    manualassignments = rprocess.loadassignments(filename)
    if manualassignments == None:
        print "No manual assignments found."
        return
    for assignment in manualassignments:
        matching = [m for m in possibleassign if assignment.netID == m.netID]
        # if this sup has not been manually assigned
        if not matching:
            continue
        
        # Removing sup assignment from possibleassign
        possibleassign.remove(matching[0])
        possibleassign.append(assignment)

        # Removing cons overlap from consoverlap
        for cons in assignment.assignments:
            co = [c for c in consoverlaps if c.netID == cons]
            consoverlaps.remove(co[0])
    

# Initializes the possibleassign list, 
def initializesups(possibleassign):
    return possibleassign

# Returns a sup ShiftAssignment for the next available sup in possibleassign for the given ShiftAssignment ascons.
# Returns None if ascons does not have any overlapping sups
# If this finds that a 'popped' sup has the max assignments, it will remove it from the consoverlaps heap
def selectnextsup(ascons, possibleassign, consoverlaps):
    while True:
        # if this cons has no overlaps
        if not len(ascons.assignments):
            return None
        nextsup = ascons.assignments.pop()
        assup = []
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

# Initializes the cons-sup overlap list.
# This should be run at least once before using selectnextcons().
# Current implementation is to turn it into a priority queue
# This way, the consultants with the least amount of overlapping sups are prioritized
def initializecons(consoverlaps):
    # Not returning this, because heapify transforms list to heap in-place
    heapq.heapify(consoverlaps)

# Gets the next cons to assign a supervisor to
# Current implementation is to pop it from a priority queue.
def selectnextcons(consoverlaps):
    return heapq.heappop(consoverlaps)

# Assigns consultants to supervisors for their CRs, based on the given sup shift report data and cons report data.
# These reports should have been already processed by rprocess.processcsv().
# Returns a tuple containing 1. the assignments of cons to sups and 2. the list of unassigned consultant netIDs
def assigncrs(supreport, consreport):
    allshifts = rprocess.loadreports(supreport, consreport)

    # possibleassign is the list of sups that CAN have more consultants scheduled for. Once the sup reaches the max number
    # of assignments, it's removed from possibleassign.
    # consoverlaps is just the priority queue (heap) of consultants, sorted by the number of sups they have overlapping shifts with.
    possibleassign, consoverlaps = populateoverlapshift(allshifts)
    print "Number of consoverlaps: " + str(len(consoverlaps))

    unassignedcons = []
    loadsavedassignments('data/manualassign.csv', possibleassign, consoverlaps)

    # Turn consoverlaps into a priority queue/heap
    initializecons(consoverlaps)
    possibleassign = initializesups(possibleassign)

    # The suggested CR assignments that will be returned once this function finishes.
    supassignments = list(possibleassign)

    # Populate the unassignedcons list.
    # As a consultant is assigned a supervisor, they are removed from unassignedcons. However, if a consultant does not
    # have any overlapping shifts with any sup, their netIDs remain in this list.
    for c in consoverlaps:
        unassignedcons.append(c.netID)

    # Loop while there are still consultants that have overlapping shifts with sups
    while len(consoverlaps) > 0:
        # selectNextCons()
        nextcons = selectnextcons(consoverlaps)
        
        # aka selectNextSup()
        nextsup = selectnextsup(nextcons, possibleassign, consoverlaps)

        if nextsup == None:
            continue
        
        # The next supervisor was selected successfully; record the assignment and remove the cons from unassigned cons
        nextsup.addassignment(nextcons.netID)
        unassignedcons.remove(nextcons.netID)
    return (supassignments, unassignedcons)

# Given a supreport and a LIST of consreports processed by rprocess.processcsv(), assigns CRs by prioritizing location.
# To use, make sure that you have a report for every location, and then order consreports by order of decreasing priority.
# For example, if you wanted to prioritize assigning those working at ARC, LSM, RBHS, and BEST (in that order):
# consreports = [ARCcons.csv, LSMcons.csv, RBHScons.csv, BESTcons.csv]
def assigncrsbylocation(supreport, consreports):
    supshifts = rprocess.loadshifts(supreport)
    supassignments = createshiftassignments(supshifts, maxassignments = 8)
    unassignedcons = []
    for location in consreports:
        consshifts = rprocess.loadshifts(location)
        # possibleassign is the list of sups that CAN have more consultants scheduled for. Once the sup reaches the max number
        # of assignments, it's removed from possibleassign.
        # consoverlaps is just the priority queue (heap) of consultants, sorted by the number of sups they have overlapping shifts with.
        alloverlaps = populateoverlapshift((supshifts, consshifts))
        consoverlaps = alloverlaps[1]

        # Populate the unassignedcons list.
        # As a consultant is assigned a supervisor, they are removed from unassignedcons. However, if a consultant does not
        # have any overlapping shifts with any sup, their netIDs remain in this list.
        for c in consoverlaps:
            if c.netID not in unassignedcons:
                unassignedcons.append(c.netID)

        # Turn consoverlaps into a priority queue/heap
        initializecons(consoverlaps)

        # Loop while there are still consultants that have overlapping shifts with sups
        while len(consoverlaps) > 0:
            # selectNextCons()
            nextcons = selectnextcons(consoverlaps)
            
            # aka selectNextSup()
            nextsup = selectnextsup(nextcons, supassignments, consoverlaps)

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