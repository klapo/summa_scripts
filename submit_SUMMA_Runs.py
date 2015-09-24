#!/usr/bin/python

# Import
import os
import sys
from settings import Create_new

####################################################################################
# submit_SUMMA_Runs.py
####################################################################################
## Description ##
# Submits indivual paramter runs to be run in parellel
#
## Instructions ##
# 1) Modify Input Values  below
# 2) Update paths (i.e. home_dir     = "/home/wayandn/")
# 3) Run ./submit_SUMMA_Runs.py
#
# Created 1/8/2013 - Nic Wayand (nicway@u.washington.edu)
# Updated 8/16/2015 
####################################################################################

#####################################################################################
# User Options - CHECK ALL 4 Required Inputs!
#####################################################################################

# 1) Define Sites to Use
Site_ID_all = ["SNQ_ALL"]

# 2) Run ID
#Run_IDs     = [80073,80076,80078,80079,80080,80095,80096,80097,80102,80115,80438,80446,80486,80494,80495,80496,80497,80095,80498,80512,80517,80518,80519,80790,80826] 
Run_IDs = [1]
#Run_IDs = range(9672,9680)
#Run_IDs = range(90001,90953)

# Define chunked runs if we have many
#R_S = 50001
#R_E = 58680
#npp = 10
#cR = int(sys.argv[1])
#steps = (R_E-R_S)/npp
#Breaklist = xrange(R_S,R_E+1,steps)
#Run_IDs = range(Breaklist[cR-1],Breaklist[cR])
#print Run_IDs[0]

# 3) Experiment Name
exp_name    = "Cont_Hist_1hr_test"

# 4) Run on Command line or in Queue?
jobrun 	    = 1 # 1 = Command line, 2 = Queue (single job), 3 = Serial Parrallel jobs (note: requires GNU parallel)

# RUN OPTIONS if jobrun==1
runJobsSerial = 1 # 1 = jobs run in serial (one at a time), 2 = jobs are submited all at once to command line

# RUN OPTIONS if jobrun==3
# Path/Name of argument file (if option 3 is used)
argument_file    = "/home/wayandn/serial_job_args/Restart_exp" # List of inputs to summa.exe for each job (is created below)
# Path/Name of pbs file for Serial parrallel jobs (if option 3 is used)
seriall_pbs = "/home/wayandn/SerialSubmit.pbs"

# General PBS options here 
your_email  = "nicway@u.washington.edu"

#####################################################################################
# Code
#####################################################################################

# Define User Paths
home_dir     = "/home/wayandn/"
main_dir     = home_dir + "summa/"
settings_dir = main_dir + "settings/"
output_dir   = main_dir + "output/"
run_dir      = main_dir + "bin/"
run_exe      = run_dir + "summa.exe"

# Run Info
NSites = len(Site_ID_all)
NIDs   = len(Run_IDs)
#print NSites
#print NIDs

#if not NIDs==(NPruns*NSites):
#    sys.exit("Number of Run_IDs must equal NPruns")

#####################################################################################
# Loop through each Site (Index from zero)
#####################################################################################
cSite = 0 # Index of current Site
while (cSite < NSites):
        
    # Define Site Info
    c_Site_ID = Site_ID_all[cSite]
    #print c_Site_ID
    
    #####################################################################################
    # Loop through each Run_ID for site (Index from zero)
    #####################################################################################
    cRID  = 0 # Index of current Run_IDs
    if jobrun == 3: # Open file for writing to (overwrite anything already there)
        fin = open(argument_file,'w')

    while (cRID < NIDs):
        #print cRID
        
        # Define paths
        cRID_char = "R_" + str(Run_IDs[cRID])
        c_fileManager    = settings_dir + c_Site_ID + "/indiv_runs/" + cRID_char + "/summa_fileManager_" + c_Site_ID + ".txt"
        c_output_dir     = output_dir + c_Site_ID + "/indiv_runs/" + cRID_char
        run_output       = c_output_dir + "/Run_output.txt"
        print c_fileManager 
        # Check Run files exists
        if not os.path.exists(c_fileManager):
             sys.exit("Run ID %s for site %s doesn't exist" % (cRID_char,c_Site_ID))
       
        if jobrun == 1: # Submit to command line
            if runJobsSerial==1:
            	run_exe_input = run_exe + " " + exp_name + " " + c_fileManager + " > " + run_output
            elif runJobsSerial==2:
 	        run_exe_input = run_exe + " " + exp_name + " " + c_fileManager + " > " + run_output + " &"

	    os.system(run_exe_input)
            print "finished run " + cRID_char
        elif jobrun == 2: # Submit run to Queue
	   # Make bew pbs name file
	   pbs_file=home_dir + "QUEUE_pbs_files/" + cRID_char + ".pbs"
           # Edit pbs.cmd file
           Create_new.pbs(pbs_file,exp_name,c_fileManager,run_output,run_dir,cRID_char,your_email)
           run_exe_input = "qsub " + home_dir + "QUEUE_pbs_files/" + cRID_char + ".pbs"
           #print run_exe_input
           os.system(run_exe_input)
           #print "finished run " + cRID_char
        elif jobrun == 3: # Submit Serial parallel jobs
	   # Write to argumentfile
	   fin.write(exp_name + " " + c_fileManager + " > " + run_output + "\n")
           	
        cRID +=1
    # End of Run_ID loop
   
    if jobrun == 3: # Close file if running serial
        # Close file
        fin.close()
    
    # Submit parallel jobs if needed 	
    if jobrun == 3: # Now submit all jobs in one qsub command
        print "Submitting serial parallel job to queue!" 
        os.system("qsub " + seriall_pbs)
    # End of Site loop
    cSite += 1    

print "\nFinished submiting\n"
