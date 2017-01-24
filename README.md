#Consultant Review Scheduler#

*rprocess.py :* preprocesser, takes report from zed and strips it of 
unnecessary information. spits out a list of cons objects that contain:
cons(netid, {list of sup netids that they overlap with})

*scheduler.py :* the actual scheduler. sub object contains:
sup(netid, {list of cons netids that overlap}, [assigned cons netids])
populates the assigned cons netids list by iterating through the rprocess
cons object list. if any cons are unassigned after iterating through, they
are collected in an unassigned list and must be manually scheduled.

