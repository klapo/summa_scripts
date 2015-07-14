#!/usr/bin/python

# Import basic functions
import os
import shutil
import re
import sys

# Import FUSE functions
import Create_new

####################################################################################
# Create_Run_Files.py
####################################################################################
## Description ##
# Sets up multiple paramter/option runs for the FUSE_SNOW model. Each Run creates a new folder under /settings/SITE/R_X
# If only one Run number is specified, then no values are updated (i.e. param_2_vary is ignored)
#
## Instructions ##
# 1) Modify Input Values  below
# 2) Run ./Create_Run_Files.py
#
## Input ##
#
# Run_IDs				- Number values for new created run files (i.e R_46)
# Site_ID_all				- Names of all sites to be included, same as site folder names, (Requires Input, Settings, and output folder set up)
# new_param_all				- Paramter names to vary, (From /settings/snow_zParamInfo.txt)
# N_param_itr				- Number of values to vary each paramter, (divided evenly between min and max, defined in snow_zParamInfo.txt)
#
## File Info ##
# Created 1/8/2013 - Nic Wayand (nicway@u.washington.edu)
####################################################################################

def my_range(start, end, step):
        while start <= end:
            yield start
            start += step

#####################################################################################
# Define Variables/Parameteres Used
#####################################################################################
# cPr                        - Index of current Multiparameter run set
# c_new_param		     - Name of current parameter
# NPruns                     - Total number of Multiparamter runs
# cSite			     - Index of current Site
# c_Site_ID		     - Name of current Site
# NSites		     - Total number of Sites

#####################################################################################
# Define Multi-run Info - Check all 6 Required Inputs!
#####################################################################################

# Define Paths
main_dir = "/home/wayandn/summa/"
settings_dir = main_dir + "settings/"
input_dir    = main_dir + "input/"
output_dir   = main_dir + "output/"
run_exe = main_dir + "bin/summa.exe"

# 1) Run IDs
#Run_IDs = my_range(20,30,1);
Run_IDs = [2];

# 2) Define Sites to Use
Site_ID_all = ["SNQ_ALL"]
#Site_ID_all = ["SNQ14C"]

# 3) Defind start and stop time (make sure only one date is uncommented!)
# SNQ13
#datestart = "2012-10-02 00:00"
#dateend   = "2013-09-30 23:00"
# SNQ14C wrf
#datestart = "2013-10-01 00:00"
#dateend   = "2014-09-11 00:00"
# SNQ14C
#datestart = "2013-10-01 01:00"
#dateend   = "2014-05-18 00:30"

# CDP 1993 to 2011
#datestart = "1993-08-01 02:00"
#dateend   = "2011-07-31 22:00"

# SNQ_ALL
#datestart = "2012-10-01 00:00"
#dateend   = "2015-05-11 21:30"

# SNQ_ALL Historic
datestart = "1989-12-26 00:00"
dateend   = "2012-10-01 00:00"


# SNQ14C
#datestart = "2013-10-01 00:30"
#dateend   = "2014-05-18 22:00"
# SNQ14C restart feb 11th
#datestart = "2014-02-11 13:00"
#dateend   = "2014-02-28 22:00"
# SNQ14C restart 6am snowboard
#datestart = "2013-10-01 00:00"
#dateend   = "2013-10-02 00:00"
#
# MFS
#datestart = "2012-10-16 00:00"
#dateend   = "2013-05-03 23:30"
# LNF
#datestart = "2005-11-01 00:00"
#dateend   = "2006-01-30 18:00"

#print Site_ID_all

# 4) Define Parameters to modify from default values and Define values for each new_param_all
# SNQ or SNQ14C
new_param_all = ['heightCanopyTop','heightCanopyBottom','winterSAI','summerLAI','maxMassVegetation','f_impede','rootingDepth', 'zmax'] #,'theta_sat', 'theta_res',  'vGn_alpha',  'vGn_n','k_soil']
new_param_val = [           0.05,             0.01,            0.01,         0.5,                  1,         0, 0.1, 0.1] #,          0.401,     0.136,          -0.84,    1.30,   0.0015]

# MFS
#new_param_all = ['heightCanopyTop','heightCanopyBottom','winterSAI']
#new_param_val = [          0.4,             0.001,               1]

# LNF
#new_param_all = ['z0Snow','tempCritRain','heightCanopyTop','heightCanopyBottom','winterSAI']
#new_param_val = [1,               273.14,          0.2,             0.01,               1]

# 5) Define which paramter to allow to vary (between min and max in snow_zLocalParamInfo) Note: this overwrites the value given in new_param_val.
param_2_vary  = 'mw_exp' 


# Run Info
NPruns = len(Run_IDs)
NSites = len(Site_ID_all)

# 6) Define Process/Methods to change from current

soilCatTbl         =           'ROSETTA'  #! (N-01) soil-category dateset
vegeParTbl         =              'USGS'  #! (N-02) vegetation category dataset
soilStress         =          'NoahType'  #! (N-03) choice of function for the soil moisture control on stomatal resistance
stomResist         =         'BallBerry'  #! (N-04) choice of function for stomatal resistance
#! ***********************************************************************************************************************
num_method         =          'itertive'  #! (F-01) choice of numerical method
fDerivMeth         =          'analytic'  #! (F-02) method used to calculate flux derivatives
LAI_method         =         'specified'  #! (F-03) method used to determine LAI and SAI
f_Richards         =          'mixdform'  #! (F-04) form of Richard's equation
groundwatr         =          'noXplict'  #! (F-05) choice of groundwater parameterization
hc_profile         =          'pow_prof'  #! (F-06) choice of hydraulic conductivity profile
bcUpprTdyn         =          'nrg_flux'  #! (F-07) type of upper boundary condition for thermodynamics
bcLowrTdyn         =          'zeroFlux'  #! (F-08) type of lower boundary condition for thermodynamics
bcUpprSoiH         =          'liq_flux'  #! (F-09) type of upper boundary condition for soil hydrology
bcLowrSoiH         =          'drainage'  #! (F-10) type of lower boundary condition for soil hydrology
veg_traits         =      'CM_QJRMS1998'  #! (F-11) choice of parameterization for vegetation roughness length and displacement height
canopyEmis         =          'simplExp'  #! (F-12) choice of parameterization for canopy emissivity
snowIncept         =         'lightSnow'  #! (F-13) choice of parameterization for snow interception
windPrfile         =    'logBelowCanopy'  #! (F-14) choice of wind profile through the canopy
astability         =          'mahrtexp'  #! (F-15) choice of stability function
canopySrad         =       'CLM_2stream'  #! (F-16) choice of canopy shortwave radiation method
alb_method         =          'varDecay'  #! (F-17) choice of albedo representation
compaction         =          'anderson'  #! (F-18) choice of compaction routine
snowLayers         =          'jrdn1991'  #! (F-19) choice of method to combine and sub-divide snow layers
thermlcond         =          'jrdn1991'  #! (F-20) choice of thermal conductivity representation
spatial_gw         =       'localColumn'  #! (F-21) choice of method for the spatial representation of groundwater
subRouting         =          'timeDlay'  #! (F-22) choice of method for sub-grid routing

Decisions_ALL = [soilCatTbl,vegeParTbl,soilStress,stomResist,num_method,fDerivMeth,LAI_method,f_Richards,groundwatr,hc_profile,bcUpprTdyn,bcLowrTdyn,bcUpprSoiH,bcLowrSoiH,veg_traits,canopyEmis,snowIncept,windPrfile,astability,canopySrad,alb_method,compaction,snowLayers,thermlcond,spatial_gw,subRouting];


# Checks
#if not NIDs==(NPruns*NSites):
#    sys.exit("Number of Run_IDs must equal NPruns")

#####################################################################################
# Loop through each Site (Index from zero)
#####################################################################################
cRID  = 0 # Index of current Run_IDs
cSite = 0 # Index of current Site
while (cSite < NSites):
        
    # Define Site Info
    c_Site_ID = Site_ID_all[cSite]
    print c_Site_ID

    # If more than one NPruns, then get value to vary
    if NPruns > 1:
	# Get Vaules of param_2_vary from LocalParamInfo
	Pvals =  Create_new.GetParamVals(param_2_vary,NPruns,settings_dir,c_Site_ID)
	print Pvals
	# Find Index specifed parameters (new_param_all)
	Iparam = new_param_all.index(param_2_vary)
    
    #####################################################################################
    # Loop through each Parameter set run (Index from zero)
    #####################################################################################
    cPR = 0
    while (cPR < NPruns):
        #print cPR
        # Define current Run ID
        cRID_char = "R_" + str(Run_IDs[cRID])
	print cRID_char

        # If more than one NPruns, Update
	if NPruns > 1:
		# Update new paramter value for param_2_vary in new_param_val
		new_param_val[Iparam] = Pvals[cPR]
			
        # Define new run paths
	c_output_dir   = output_dir + c_Site_ID + "/" + cRID_char
        c_settings_dir = settings_dir + c_Site_ID + "/" + cRID_char
        run_output     = c_output_dir + "/Run_output.txt"
        
        # Make needed directories
        if not os.path.exists(c_output_dir):
            os.makedirs(c_output_dir)
#        else:
#            sys.exit("This Run ID already exits, pick a new one")

	if not os.path.exists(c_settings_dir):
            os.makedirs(c_settings_dir)
 #       else:
 #           sys.exit("This Run ID already exits, pick a new one")


        ## Now create 5 needed files for current Run ID

        # Create the file Manager
        Create_new.file_Manager(settings_dir,input_dir,output_dir,c_Site_ID,cRID_char)
        
	# Create the snow Desicians file
	Create_new.Desicions(Decisions_ALL,settings_dir,c_Site_ID,cRID_char,datestart,dateend)

        # Edit Parameter settings for current run
        Create_new.ParamTrial(new_param_all,new_param_val,param_2_vary,NPruns,settings_dir,c_Site_ID,cRID_char)

        # Create run output file (overwrites previous)
        if not os.path.exists(run_output):
            ftemp = open(run_output,'w')
            ftemp.close() # Simple way to make a file

	# See submit_FUSE_SNOW_Runs.py to submit Runs    
	    
        # End of current Paramter set Run
        cPR  += 1
        cRID += 1
    # End of all Parameter set Runs
    cSite += 1
    
# End of all Sites
