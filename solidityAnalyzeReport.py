"""This module contains functionality for hooking in detection modules and
executing them."""

from mythril.mythril import MythrilDisassembler, MythrilAnalyzer
from mythril.ethereum import util
from mythril.analysis.symbolic import SymExecWrapper
#from zoneinfo import ZoneInfo
from backports.zoneinfo import ZoneInfo
from datetime import datetime, timezone
import os
import json
import pytz
import psycopg2
from psycopg2 import Error
from dotenv import load_dotenv, find_dotenv
load_dotenv(find_dotenv())


class SolidityAnalyzeReporter:
    connection = None
    cursor = None
    report = None
    databaseExecSuccess = False

    def get_db_connection(self):
        try:
            self.connection = psycopg2.connect(user=os.getenv('DB_USERNAME'),
                                password=os.getenv('DB_PASSWORD'),
                                host=os.getenv('DB_HOSTNAME'),
                                port=os.getenv('DB_PORT'),
                                database=os.getenv('DATABASE'))
            # Create a cursor to perform database operations
            self.cursor = self.connection.cursor()
        except (Exception, Error) as error:
            print("Error while connecting to PostgreSQL", error)

    def get_db_connection_close(self):

        if self.connection:
            self.connection.close()
            print("PostgreSQL connection is closed")

    def get_db_execute(self, statement):
        try:
            self.get_db_connection()
            self.cursor.execute(statement)

        except Exception as error:
            # log in the file
            return dict({"error": "error occurred in execution of statement in DB"})

    def getPytzReplace(self,dateValue):

        tz = pytz.timezone('Asia/Kolkata')
        dateValue = dateValue.replace(tzinfo=pytz.utc).astimezone(tz)
        dateValue = str(dateValue)[0:16]
        return dateValue

    def getJsonValues(self,jsonData):

        jsonvalues = str(jsonData.values())
        response = jsonvalues[12:len(jsonvalues) - 1]
        response = response.replace("'", '"')
        return response
    
    def getBuildResultList(self):
     
        buildStmt = "select * from build_ids;"
        self.get_db_execute(buildStmt)
        data = self.cursor.fetchall()
        self.get_db_connection_close()
        buildCount = len(data)
        buildResultDict = {}
        for i in range(buildCount):         
           buildResultDict[i] = dict({'id': data[i][0], 'build_id': data[i][1], 'jobname' : data[i][2],
                                      'datepresent':self.getPytzReplace(data[i][4]),'status': data[i][3]})

        return buildResultDict
    
    
    def updateBuildDetails(self,jobName,buildNum, buildInfo):

        buildStmt = "INSERT INTO build_ids (jobname,build_id,status) values (\'" + jobName + "\'," + str(buildNum) + ",\'" + buildInfo + "\');"
        print(buildStmt)
        self.get_db_execute(buildStmt)
        self.connection.commit()
    

    def getStatusOfScan(self, scanId):

        highcount = 0
        lowcount = 0
        mediumcount = 0
        issue_count_high_stmt = " select count(*) from issues where scanId=" + str(scanId)  + " and severity='high'; "
        issue_count_low_stmt = " select count(*) from issues where scanId=" + str(scanId)  + " and severity='low'; "
        issue_count_medium_stmt = " select count(*) from issues where scanId=" + str(scanId)  + " and severity='medium'; "
        self.get_db_execute(issue_count_high_stmt)
        highcount = self.cursor.fetchone()
        self.get_db_execute(issue_count_low_stmt)
        lowcount = self.cursor.fetchone()
        self.get_db_execute(issue_count_medium_stmt)
        mediumcount = self.cursor.fetchone()
        if highcount >= lowcount and highcount >= mediumcount:
            status = "high"
        elif mediumcount >= highcount and mediumcount >= lowcount:
            status = "medium"
        elif lowcount >= highcount and lowcount >= mediumcount:
            status = "low"
        else:
            status = "low"
        return status

    
    def getIssueCount(self, scanId):

        issue_stmt = " select count(*) from issues where scanId = " + str(scanId)
        self.get_db_execute(issue_stmt)
        issueCount = self.cursor.fetchone()
        self.get_db_connection_close()
        return issueCount[0]

    def getIssueDetails(self, issueId):

        issue_stmt = " select * from issues where issueId = " + str(issueId)
        self.get_db_execute(issue_stmt)
        data = self.cursor.fetchall()
        contract_stmt = " select contractname from contracts where contractid = " + str(data[0][2])
        self.get_db_connection_close()
        self.get_db_execute(contract_stmt)
        contract_name = self.cursor.fetchone()
        issue_info_dict = {}
        issue_info_dict = dict({'issueId': data[0][0], 'scanId': data[0][1], 'contractName': contract_name[0],
                                'swcId': data[0][3], 'description_head': data[0][4], 'description_tail': data[0][5],
                                'swctitle': data[0][6], 'linenum': data[0][7], 'filename': data[0][8],
                                'datepresent': data[0][9], 'severity': data[0][10]})
        self.get_db_connection_close()
        return issue_info_dict

    def editScanDetails(self, scanName, date):

        selectScanStmt = "select * from solidityscans where scanname = '" + scanName + "' and cast(datepresent as varchar) LIKE  '" + date + "%';"

        print(selectScanStmt)

        self.get_db_execute(selectScanStmt)
        data = self.cursor.fetchall()

        scanDetailsDict = {}
        if (len(data) > 0):
            datePresent = str(data[0][4])
            scanDetailsDict = dict(
                {'scanid': data[0][0], 'scanname': data[0][1], 'path': data[0][2], 'result': data[0][3],
                 'datepresent': datePresent})
        self.get_db_connection_close()
        return scanDetailsDict

    def updateScanDetails(self, scanId, scanName, result):

        updateScanStmt = "update solidityscans set scanname = '" + scanName + "', result = '" + result + "' where scanid = " + str(scanId) + ';'
        self.get_db_execute(updateScanStmt)
        self.connection.commit()
        self.get_db_connection_close()
        return dict({'result': 'Successfully updated'})

    def deleteScanDetailsWithId(self, scanId):

        deleteScanStmt = " delete from solidityscans where scanId = " + scanId
        self.get_db_execute(deleteScanStmt)
        self.connection.commit()
        self.get_db_connection_close()
        return "Successfully Deleted"

    def deleteScanDetails(self, scanName, Date):

        deleteScanStmt = " delete from solidityscans where scanname = \'" + scanName + "\' and and datepresent = \'" + Date + "%\'"
        self.get_db_execute(deleteScanStmt)
        self.connection.commit()
        self.get_db_connection_close()
        return "Successfully Deleted"

    def getScanList(self):

        scanStmt = " select * from solidityscans"
        self.get_db_execute(scanStmt)
        data = self.cursor.fetchall()
        self.get_db_connection_close()
        return data

    def getScanDetails(self, scanId):

        scanStmt = "select * from solidityscans where scanid =  " + scanId
        self.get_db_execute(scanStmt)
        data = self.cursor.fetchall()
        self.get_db_connection_close()
        return data

    def getNumberOfScans(self):

        scanStmt = "select count(*) from solidityscans;"
        self.get_db_execute(scanStmt)
        data = self.cursor.fetchone()
        self.get_db_connection_close()
        return data[0]

    def getNumberOfSmartContracts(self):

        scanStmt = "select count(*) from contracts;"
        self.get_db_execute(scanStmt)
        data = self.cursor.fetchone()
        self.get_db_connection_close()
        return data[0]

    def getNumberOfVulnerabilities(self):

        scanStmt = "select count(*) from issues;"
        self.get_db_execute(scanStmt)
        data = self.cursor.fetchone()
        self.get_db_connection_close()
        return data[0]

    def getSmartContractsList(self, scanId):

        scanStmt = ""
        if scanId is not None:
            scanStmt = "select * from contracts where scanid = " + str(scanId)
            scanResultStmt = "select result from solidityscans where scanid = " + str(scanId)
        else:
            scanStmt = "select * from contracts"
            scanResultStmt = "select result from solidityscans"
        self.get_db_execute(scanStmt)
        data = self.cursor.fetchall()
        self.get_db_connection_close()
        print (data)

        self.get_db_execute(scanResultStmt)
        result = self.cursor.fetchall()
        self.get_db_connection_close()

        contractCount = len(data)
        contractResultDict = {}
        for i in range(contractCount):
           contractResultDict[i] = dict(
           {'contractId': data[i][0], 'scanId': data[i][1], 'contractname': data[i][2],
            'datepresent': self.getPytzReplace(data[i][3]),'result' : result[i][0]})
        print (contractResultDict)

        return contractResultDict

    def getIssueIdsList(self, scanId):

        # Executing a SQL query
        issueIdsStmt = "select issueid from issues where scanid = " + str(scanId)
        self.get_db_execute(issueIdsStmt)
        issueIdData = self.cursor.fetchall()
        self.get_db_connection_close()
        return issueIdData

    def getIssuesDetailList(self, scanId):

        # Executing a SQL query
        issuesDetailStmt = "select * from issues where scanid = " + str(scanId)
        self.get_db_execute(issuesDetailStmt)
        data = self.cursor.fetchall()
        self.get_db_connection_close()
        totIssues = len(data)
        issueInfoDict = {}
        for i in range(totIssues):
            datevalue = data[i][9]
            datevalue.replace(tzinfo=pytz.utc)
            datevalue = str(datevalue)
            # Executing a SQL query
            contractStmt = "select contractName from contracts where contractId = " + str(data[i][2])
            self.get_db_execute(contractStmt)
            contractName = self.cursor.fetchone()
            self.get_db_connection_close()
            issueInfoDict[i] = dict({'issueId': data[i][0], 'scanId': data[i][1], 'contractname': contractName[0],
                                     'swcId': data[i][3], 'description_head': data[i][4],
                                     'description_tail': data[i][5],
                                     'swctitle': data[i][6], 'linenum': data[i][7], 'filename': data[i][8],
                                     'datepresent': datevalue, 'severity': data[i][10]})

        jsonvalues = str(issueInfoDict.values())
        response = jsonvalues[12:len(jsonvalues) - 1]
        response = response.replace("'", '"')
        return response

    def getSwcIdsList(self, scanId):

        # Executing a SQL query
        SwcIdsStmt = "select swcid from issues where scanid = " + str(scanId)
        self.get_db_execute(SwcIdsStmt)
        swcIdData = self.cursor.fetchall()
        self.get_db_connection_close()
        issueIdsStmt = "select issueid from issues where scanid = " + str(scanId)
        self.get_db_execute(issueIdsStmt)
        issueIdData = self.cursor.fetchall()
        self.get_db_connection_close()
        return issueIdData, swcIdData

    def getCompilerVersion(self, solidity_file):

        solidityFile = open(solidity_file, 'r')
        Lines = solidityFile.readlines()
        compilerVersion = ''
        for line in Lines:
            if ('pragma' in line):
                totLenOfLine = len(line)
                found = line.find("^", 0, totLenOfLine)
                if (found != -1):
                    compilerVersion = line[found + 1:totLenOfLine - 2]
                else:
                    gtfound = line.find(">=", 0, totLenOfLine)
                    ltfound = line.find('<', 0, totLenOfLine)
                    compilerVersion = line[gtfound + 2:ltfound - 1]
                    if (line[ltfound - 1] == '.'):
                        compilerVersion = compilerVersion + '0'
                        print(compilerVersion)
                break
        commandToExec = 'solc-select install ' + compilerVersion
        os.system(commandToExec)
        commandToExec = 'solc-select use ' + compilerVersion
        os.system(commandToExec)

        return compilerVersion

    # pass solidityFiles List
    def solidity_scan(self, basePath, solidityFile, scanName):
        solidity_file = basePath + '/' + solidityFile
        current_scan_id = 0
        result = ''
        current_date_present = ''
        # Dynamically pass the compiler
        compilerVersion = self.getCompilerVersion(solidity_file)
        disassembler = MythrilDisassembler(eth=None, solc_version=compilerVersion)
        addressVal, contracts = disassembler.load_from_solidity([str(solidity_file)])

        for contract in contracts:

            analyzer = MythrilAnalyzer(disassembler)
            sym = SymExecWrapper(
                contract,
                address=util.get_indexed_address(0),
                strategy="dfs",
                execution_timeout=500, )
            # report
            report = analyzer.fire_lasers(sym)

            outputs = json.loads(str(report.as_swc_standard_format()))
            issue_dict = outputs[0]
            issueCount = len(issue_dict['issues'])

            result = ''
            if issueCount > 0:
                result = 'vulnPresent'
            else:
                result = 'vulnNotPresent'
            # Executing a SQL query
            scanStmt = "INSERT INTO solidityscans (scanname, path, result) values (\'" + scanName + "\',\'" + solidity_file + "\',\'" + result + "\');"

            self.get_db_execute(scanStmt)
            self.connection.commit()
            self.cursor.execute("SELECT MAX(scanid), MAX(datePresent) FROM solidityscans;")
            data = self.cursor.fetchall()
            self.get_db_connection_close()
            current_scan_id = data[0][0]
            current_date_present = data[0][1]

            fileStmt = "INSERT INTO Files (scanid,filename) values (" + str(
                current_scan_id) + ",\'" + solidityFile + "\');"
            self.get_db_execute(fileStmt)
            self.connection.commit()
            self.get_db_connection_close()
            contractStmt = "INSERT INTO Contracts (scanid,contractname,datepresent) values (" + str(
                current_scan_id) + ",\'" + contract.name + "',\'" + str(current_date_present) + "\');"
            self.get_db_execute(contractStmt)
            self.connection.commit()
            self.get_db_connection_close()
            maxContractStmt = "SELECT MAX(contractid) FROM contracts;"
            self.get_db_execute(maxContractStmt)
            data = self.cursor.fetchone()
            self.get_db_connection_close()
            current_contract_id = data[0]

            for i in range(issueCount):
                issue = issue_dict['issues'][i]
                description_head = issue_dict['issues'][i]['description']['head']
                description_tail = issue_dict['issues'][i]['description']['tail']
                severity = issue_dict['issues'][i]['severity']
                swcID = issue_dict['issues'][i]['swcID']
                swcTitle = issue_dict['issues'][i]['swcTitle']
                sourceMap = issue_dict['issues'][i]['locations'][0]['sourceMap']
                address = sourceMap.partition(":")[0]
                remaining = sourceMap.partition(":")[2]
                index = remaining.partition(":")[2]
                sourceCodeInfo = contract.get_source_info(int(address))
                lineNum = 0
                fileName = ''
                if (sourceCodeInfo is not None):
                    lineNum = sourceCodeInfo.lineno
                    fileName = sourceCodeInfo.filename
                if lineNum is None:
                    lineNum = 0
                    fileName = contract.name

                issueStmt = "INSERT INTO Issues (scanid,contractid,swcid,descriptionhead,descriptiontail,swctitle,linenum,filename,datepresent, severity) values (" + str(
                    current_scan_id) + "," + str(
                    current_contract_id) + ",\'" + swcID + "\',\'" + description_head + "\',\'" + description_tail + "\',\'" + swcTitle + "\'," + str(
                    lineNum) + ",\'" + fileName + "\',\'" + str(current_date_present) + "\',\'" + severity + "\');"
                self.get_db_execute(issueStmt)
                self.connection.commit()
                self.get_db_connection_close()
        return current_scan_id, result, current_date_present


if __name__ == "__main__":
    SolidityAnalyzeReporter().solidity_scan()
