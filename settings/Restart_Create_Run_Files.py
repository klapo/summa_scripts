#!/usr/bin/python

# Import basic functions
import os
import shutil
import re
import sys
import datetime
import numpy
import itertools

# Import FUSE functions
import Create_new

####################################################################################
# Restart_Create_Run_Files.py
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
# new_param_all				- Paramter names to vary, (From /settings/summa_zParamInfo.txt)
# N_param_itr				- Number of values to vary each paramter, (divided evenly between min and max, defined in summa_zParamInfo.txt)
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
#Run_IDs = [1];

# 2) Define Sites to Use
Site_ID_all = ["SNQ_ALL"]
#Site_ID_all = ["SNQ14C"]

# 3) Define time step of runs
timestep = 30; # in minutes

# Name of forcing file to use (found in input_dir/Site_ID_all/)
forcing_file = "summa_zForcingInfo_SNQ_NWAC.txt"

# Specify level of variables to output (1: HIGH (i.e. many variables), 2: LOW (i.e. only most "important" variables)
Var_out_lev = 2

# Define base HRU to use
base_hru_num = 1001

#SNQ_ALL
Restartdir = "Restart_Recent_noSnow"

# 3) Define first run number (i.e /Settings/R_X), for restart run. Number of restart runs is determined from the number of restart files
#    in the Restartdir
First_Run_number = 40000

# User defines parameters to hold constant and parameters to allow to vary

# Constant parameters (applied to all runs)
new_param_all = ['tempCritRain','tempRangeTimestep','heightCanopyTop','heightCanopyBottom','winterSAI','summerLAI','maxMassVegetation','f_impede','rootingDepth','zmax']
new_param_val = [         273.66,                 1,           0.05,             0.01,            0.01,         0.5,                  1,         0, 0.1, 0.1]

# Parameters to vary
param_2_vary  = ['densScalGrowth','tempScalGrowth','grainGrowthRate','densScalOvrbdn','tempScalOvrbdn']

# Number of samples from parameter space
Num_Sam = 3

# For each parameter to vary
Pvals  = []; # Initialize list of values
#Pnames = []; # Initialize list of names
for cP in range(0,len(param_2_vary)):
        print cP
        # Get Values of param_2_vary from LocalParamInfo file in settings
        Pvals.append(Create_new.GetParamVals(param_2_vary[cP],Num_Sam,settings_dir,Site_ID_all[0]))
        #Pnames.append(param_2_vary+new_param_all)

# Determine all posible combiations here
Option_permutations = list(itertools.product(*Pvals))

# Combine variable and constant parameters
Param_valu = []
for cP in range(0,len(Option_permutations)):
        Param_valu.append(list(Option_permutations[cP])+new_param_val)
# Combine parameter names
Param_name = param_2_vary+new_param_all


# 6) Define Process/Methods to change from current


soilCatTbl         =           'ROSETTA'  #! (03) soil-category dateset
vegeParTbl         =              'USGS'  #! (04) vegetation category dataset
soilStress         =          'NoahType'  #! (05) choice of function for the soil moisture control on stomatal resistance
stomResist         =         'BallBerry'  #! (06) choice of function for stomatal resistance
#! ***********************************************************************************************************************
num_method         =          'itertive'  #! (07) choice of numerical method
fDerivMeth         =          'analytic'  #! (08) method used to calculate flux derivatives
LAI_method         =         'specified'  #! (09) method used to determine LAI and SAI
f_Richards         =          'mixdform'  #! (10) form of Richard's equation
groundwatr         =          'noXplict'  #! (11) choice of groundwater parameterization
hc_profile         =          'pow_prof'  #! (12) choice of hydraulic conductivity profile
bcUpprTdyn         =          'nrg_flux'  #! (13) type of upper boundary condition for thermodynamics
bcLowrTdyn         =          'zeroFlux'  #! (14) type of lower boundary condition for thermodynamics
bcUpprSoiH         =          'liq_flux'  #! (15) type of upper boundary condition for soil hydrology
bcLowrSoiH         =          'drainage'  #! (16) type of lower boundary condition for soil hydrology
veg_traits         =      'CM_QJRMS1998'  #! (17) choice of parameterization for vegetation roughness length and displacement height
canopyEmis         =          'simplExp'  #! (18) choice of parameterization for canopy emissivity
snowIncept         =         'lightSnow'  #! (19) choice of parameterization for snow interception
windPrfile         =    'logBelowCanopy'  #! (20) choice of wind profile through the canopy
astability         =          'mahrtexp'  #! (21) choice of stability function
canopySrad         =       'CLM_2stream'  #! (22) choice of canopy shortwave radiation method
alb_method         =          'varDecay'  #! (23) choice of albedo representation
compaction         =          'anderson'  #! (24) choice of compaction routine
snowLayers         =          'jrdn1991'  #! (25) choice of method to combine and sub-divide snow layers
thCondSnow         =          'jrdn1991'  #! (26) choice of thermal conductivity representation for snow
thCondSoil         =        'mixConstit'  #! (27) choice of thermal conductivity representation for soil
spatial_gw         =       'localColumn'  #! (28) choice of method for the spatial representation of groundwater
subRouting         =          'timeDlay'  #! (29) choice of method for sub-grid routing
snowDenNew         =         'pahaut_76'  #! (30) choice of method for new snow density

# Store all decisions
Decisions_ALL = [soilCatTbl,vegeParTbl,soilStress,stomResist,num_method,fDerivMeth,LAI_method,f_Richards,groundwatr,hc_profile,bcUpprTdyn,bcLowrTdyn,bcUpprSoiH,bcLowrSoiH,veg_traits,canopyEmis,snowIncept,windPrfile,astability,canopySrad,alb_method,compaction,snowLayers,thCondSnow,thCondSoil,spatial_gw,subRouting,snowDenNew];

# Get list of restart files
ReICpath  = settings_dir + Site_ID_all[0] + "/" + Restartdir + "/"
ICfiles_list = os.listdir(ReICpath)
ICfiles_list.sort()
#print ICfiles_list
#print len(ICfiles_list)
#print ICfiles_list[0]

# Make list of run IDs based on length of ICfiles_list
Run_IDs = range(1,len(ICfiles_list)+1)
Run_IDs = numpy.array(Run_IDs) + First_Run_number
Run_IDs = Run_IDs.tolist()
#Run_IDs = range(1,11)
#print len(Run_IDs)

# Run Info
NPruns = len(Run_IDs) # Number of restart runs
NSites = len(Site_ID_all) # Number of cites

#sys.exit()
 



#####################################################################################
# Loop through each Site (Index from zero)
#####################################################################################
cRID  = 0 # Index of current Run_IDs
cSite = 0 # Index of current Site
while (cSite < NSites):
        
    # Define Site Info
    c_Site_ID = Site_ID_all[cSite]
    print c_Site_ID

    #####################################################################################
    # Loop through each Parameter set run (Index from zero)
    #####################################################################################
    cPR = 0
    while (cPR < NPruns):
        #print cPR
        # Define current Run ID
        cRID_char = "R_" + str(Run_IDs[cRID])
	print cRID_char
			
        # Define new run paths
	c_output_dir   = output_dir + c_Site_ID + "/" + cRID_char
        c_settings_dir = settings_dir + c_Site_ID + "/" + cRID_char
        run_output     = c_output_dir + "/Run_output.txt"
        Flist_file     = settings_dir + c_Site_ID + "/" + cRID_char + "/summa_zForcingFileList.txt"
        Alist_file     = settings_dir + c_Site_ID + "/" + cRID_char + "/summa_zLocalAttributes.txt"


        # Make needed directories
        if not os.path.exists(c_output_dir):
            os.makedirs(c_output_dir)

	if not os.path.exists(c_settings_dir):
            os.makedirs(c_settings_dir)

        ## Now create 5 needed files for current Run ID

        # Create the file Manager
	IC_file = ICfiles_list[cPR]
        #Create_new_V2.file_Manager(settings_dir,input_dir,output_dir,c_Site_ID,cRID_char,IC_file,Restartdir)
        Create_new.file_manager_restart(settings_dir,input_dir,output_dir,c_Site_ID,cRID_char,IC_file,Restartdir,Var_out_lev)
	
	# Get length of restart simulation
	Datein    = datetime.datetime.strptime(IC_file, "%Y-%m-%d_%H_%M")	
	Datestart = Datein + datetime.timedelta(minutes=timestep)
	Dateend   = Datein + datetime.timedelta(days=1) # Restart time period hard coded here
	
	datestart = Datestart.strftime("%Y-%m-%d %H:%M")
	dateend   = Dateend.strftime("%Y-%m-%d %H:%M")

	# Create Desicions file
	Create_new.Desicions(Decisions_ALL,settings_dir,c_Site_ID,cRID_char,datestart,dateend)

	# Create the Parameter settings files (uses multiple HRUs for each parameter set)
        Create_new.ParamTrial_Multi_hru(Param_name,Param_valu,settings_dir,c_Site_ID,cRID_char)

	# Create the Forcing file
        NHRUs = len(Param_valu)
        Create_new.Forcing_file(c_Site_ID,Flist_file,forcing_file,base_hru_num,NHRUs)

        # Create the Local Attributes file
        Create_new.Local_Attributes_file(Alist_file,base_hru_num,NHRUs)

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
