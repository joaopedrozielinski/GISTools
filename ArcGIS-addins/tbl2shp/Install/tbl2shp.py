"""
table2shape v 0.1

This software is released into the public domain as an open source.  
You are free to use it in any way you like, i.e. copy, share, modify, reproduce or in any ways that are described under open source license.
Except that you may credit the work to the original developer.

This software is provided "as is" with no expressed or implied warranty.
I accept no liability for any damage or loss of business that this software may cause.
However, I am more than happy to recieve any bugs reports via email address below.
The bugs will be addressed within my project scope.
 
This software has been tested with ArcGIS Desktop 10 series.
The test suites are not attached with this software package.

This source code is originally written by Vong Vithyea Srey (srey.vongvithyea@gmail.com).
The first version is released on 29th Nov 2013.

"""



import arcpy
import pythonaddins as pa
import os.path



"""
Global dictionary to hold all the contents of the messages in this package
"""
msgDict = { "OpenDialog" : "Select a table file",
            "SaveDialog" : "Save to",
            "TabCannotFound" : "The table file can not be found, please try again.",
            "NotContainXYCoords" : "The given table does neither contain XCoord nor YCoord field.\nPlease edit the given table before trying again.",
            "FileNameErr" : "File name is not correct. Please try again.",
            "GenErrToDev" : "Report below error to the developer via: srey.vongvithyea@gmail.com\n",
            "WantReplace?" : "The given file name exists. Would you like to replace?\n\"Replace\" means that the existing file will be purged and replaced with a new file.\nIf you are not replacing it, the new features will be appended to the end of the existing shapefile.",
            "PointSetInsufficient" : "Some Points Sets are insufficient to form a feature.\ni.e. A line must be formed by a set of at least 2 points. A polygon must be formed by a set of at least 3 points.\nWould you like to skip those sets and continue?",
            "DifferentTypeCantAppend" : "The existing shapefile contains a different type of geometry. \nThe process cannot be completed successfully"
          }

"""
Global Constants used to seperate (argument) geometry types between Polyline and Polygon.
"""
GEOM_LINE_STR = "polyline"
GEOM_GON_STR = "polygon"



"""
Global method (a helper) to do read the X-Y coordinates and the path to save the file
@return xyCoords: is an array of tuples (x, y), which each tuple is (x, y) coordinate of a point
@return shpPath: a shapefile path that the geometry objects will be saved to
"""
def getXYCoordsAndShpPath():
    # get a helper to read the input path
    dbfPath = readPath()
    if dbfPath is None: return (None, None)

    # get a helper to read the table and return the array of X-Y coordinates
    xyCoords = getXYCoordsFromGivenFileAsArrayOfTuples(dbfPath)
    if xyCoords is None: return (None, None)

    # get a helper to get the path to be saved to
    shpPath = savePath()
    if shpPath is None: return (None, None)
        
    return (xyCoords, shpPath)



"""
Global method (a helper) to get the path of the table file.
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
Global method (a helper) to get the path to save file to.
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
Global method (a helper) to get the X-Y coordinate from the given file.
@parameter file: is the path to the table file. (it can be *.shp, *.dbf and *.csv)
@ return : an array of X-Y coordinate values
         : None if there is a problem in reading the field XCoord and YCoord from the given file path
"""
def getXYCoordsFromGivenFileAsArrayOfTuples(file):
    # if the given file path doesn't exist
    if not os.path.exists(file):
        pa.MessageBox(msgDict["TabCannotFound"], "Error")
        return None

    # geting the array of X-Y coordinates
    try:
        xyNumPyArr = arcpy.da.TableToNumPyArray(file, ("xcoord", "ycoord"))
        return [tuple(xyNumpy) for xyNumpy in xyNumPyArr]

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
Global method (a helper) to pop up a general unexpected error message.
The message content is telling user to contact developer to solve the error.
"""
def printErrorMessage(e):
    txt = msgDict["GenErrToDev"]
    txt = txt + "\"" + e.message  + "\""
    pa.MessageBox(txt, "Error", 0)



"""
Global method (a helper) to tell the user the path needed to be save to exists,
and ask if it should be replaced.
@return: True if the user's answer is "Yes"
       : Flase otherwise
"""
def doesUserWantingToReplace():
    result = pa.MessageBox(msgDict["WantReplace?"],"File exists.", 4)
    return True if result == "Yes" else False



"""
Global method (a helper) to tell the user that the give table cotaining some points sets
that containing insufficient points to form a geometry type.
i.e. a line must be formed by a points set of at least 2 points
     a polygon must be formed by a points set of at least 3 points
@return: True if the user's answer is "Yes"
       : Flase otherwise
"""
def doesUserWantingToSkipInsufficientPointsSets():
    result = pa.MessageBox(msgDict["PointSetInsufficient"], "Error", 4)
    return True if result == "Yes" else False



"""
Global method (a helper) to convert the given xyCoords into array of Points Sets (representing all geometry features).
i.e. a Points Set (which is an element of the result array), which is an array, is representing a geometry feature.
@param xyCoords: is an array that stores all the points representing all the features
    
    # e.g: a value of xyCoords: [(1,2,), (2,3), (0,0), (5,5), (6,6), (0,0), (3,2), (5,6)]
    # this xyCoords representing 3 lines: [(1,2,), (2,3)], [(5,5), (6,6)] and [(3,2), (5,6)]
    # the returning results should be: [[(1,2,), (2,3)], [(5,5), (6,6)], [(3,2), (5,6)]]

    # e.g: a value of xyCoords: [(5,2), (1,2,), (2,3), (0,0), (5,5), (6,6), (9,9), (8,8)]
    # this xyCoords representing 2 polygons: [(5,2), (1,2,), (2,3)] and [(5,5), (6,6), (9,9), (8,8)]
    # the returning results should be: [[(5,2), (1,2,), (2,3)], [(5,5), (6,6), (9,9), (8,8)]]
@return: is an array of features. Each feature is an array of points which is forming that feature.
"""
def convertXYCoordsArrayToFeatPtnsArray(xyCoords):
    # an array of points (a Points Set) representing a geometry feature
    aFeatPtns = []
    # an array of geometry features 
    featPtnsArray = []

    # xyCoords store all the points representing all the geometry features
    # a set of points (representing a geometry feature) seperated by (0,0)
    # e.g: a value of xyCoords: [(1,2,), (2,3), (0,0), (5,5), (6,6), (0,0), (3,2), (5,6)]
    # this xyCoords representing 3 lines: [(1,2,), (2,3)], [(5,5), (6,6)] and [(3,2), (5,6)]
    # this loop put each set of points (representing a line) into an array
    # and these arrays (representing all the lines) will be stored in featPtnsArray
    # (It works the same way for Polygon)
    for xyCoord in xyCoords:
        # when reach a seperator, flush out the aFeatPtns into featPtnsArray
        # then restart the process
        if xyCoord == (0,0) and aFeatPtns != []:
            featPtnsArray.append(aFeatPtns)
            aFeatPtns = []
            continue

        # storing the (x,y) value into the aFeatPtns
        if xyCoord != (0,0):
            aFeatPtns.append(xyCoord)

    # after complete for loop, check if the aFeatPtns is not empty.
    # if it is not, then flush it out to featPtnsArray
    if aFeatPtns != []:
        featPtnsArray.append(aFeatPtns)

    return featPtnsArray



"""
Convert the given array of features (each feature is an array of points) to the array of geometry object (either Polyline or Polygon depends on given geometry type)
@param featPtnsArray: is an array of feature, which each feature is an array of points. (more description at the convertXYCoordsArrayToFeatPtnsArray() method)
@param geometryType: is a string to represent whether the returning result is an array of Polyline or Polygon.
@return: is an array of geometry object (either Polyline or Polygon, depends on geometryType).
"""
def convertFeatPtnsArrayToPolygeometryArray(featPtnsArray, geometryType):
    # an array of geometry object (either Polyline or Polygon object)
    polygeomArray = []
    firstTimeToAsk = True
    userWantToSkipInsufficientPoints = False
        
    # this loop convert each set of points (representing a geometry object (either Polyline or Polygon object)) to a geometry object
    # and put all the geometry objects into polygeomArray variable
    for aFeatPtns in featPtnsArray:
        # If geometry type is polyline, then the points of a feature must be at least 2
            # because a Polyline is made up by at least 2 points
        # If geometry type is polygon, then the points of a feature must be at least 3
            # because a Polygon is made up by at least 3 points
        if (geometryType == GEOM_LINE_STR and len(aFeatPtns) < 2) or (geometryType == GEOM_GON_STR and len(aFeatPtns) < 3):
            # if it is first time, then ask the user
            if firstTimeToAsk:
                # ask user if they want to continue by skipping the sets that containing insufficient points
                userWantToSkipInsufficientPoints = doesUserWantingToSkipInsufficientPointsSets()
                firstTimeToAsk = False
            # if it is not first time, means that the user chose to skip (if user didn't choose to skip the method return, and this line cannot be re-executed)

            
            # if user wants to skip, then the process continue by just skipping those sets
            if userWantToSkipInsufficientPoints:
                continue
            # if user doesn't want to skip, then cancel the process, since it doesn't make sense to continue.
            else:
                return

        # add geometry objects into the array
        if geometryType == GEOM_LINE_STR:
            polygeomArray.append(arcpy.Polyline(  arcpy.Array([arcpy.Point(*coord) for coord in aFeatPtns] )  ))
        else:
            polygeomArray.append(arcpy.Polygon(  arcpy.Array([arcpy.Point(*coord) for coord in aFeatPtns] )  ))
    return polygeomArray        



"""
write the given array (of geometry objects) into the shapefile which is determined by the given path (shpPath)
@param: geomArray is an array of geometry objects (it can be MultiPoint, Polyline or Polygon geometry)
@param: shpPath is a file path that the geometry will be saved to
"""
def writeGeometryObjectsArrayToShapeFile(geomArray, shpPath):
    try:
        if os.path.exists(shpPath):
            userWantToReplace = doesUserWantingToReplace()

            # if user want to replace, then just trigger the overwriteOutput boolean to True
            # The CopyFeatures_management() method will remove the existing file and create a new one
            if userWantToReplace:
                arcpy.env.overwriteOutput = True

            # otherwise append to the existing file
            else:
                # if the geometry type of the existing shapefile is different from the array elements
                # Then, the process can't be completed. So, pop up a message telling the user.
                if arcpy.Describe(shpPath).shapeType.lower() != geomArray[0].type.lower():
                    pa.MessageBox(msgDict["DifferentTypeCantAppend"], "Error")
                    return

                arcpy.Append_management(geomArray, shpPath,"NO_TEST", "", "")
                return

        # create a new Geometry (MultiPoint, Polyline or Polygon - depend on the given geomArray) shapefile
        arcpy.CopyFeatures_management(geomArray, shpPath)

    except arcpy.ExecuteError as ee:
        if "The name contains invalid characters" in ee.message :
                pa.MessageBox(msgDict["FileNameErr"], "Error")
                return

        errMsg = ee.message + "Please try again."
        pa.MessageBox(errMsg, "Error")
            
    except Exception as e:
        errMsg = e.message + "Please try again."
        a.MessageBox(errMsg, "Error")











##################################################################
#                                                                #
"""   Class handle the click event of the tabble2line button   """
#                                                                #
##################################################################

class tbl2Line(object):
    """Constructor"""
    def __init__(self):
        self.enabled = True
        self.checked = False
		


    """
    Implementation for table2shape.tbls2LineBtn (Button)
    This method get called when the button has been clicked
    """
    def onClick(self):
        # get the array of X-Y coordiantes and the path to be saved to
        xyCoords, shpPath = getXYCoordsAndShpPath()
        if xyCoords is None or shpPath is None: return

        # more detail of this code described in the method itself
        featPtnsArray = convertXYCoordsArrayToFeatPtnsArray(xyCoords)
        if featPtnsArray is None or featPtnsArray == []: return

        # more detail of this code described in the method itself
        polylineArray = convertFeatPtnsArrayToPolygeometryArray(featPtnsArray, geometryType = GEOM_LINE_STR)
        if polylineArray is None or featPtnsArray == []: return

        writeGeometryObjectsArrayToShapeFile(polylineArray, shpPath)
            









##################################################################
#                                                                #
""" Class handle the click event of the tabble2Polygon button  """
#                                                                #
##################################################################
    
class tbl2Plgon(object):
    
    """Constructor"""
    def __init__(self):
        self.enabled = True
        self.checked = False



    """
    Implementation for table2shape.tbls2PlgonBtn (Button)
    This method get called when the button has been clicked
    """
    def onClick(self):
        # get the array of X-Y coordiantes and the path to be saved to
        xyCoords, shpPath = getXYCoordsAndShpPath()
        if xyCoords is None or shpPath is None: return

        # more detail of this code described in the method itself
        featPtnsArray = convertXYCoordsArrayToFeatPtnsArray(xyCoords)
        if featPtnsArray is None or featPtnsArray == []: return

        # more detail of this code described in the method itself
        polygonArray = convertFeatPtnsArrayToPolygeometryArray(featPtnsArray, geometryType = GEOM_GON_STR)
        if polygonArray is None or featPtnsArray == []: return

        writeGeometryObjectsArrayToShapeFile(polygonArray, shpPath)

		








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
    Implementation for table2shape.tbl2PntsBtn (Button)
    This method get called when the button has been clicked
    """
    def onClick(self):
        # get the array of X-Y coordiantes and the path to be saved to
        xyCoords, shpPath = getXYCoordsAndShpPath()
        if xyCoords is None or shpPath is None: return

        # make array of PointGeometry objects
        ptGeoms = [arcpy.PointGeometry(arcpy.Point(*XY)) for XY in xyCoords]
            
        writeGeometryObjectsArrayToShapeFile(ptGeoms, shpPath)
