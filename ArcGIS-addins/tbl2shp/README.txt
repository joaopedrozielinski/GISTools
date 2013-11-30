Table2Shape
===========


* What this package includes:
=============================

  tbl2shp folder:

    + makeaddin.py          : A script that will create a .esriaddin file out of this 
                              project, suitable for sharing or deployment.

    + config.xml            : The AddIn configuration file.
 
    + Install/tbl2shp.py    : The Python project used for the implementation of the
                              AddIn. The specific python script to be used as the root
                              module is specified in config.xml.

   tbl2shp.esriaddin        : The add-in tool

   README.txt               : This file

   pntTblExmpl.csv          : The example of the input table file that need to be coverted to Point shapefile.

   polyLGTblExmpl.csv       : The example of the input table file that need to be coverted to either Polyline or Polygon shapefile.






* Installation Requirements:
============================
  + ArcGIS Desktop 10.0 or higher

  + Python 2.6 or higher (Normally it comes with ArcGIS Desktop 10.0)





* Installation Instruction:
===========================
  + Double-click on tbl2shp.esriaddi

  + Follow the instruction dialog





* What is the input (table file):
=================================
  + The table file can be *.dbf, *.cvs or *.shp.

  + The table file must contain XCoord field and YCoord field

  + For table file that represent the Polyline or Polygon:
    The coordinates of each set of points for each feature (i.e. each line or polygon) 
    is seperated by value XCoord=0 and YCoor=0. (The example of table file is given in polyLGTblExmpl.csv)

     - In the given example (polyLGTblExmpl.csv): There are 3 features (of either line or polygon). 
     It means that:
     - the tbl2line tool will produce a polyline shapefile containing 3 different lines
     - the tbl2plgon tool will produce a polygon shapefile containing 3 different polygon

  *** This rule does not apply on tbl2Point function. The tbl2Point will convert all the values to the
      poits regardless of those values. (The example of the table file is given in ptnTblExmpl.csv)





* How to get it in ArcMap:
==========================
  + Customize -> Add-In Manager... 

  + In the Add-In Manager table, the tbl2shp is shown in the My Add-Ins block.
    If tbl2shp is not shown here, please re-install it.

  + Click on Customize... button

  + In Customize table, tick on tbl2shp which is listed in Toolbars list.

  + Click on any button you wish to use:
    - 2Pnt Button: Convert the given table file to a Point Shapefile
    - 2Line Button: Convert the given table file to a Polyline Shapefile
    - 2Plgon Button: Convert the given table file to a Polygon Shapefile





* Disclaimer and License:
=========================

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
      




* Do not freak out:
===================

Since ArcGIS Engine is not supporting multi-tasking on multi processors.
Thus this software is solely running on a single processor, regardless of your system architecture.

If you have a big data (normally it would be more than 500,000 features ~ about a few million points), the ArcMap will look like
not responding. However, it is busy in processing those data.

Please check the Task Manager if you are concerning about the process.

