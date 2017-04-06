#!/usr/bin/python
import os
import shutil
import re
import sys
import numpy

'''
This script holds functions to make new settings files:
    summa_file_Manager_X.txt
    summa_zDecisions_X.txt
    summa_zParamTrial_X.txt
    pbd.cmd
'''


def file_Manager(settings_dir, input_dir, output_dir, c_Site_ID, cRID_char):
    ####################################################
    # Create new file Manager
    # INPUT:
    #   settings_dir = string, path to settings directory
    #   input_dir = string, path to input directory
    #   c_SITE_ID = string, name of the site (e.g., SNQ for Snoqualmie)
    #   cRID_char = string, run number/run description (for multiple experiments)
    #
    # c_Site_ID/cRID_char (i.e. SNQ/R_1)
    SITE_RUN = c_Site_ID + "/indiv_runs/" + cRID_char

    # filename
    new_file = settings_dir + SITE_RUN + "/summa_fileManager_" + c_Site_ID + ".txt"

    # Open file for reading
    fin = open(new_file, "w")

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
    fin.write("'" + c_Site_ID + "_" + cRID_char + "'                                        ! OUTPUT_PREFIX\n")

    # Close file
    fin.close()

    print("Finished creating new file Manager")

    return


def file_Manager_Multi_HRUs(settings_dir, input_dir, output_dir, c_Site_ID, cRID_char, Var_out_lev):
    ####################################################
    # Create new file Manager if ther are multiple HRUs
    # directories
    # c_Site_ID/cRID_char (i.e. SNQ/R_1)
    SITE_RUN = c_Site_ID + "/indiv_runs/" + cRID_char

    # filename
    new_file = settings_dir + SITE_RUN + "/summa_fileManager_" + c_Site_ID + ".txt"

    # Open file for reading
    fin = open(new_file, "w")

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
    if Var_out_lev == 1:
        fin.write("'meta/summa_zLocalModelVarMeta.txt'                  ! META_LOCALMVAR   = metadata for local model variables\n")
    elif Var_out_lev == 2:
        fin.write("'meta/summa_zLocalModelVarMeta.txt.light'                  ! META_LOCALMVAR   = metadata for local model variables\n")
    else:
        print("Var_out_lev must be option 1 or 2")
        return

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
    fin.write("'" + c_Site_ID + "_" + cRID_char + "'                                        ! OUTPUT_PREFIX\n")

    # Close file
    fin.close()

    print("Finished creating new file Manager")

    return


def file_manager_restart(settings_dir,
                         input_dir,
                         output_dir,
                         c_Site_ID,
                         cRID_char,
                         IC_file,
                         Restartdir,
                         Var_out_lev):
    ####################################################
    # Create new file Manager (For Restart simulations)
    # directories
    # c_Site_ID/cRID_char (i.e. SNQ/R_1)
    SITE_RUN = c_Site_ID + "/indiv_runs/" + cRID_char

    # filename
    new_file = settings_dir + SITE_RUN + "/summa_fileManager_" + c_Site_ID + ".txt"

    # Open file for reading
    fin = open(new_file, "w")

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
    if Var_out_lev == 1:
        fin.write("'meta/summa_zLocalModelVarMeta.txt'                  ! META_LOCALMVAR   = metadata for local model variables\n")
    elif Var_out_lev == 2:
        fin.write("'meta/summa_zLocalModelVarMeta.txt.light'                  ! META_LOCALMVAR   = metadata for local model variables\n")
    else:
        print("Var_out_lev must be option 1 or 2")
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
              "'" + c_Site_ID + "/" + Restartdir + "/" + IC_file + "'              ! MODEL_INITCOND  = model initial conditions\n")

    # paths that change for each run
    fin.write("'" + SITE_RUN + "/summa_zParamTrial_" + c_Site_ID + ".txt'           ! PARAMETER_TRIAL = trial values for model parameters\n")
    fin.write("'" + c_Site_ID + "_" + cRID_char + "'                                        ! OUTPUT_PREFIX\n")

    # Close file
    fin.close()

    print("Finished creating new file Manager")

    return


def Desicions(allDecisions, settings_dir, c_Site_ID, cRID_char, datestart, dateend):
    ####################################################
    # Create new Decision file
    # INPUT:
    #   allDecisions = dictionary, keys are parameterizations and items are
    #                  the parameter option. Keys that are not specified are
    #                  given a default value.
    # settings_dir = string, path to settings directory

    # Dictionary of default decisions
    allDecisionsDefault = {}
    allDecisionsDefault['soilCatTbl'] = 'ROSETTA'  # (03) soil-category dateset
    allDecisionsDefault['vegeParTbl'] = 'USGS'  # (04) vegetation category dataset
    allDecisionsDefault['soilStress'] = 'NoahType'  # (05) choice of funct. for soil moisture control on stomatal resistance
    allDecisionsDefault['stomResist'] = 'BallBerry'  # (06) choice of function for stomatal resistance
    allDecisionsDefault['num_method'] = 'itertive'  # (07) choice of numerical method
    allDecisionsDefault['fDerivMeth'] = 'analytic'  # (08) method used to calculate flux derivatives
    allDecisionsDefault['LAI_method'] = 'specified'  # (09) method used to determine LAI and SAI
    allDecisionsDefault['f_Richards'] = 'mixdform'  # (10) form of Richard's equation
    allDecisionsDefault['groundwatr'] = 'noXplict'  # (11) choice of groundwater parameterization
    allDecisionsDefault['hc_profile'] = 'pow_prof'  # (12) choice of hydraulic conductivity profile
    allDecisionsDefault['bcUpprTdyn'] = 'nrg_flux'  # (13) type of upper boundary condition for thermodynamics
    allDecisionsDefault['bcLowrTdyn'] = 'zeroFlux'  # (14) type of lower boundary condition for thermodynamics
    allDecisionsDefault['bcUpprSoiH'] = 'liq_flux'  # (15) type of upper boundary condition for soil hydrology
    allDecisionsDefault['bcLowrSoiH'] = 'drainage'  # (16) type of lower boundary condition for soil hydrology
    allDecisionsDefault['veg_traits'] = 'CM_QJRMS1998'  # (17) choice of param. for veg roughness & displacement height
    allDecisionsDefault['canopyEmis'] = 'simplExp'  # (18) choice of parameterization for canopy emissivity
    allDecisionsDefault['snowIncept'] = 'lightSnow'  # (19) choice of parameterization for snow interception
    allDecisionsDefault['windPrfile'] = 'logBelowCanopy'  # (20) choice of wind profile through the canopy
    allDecisionsDefault['astability'] = 'standard'  # (21) choice of stability function
    allDecisionsDefault['canopySrad'] = 'CLM_2stream'  # (22) choice of canopy shortwave radiation method
    allDecisionsDefault['alb_method'] = 'varDecay'  # (23) choice of albedo representation
    allDecisionsDefault['compaction'] = 'anderson'  # (24) choice of compaction routine
    allDecisionsDefault['snowLayers'] = 'jrdn1991'  # (25) choice of method to combine and sub-divide snow layers
    allDecisionsDefault['thCondSnow'] = 'jrdn1991'  # (26) choice of thermal conductivity representation for snow
    allDecisionsDefault['thCondSoil'] = 'mixConstit'  # (27) choice of thermal conductivity representation for soil
    allDecisionsDefault['spatial_gw'] = 'localColumn'  # (28) choice of method for the spatial representation of groundwater
    allDecisionsDefault['subRouting'] = 'timeDlay'  # (29) choice of method for sub-grid routing
    allDecisionsDefault['snowDenNew'] = 'pahaut_76'  # (30) choice of method for new snow density

    # Check for user-supplied decisions
    allDecisions = {}
    for dec in allDecisionsDefault:
        try:
            myDecisions[dec]
            allDecisions[dec] = myDecisions[dec]
        except KeyError:
            allDecisions[dec] = allDecisionsDefault[dec]

    # filename
    new_file = settings_dir + c_Site_ID + "/indiv_runs/" + cRID_char + "/summa_zDecisions_" + c_Site_ID + ".txt"

    # Open file for reading
    fin = open(new_file, "w")

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
    # Print Desicians (allDecisions indexed by zero)
    fin.write("soilCatTbl                      " + allDecisions['soilCatTbl'] + " ! (03) soil-category dateset\n")
    fin.write("vegeParTbl                      " + allDecisions['vegeParTbl'] + " ! (04) vegetation category dataset\n")
    fin.write("soilStress                      " + allDecisions['soilStress'] + " ! (05) choice of function for the soil moisture control on stomatal resistance\n")
    fin.write("stomResist                      " + allDecisions['stomResist'] + " ! (06) choice of function for stomatal resistance\n")
    fin.write("! ***********************************************************************************************************************\n")
    fin.write("num_method                      " + allDecisions['num_method'] + " ! (07) choice of numerical method\n")
    fin.write("fDerivMeth                      " + allDecisions['fDerivMeth'] + " ! (08) method used to calculate flux derivatives\n")
    fin.write("LAI_method                      " + allDecisions['LAI_method'] + " ! (09) method used to determine LAI and SAI\n")
    fin.write("f_Richards                      " + allDecisions['f_Richards'] + " ! (10) form of Richard's equation\n")
    fin.write("groundwatr                      " + allDecisions['groundwatr'] + " ! (11) choice of groundwater parameterization\n")
    fin.write("hc_profile                      " + allDecisions['hc_profile'] + " ! (12) choice of hydraulic conductivity profile\n")
    fin.write("bcUpprTdyn                      " + allDecisions['bcUpprTdyn'] + " ! (13) type of upper boundary condition for thermodynamics\n")
    fin.write("bcLowrTdyn                      " + allDecisions['bcLowrTdyn'] + " ! (14) type of lower boundary condition for thermodynamics\n")
    fin.write("bcUpprSoiH                      " + allDecisions['bcUpprSoiH'] + " ! (15) type of upper boundary condition for soil hydrology\n")
    fin.write("bcLowrSoiH                      " + allDecisions['bcLowrSoiH'] + " ! (16) type of lower boundary condition for soil hydrology\n")
    fin.write("veg_traits                      " + allDecisions['veg_traits'] + " ! (17) choice of parameterization for vegetation roughness length and displacement height\n")
    fin.write("canopyEmis                      " + allDecisions['canopyEmis'] + " ! (18) choice of parameterization for canopy emissivity\n")
    fin.write("snowIncept                      " + allDecisions['snowIncept'] + " ! (19) choice of parameterization for snow interception\n")
    fin.write("windPrfile                      " + allDecisions['windPrfile'] + " ! (20) choice of wind profile through the canopy\n")
    fin.write("astability                      " + allDecisions['astability'] + " ! (21) choice of stability function\n")
    fin.write("canopySrad                      " + allDecisions['canopySrad'] + " ! (22) choice of canopy shortwave radiation method\n")
    fin.write("alb_method                      " + allDecisions['alb_method'] + " ! (23) choice of albedo representation\n")
    fin.write("compaction                      " + allDecisions['compaction'] + " ! (24) choice of compaction routine\n")
    fin.write("snowLayers                      " + allDecisions['snowLayers'] + " ! (25) choice of method to combine and sub-divide snow layers\n")
    fin.write("thCondSnow                      " + allDecisions['thCondSnow'] + " ! (26) choice of thermal conductivity representation\n")
    fin.write("thCondSoil                      " + allDecisions['thCondSoil'] + " ! (27) choice of method for the spatial representation of groundwater\n")
    fin.write("spatial_gw                      " + allDecisions['spatial_gw'] + " ! (28) choice of method for the spatial representation of groundwater\n")
    fin.write("subRouting                      " + allDecisions['subRouting'] + " ! (29) choice of method for sub-grid routing\n")
    fin.write("snowDenNew                      " + allDecisions['snowDenNew'] + " ! (30) choice of method for new snow density\n")

    print("Finished creating new Decision file")

    return


def GetParamVals(param_2_vary, NPruns, settings_dir, c_Site_ID):
    ####################################################
    # Get values for given parameter from Local
    # filename
    param_limits_file = settings_dir + c_Site_ID + "/summa_zLocalParamInfo.txt"

    # Get Param limits from summa_zParamInfo.txt in ~/settings/
    param_ex = "(.*)" + param_2_vary + "(.*)"  # improve serachability
    fparam = open(param_limits_file, "r")  # Open summa_zLocalParamInfo to search
    paramfound = 0  # Logical for finding param
    for line in fparam:
        if re.match(param_ex, line):
            paramfound = 1
            temp1 = line.split()
            val_l = temp1[4]  # (Lower value)
            val_u = temp1[6]  # (Upper value)
            val_d = temp1[2]  # (Default value)
            if "d" in val_l:  # replace d with e (fortran to python exponent syntax)
                val_l = float(val_l.replace('d', 'e'))
            else:
                val_l = float(val_l)
            if "d" in val_u:  # replace d with e (fortran to python exponent syntax)
                val_u = float(val_u.replace('d', 'e'))
            else:
                val_u = float(val_u)

    if (paramfound == 0):
        sys.exit("Check spelling of Parameter to vary")

    fparam.close()  # Close file

    # Cases for number of param values to return
    Pvals = []  # Initialize param val list

    # NPruns == 1 --> return default
    if NPruns == 1:
        print('Returning default parameter values')
        Pvals = [val_d]
    # NPruns == 2 --> return upper and lower
    elif NPruns == 2:
        print('Returning lower and upper parameter values')
        Pvals = [val_l, val_u]
    # NPruns > 1 --> split up
    else:
        print('Returning parameter values between lower and upper bounds')
        Pvals = numpy.linspace(val_l, val_u, NPruns, True)

    print(Pvals)
    return (Pvals)


def ParamTrial(new_param_all, new_param_val, settings_dir, c_Site_ID, cRID_char):
    ####################################################
    # Create new Param Trial file
    # Define new Paramter file
    new_file = settings_dir + c_Site_ID + "/indiv_runs/" + cRID_char + "/summa_zParamTrial_" + c_Site_ID + ".txt"

    # Open file for writing
    fin = open(new_file, "w")

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
    valtext = "    ".join(map(str, new_param_val))
    print(valtext)

    fin.write("hruIndex %s\n" % paramtext)
    fin.write("1001     %s\n" % valtext)  # NOTE: HRU 1001 HARDCODED (need to make dynamic for multiple HRUs)

    # Close file
    fin.close()

    print("Finished creating new summa_zParamTrial file")

    return


def ParamTrial_Multi_hru(new_param_all, new_param_val, settings_dir, c_Site_ID, cRID_char):
    ####################################################
    # Create new Param Trial file (With multiple HRUs)
    # Define new Paramter file
    new_file = settings_dir + c_Site_ID + "/indiv_runs/" + cRID_char + "/summa_zParamTrial_" + c_Site_ID + ".txt"

    # Open file for writing
    fin = open(new_file, "w")

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

    fin.write("hruIndex %s\n" % paramtext)

    for chru in range(0, len(new_param_val)):
        c_values = "    ".join(map(str, new_param_val[chru]))
        c_hru = 1001 + chru
        fin.write("%d     %s\n" % (c_hru, c_values))

    # Close file
    fin.close()

    return


def Forcing_file(c_Site_ID, Flist_file, forcing_file, base_hru_num, NHRUs):
    ####################################################
    # Create Forcing file
    # Open file for writing
    fin = open(Flist_file, "w")

    fin.write("! ****************************************************************************************************\n"
              "! List of forcing data files used in each HRU\n"
              "!\n"
              "! This file includes two 'words' per line:\n"
              "!  (1) The HRU index (must match the indices in the local attributes file)\n"
              "!  (2) The name of the descriptor file assigned to each HRU index\n"
              "!        --> filename must be in single quotes\n"
              "! ****************************************************************************************************\n")
    for chru in range(0, NHRUs):
        fin.write("   " + str(base_hru_num + chru) + "    " + "'" + str(c_Site_ID) + "/" + str(forcing_file) + "'\n")

    fin.close()

    return


def Local_Attributes_file(Alist_file, base_hru_num, NHRUs):
    ####################################################
    # Create Local Attributes file
    # Open file for writing
    fin = open(Alist_file, "w")

    fin.write("hruIndex    HRUarea  latitude  longitude  elevation  tan_slope  contourLength  mHeight  vegTypeIndex  soilTypeIndex  slopeTypeIndex  downHRUindex\n")

    for chru in range(0, NHRUs):
        fin.write(str(base_hru_num + chru) +
                  "     1.0     47.4249    -121.4138    921.0          \
                  0              1     7.15             7             2               1             0\n")
        fin.close()
        return


def pbs(pbs_file, exp_name, c_fileManager, run_output, run_dir, cRID_char, your_email):
    ####################################################
    # Create pbs.cmd file for qsub summission
    # Open file for writing
    fin = open(pbs_file, "w")

    # Write file
    fin.write("#!/bin/bash\n"
              "\n"
              "#PBS -N " + cRID_char + "_" + exp_name + "\n"
              "##PBS -m e -M " + your_email + "\n"
              "##PBS -l nodes=hydro-c1-node7+hydro-c1-node6+hydro-c1-node4:ppn=1\n"
              "#PBS -l nodes=1:ppn=1\n"
              "#PBS -l walltime=01:00:00\n"
              "#PBS -l pmem=10GB\n"
              "#PBS -o /home/wayandn/qsub_output/o." + cRID_char + "\n"
              "#PBS -e /home/wayandn/qsub_output/e." + cRID_char + "\n"
              "##PBS -j oe\n"
              "export LD_LIBRARY_PATH=/opt/netcdf-4.3.0+ifort-12.1/lib\n"
              "\n"
              "cd " + run_dir + "/\n")
    fin.write("./summa.exe ")
    fin.write(exp_name + " " + c_fileManager + " > " + run_output + "\n")

    # Close file
    fin.close()

    print("New pbs file made")

    return
