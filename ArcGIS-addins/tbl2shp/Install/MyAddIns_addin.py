import arcpy
import pythonaddins as pa
#from threading import Thread
import multiprocessing

def readPath():
    path = ""
    try:
        path = pa.OpenDialog("Select a dBase file", False, "C:/Users/Hiang/Documents", "Open")
    except Exception as e:
        printErrorMessage(e)
        path = None
    return path

def savePath():
    path = ""
    try:
        path = pa.SaveDialog("Save to", "", "~/")
    except Exception as e:
        printErrorMessage(e)
        path = None
    return path


def getXYCoordsAsArrayOfTuples(file):
    xyCoords = []
    try:
        xyCoords = arcpy.da.TableToNumPyArray(file, ("xcoord", "ycoord"))
    except Exception as e:
        printErrorMessage(e)
        xyCoords = None
        pass

    
    return xyCoords



def printErrorMessage(e):
    txt = "Report below error to the developer at: srey.vongvithyea@gmail.com\n"
    txt = txt + "\"" + e.message  + "\""
    pa.MessageBox(txt, "Error", 0)










class tbl2Line(object):
    """Implementation for MyAddIns_addin.dbf2LinesBtn (Button)"""
    def __init__(self):
        self.enabled = True
        self.checked = False
    def onClick(self):
        pass

class tbl2Plgone(object):
    """Implementation for MyAddIns_addin.dbf2PlgoneBtn (Button)"""
    def __init__(self):
        self.enabled = True
        self.checked = False
    def onClick(self):
        pass






class tbl2Pnt(object):
    """Implementation for MyAddIns_addin.dbf2PntsBtn (Button)"""
    def __init__(self):
        self.enabled = True
        self.checked = False
    def onClick(self):
        print "start"

       
        
        dbfPath = readPath()
        print dbfPath
        if dbfPath is None:
            print "None here"
            return
        

        print "process started"

        
        xyCoords = getXYCoordsAsArrayOfTuples(dbfPath)
        if xyCoords is None:
            return
        #print xyCoords

        print "process finished"

        shpPath = savePath()
        print shpPath
        if shpPath is None:
            print "None here"
            return
        
        # make array of new point features
        ptGeoms = [arcpy.PointGeometry(arcpy.Point(*XY)) for XY in xyCoords]


        arcpy.CopyFeatures_management(ptGeoms, shpPath)

        #arcpy.Append_management(ptGeoms, shpPath,"NO_TEST", "", "")




        
        print "end"

