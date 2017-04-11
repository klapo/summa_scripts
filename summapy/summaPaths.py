import os


def checkFile(dirSettings, siteID, expName, fName, expID=''):
    # Checks that path exists
    # Creates path to desired file, fName
    # Opens file
    # Returns object of the open file, fin
    #
    # INPUT:
    #   dirSettings: string to model settings directory
    #   siteID: string of the site name
    #   expName: string of the experiment name
    #   fName: string of the file name. Needs to end in an underscore
    #   expID: string of the experiment ID
    #
    # Files relevant to the entire experiment/run should not provide expID.
    # Files for a specific run/experiment should provide expID
    # Do not include underscores in strings, they are automatically included

    # File name (check for underscore)
    if not fName[-1] == '_':
        fName += '_'

    if not expID == '':
        expID = '_' + expID

    # File path
    if dirSettings[-1] == '/':
        fPath = dirSettings + siteID + '_' + expName
    else:
        fPath = dirSettings + '/' + siteID + '_' + expName
    newFile = fPath + '/' + fName + expName + expID + '.txt'

    # Open file for reading
    try:
        fin = open(newFile, "w")
    except FileNotFoundError:
        os.makedirs(fPath)
        fin = open(newFile, "w")

    return(fin)


def checkPath(dirSettings, siteID, expName, expID=''):
    # Checks that path exists
    # Creates desired path exists
    #
    # INPUT:
    #   dirSettings: string to model settings directory
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
    if dirSettings[-1] == '/':
        fPath = dirSettings + siteID + '_' + expName + expID
    else:
        fPath = dirSettings + '/' + siteID + '_' + expName + expID

    # Open file for reading
    if not os.path.exists(fPath):
        os.makedirs(fPath)
    return(fPath)
