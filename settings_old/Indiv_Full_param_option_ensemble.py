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
import func_Restart_Create
import Create_new


# Run every possible combination  of options (now using default parameters)
# Each run is a different HRU
# Provdies full "option space"
#
# Submits each option/parameter permutation as a single individual run

## All available options. Use this as a guide to edit below, or copy and paste, then edit.
#
#soilCatTbl         =          ['ROSETTA','STAS','STAS-RUC']  #! (03) soil-category dateset
#vegeParTbl         =          ['USGS','MODIFIED_IGBP_MODIS_NOAH']  #! (04) vegetation category dataset
#soilStress         =          ['NoahType', 'CLM_Type', 'SiB_Type']  #! (05) choice of function for the soil moisture control on stomatal resistance
#stomResist         =          ['BallBerry', 'Jarvis', 'simpleResistance']  #! (06) choice of function for stomatal resistance
##! ***********************************************************************************************************************
#num_method         =          ['itertive','non_iter','itersurf']  #! (07) choice of numerical method
#fDerivMeth         =          ['numerical','analytic']  #! (08) method used to calculate flux derivatives
#LAI_method         =          ['monTable','specified']  #! (09) method used to determine LAI and SAI
#f_Richards         =          ['moisture','mixdform']  #! (10) form of Richard's equation
#groundwatr         =          ['qTopmodl','bigBuckt','noXplict']  #! (11) choice of groundwater parameterization
#hc_profile         =          ['constant','pow_prof']  #! (12) choice of hydraulic conductivity profile
#bcUpprTdyn         =          ['presTemp','nrg_flux']  #! (13) type of upper boundary condition for thermodynamics
#bcLowrTdyn         =          ['presTemp','zeroFlux']  #! (14) type of lower boundary condition for thermodynamics
#bcUpprSoiH         =          ['presHead','liq_flux']  #! (15) type of upper boundary condition for soil hydrology
#bcLowrSoiH         =          ['drainage','presHead','bottmPsi','zeroFlux']  #! (16) type of lower boundary condition for soil hydrology
#veg_traits         =          ['Raupach_BLM1994','CM_QJRMS1998','vegTypeTable']  #! (17) choice of parameterization for vegetation roughness length and displacement height
#canopyEmis         =          ['simplExp','difTrans']  #! (18) choice of parametrization for canopy emissivity
#snowIncept         =          ['stickySnow','lightSnow']  #! (19) choice of parameterization for snow interception
#windPrfile         =          ['exponential','logBelowCanopy']  #! (20) choice of wind profile through the canopy
#astability         =          ['standard','louisinv','mahrtexp']  #! (21) choice of stability function
#canopySrad         =          ['noah_mp','CLM_2stream','UEB_2stream','NL_scatter','BeersLaw']  #! (22) choice of canopy shortwave radiation method
#alb_method         =          ['conDecay','varDecay']  #! (23) choice of albedo representation
#compaction         =          ['consettl','anderson']  #! (24) choice of compaction routine
#snowLayers         =          ['CLM_2010','jrdn1991']  #! (25) choice of method to combine and sub-divide snow layers
#thCondSnow         =          ['tyen1965','melr1977','jrdn1991','smnv2000']  #! (26) choice of thermal conductivity representation for snow
#thCondSoil         =          ['funcSoilWet','mixConstit','hanssonVZJ']  #! (27) choice of thermal conductivity representation for soil
#spatial_gw         =          ['localColumn','singleBasin']  #! (28) choice of method for the spatial representation of groundwater
#subRouting         =          ['timeDlay','qInstant']  #! (29) choice of method for sub-grid routing
#snowDenNew         =          ['constDens','anderson','hedAndPom','pahaut_76']  #! (30) choice of method for new snow density

############################################
# Begin User Settings
############################################	

# Define Paths
main_dir = "/home/wayandn/summa/"
settings_dir = main_dir + "settings/"
input_dir    = main_dir + "input/"
output_dir   = main_dir + "output/"
indiv_runs   = "indiv_runs/"
run_exe = main_dir + "bin/summa.exe"

# Define Sites to Use
Site_ID_all = ["SNQ_ALL"]

# Define first run number 
First_Run_number = 40000

# SNQ_ALL Recent
#datestart = "2012-10-01 01:00"
#dateend   = "2015-05-11 21:30"

# SNQ_ALL Historical hourly
#datestart = "2000-10-01 00:00"
#dateend   = "2015-05-11 21:00"

# SNQ_ALL 1989-2015
datestart = "2002-10-01 01:00"
#dateend   = "2015-05-11 21:00"
dateend   = "2010-10-01 21:00"


# Name of forcing file to use (found in input_dir/Site_ID_all/)
#forcing_file = "summa_zForcingInfo_SNQ_NWAC.txt"
#forcing_file = "SNQ_Hist_Historic_WY_1989_2015.txt"
forcing_file = "summa_zForcingInfo_Historic_hrly.txt"

# Specify level of variables to output (1: HIGH (i.e. many variables), 2: LOW (i.e. only most "important" variables)
Var_out_lev = 2

# Define base HRU to use
base_hru_num = 1001 

# User defines model options to create settings for (all combinations)
soilCatTbl         =          ['ROSETTA']  #! (03) soil-category dateset
vegeParTbl         =          ['USGS']  #! (04) vegetation category dataset
soilStress         =          ['NoahType']  #! (05) choice of function for the soil moisture control on stomatal resistance
stomResist         =          ['BallBerry']  #! (06) choice of function for stomatal resistance
#! ***********************************************************************************************************************
num_method         =          ['itertive']  #! (07) choice of numerical method
fDerivMeth         =          ['analytic']  #! (08) method used to calculate flux derivatives
LAI_method         =          ['specified']  #! (09) method used to determine LAI and SAI
f_Richards         =          ['mixdform']  #! (10) form of Richard's equation
groundwatr         =          ['noXplict']  #! (11) choice of groundwater parameterization
hc_profile         =          ['pow_prof']  #! (12) choice of hydraulic conductivity profile
bcUpprTdyn         =          ['nrg_flux']  #! (13) type of upper boundary condition for thermodynamics
bcLowrTdyn         =          ['zeroFlux']  #! (14) type of lower boundary condition for thermodynamics
bcUpprSoiH         =          ['liq_flux']  #! (15) type of upper boundary condition for soil hydrology
bcLowrSoiH         =          ['drainage']  #! (16) type of lower boundary condition for soil hydrology
veg_traits         =          ['CM_QJRMS1998']  #! (17) choice of parameterization for vegetation roughness length and displacement height
canopyEmis         =          ['difTrans']  #! (18) choice of parametrization for canopy emissivity
snowIncept         =          ['stickySnow']  #! (19) choice of parameterization for snow interception
windPrfile         =          ['logBelowCanopy']  #! (20) choice of wind profile through the canopy
astability         =          ['mahrtexp']  #! (21) choice of stability function
canopySrad         =          ['CLM_2stream']  #! (22) choice of canopy shortwave radiation method
alb_method         =          ['varDecay']  #! (23) choice of albedo representation
compaction         =          ['anderson']  #! (24) choice of compaction routine
snowLayers         =          ['CLM_2010']  #! (25) choice of method to combine and sub-divide snow layers
thCondSnow         =          ['jrdn1991']  #! (26) choice of thermal conductivity representation for snow
thCondSoil         =          ['mixConstit']  #! (27) choice of thermal conductivity representation for soil
spatial_gw         =          ['localColumn']  #! (28) choice of method for the spatial representation of groundwater
subRouting         =          ['timeDlay']  #! (29) choice of method for sub-grid routing
snowDenNew         =          ['hedAndPom']  #! (30) choice of method for new snow density

# User defines parameters to hold constant and parameters to allow to vary

# Constant parameters (applied to all runs)
#new_param_all = ['a_sn','b_sn','c_sn','tempCritRain','tempRangeTimestep','heightCanopyTop','heightCanopyBottom','winterSAI','summerLAI','maxMassVegetation','f_impede','rootingDepth','zmax']
#new_param_val = [ 80.0,    1.0,    16.0,        273.16,                 0.5,           0.05,             0.01,            0.01,         0.5,                  1,         0, 0.1, 0.1]

new_param_all = ['heightCanopyTop','heightCanopyBottom','winterSAI','summerLAI','maxMassVegetation','f_impede','rootingDepth','zmax']
new_param_val = [             0.05,             0.01,            0.01,         0.5,                  1,         0, 0.1, 0.1]

# Parameters to vary
#param_2_vary = ['tempCritRain','tempRangeTimestep','a_sn','b_sn','c_sn','densScalGrowth','tempScalGrowth','grainGrowthRate','densScalOvrbdn','tempScalOvrbdn']
#param_2_vary = []
# HedAndPom
param_2_vary = ['tempCritRain','tempRangeTimestep','densScalOvrbdn','tempScalOvrbdn','newSnowDenMin','newSnowDenMult','newSnowDenScal']
#Pahaut 1976
#param_2_vary = ['tempCritRain','tempRangeTimestep','a_sn','b_sn','c_sn','densScalOvrbdn','tempScalOvrbdn']
# anderson
#param_2_vary = ['tempCritRain','tempRangeTimestep','densScalOvrbdn','tempScalOvrbdn','newSnowDenMin','d_sn']
#constantDens
#param_2_vary = ['tempCritRain','tempRangeTimestep','constSnowDen','densScalOvrbdn','tempScalOvrbdn']



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

############################################
# End User Settings
############################################

# Store all decisions
Decisions_ALL = [soilCatTbl,vegeParTbl,soilStress,stomResist,num_method,fDerivMeth,LAI_method,f_Richards,groundwatr,hc_profile,bcUpprTdyn,bcLowrTdyn,bcUpprSoiH,bcLowrSoiH,veg_traits,canopyEmis,snowIncept,windPrfile,astability,canopySrad,alb_method,compaction,snowLayers,thCondSnow,thCondSoil,spatial_gw,subRouting,snowDenNew];

# Get all possible permutations
Option_permutations = list(itertools.product(*Decisions_ALL))

# Determine total number of runs to submit
NoptioRuns = len(Option_permutations)
NparamRuns = len(Param_valu)
NrunsTot = NoptioRuns * NparamRuns
print("Total number of options configurations ",NoptioRuns)
print("Total number of param configurations ",NparamRuns)
print("Total number of Runs ",NrunsTot)

# Make list of run IDs based on length of NrunsTot
Run_IDs = range(1,NrunsTot+1)
Run_IDs = numpy.array(Run_IDs) + First_Run_number - 1
Run_IDs = Run_IDs.tolist()

# Run Info
NSites = len(Site_ID_all)


# For each cite
cSite = 0 # Index of current Site
while (cSite < NSites):

    # Define Site Info
    c_Site_ID = Site_ID_all[cSite]
    print c_Site_ID

    # For each simulation
    cRun_tot = 0 # inde of run number in Run_IDs
    cRun_opt = 0 # Index of current option configuration
    while (cRun_opt < NoptioRuns):
        #cRID_char = "R_" + str(Run_IDs[cReRun])
	#print cRID_char	

        # Get current options
        c_Decisions = Option_permutations[cRun_opt]

	# For each parameter set
	cRun_par = 0 # Index of current parameter configuration 
        while (cRun_par < NparamRuns):

		cRID_char = "R_" + str(Run_IDs[cRun_tot])
        	print cRID_char
	
		# Make directory if not exist
		#dir_new = settings_dir + c_Site_ID + "/" + indiv_runs + "/" + cRID_char
		#if not os.path.exists(dir_new):
	#		os.makedirs(dir_new)
	
		# Create each daily settings file for this simulation
        	func_Restart_Create.Create_Restart(settings_dir,input_dir,output_dir,run_exe,c_Site_ID,cRID_char,c_Decisions,Param_name,Param_valu[cRun_par],datestart,dateend,forcing_file,base_hru_num,Var_out_lev)
		
		# Update indices
		cRun_par = cRun_par + 1
		cRun_tot = cRun_tot + 1        

        # Update current option number
	cRun_opt = cRun_opt + 1

    # Update current Site number
    cSite = cSite + 1
