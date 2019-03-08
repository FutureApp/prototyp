#!/usr/bin/python

import sys, getopt
import influxdb as idb
import pandas as pd
from os import path

DEBUG = True

# the default values, could be override during program-call
input_host              = 'inlfux-server'
input_port              = 8086
input_searchingDB       = 'k8s'
input_exportTyp         = 'xlsx'
input_exportDir         = '/results'
input_exportFilename    = 'exp_00'
input_leftTimeBorder    = '000000000000'
input_rightTimeBorder   = '000000000000'

    
def main(argv):
    print("in")
    handleInput(argv)
    print(input_host)
    print("out")
    exit(0)
    input_searchingForDB    = '_internal'
    client                  = idb.InfluxDBClient(host='localhost',port=8086)
    myDBExists              = existsDB(client,input_searchingForDB)
    
    if not myDBExists:
        abortExecBecauseDBNotFound(input_searchingForDB)

    client.switch_database(database = input_searchingForDB)
    
    listOfMeasurements = client.get_list_measurements()
    exWriter = pd.ExcelWriter('./export_dataframe2.xlsx')
    for measurement in listOfMeasurements:
        nameOfMea = measurement['name']
        print(nameOfMea)
        query = 'SELECT * FROM "{}"'.format(nameOfMea)
        points = client.query(query, chunked=True, chunk_size=10000).get_points()
        dfs = pd.DataFrame(points)
        dfs.to_excel(exWriter,sheet_name=nameOfMea)
    exWriter.close()

def handleInputs(argv):
    print("Input handle")
    try:
        opts, args = getopt.getopt(argv,"h",["host="])
    except getopt.GetoptError:
        printHelpAndExit()
    for opt, arg in opts:
      if opt == '-h':
          printHelpAndExit()
      elif opt in ("--host"):
         inputfile = arg
        
def printHelpAndExit():
    print(  """Usage & Help
    The purpose of the script is to call given InfluxDB-instance in order to download all performance data from a specific
    database and export each measurements. HINT: Each value contains defaults-value which are set already.
    E.g call: bash collector.py --host=localhost --port=8086    

    --host      <name>                  : Specifies here how to access the influxdb-server. E.g the <IP-address> or maybe <localhost> 
    --port      <number>                : Portnumber where to call the influxdb-server on.
    --dbname    <name>                  : Name of the DB where to collect data from.
    --exportTyp <xlxs|sep-xlxs|cvs>     : xlxs      - for excel-export. One measurement to one sheet on the same workbook
                                          sep-xlxs  - for excel-export. Each measurment goes into a differente workbook
                                          cvs       - for cvs-export. Each measurment goes into a differente file.
    --exportDir <pathToDir>             : Path to directory where to export all files. If Dir not exists then a new dir will be created.
    --leftTimeBorder                    : Specifie the lowest/latest timestamp you are intressted in.      Default 00000000
    --rightTimeBorder                   : Specifie the highest/recently timestamp you are intressted in.   Default 99999999
            """)
    sys.exit(2)
def handleInput(argv):
   try:
      opts, args = getopt.getopt(argv,"h",["help=","host=" ,"port=","dbname=","exportTyp=","exportDir=","leftTimeBorder=","rightTimeBorder="])
   except getopt.GetoptError:
        print("gtop error")
        printHelpAndExit()
        sys.exit(2)
   for opt, arg in opts:
        if opt == '-h':
            print("-h")
            printHelpAndExit()
        elif opt in ("--help"):
            printHelpAndExit()
        elif opt in ("--host"):
            print("deck")
            input_host = arg
        elif opt in ("--port"):
            print("deck")
            input_port = arg
        elif opt in ("--dbname"):
            input_searchingDB = arg
        elif opt in ("--exportTyp"):
            input_exportTyp = arg
        elif opt in ("--exportDir"):
            input_exportDir = arg
        elif opt in ("--leftTimeBorder"):
            input_leftTimeBorder = arg
        elif opt in ("--rightTimeBorder"):
            input_rightTimeBorder = arg




def queryEverythingFromMeasure(client, meas):
    query='SELECT * FROM "{}"'.format(meas)
    qResult = client.query(query = query)
    print(qResult)

def debugPrint(message):
    if(DEBUG == True):
        print('DEBUG: ' + message)

def abortExecBecauseDBNotFound(dbname):
    print('Execution will stop because the required DB < {} > was not found.'.format(dbname))
    print('Stoping now.')
    sys.exit(1)

def existsDB(influxdbClient, DBName):
    found = False
    for dbs in influxdbClient.get_list_database():
        if dbs['name'] == DBName:
            found = True
            break
    return found
    
main(sys.argv[1:])