#Consultant Review Scheduler#

Given a list of shifts including ID and start/end times for supervisors and consultants, assigns a consultant to a supervisor whose shifts overlap in order to schedule Consultant Reviews.

*rprocess.py*
Performs data-related operations on shift information from Zed, including:
* Report preprocessing (removing unnecessary columns, renaming some columns)
* Loads the preprocessed reports into memory

*cr.py*
Contains class definitions necessary for the scheduling algorithm.

*zeddie.py* 
Where the bulk of the scheduling algorithm takes place, leveraging data structures from cr.py and reports loaded from rprocess.py.
Consultants with a lesser number of overlapping shifts with supervisors are prioritized, and will only count as overlapping if the shift overlap is greater than or equal to 30 minutes.

##Usage##
**Works only with Python 2.X**
First, download two separate reports from Zed; one being the shifts for supervisors for the given period, and another being the shifts for consultants in the same period.
`python rprocess.py [sup report] [cons report]`

Next, run Zeddie using the two generated reports (by default, should be 'data/sups.csv' and 'data/cons.csv') as input:
`python zeddie.py [sup report] [cons report]`

Zeddie should print out both the assignments for each supervisor, as well as the list of consultants who were not able to be assigned to a supervisor (because they did not have any overlapping shifts).