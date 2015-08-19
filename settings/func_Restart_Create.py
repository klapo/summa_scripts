#!/usr/bin/python

import os
#import shutil
#import re
#import sys
#import datetime
#import numpy
#import itertools

# Import FUSE functions
#import func_Restart_Create
#import Create_new_V2
import Create_new


def Create_Restart(settings_dir,input_dir,output_dir,run_exe,c_Site_ID,cRID_char,c_Decisions,new_param_all,new_param_val,datestart,dateend,forcing_file,base_hru_num,Var_out_lev):
	
	# Define new run paths for current run
	c_output_dir   = output_dir   + c_Site_ID + "/" + cRID_char
	c_settings_dir = settings_dir + c_Site_ID + "/" + cRID_char
	run_output     = c_output_dir + "/Run_output.txt"
	Flist_file     = settings_dir + c_Site_ID + "/" + cRID_char + "/summa_zForcingFileList.txt"	
	Alist_file     = settings_dir + c_Site_ID + "/" + cRID_char + "/summa_zLocalAttributes.txt"	

	# Make needed directories
	if not os.path.exists(c_output_dir):
		os.makedirs(c_output_dir)

	if not os.path.exists(c_settings_dir):
		os.makedirs(c_settings_dir)

	# Create the file Manager
	Create_new.file_Manager_Multi_HRUs(settings_dir,input_dir,output_dir,c_Site_ID,cRID_char,Var_out_lev)

	# Create the Desicians file
	Create_new.Desicions(c_Decisions,settings_dir,c_Site_ID,cRID_char,datestart,dateend)
	
	# Check if we call have a single or multiple paramTrial
	if (type(new_param_all[0]) is list): # Is a list if we have multiple hru (param sets), otherwise it is a float
		
		# Creat the Parameter settings files (uses multiple HRUs for each parameter set)
		Create_new.ParamTrial_Multi_hru(new_param_all,new_param_val,settings_dir,c_Site_ID,cRID_char)
		NHRUs = len(new_param_val)
	else:

		# Creat the Parameter settings files (single param configuration (hru))
                Create_new.ParamTrial(new_param_all,new_param_val,settings_dir,c_Site_ID,cRID_char)
		NHRUs = 1;

	# Create the Forcing file
	Create_new.Forcing_file(c_Site_ID,Flist_file,forcing_file,base_hru_num,NHRUs)

	# Create the Local Attributes file
	Create_new.Local_Attributes_file(Alist_file,base_hru_num,NHRUs)	

	# run output file (overwrites previous)
	if not os.path.exists(run_output):
		ftemp = open(run_output,'w')
		ftemp.close() # Simple way to make a file

	# See submit_FUSE_SNOW_Runs.py to submit Runs   
 
    #print valtext
