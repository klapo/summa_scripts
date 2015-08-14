#!/usr/bin/python
import os
import shutil
import re
import sys
import numpy



# Created 01/07/2013 - Nic Wayand (nicway@u.washington.edu)

# This script holds functions to make new settings files:
# summa_file_Manager_X.txt
# summa_zDecisions_X.txt
# summa_zParamTrial_X.txt
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
    new_file = settings_dir + SITE_RUN + "/summa_fileManager_" + c_Site_ID + ".txt"

    # Open file for reading
    fin = open(new_file,"w")

    # Print header Info
    fin.write("SUMMA_FILE_MANAGER_V1.0\n! Comment line:\n! *** paths (must be in single quotes)\n")
    
    # Print paths (ORDER IS IMPORTANT!!!)
    fin.write("'" + settings_dir + "'          ! SETNGS_PATH\n")
    fin.write("'" + input_dir + c_Site_ID + "/'         ! INPUT_PATH\n")
    fin.write("'" + output_dir + SITE_RUN + "/'    ! OUTPUT_PATH\n")

    # Print control file paths
    fin.write("! *** control files (must be in single quotes)\n")

    # path that changes for each run
    fin.write("'" + SITE_RUN + "/summa_zDecisions_" + c_Site_ID + ".txt'            ! M_DECISIONS     = definition of model decisions\n")

    # paths that are the same for ALL runs
    fin.write("'meta/summa_zTimeMeta.txt'                           ! META_TIME        = metadata for time\n"
              "'meta/summa_zLocalAttributeMeta.txt'                 ! META_ATTR        = metadata for local attributes\n"
              "'meta/summa_zCategoryMeta.txt'                       ! META_TYPE        = metadata for local classification of veg, soil, etc.\n"
              "'meta/summa_zForceMeta.txt'                          ! META_FORCE       = metadata for model forcing variables\n"
              "'meta/summa_zLocalParamMeta.txt'                     ! META_LOCALPARAM  = metadata for local model parameters\n"
              "'meta/summa_zLocalModelVarMeta.txt'                  ! META_LOCALMVAR   = metadata for local model variables\n"
              "'meta/summa_zLocalModelIndexMeta.txt'                ! META_INDEX       = metadata for model indices\n"
              "'meta/summa_zBasinParamMeta.txt'                     ! META_BASINPARAM  = metadata for basin-average model parameters\n"
              "'meta/summa_zBasinModelVarMeta.txt'                  ! META_BASINMVAR   = metadata for basin-average model variables\n")

    # paths that change for each site
    fin.write("'" + c_Site_ID + "/summa_zLocalAttributes.txt'              ! LOCAL_ATTRIBUTES = local attributes\n"
              "'" + c_Site_ID + "/summa_zLocalParamInfo.txt'             ! LOCALPARAM_INFO  = default values and constraints for local model parameters\n"
              "'" + c_Site_ID + "/summa_zBasinParamInfo.txt'             ! BASINPARAM_INFO  = default values and constraints for basin-average model parameters\n"
              "'" + c_Site_ID + "/summa_zForcingFileList.txt'                ! FORCING_FILELIST = list of files used in each HRU\n"
              "'" + c_Site_ID + "/summa_zInitialCond.txt'              ! MODEL_INITCOND  = model initial conditions\n")

    # paths that change for each run
    fin.write("'" + SITE_RUN + "/summa_zParamTrial_" + c_Site_ID + ".txt'           ! PARAMETER_TRIAL = trial values for model parameters\n")
    #fin.write("'/summa_zParamTrial_Restart_part.txt'           ! PARAMETER_TRIAL = trial values for model parameters\n")
    fin.write("'" + c_Site_ID + "_" + cRID_char + "'                                        ! OUTPUT_PREFIX\n")

    # Close file
    fin.close()

    print "Finished creating new file Manager"

    return

# Create new file Manager if ther are multiple HRUs
def file_Manager_Multi_HRUs(settings_dir,input_dir,output_dir,c_Site_ID,cRID_char,Var_out_lev):

    # directories
    #c_Site_ID/cRID_char (i.e. SNQ/R_1)
    SITE_RUN = c_Site_ID + "/" + cRID_char

    # filename
    new_file = settings_dir + SITE_RUN + "/summa_fileManager_" + c_Site_ID + ".txt"

    # Open file for reading
    fin = open(new_file,"w")

    # Print header Info
    fin.write("SUMMA_FILE_MANAGER_V1.0\n! Comment line:\n! *** paths (must be in single quotes)\n")

    # Print paths (ORDER IS IMPORTANT!!!)
    fin.write("'" + settings_dir + "'          ! SETNGS_PATH\n")
    fin.write("'" + input_dir + c_Site_ID + "/'         ! INPUT_PATH\n")
    fin.write("'" + output_dir + SITE_RUN + "/'    ! OUTPUT_PATH\n")

    # Print control file paths
    fin.write("! *** control files (must be in single quotes)\n")

    # path that changes for each run
    fin.write("'" + SITE_RUN + "/summa_zDecisions_" + c_Site_ID + ".txt'            ! M_DECISIONS     = definition of model decisions\n")

    # paths that are the same for ALL runs
    fin.write("'meta/summa_zTimeMeta.txt'                           ! META_TIME        = metadata for time\n"
              "'meta/summa_zLocalAttributeMeta.txt'                 ! META_ATTR        = metadata for local attributes\n"
              "'meta/summa_zCategoryMeta.txt'                       ! META_TYPE        = metadata for local classification of veg, soil, etc.\n"
              "'meta/summa_zForceMeta.txt'                          ! META_FORCE       = metadata for model forcing variables\n"
              "'meta/summa_zLocalParamMeta.txt'                     ! META_LOCALPARAM  = metadata for local model parameters\n")
    # Option for level of output variables (helps reduce size of netcdf files)
    if Var_out_lev==1:
	fin.write("'meta/summa_zLocalModelVarMeta.txt'                  ! META_LOCALMVAR   = metadata for local model variables\n")
    elif Var_out_lev==2:
	fin.write("'meta/summa_zLocalModelVarMeta.txt.light'                  ! META_LOCALMVAR   = metadata for local model variables\n")
    else:
	print "Var_out_lev must be option 1 or 2"
	return

    # Cont. printing
    
    fin.write("'meta/summa_zLocalModelIndexMeta.txt'                ! META_INDEX       = metadata for model indices\n"
              "'meta/summa_zBasinParamMeta.txt'                     ! META_BASINPARAM  = metadata for basin-average model parameters\n"
              "'meta/summa_zBasinModelVarMeta.txt'                  ! META_BASINMVAR   = metadata for basin-average model variables\n")

    # paths that change for each site
    fin.write("'" + SITE_RUN + "/summa_zLocalAttributes.txt'              ! LOCAL_ATTRIBUTES = local attributes\n"
              "'" + c_Site_ID + "/summa_zLocalParamInfo.txt'             ! LOCALPARAM_INFO  = default values and constraints for local model parameters\n"
              "'" + c_Site_ID + "/summa_zBasinParamInfo.txt'             ! BASINPARAM_INFO  = default values and constraints for basin-average model parameters\n"
              "'" + SITE_RUN + "/summa_zForcingFileList.txt'                ! FORCING_FILELIST = list of files used in each HRU\n"
              "'" + c_Site_ID + "/summa_zInitialCond.txt'              ! MODEL_INITCOND  = model initial conditions\n")

    # paths that change for each run
    fin.write("'" + SITE_RUN + "/summa_zParamTrial_" + c_Site_ID + ".txt'           ! PARAMETER_TRIAL = trial values for model parameters\n")
    #fin.write("'/summa_zParamTrial_Restart_part.txt'           ! PARAMETER_TRIAL = trial values for model parameters\n")
    fin.write("'" + c_Site_ID + "_" + cRID_char + "'                                        ! OUTPUT_PREFIX\n")

    # Close file
    fin.close()

    print "Finished creating new file Manager"

    return



# Create new file Manager (For Restart simulations)
def file_manager_restart(settings_dir,input_dir,output_dir,c_Site_ID,cRID_char,IC_file,Restartdir,Var_out_lev):

    # directories
    #c_Site_ID/cRID_char (i.e. SNQ/R_1)
    SITE_RUN = c_Site_ID + "/" + cRID_char

    # filename
    new_file = settings_dir + SITE_RUN + "/summa_fileManager_" + c_Site_ID + ".txt"

    # Open file for reading
    fin = open(new_file,"w")

    # Print header Info
    fin.write("SUMMA_FILE_MANAGER_V1.0\n! Comment line:\n! *** paths (must be in single quotes)\n")

    # Print paths (ORDER IS IMPORTANT!!!)
    fin.write("'" + settings_dir + "'          ! SETNGS_PATH\n")
    fin.write("'" + input_dir + c_Site_ID + "/'         ! INPUT_PATH\n")
    fin.write("'" + output_dir + SITE_RUN + "/'    ! OUTPUT_PATH\n")

    # Print control file paths
    fin.write("! *** control files (must be in single quotes)\n")

    # path that changes for each run
    fin.write("'" + SITE_RUN + "/summa_zDecisions_" + c_Site_ID + ".txt'            ! M_DECISIONS     = definition of model decisions\n")

    # paths that are the same for ALL runs
    fin.write("'meta/summa_zTimeMeta.txt'                           ! META_TIME        = metadata for time\n"
              "'meta/summa_zLocalAttributeMeta.txt'                 ! META_ATTR        = metadata for local attributes\n"
              "'meta/summa_zCategoryMeta.txt'                       ! META_TYPE        = metadata for local classification of veg, soil, etc.\n"
              "'meta/summa_zForceMeta.txt'                          ! META_FORCE       = metadata for model forcing variables\n"
              "'meta/summa_zLocalParamMeta.txt'                     ! META_LOCALPARAM  = metadata for local model parameters\n")
    # Option for level of output variables (helps reduce size of netcdf files)
    if Var_out_lev==1:
	fin.write("'meta/summa_zLocalModelVarMeta.txt'                  ! META_LOCALMVAR   = metadata for local model variables\n")
    elif Var_out_lev==2:
	fin.write("'meta/summa_zLocalModelVarMeta.txt.light'                  ! META_LOCALMVAR   = metadata for local model variables\n")
    else:
	print "Var_out_lev must be option 1 or 2"
	return

    # Cont. printing
    fin.write("'meta/summa_zLocalModelIndexMeta.txt'                ! META_INDEX       = metadata for model indices\n"
              "'meta/summa_zBasinParamMeta.txt'                     ! META_BASINPARAM  = metadata for basin-average model parameters\n"
              "'meta/summa_zBasinModelVarMeta.txt'                  ! META_BASINMVAR   = metadata for basin-average model variables\n")

    # paths that change for each site
    fin.write("'" + SITE_RUN + "/summa_zLocalAttributes.txt'              ! LOCAL_ATTRIBUTES = local attributes\n"
              "'" + c_Site_ID + "/summa_zLocalParamInfo.txt'             ! LOCALPARAM_INFO  = default values and constraints for local model parameters\n"
              "'" + c_Site_ID + "/summa_zBasinParamInfo.txt'             ! BASINPARAM_INFO  = default values and constraints for basin-average model parameters\n"
              "'" + SITE_RUN  + "/summa_zForcingFileList.txt'                ! FORCING_FILELIST = list of files used in each HRU\n"
              "'" + c_Site_ID + "/" + Restartdir + "/" + IC_file + "'              ! MODEL_INITCOND  = model initial conditions\n")

    # paths that change for each run
    fin.write("'" + SITE_RUN + "/summa_zParamTrial_" + c_Site_ID + ".txt'           ! PARAMETER_TRIAL = trial values for model parameters\n")
    #fin.write("'" + c_Site_ID + "/summa_zParamTrial_Restart_part.txt'           ! PARAMETER_TRIAL = trial values for model parameters\n")
    fin.write("'" + c_Site_ID + "_" + cRID_char + "'                                        ! OUTPUT_PREFIX\n")

    # Close file
    fin.close()

    print "Finished creating new file Manager"

    return

# Create new Decision file
def Desicions(Decisions_ALL,settings_dir,c_Site_ID,cRID_char,datestart,dateend):

    # directories

    # filename
    new_file = settings_dir + c_Site_ID + "/" + cRID_char + "/summa_zDecisions_" + c_Site_ID + ".txt"

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
    fin.write("simulStart              '" + datestart + "'  ! (01) simulation start time -- must be in single quotes\n"
              "simulFinsh              '" + dateend + "'  ! (02) simulation end time -- must be in single quotes\n"
              "! ***********************************************************************************************************************\n")
    # Print Desicians (Decisions_ALL indexed by zero)
    fin.write("soilCatTbl                      " + Decisions_ALL[0]  + " ! (03) soil-category dateset\n")
    fin.write("vegeParTbl                      " + Decisions_ALL[1]  + " ! (04) vegetation category dataset\n")
    fin.write("soilStress                      " + Decisions_ALL[2]  + " ! (05) choice of function for the soil moisture control on stomatal resistance\n")
    fin.write("stomResist                      " + Decisions_ALL[3]  + " ! (06) choice of function for stomatal resistance\n")
    fin.write("! ***********************************************************************************************************************\n")
    fin.write("num_method                      " + Decisions_ALL[4]  + " ! (07) choice of numerical method\n")
    fin.write("fDerivMeth                      " + Decisions_ALL[5]  + " ! (08) method used to calculate flux derivatives\n")
    fin.write("LAI_method                      " + Decisions_ALL[6]  + " ! (09) method used to determine LAI and SAI\n")
    fin.write("f_Richards                      " + Decisions_ALL[7]  + " ! (10) form of Richard's equation\n")
    fin.write("groundwatr                      " + Decisions_ALL[8]  + " ! (11) choice of groundwater parameterization\n")
    fin.write("hc_profile                      " + Decisions_ALL[9]  + " ! (12) choice of hydraulic conductivity profile\n")
    fin.write("bcUpprTdyn                      " + Decisions_ALL[10]  + " ! (13) type of upper boundary condition for thermodynamics\n")
    fin.write("bcLowrTdyn                      " + Decisions_ALL[11]  + " ! (14) type of lower boundary condition for thermodynamics\n")
    fin.write("bcUpprSoiH                      " + Decisions_ALL[12]  + " ! (15) type of upper boundary condition for soil hydrology\n")
    fin.write("bcLowrSoiH                      " + Decisions_ALL[13]  + " ! (16) type of lower boundary condition for soil hydrology\n")
    fin.write("veg_traits                      " + Decisions_ALL[14]  + " ! (17) choice of parameterization for vegetation roughness length and displacement height\n")
    fin.write("canopyEmis                      " + Decisions_ALL[15]  + " ! (18) choice of parameterization for canopy emissivity\n")
    fin.write("snowIncept                      " + Decisions_ALL[16]  + " ! (19) choice of parameterization for snow interception\n")
    fin.write("windPrfile                      " + Decisions_ALL[17]  + " ! (20) choice of wind profile through the canopy\n")
    fin.write("astability                      " + Decisions_ALL[18]  + " ! (21) choice of stability function\n")
    fin.write("canopySrad                      " + Decisions_ALL[19]  + " ! (22) choice of canopy shortwave radiation method\n")
    fin.write("alb_method                      " + Decisions_ALL[20]  + " ! (23) choice of albedo representation\n")
    fin.write("compaction                      " + Decisions_ALL[21]  + " ! (24) choice of compaction routine\n")
    fin.write("snowLayers                      " + Decisions_ALL[22]  + " ! (25) choice of method to combine and sub-divide snow layers\n")
    fin.write("thCondSnow                      " + Decisions_ALL[23]  + " ! (26) choice of thermal conductivity representation\n")
    fin.write("thCondSoil                      " + Decisions_ALL[24]  + " ! (27) choice of method for the spatial representation of groundwater\n")
    fin.write("spatial_gw                      " + Decisions_ALL[25]  + " ! (28) choice of method for the spatial representation of groundwater\n")
    fin.write("subRouting                      " + Decisions_ALL[26]  + " ! (29) choice of method for sub-grid routing\n")
    fin.write("snowDenNew                      " + Decisions_ALL[27]  + " ! (30) choice of method for new snow density\n")

    print "Finished creating new Decision file"

    return

# Get values for given parameter from Local
def GetParamVals(param_2_vary,NPruns,settings_dir,c_Site_ID):

    # filename
    param_limits_file = settings_dir + c_Site_ID + "/summa_zLocalParamInfo.txt"
    
    # Get Param limits from summa_zParamInfo.txt in ~/settings/
    param_ex = "(.*)" + param_2_vary + "(.*)" # imporve serachability
    fparam = open(param_limits_file,"r") # Open summa_zLocalParamInfo to search
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
def ParamTrial(new_param_all,new_param_val,settings_dir,c_Site_ID,cRID_char):

    # Define new Paramter file
    new_file          = settings_dir + c_Site_ID + "/" + cRID_char + "/summa_zParamTrial_" + c_Site_ID + ".txt"
    
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

    print "Finished creating new summa_zParamTrial file"

    return

# Create new Param Trial file (With multiple HRUs)
def ParamTrial_Multi_hru(new_param_all,new_param_val,settings_dir,c_Site_ID,cRID_char):

    # Define new Paramter file
    new_file          = settings_dir + c_Site_ID + "/" + cRID_char + "/summa_zParamTrial_" + c_Site_ID + ".txt"

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

    # Print c_new_param
    paramtext = "    ".join(new_param_all)
    
    fin.write("hruIndex %s\n" %paramtext)
    
    for chru in range(0,len(new_param_val)):
        c_values = "    ".join(map(str,new_param_val[chru]))
        c_hru = 1001 + chru
        fin.write("%d     %s\n" %(c_hru, c_values) )
    
    # Close file
    fin.close()

    return


# Create Forcing file
def Forcing_file(c_Site_ID,Flist_file,forcing_file,base_hru_num,NHRUs):
	# Open file for writing
	fin = open(Flist_file,"w")

	
	fin.write("! ****************************************************************************************************\n"
		"! List of forcing data files used in each HRU\n"
		"!\n"
		"! This file includes two 'words' per line:\n"
		"!  (1) The HRU index (must match the indices in the local attributes file)\n"
		"!  (2) The name of the descriptor file assigned to each HRU index\n"
		"!        --> filename must be in single quotes\n"
		"! ****************************************************************************************************\n")
	for chru in range(0,NHRUs):
		fin.write("   " + str(base_hru_num+chru) + "    " + "'" + str(c_Site_ID) + "/" +  str(forcing_file) + "'\n")
	
	fin.close()

	return

# Create Local Attributes file
def Local_Attributes_file(Alist_file,base_hru_num,NHRUs):
        # Open file for writing
        fin = open(Alist_file,"w")

	fin.write("hruIndex    HRUarea  latitude  longitude  elevation  tan_slope  contourLength  mHeight  vegTypeIndex  soilTypeIndex  slopeTypeIndex  downHRUindex\n")
	
	for chru in range(0,NHRUs):
                fin.write(str(base_hru_num+chru) + "     1.0     47.4249    -121.4138    921.0          0              1     7.15             7             2               1             0\n")

        fin.close()

        return




          
# Create pbs.cmd file for qsub summission
def pbs(pbs_file,exp_name,c_fileManager,run_output,run_dir,cRID_char,your_email):

    # Open file for writing
    fin = open(pbs_file,"w")

    # Write to file
    fin.write("#!/bin/bash\n"
              "\n"
              "#PBS -N " + cRID_char + "_" + exp_name  + "\n"
              "##PBS -m e -M " + your_email + "\n"
              "##PBS -l nodes=hydro-c1-node7+hydro-c1-node6+hydro-c1-node4:ppn=1\n"
 	      "#PBS -l nodes=1:ppn=1\n"
              "#PBS -l walltime=01:00:00\n"
	      "#PBS -l pmem=10GB\n"
	      "#PBS -o /home/wayandn/qsub_output/o." + cRID_char + "\n" 
	      "#PBS -e /home/wayandn/qsub_output/e." + cRID_char + "\n"
	      "##PBS -j oe\n"
	      "export LD_LIBRARY_PATH=/opt/netcdf-4.3.0+ifort-12.1/lib\n"		
	       #"#PBS -e errors/" + cRID_char + ".$PBS_O_JOBID.txt\n"
              "\n"
              "cd " + run_dir + "/\n")
    fin.write("./summa.exe ")
    fin.write(exp_name + " " + c_fileManager + " > " + run_output + "\n")

    # Close file
    fin.close()

    print "New pbs file made"

    return


