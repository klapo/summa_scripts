import os


def buildFileName(fName, expID, fType='.txt'):
    if not expID == '':
        expID = '_' + expID
    fullFilename = fName + expID + fType
    return fullFilename


def checkFile(dirModel, siteID, expName, fName, expID='', fType='.txt', mode='w'):
    # Checks that path exists
    # Creates path to desired file, fName
    # Opens file
    # Returns object of the open file, fin
    #
    # INPUT:
    #   dirModel: string to model directory
    #   siteID: string of the site name
    #   expName: string of the experiment name
    #   fName: string of the file name. Needs to end in an underscore
    #   expID: string of the experiment ID
    #
    # Files relevant to the entire experiment/run should not provide expID.
    # Files for a specific run/experiment should provide expID
    # Do not include underscores in strings, they are automatically included

    # File path and name
    fPath = checkPath(dirModel, siteID, expName, expID)
    fullFilename = buildFileName(fName, expID, fType)
    newFile = fPath + '/' + fullFilename

    # Open/create and return object
    fin = open(newFile, mode)
    return(fin)


def checkPath(dirModel, siteID, expName, expID=''):
    # Checks that path exists
    # Creates desired path exists
    #
    # INPUT:
    #   dirModel: string to model directory
    #   siteID: string of the site name
    #   expName: string of the experiment name
    #   fName: string of the file name. Needs to end in an underscore
    #   expID: string of the experiment ID
    #
    # Files relevant to the entire experiment/run should not provide expID.
    # Files for a specific run/experiment should provide expID.
    # Do not include underscores in strings, they are automatically included

    if not expID == '':
        expID = '_' + expID

    # File path
    if dirModel[-1] == '/':
        fPath = dirModel + expName + '/' + siteID
    else:
        fPath = dirModel + '/' + expName + '/' + siteID

    # Open file for reading
    if not os.path.exists(fPath):
        os.makedirs(fPath)
        os.chmod(fPath, mode=0o777)
    return(fPath)
