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
import Create_new_V2
import Create_new


# Run every possible combination  of options (now using default parameters)
# Each run is a different HRU
# Provdies full "option space"

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
run_exe = main_dir + "bin/summa.exe"

# Define Sites to Use
Site_ID_all = ["SNQ_ALL"]

# Define first run number 
First_Run_number = 30000

# SNQ_ALL Recent
datestart = "2012-10-01 00:00"
dateend   = "2015-05-11 21:30"

# All available options
soilCatTbl         =          ['ROSETTA']  #! (03) soil-category dateset
vegeParTbl         =          ['USGS']  #! (04) vegetation category dataset
soilStress         =          ['CLM_Type']  #! (05) choice of function for the soil moisture control on stomatal resistance
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
canopyEmis         =          ['simplExp']  #! (18) choice of parametrization for canopy emissivity
snowIncept         =          ['stickySnow']  #! (19) choice of parameterization for snow interception
windPrfile         =          ['logBelowCanopy']  #! (20) choice of wind profile through the canopy
astability         =          ['standard']  #! (21) choice of stability function
canopySrad         =          ['CLM_2stream']  #! (22) choice of canopy shortwave radiation method
alb_method         =          ['conDecay']  #! (23) choice of albedo representation
compaction         =          ['consettl','anderson']  #! (24) choice of compaction routine
snowLayers         =          ['CLM_2010','jrdn1991']  #! (25) choice of method to combine and sub-divide snow layers
thCondSnow         =          ['tyen1965']  #! (26) choice of thermal conductivity representation for snow
thCondSoil         =          ['mixConstit']  #! (27) choice of thermal conductivity representation for soil
spatial_gw         =          ['localColumn']  #! (28) choice of method for the spatial representation of groundwater
subRouting         =          ['timeDlay']  #! (29) choice of method for sub-grid routing
snowDenNew         =          ['constDens','anderson','hedAndPom','pahaut_76']  #! (30) choice of method for new snow density

############################################
# End User Settings
############################################



# Store all decisions
Decisions_ALL = [soilCatTbl,vegeParTbl,soilStress,stomResist,num_method,fDerivMeth,LAI_method,f_Richards,groundwatr,hc_profile,bcUpprTdyn,bcLowrTdyn,bcUpprSoiH,bcLowrSoiH,veg_traits,canopyEmis,snowIncept,windPrfile,astability,canopySrad,alb_method,compaction,snowLayers,thCondSnow,thCondSoil,spatial_gw,subRouting,snowDenNew];



# Get all possible permutations
Option_permutations = list(itertools.product(*Decisions_ALL))



# Determine total number of runs to submit
NrunsTot = len(Option_permutations)
print(NrunsTot)

# Make list of run IDs based on length of NrunsTot
Run_IDs = range(1,NrunsTot+1)
Run_IDs = numpy.array(Run_IDs) + First_Run_number
Run_IDs = Run_IDs.tolist()

# Run Info
NSites = len(Site_ID_all)



## Parameter info here (for now just default parameters for each option)

# Default Parameters to modify from default values and Define values for each new_param_all
new_param_all = ['heightCanopyTop','heightCanopyBottom','winterSAI','summerLAI','maxMassVegetation','f_impede','rootingDepth','zmax'] #,'theta_sat', 'theta_res',  'vGn_alpha',  'vGn_n','k_soil']
new_param_val = [           0.05,             0.01,            0.01,         0.5,                  1,         0, 0.1, 0.1] #,          0.401,     0.136,          -0.84,    1.30,   0.0015]


# Get Values of param_2_vary from LocalParamInfo file in settings
#Pvals =  Create_new.GetParamVals(param_2_vary,NPruns,settings_dir,c_Site_ID)
#print Pvals
# Find Index specified parameters (new_param_all)
#Iparam = new_param_all.index(param_2_vary)


# For each cite
cSite = 0 # Index of current Site
while (cSite < NSites):

    # Define Site Info
    c_Site_ID = Site_ID_all[cSite]
    print c_Site_ID

    # For each simulation
    cReRun = 0; # Index of current run
    while (cReRun < NrunsTot):
        cRID_char = "R_" + str(Run_IDs[cReRun])
	print cRID_char	

        # Get current options
        c_Decisions = Option_permutations[cReRun]
        #print(c_Decisions)

        # Update parameters 
        #new_param_val[Iparam] = Pvals[cReRun]

        # Create each daily settings file for this Restart simulation
        func_Restart_Create.Create_Restart(settings_dir,input_dir,output_dir,run_exe,c_Site_ID,cRID_char,c_Decisions,new_param_all,new_param_val,datestart,dateend)
        
        # Submit this Restart simulations

	cReRun = cReRun + 1

    cSite = cSite + 1
