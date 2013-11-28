import arcpy
import pythonaddins as pa
import os.path



"""
Static dictionary to hold all the contents of the messages in this package
"""
msgDict = { "OpenDialog" : "Select a table file",
            "SaveDialog" : "Save to",
            "TabCannotFound" : "Table file can not be found, please try again.",
            "NotContainXYCoords" : "The given table does neither contain XCoord nor YCoord field.\nPlease edit the given table before trying again.",
            "FileNameErr" : "File name is not correct. Please try again.",
            "GenErrToDev" : "Report below error to the developer at: srey.vongvithyea@gmail.com\n",
            "WantReplace?" : "The given file name exists. Would you like to replace?\n\"Replace\" means that the existing file will be purged and replaced with a new file."
          }



"""
Static method (a helper) to do read the X-Y coordinates and the path to save the file
"""
def getXYCoordsAndShpPath():
    # get a helper to read the input path
    dbfPath = readPath()
    if dbfPath is None: return (None, None)

    # get a helper to read the table and return the array of X-Y coordinates
    xyCoords = getXYCoordsAsArrayOfTuples(dbfPath)
    if xyCoords is None: return (None, None)

    # get a helper to get the path to be saved to
    shpPath = savePath()
    if shpPath is None: return (None, None)
        
    return (xyCoords, shpPath)



"""
Static method (a helper) to get the path of the table file.
Table file can be shapefile (*.shp), dBase file (*.dbf) and *.CSV
@return : the path of the file need to be opened
        : None if the opening process is not successful
"""
def readPath():
    try:
        return pa.OpenDialog(msgDict["OpenDialog"], False, "~/", "Open")
    except Exception as e:
        printErrorMessage(e)
        return None

    

"""
Static method (a helper) to get the path to save file to.
The save path must be followed the Windows name rules.
The save path should be finished
@return : the path that file needed to be saved to
        : None if the process is not successful
"""
def savePath():
    try:
        path = pa.SaveDialog(msgDict["SaveDialog"], "", "~/")
        if path is None: return None

        # trying to add ".shp" to the end of the path if it is not included
        path = path.strip()
        if path.rfind(".shp") != (len(path) - len(".shp")):
            if path.rfind(".") != (len(path) -1): path += ".shp"
            else: path += "shp"
            
        if path.count(".") > 1:
            pa.MessageBox(msgDict["FileNameErr"], "Error")
            return None
        return path
        
    except Exception as e:
        printErrorMessage(e)
        return None



"""
Static method (a helper) to get the X-Y coordinate from the given file.
@parameter file: is the path to the table file. (it can be *.shp, *.dbf and *.csv)
@ return : an array of X-Y coordinate values
         : None if there is a problem in reading the field XCoord and YCoord from the given file path
"""
def getXYCoordsAsArrayOfTuples(file):
    # if the given file path doesn't exist
    if not os.path.exists(file):
        pa.MessageBox(msgDict["TabCannotFound"], "Error")
        return None

    # geting the array of X-Y coordinates
    try:
        return arcpy.da.TableToNumPyArray(file, ("xcoord", "ycoord"))

    # if there is neither "xcoord" nor "ycoord" the TableToNumPyArray will raise RuntimeError
    except RuntimeError as re:
        if "A column was specified that does not exist" in re.message:
            pa.MessageBox(msgDict["NotContainXYCoords"], "Error")
            return None

    # other unexpected error that can be caused by user activities
    except Exception as e:
        printErrorMessage(e)
        return None



"""
Static method (a helper) to pop up a general unexpected error message.
The message content is telling user to contact developer to solve the error.
"""
def printErrorMessage(e):
    txt = msgDict["GenErrToDev"]
    txt = txt + "\"" + e.message  + "\""
    pa.MessageBox(txt, "Error", 0)



"""
Static method (a helper) to tell the user the path needed to be save to exists,
and ask if it should be replaced.
"""
def doesUserWantingToReplace():
    result = pa.MessageBox(msgDict["WantReplace?"],
                           "File exists.", 4)
    return True if result == "Yes" else False









##################################################################
#                                                                #
"""   Class handle the click event of the tabble2line button   """
#                                                                #
##################################################################

class tbl2Line(object):
    """Implementation for MyAddIns_addin.dbf2LinesBtn (Button)"""
    def __init__(self):
        self.enabled = True
        self.checked = False
    def onClick(self):
        pass









##################################################################
#                                                                #
""" Class handle the click event of the tabble2Polygon button  """
#                                                                #
##################################################################
    
class tbl2Plgon(object):
    """Implementation for MyAddIns_addin.dbf2PlgoneBtn (Button)"""
    def __init__(self):
        self.enabled = True
        self.checked = False
    def onClick(self):
        pass









##################################################################
#                                                                #
"""  Class handle the click event of the table2Poit button     """
#                                                                #
##################################################################
    
class tbl2Pnt(object):
    
    """ Constructor """
    def __init__(self):
        self.enabled = True
        self.checked = False



    """
    Implementation for MyAddIns_addin.dbf2PntsBtn (Button)
    This method get called when the button has been clicked
    """
    def onClick(self):
        # get the array of X-Y coordiantes and the path to be saved to
        xyCoords, shpPath = getXYCoordsAndShpPath()
        if xyCoords is None: return

        try:
            # make PointGeometry object
            ptGeoms = [arcpy.PointGeometry(arcpy.Point(*XY)) for XY in xyCoords]
            
            if os.path.exists(shpPath):
                userWantToReplace = doesUserWantingToReplace()

                # if user want to replace, then just trigger then overwriteOutput boolean to True
                # The CopyFeatures_management() method will remove the existing file and create a new one
                if userWantToReplace:
                    arcpy.env.overwriteOutput = True

                # other append to the existing file
                else:
                    arcpy.Append_management(ptGeoms, shpPath,"NO_TEST", "", "")
                    return

            # create a new Point shapefile
            arcpy.CopyFeatures_management(ptGeoms, shpPath)

        except arcpy.ExecuteError as ee:
            errMsg = ee.message + "Please try again."
            pa.MessageBox(errMsg, "Error")
            
        except Exception as e:
            errMsg = e.message + "Please try again."
            pa.MessageBox(errMsg, "Error")
