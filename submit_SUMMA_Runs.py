#!/usr/bin/python

# Import
import os
import sys
import Create_new

####################################################################################
# submit_SUMMA_Runs.py
####################################################################################
## Description ##
# Submits indivual paramter runs to be run in parellel
#
## Instructions ##
# 1) Modify Input Values  below
# 2) Run ./submit_SUMMA_Runs.py
#
## Input ##
#
# Site_ID_all  				- Site ID
# Run_IDs				- Run ID values to submit
# exp_name				- Name of experiment (identifyer for output filename, also used to merge multiple output netcdf files together)
# jobrun				- Option to run model on 1) Command line, or 2) On Queue
#
## File Info ##
# Created 1/8/2013 - Nic Wayand (nicway@u.washington.edu)
####################################################################################

#####################################################################################
# Define Variables/Parameteres Used
#####################################################################################


#####################################################################################
# User Options - CHECK ALL 4 Required Inputs!
#####################################################################################

# 1) Define Sites to Use
Site_ID_all = ["SNQ_ALL"]

# 2) Run ID
#Run_IDs     = [5] #,21,23,24,25,26,27,28,29,30,31,32,33,34,35,36,37,38,39,40,41,42,43,44,45,46,47,48,49,50,51,52,53,54]
Run_IDs = range(1001,1952)
#Run_IDs = range(1,364)

# 3) Experiment Name
exp_name    = "Rec_Rest_nosnow"

# 4) Run on Command line or in Queue?
jobrun 	    = 1 # 1 = Command line, 2 = Queue
# Name of pbs file (if option 2 is used)
pbs_file    = "/home/wayandn/pbs.cmd"
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
    while (cRID < NIDs):
        #print cRID
        
        # Define paths
        cRID_char = "R_" + str(Run_IDs[cRID])
        c_fileManager    = settings_dir + c_Site_ID + "/" + cRID_char + "/summa_fileManager_" + c_Site_ID + ".txt"
        c_output_dir     = output_dir + c_Site_ID + "/" + cRID_char
        run_output       = c_output_dir + "/Run_output.txt"
        print c_fileManager 
        # Check Run files exists
        if not os.path.exists(c_fileManager):
             sys.exit("Run ID %s for site %s doesn't exist" % (cRID_char,c_Site_ID))
       
        if jobrun == 1: # Submit to command line
            run_exe_input = run_exe + " " + exp_name + " " + c_fileManager + " > " + run_output + " &"
            os.system(run_exe_input)
        elif jobrun == 2: # Submit run to Queue

           # Edit pbs.cmd file
           Create_new.pbs(pbs_file,exp_name,c_fileManager,run_output,run_dir,cRID_char,your_email)
           run_exe_input = "qsub " + home_dir + "pbs.cmd "
           #print run_exe_input
           os.system(run_exe_input)

        # End of Run_ID loop
        cRID +=1
    # End of Site loop
    cSite += 1    

print "\nFinished submiting\n"
