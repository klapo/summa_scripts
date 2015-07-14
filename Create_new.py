#!/usr/bin/python
import os
import shutil
import re
import sys
import numpy



# Created 01/07/2013 - Nic Wayand (nicway@u.washington.edu)

# This script holds functions to make new settings files:
# snow_file_Manager_X.txt
# snow_zDecisions_X.txt
# snow_zParamTrial_X.txt
# pbd.cmd

####################################################
# Code
####################################################


# Create new file Manager
def file_Manager(settings_dir,input_dir,output_dir,c_Site_ID,cRID_char):

    # directories
    #c_Site_ID/cRID_char (i.e. SNQ/R_1)
    SITE_RUN = c_Site_ID + "/" + cRID_char

    # filename
    new_file = settings_dir + SITE_RUN + "/snow_fileManager_" + c_Site_ID + ".txt"

    # Open file for reading
    fin = open(new_file,"w")

    # Print header Info
    fin.write("SNOW_FILEMANAGER_V1.4\n! Comment line:\n! *** paths (must be in single quotes)\n")
    
    # Print paths (ORDER IS IMPORTANT!!!)
    fin.write("'" + settings_dir + "'          ! SETNGS_PATH\n")
    fin.write("'" + input_dir + c_Site_ID + "/'         ! INPUT_PATH\n")
    fin.write("'" + output_dir + SITE_RUN + "/'    ! OUTPUT_PATH\n")

    # Print control file paths
    fin.write("! *** control files (must be in single quotes)\n")

    # path that changes for each run
    fin.write("'" + SITE_RUN + "/snow_zDecisions_" + c_Site_ID + ".txt'            ! M_DECISIONS     = definition of model decisions\n")

    # paths that are the same for ALL runs
    fin.write("'snow_zTimeMeta.txt'                           ! META_TIME        = metadata for time\n"
              "'snow_zLocalAttributeMeta.txt'                 ! META_ATTR        = metadata for local attributes\n"
              "'snow_zCategoryMeta.txt'                       ! META_TYPE        = metadata for local classification of veg, soil, etc.\n"
              "'snow_zForceMeta.txt'                          ! META_FORCE       = metadata for model forcing variables\n"
              "'snow_zLocalParamMeta.txt'                     ! META_LOCALPARAM  = metadata for local model parameters\n"
              "'snow_zLocalModelVarMeta.txt'                  ! META_LOCALMVAR   = metadata for local model variables\n"
              "'snow_zLocalModelIndexMeta.txt'                ! META_INDEX       = metadata for model indices\n"
              "'snow_zBasinParamMeta.txt'                     ! META_BASINPARAM  = metadata for basin-average model parameters\n"
              "'snow_zBasinModelVarMeta.txt'                  ! META_BASINMVAR   = metadata for basin-average model variables\n")

    # paths that change for each site
    fin.write("'" + c_Site_ID + "/snow_zLocalAttributes.txt'              ! LOCAL_ATTRIBUTES = local attributes\n"
              "'" + c_Site_ID + "/snow_zLocalParamInfo.txt'             ! LOCALPARAM_INFO  = default values and constraints for local model parameters\n"
              "'" + c_Site_ID + "/snow_zBasinParamInfo.txt'             ! BASINPARAM_INFO  = default values and constraints for basin-average model parameters\n"
              "'" + c_Site_ID + "/snow_zForcingFileList.txt'                ! FORCING_FILELIST = list of files used in each HRU\n"
              "'" + c_Site_ID + "/snow_zInitialCond.txt'              ! MODEL_INITCOND  = model initial conditions\n")

    # paths that change for each run
    fin.write("'" + SITE_RUN + "/snow_zParamTrial_" + c_Site_ID + ".txt'           ! PARAMETER_TRIAL = trial values for model parameters\n")
    fin.write("'" + c_Site_ID + "_" + cRID_char + "'                                        ! OUTPUT_PREFIX\n")

    # Close file
    fin.close()

    print "Finished creating new file Manager"

    return

# Create new Decision file
def Desicions(Decisions_ALL,settings_dir,c_Site_ID,cRID_char,datestart,dateend):

    # directories

    # filename
    new_file = settings_dir + c_Site_ID + "/" + cRID_char + "/snow_zDecisions_" + c_Site_ID + ".txt"

    # Open file for reading
    fin = open(new_file,"w")

    # Print header info
    fin.write("! ***********************************************************************************************************************\n"
              "! DEFINITION OF THE MODEL DECISIONS\n"
              "! ***********************************************************************************************************************\n"
              "! This file defines the modeling decisions used.\n"
              "! NOTES:\n"
              "! (1) lines starting with ! are treated as comment lines -- there is no limit on the number of comment lines\n"
              "! (2) the name of the decision is followed by the character string defining the decision\n"
              "! (3) the simulation start/end times must be within single quotes\n"
              "! ***********************************************************************************************************************\n")
    fin.write("simulStart              '" + datestart + "'  ! (T-01) simulation start time -- must be in single quotes\n"
              "simulFinsh              '" + dateend + "'  ! (T-02) simulation end time -- must be in single quotes\n"
              "! ***********************************************************************************************************************\n")
    # Print Desicians (Decisions_ALL indexed by zero)
    fin.write("soilCatTbl                      " + Decisions_ALL[0]  + " ! (N-01) soil-category dateset\n")
    fin.write("vegeParTbl                      " + Decisions_ALL[1]  + " ! (N-02) vegetation category dataset\n")
    fin.write("soilStress                      " + Decisions_ALL[2]  + " ! (N-03) choice of function for the soil moisture control on stomatal resistance\n")
    fin.write("stomResist                      " + Decisions_ALL[3]  + " ! (N-04) choice of function for stomatal resistance\n")
    fin.write("! ***********************************************************************************************************************\n")
    fin.write("num_method                      " + Decisions_ALL[4]  + " ! (F-01) choice of numerical method\n")
    fin.write("fDerivMeth                      " + Decisions_ALL[5]  + " ! (F-02) method used to calculate flux derivatives\n")
    fin.write("LAI_method                      " + Decisions_ALL[6]  + " ! (F-03) method used to determine LAI and SAI\n")
    fin.write("f_Richards                      " + Decisions_ALL[7]  + " ! (F-04) form of Richard's equation\n")
    fin.write("groundwatr                      " + Decisions_ALL[8]  + " ! (F-05) choice of groundwater parameterization\n")
    fin.write("hc_profile                      " + Decisions_ALL[9]  + " ! (F-06) choice of hydraulic conductivity profile\n")
    fin.write("bcUpprTdyn                      " + Decisions_ALL[10]  + " ! (F-07) type of upper boundary condition for thermodynamics\n")
    fin.write("bcLowrTdyn                      " + Decisions_ALL[11]  + " ! (F-08) type of lower boundary condition for thermodynamics\n")
    fin.write("bcUpprSoiH                      " + Decisions_ALL[12]  + " ! (F-09) type of upper boundary condition for soil hydrology\n")
    fin.write("bcLowrSoiH                      " + Decisions_ALL[13]  + " ! (F-10) type of lower boundary condition for soil hydrology\n")
    fin.write("veg_traits                      " + Decisions_ALL[14]  + " ! (F-11) choice of parameterization for vegetation roughness length and displacement height\n")
    fin.write("canopyEmis                      " + Decisions_ALL[15]  + " ! (F-12) choice of parameterization for canopy emissivity\n")
    fin.write("snowIncept                      " + Decisions_ALL[16]  + " ! (F-13) choice of parameterization for snow interception\n")
    fin.write("windPrfile                      " + Decisions_ALL[17]  + " ! (F-14) choice of wind profile through the canopy\n")
    fin.write("astability                      " + Decisions_ALL[18]  + " ! (F-15) choice of stability function\n")
    fin.write("canopySrad                      " + Decisions_ALL[19]  + " ! (F-16) choice of canopy shortwave radiation method\n")
    fin.write("alb_method                      " + Decisions_ALL[20]  + " ! (F-17) choice of albedo representation\n")
    fin.write("compaction                      " + Decisions_ALL[21]  + " ! (F-18) choice of compaction routine\n")
    fin.write("snowLayers                      " + Decisions_ALL[22]  + " ! (F-19) choice of method to combine and sub-divide snow layers\n")
    fin.write("thermlcond                      " + Decisions_ALL[23]  + " ! (F-20) choice of thermal conductivity representation\n")
    fin.write("spatial_gw                      " + Decisions_ALL[24]  + " ! (F-21) choice of method for the spatial representation of groundwater\n")
    fin.write("subRouting                      " + Decisions_ALL[25]  + " ! (F-22) choice of method for sub-grid routing\n")
    # Print Desician Info
    fin.write("! ***********************************************************************************************\n"
    "! ***** description of the options available -- nothing below this point is read ****************\n"
    "! THIS IS OUTOF DATE\n"
    "! ***********************************************************************************************\n"
    "! (1) choice of numerical method\n"
    "! itertive  ! iterative\n"
    "! non_iter  ! non-iterative\n"
    "! itersurf  ! iterate only on the surface energy balance\n"
    "! -----------------------------------------------------------------------------------------------\n"
    "! (2) method used to calculate flux derivatives\n"
    "! numericl  ! numerical derivatives\n"
    "! analytic  ! analytical derivatives\n"
    "! -----------------------------------------------------------------------------------------------\n"
    "! (3) form of Richards' equation\n"
    "! moisture  ! moisture-based form of Richards' equation\n"
    "! mixdform  ! mixed form of Richards' equation\n"
    "! -----------------------------------------------------------------------------------------------\n"
    "! (4) choice of groundwater parameterization\n"
    "! movBound  ! moving lower boundary\n"
    "! bigBuckt  ! a big bucket (lumped aquifer model)\n"
    "! noXplict  ! no explicit groundwater parameterization\n"
    "! -----------------------------------------------------------------------------------------------\n"
    "! (5) choice of upper boundary conditions for thermodynamics\n"
    "! presTemp  ! prescribed temperature\n"
    "! nrg_flux  ! energy flux\n"
    "! -----------------------------------------------------------------------------------------------\n"
    "! (6) choice of lower boundary conditions for thermodynamics\n"
    "! presTemp  ! prescribed temperature\n"
    "! zeroFlux  ! zero flux\n"
    "! -----------------------------------------------------------------------------------------------\n"
    "! (7) choice of upper boundary conditions for soil hydrology\n"
    "! presHead  ! prescribed head (volumetric liquid water content for mixed form of Richards' eqn)\n"
    "! liq_flux  ! liquid water flux\n"
    "! -----------------------------------------------------------------------------------------------\n"
    "! (8) choice of lower boundary conditions for soil hydrology\n"
    "! drainage  ! free draining\n"
    "! bottmPsi  ! function of matric head in the lower-most layer\n"
    "! gwCouple  ! coupled to the groundwater sub-model (matric head=0 as a moving lower boundary)\n"
    "! -----------------------------------------------------------------------------------------------\n"
    "! (9) choice of stability function\n"
    "! standard  ! standard MO similarity, a la Anderson (1979)\n"
    "! louisinv  ! Louis (1979) inverse power function\n"
    "! mahrtexp  ! Mahrt (1987) exponential function\n"
    "! -----------------------------------------------------------------------------------------------\n"
    "! (10) choice of compaction routine\n"
    "! consettl  ! constant settlement rate\n"
    "! anderson  ! semi-empirical method of Anderson (1976)\n"
    "! -----------------------------------------------------------------------------------------------\n"
    "! (11) choice of thermal conductivity\n"
    "! tyen1965  ! Yen (1965)\n"
    "! melr1977  ! Mellor (1977)\n"
    "! jrdn1991  ! Jordan (1991)\n"
    "! smnv2000  ! Smirnova et al. (2000)\n"
    "! -----------------------------------------------------------------------------------------------\n"
    "! (12) choice of albedo representation\n"
    "! fsnowage  ! function of snow age\n"
    "! batslike  ! BATS-like approach, with destructive metamorphism + soot content\n"
    "! ***********************************************************************************************\n")

    print "Finished creating new Decision file"

    return

# Get values for given parameter from Local
def GetParamVals(param_2_vary,NPruns,settings_dir,c_Site_ID):

# filename
    param_limits_file = settings_dir + c_Site_ID + "/snow_zLocalParamInfo.txt"
    
    # Get Param limits from snow_zParamInfo.txt in ~/settings/
    param_ex = "(.*)" + param_2_vary + "(.*)" # imporve serachability
    fparam = open(param_limits_file,"r") # Open snow_zLocalParamInfo to search
    paramfound = 0 # Logical for finding param
    for line in fparam: # For each line
        if re.match(param_ex,line):
            paramfound = 1
            temp1 = line.split()
            val_l = temp1[4] # (Lower value)
            val_u = temp1[6] # (Upper value)
            val_d = temp1[2] # (Default value)
            if "d" in val_l: # replace d with e (fortran to python exponent syntax)
                val_l = float(val_l.replace('d','e'))
            else:
                val_l = float(val_l)
            if "d" in val_u: # replace d with e (fortran to python exponent syntax)
                val_u = float(val_u.replace('d','e'))
            else:
                val_u = float(val_u)
                
    if (paramfound == 0):
        sys.exit("Check spelling of Parameter to vary")
        
    fparam.close() # Close file

    ## Cases for number of param values to return
    Pvals = [] # Initialize param val list

    # NPruns == 1 --> return default
    if NPruns == 1:
        print 'Returning default parameter values'
        Pvals = [val_d]
    # NPruns == 2 --> return upper and lower
    elif NPruns == 2:
        print 'Returning lower and upper parameter values'
        Pvals = [val_l,val_u]
    # NPruns > 1 --> split up
    else:
        print 'Returning parameter values between lower and upper bounds'
        Pvals = numpy.linspace(val_l,val_u,NPruns,True)

    print Pvals
    return (Pvals)

# Create new Param Trial file
def ParamTrial(new_param_all,new_param_val,param_2_vary,NPruns,settings_dir,c_Site_ID,cRID_char):

    # Define new Paramter file
    new_file          = settings_dir + c_Site_ID + "/" + cRID_char + "/snow_zParamTrial_" + c_Site_ID + ".txt"
    
    # Open file for writing
    fin = open(new_file,"w")

    # Print header info
    fin.write("! ***********************************************************************************************************************\n"
              "! ***********************************************************************************************************************\n"
              "! ***** DEFINITION OF TRIAL MODEL PARAMETER VALUES **********************************************************************\n"
              "! ***********************************************************************************************************************\n"
              "! ***********************************************************************************************************************\n"
              "! Note: Lines starting with ""!"" are treated as comment lines -- there is no limit on the number of comment lines.\n"
              "!\n"
              "! Variable names are important: They must match the variables in the code, and they must occur before the data.\n"
              "!  NOTE: must include information for all HRUs\n"
              "! ***********************************************************************************************************************\n")
    #help(new_param_val)
    
    # Print c_new_param
    paramtext = "    ".join(new_param_all)
    valtext   = "    ".join(map(str,new_param_val))
    print valtext
    
    fin.write("hruIndex %s\n" %paramtext)
    fin.write("1001     %s\n" %valtext) # NOTE: HRU 1001 HARDCODED (need to make dynamic for multiple HRUs)
    
    # Close file
    fin.close()

    print "Finished creating new snow_zParamTrial file"

    return
          
# Create pbs.cmd file for qsub summission
def pbs(exp_name,c_fileManager,run_output,cRID_char):

    # Directories
    new_file = "/home/wayandn/pbs.cmd"

    # Open file for writing
    fin = open(new_file,"w")

    # Write to file
    fin.write("#!/bin/sh\n"
              "\n"
              "#PBS -N " + cRID_char + "_" + exp_name  + "\n"
              "#PBS -m abe -M nicway@u.washington.edu\n"
              "#PBS -l nodes=1:ppn=8\n"
              "#PBS -l walltime=24:00:00\n"
	      "#PBS -l pmem=10GB\n"
	      "#PBS -j oe\n"		
	       #"#PBS -e errors/" + cRID_char + ".$PBS_O_JOBID.txt\n"
              "\n"
              "cd /home/wayandn/FUSE_SNOW/bin/\n")
    fin.write("./summa.exe ")
    fin.write(exp_name + " " + c_fileManager + " > " + run_output + "\n")

    # Close file
    fin.close()

    print "New pbs file made"

    return


