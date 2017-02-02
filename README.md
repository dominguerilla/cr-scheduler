#Consultant Review Scheduler#

*rprocess.py*
Performs data-related operations on shift information from Zed, including:
    - Report preprocessing (removing unnecessary columns, renaming some columns)
    - Loads the preprocessed reports into memory

*cr.py*
Contains class definitions necessary for the scheduling algorithm.

*zeddie.py* 
Where the bulk of the scheduling algorithm takes place, leveraging data structures from cr.py and reports loaded from rprocess.py.
Consultants with a lesser number of overlapping shifts with supervisors are prioritized.

##Usage##
First, download two separate reports from Zed; one being the shifts for supervisors for the given period, and another being the shifts for consultants in the same period.
`python rprocess.py [sup report] [cons report]`

Next, run Zeddie using the two generated reports (by default, should be 'data/sups.csv' and 'data/cons.csv') as input:
`python zeddie.py [sup report] [cons report]`

Zeddie should print out both the assignments for each supervisor, as well as the list of consultants who were not able to be assigned to a supervisor (because they did not have any overlapping shifts).