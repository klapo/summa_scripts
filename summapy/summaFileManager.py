import os
import shutil
import re
import sys
import numpy as np
from summapy.summaPaths import checkFile, checkPath, buildFileName

'''
This script holds functions to setup a summa run:
    summa_file_Manager_X.txt
    summa_zDecisions_X.txt
    summa_zParamTrial_X.txt
    pbd.cmd
'''


def fileManager(dirModel, siteID, expName, expID=''):
    # Create new file Manager
    # INPUT:

    # -------------------------------------------------------------------------
    # Check files
    # Check for input, settings, and output directories
    dirSettings = checkPath(dirModel + 'settings/', siteID, expName)
    dirInput = checkPath(dirModel + 'input/', siteID, expName)
    dirOutput = checkPath(dirModel + 'output/', siteID, expName)

    # Create decision file name
    fDecisionsName = buildFileName('summa_zDecisions', expID)

    # Open/create the file manager
    fManager = checkFile(dirModel + 'settings/', siteID, expName, 'summa_fileManager', expID)

    # -------------------------------------------------------------------------
    # Write the file
    # Print header Info
    fManager.write("SUMMA_FILE_MANAGER_V1.0\n! Comment line:\n! *** paths (must be in single quotes)\n")

    # Print paths (ORDER IS IMPORTANT!!!)
    fManager.write("'" + dirSettings + "'  ! SETTING_PATH\n")
    fManager.write("'" + dirInput + "/'  ! INPUT_PATH\n")
    fManager.write("'" + dirOutput + "/'  ! OUTPUT_PATH\n")

    # Print control file paths
    fManager.write("! *** control files (must be in single quotes)\n")

    # path that changes for each run
    fManager.write("'" + dirSettings + fDecisionsName + '  ! M_DECISIONS = definition of model decisions\n')

    # paths that are the same for ALL runs
    # Fix these paths to point to the meta directory included with the package
    fManager.write("'meta/summa_zTimeMeta.txt'              ! META_TIME = metadata for time\n"
                   "'meta/summa_zLocalAttributeMeta.txt'    ! META_ATTR = metadata for local attributes\n"
                   "'meta/summa_zCategoryMeta.txt'          ! META_TYPE = metadata for local classification of veg, soil, etc.\n"
                   "'meta/summa_zForceMeta.txt'             ! META_FORCE = metadata for model forcing variables\n"
                   "'meta/summa_zLocalParamMeta.txt'        ! META_LOCALPARAM  = metadata for local model parameters\n"
                   "'meta/summa_zLocalModelVarMeta.txt'     ! META_LOCALMVAR  = metadata for local model variables\n"
                   "'meta/summa_zLocalModelIndexMeta.txt'   ! META_INDEX = metadata for model indices\n"
                   "'meta/summa_zBasinParamMeta.txt'        ! META_BASINPARAM = metadata for basin-average model parameters\n"
                   "'meta/summa_zBasinModelVarMeta.txt'     ! META_BASINMVAR = metadata for basin-average model variables\n")

    # paths that change for each site
    fManager.write("'" + dirSettings + "/summa_zLocalAttributes.txt'    ! LOCAL_ATTRIBUTES = local attributes\n"
                   "'" + dirSettings + "/summa_zLocalParamInfo.txt'     ! LOCALPARAM_INFO = default values and constraints for local model parameters\n"
                   "'" + dirSettings + "/summa_zBasinParamInfo.txt'     ! BASINPARAM_INFO = default values and constraints for basin-average model parameters\n"
                   "'" + dirSettings + "/summa_zForcingFileList.txt'    ! FORCING_FILELIST = list of files used in each HRU\n"
                   "'" + dirSettings + "/summa_zInitialCond.txt'        ! MODEL_INITCOND = model initial conditions\n")

    # paths that change for each run
    if expID == '':
        expID = expName + '_' + siteID
    fManager.write("'" + dirSettings + "/summa_zParamTrial.txt'  ! PARAMETER_TRIAL = trial values for model parameters\n")
    fManager.write("'" + expID + "'  ! OUTPUT_PREFIX\n")

    # Close file
    fManager.close()

    print("Finished creating new file Manager")

    return


def decision(userDecisions, dirModel, siteID, expName, datestart, dateend, expID=''):
    ####################################################
    # Create new Decision file
    # INPUT:
    #   userDecisions = dictionary, keys are parameterizations and items are
    #                  the parameter option. Keys that are not specified are
    #                  given a default value.
    #   dirModel = string, path to settings directory

    # -------------------------------------------------------------------------
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
            allDecisions[dec] = userDecisions[dec]
        except KeyError:
            allDecisions[dec] = allDecisionsDefault[dec]

    # -------------------------------------------------------------------------
    # Write the decision file
    # Filename and directory paths
    fin = checkFile(dirModel + 'settings/', siteID, expName, 'summa_zDecisions', expID)

    # Format datetime objects into desired strings
    dateStartString = datestart.strftime('%Y-%m-%D %H:%M')
    dateEndString = dateend.strftime('%Y-%m-%D %H:%M')

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
    fin.write("simulStart              '" + dateStartString + "'  ! (01) simulation start time -- must be in single quotes\n"
              "simulFinsh              '" + dateEndString + "'  ! (02) simulation end time -- must be in single quotes\n"
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


def getParamVals(param_2_vary, NPruns, dirModel, siteID, expName, expID=''):
    ####################################################
    # Get values for given parameter from Local
    # INPUT:
    #

    # -------------------------------------------------------------------------
    # Check for the file containing default parameter values
    try:
        fParam = checkFile(dirModel + 'settings/', siteID, expName,
                           'summa_zLocalParamInfo', expID, mode='r')
    except FileNotFoundError:
        paramLocalParamInfo(dirModel, siteID, expName)
        fParam = checkFile(dirModel + 'settings/', siteID, expName,
                           'summa_zLocalParamInfo', expID, mode='r')

    # -------------------------------------------------------------------------
    # Get Param limits from summa_zParamInfo.txt in ~/settings/
    param_ex = "(.*)" + param_2_vary + "(.*)"  # improve serachability

    paramfound = 0  # Logical for finding param
    for line in fParam:
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

    fParam.close()  # Close file

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


def paramLocalParamInfo(dirModel, siteID, expName):
    ####################################################
    # Create local param info. This file contains the default, min, and max
    # param values. Default values are only used if param values are not
    # specfieid in paramTrial.
    # Copy-pastes the _generic version of the file by default. Non-default
    # values can be supplied.

    # find settings/summa_zLocalParamInfo_generic.txt included with the package
    dirLocalParamInfo, _ = os.path.split(__file__)
    pathPackageLocalParamInfo = os.path.join(dirLocalParamInfo, 'settings', 'summa_zLocalParamInfo_generic.txt')

    # Copy the file to the model directory
    pathLocalParamInfo = checkPath(dirModel + 'settings/', siteID, expName)
    shutil.copy(pathPackageLocalParamInfo, pathLocalParamInfo + '/summa_zLocalParamInfo.txt')

    return


def paramTrial(strParam, valParam, dirModel, siteID, expName, expID=''):
    ####################################################
    # Create new Param Trial file

    # -------------------------------------------------------------------------
    # Define new Paramter file
    if not dirModel[-1] == '/':
        dirModel = dirModel + '/'
    fParamTrial = checkFile(dirModel + 'settings/', siteID, expName,
                            'summa_zParamTrial', expID)

    # Print header info
    fParamTrial.write(
        "! ***********************************************************************************************************************\n"
        "! ***********************************************************************************************************************\n"
        "! ***** DEFINITION OF TRIAL MODEL PARAMETER VALUES **********************************************************************\n"
        "! ***********************************************************************************************************************\n"
        "! ***********************************************************************************************************************\n"
        "! Note: Lines starting with ""!"" are treated as comment lines -- there is no limit on the number of comment lines.\n"
        "!\n"
        "! Variable names are important: They must match the variables in the code, and they must occur before the data.\n"
        "!  NOTE: must include information for all HRUs\n"
        "! ***********************************************************************************************************************\n")

    # write parameter identifier line and parameter value line
    valParam = np.atleast_1d(valParam)  # force '0 dimensional arrays' (e.g.,1 value) to be 1 dimensional
    paramtext = "    ".join(strParam)
    valtext = "    ".join(map(str, valParam))
    print(valtext)

    fParamTrial.write("hruIndex %s\n" % paramtext)
    fParamTrial.write("1001     %s\n" % valtext)  # NOTE: HRU 1001 HARDCODED (need to make dynamic for multiple HRUs)

    # Close file
    fParamTrial.close()

    print("Finished creating new summa_zParamTrial file")

    return


def forcingFile(c_Site_ID, Flist_file, forcing_file, base_hru_num, NHRUs):
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
        fin.write("   " + str(base_hru_num + chru) + "    " + "'" +
                  str(c_Site_ID) + "/" + str(forcing_file) + "'\n")

    fin.close()

    return


def Local_Attributes_file(Alist_file, base_hru_num, NHRUs):
    ####################################################
    # Create Local Attributes file
    # Open file for writing
    # Need to update to take input lat, lon, elev etc.
    fin = open(Alist_file, "w")

    fin.write("hruIndex    HRUarea  latitude  longitude  elevation  tan_slope  \
               contourLength  mHeight  vegTypeIndex  soilTypeIndex  \
               slopeTypeIndex  downHRUindex\n")

    for chru in range(0, NHRUs):
        fin.write(str(base_hru_num + chru) +
                  "     1.0     47.4249    -121.4138    921.0          \
                  0              1     7.15             7             \
                  2               1             0\n")
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
