#!/usr/bin/python

import os
import shutil
import re
import sys
import datetime
import numpy
import itertools

# Import FUSE functions
import func_Restart_Create
import Create_new_V2
import Create_new


def Create_Restart(settings_dir,input_dir,output_dir,run_exe,c_Site_ID,cRID_char,c_Decisions,new_param_all,new_param_val,datestart,dateend):
	
	# Define new run paths for current run
	c_output_dir   = output_dir   + c_Site_ID + "/" + cRID_char
	c_settings_dir = settings_dir + c_Site_ID + "/" + cRID_char
	run_output     = c_output_dir + "/Run_output.txt"

	# Make needed directories
	if not os.path.exists(c_output_dir):
		os.makedirs(c_output_dir)

	if not os.path.exists(c_settings_dir):
		os.makedirs(c_settings_dir)

	# Create the file Manager
	Create_new.file_Manager(settings_dir,input_dir,output_dir,c_Site_ID,cRID_char)

	# Create the Desicians file
	Create_new.Desicions(c_Decisions,settings_dir,c_Site_ID,cRID_char,datestart,dateend)

	# Edit Parameter settings for current run
	Create_new.ParamTrial(new_param_all,new_param_val,settings_dir,c_Site_ID,cRID_char)
	
	# run output file (overwrites previous)
	if not os.path.exists(run_output):
		ftemp = open(run_output,'w')
		ftemp.close() # Simple way to make a file

	# See submit_FUSE_SNOW_Runs.py to submit Runs   
 