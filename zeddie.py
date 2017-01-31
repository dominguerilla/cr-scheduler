import scheduler
import rprocess
import cr

allshifts = rprocess.loadreports('data/sups.csv', 'data/cons.csv')
consoverlaps, supassignments = scheduler.populateoverlapshift(allshifts)