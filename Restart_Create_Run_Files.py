#!/usr/bin/python

# Import basic functions
import os
import shutil
import re
import sys
import datetime

# Import FUSE functions
import Create_new_V2

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
#Run_IDs = [1];

# 2) Define Sites to Use
Site_ID_all = ["SNQ13"]
#Site_ID_all = ["SNQ14C"]

# Extra) path to Restart files
#
# Careful, you must manually updat this in Creat_new_V2.py!!!
# need to chane this to be automatic 11/20/2014
#
# SNQ14C
#ReICpath = settings_dir + Site_ID_all[0] + "/Restart_ICs/"
#ReICpath = settings_dir + Site_ID_all[0] + "/Restart_Default/"
#ReICpath  = settings_dir + Site_ID_all[0] + "/Restart_cons_alb_com/" 
#ReICpath  = settings_dir + Site_ID_all[0] + "/Restart_Cac_noSnow/"

#SNQ13
#ReICpath  = settings_dir + Site_ID_all[0] + "/Restart_Default/"
ReICpath  = settings_dir + Site_ID_all[0] + "/Restart_noSnow/"

# 3) Define start and stop time (make sure only one date is uncommented!)
# Now taken from IC files ( see below )

#print Site_ID_all

# 4) Define Parameters to modify from default values and Define values for each new_param_all
# SNQ14C restart: Like a snowboard
#new_param_all = ['heightCanopyTop','heightCanopyBottom','winterSAI','summerLAI','maxMassVegetation','f_impede']
#new_param_val = [           0.000001,             0.0000001,            0.00,         0.00,                  0,  0]

new_param_all = ['heightCanopyTop','heightCanopyBottom','winterSAI','summerLAI','maxMassVegetation','f_impede','rootingDepth','zmax'] #,'theta_sat', 'theta_res',  'vGn_alpha',  'vGn_n','k_soil']
new_param_val = [           0.05,             0.01,            0.01,         0.5,                  1,         0, 0.1, 0.1] #,          0.401,     0.136,          -0.84,    1.30,   0.0015]


# MFS
#new_param_all = ['heightCanopyTop','heightCanopyBottom','winterSAI']
#new_param_val = [          0.4,             0.001,               1]

# LNF
#new_param_all = ['z0Snow','tempCritRain','heightCanopyTop','heightCanopyBottom','winterSAI']
#new_param_val = [1,               273.14,          0.2,             0.01,               1]

# 5) Define which paramter to allow to vary (between min and max in snow_zLocalParamInfo) Note: this overwrites the value given in new_param_val.
param_2_vary  = 'mw_exp' 

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
alb_method         =          'conDecay'  #! (F-17) choice of albedo representation
compaction         =          'consettl'  #! (F-18) choice of compaction routine
snowLayers         =          'jrdn1991'  #! (F-19) choice of method to combine and sub-divide snow layers
thermlcond         =          'jrdn1991'  #! (F-20) choice of thermal conductivity representation
spatial_gw         =       'localColumn'  #! (F-21) choice of method for the spatial representation of groundwater
subRouting         =          'timeDlay'  #! (F-22) choice of method for sub-grid routing

Decisions_ALL = [soilCatTbl,vegeParTbl,soilStress,stomResist,num_method,fDerivMeth,LAI_method,f_Richards,groundwatr,hc_profile,bcUpprTdyn,bcLowrTdyn,bcUpprSoiH,bcLowrSoiH,veg_traits,canopyEmis,snowIncept,windPrfile,astability,canopySrad,alb_method,compaction,snowLayers,thermlcond,spatial_gw,subRouting];


# Checks
#if not NIDs==(NPruns*NSites):
#    sys.exit("Number of Run_IDs must equal NPruns")

# Get list of restart files

ICfiles_list = os.listdir(ReICpath)
ICfiles_list.sort()
#print ICfiles_list
#print len(ICfiles_list)
#print ICfiles_list[0]

# Make list of run IDs based on length of ICfiles_list
Run_IDs = range(1,len(ICfiles_list)+1)
#Run_IDs = range(1,11)
#print len(Run_IDs)

# Run Info
NPruns = len(Run_IDs)
NSites = len(Site_ID_all)

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

    # If more than one NPruns, then get value to vary
    #if NPruns > 1:
	# Get Vaules of param_2_vary from LocalParamInfo
	#Pvals =  Create_new_V2.GetParamVals(param_2_vary,NPruns,settings_dir,c_Site_ID)
	#print Pvals
	## Find Index specifed parameters (new_param_all)
	#Iparam = new_param_all.index(param_2_vary)
    
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
	#if NPruns > 1:
	#	# Update new paramter value for param_2_vary in new_param_val
	#	new_param_val[Iparam] = Pvals[cPR]
			
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
	IC_file = ICfiles_list[cPR]
        Create_new_V2.file_Manager(settings_dir,input_dir,output_dir,c_Site_ID,cRID_char,IC_file)
        
	# Create the snow Desicians file
	
	Datein = datetime.datetime.strptime(IC_file, "%Y-%m-%d_%H_%M")	
	Datestart = Datein + datetime.timedelta(minutes=30)
	Dateend   = Datein + datetime.timedelta(days=1) # Restart time period hard coded here
	
	datestart = Datestart.strftime("%Y-%m-%d %H:%M")
	dateend   = Dateend.strftime("%Y-%m-%d %H:%M")

	#print datestart
	#print dateend

	#sys.exit()

	#fulldate = IC_file.split('_')
	#yyyymmdd = fulldate[0].split('-')
	#cdd = int(yyyymmdd[2])
	#ndd = cdd + 1;
	
	#datestart = fulldate[0] + " 06:30"
	#dateend   = yyyymmdd[0] + "-" + yyyymmdd[1] + "-" + str(ndd).zfill(2) + " 06:00"

	#print datestart
	#print dateend

	#sys.exit()

	Create_new_V2.Desicions(Decisions_ALL,settings_dir,c_Site_ID,cRID_char,datestart,dateend)

        # Edit Parameter settings for current run
        Create_new_V2.ParamTrial(new_param_all,new_param_val,param_2_vary,NPruns,settings_dir,c_Site_ID,cRID_char)

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
