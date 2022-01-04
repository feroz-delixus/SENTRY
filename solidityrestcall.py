from flask import Flask, request, redirect, render_template
from flask_cors import CORS, cross_origin
from pathlib import Path
import os, sys, jenkins

logFileWr = None
api = Flask(__name__)
CORS(api, resources={r"/api/*": {"origins": "*"}})
api.config['CORS_HEADERS'] = 'Content-Type'


CURRENT_DIR = os.path.dirname(os.path.abspath(__file__))
sys.path.append(os.path.dirname(CURRENT_DIR))
from solidityAnalyzeReport import SolidityAnalyzeReporter

mythModule = SolidityAnalyzeReporter()


@api.errorhandler(Exception)
def handle_exception(error):
    return {'message': str(error)}, getattr(error, 'code', 500)


@api.route('/')
def rediret_to_mythril_frontend():
    return redirect("http://13.126.95.15", code=302)


@api.route("/api")
def index():
    return "Mythril scan APIs - Test CI/CD. Root API call"

def getBuildInfo(jobName):
   jenkinsAccess = jenkins.Jenkins('http://localhost:8080', username='valliammal', password='delixus-123');
   last_build_number = jenkinsAccess.get_job_info(jobName)['lastCompletedBuild'] ['number']
   build_info=jenkinsAccess.get_build_info(jobName,last_build_number)
   if build_info['result']=='SUCCESS':
      print("Build Success ")
   else:
      print(" Build Failed ")
   return dict({'JobName': jobName, 'build_number' : last_build_number, 'build_info' : build_info['result'] })

# http://localhost:5000/api/buildDetails
@api.route('/api/buildDetails', methods=['GET'])
def getBuildDetails():
    executeWithDB = request.args.get('storeInDb')
    buildDetailsDict = {}
    jobName = 'Python-Backend-APIs'
    buildDetailsDict[0] = getBuildInfo(jobName)
    jobName = 'Frontend-Angular'
    buildDetailsDict[1] = getBuildInfo(jobName)
  
    if (executeWithDB == '1'):
       mythModule.updateBuildDetails(buildDetailsDict[0]['JobName'],buildDetailsDict[0]['build_number'], buildDetailsDict[0]['build_info'])
       mythModule.updateBuildDetails(buildDetailsDict[1]['JobName'],buildDetailsDict[1]['build_number'], buildDetailsDict[1]['build_info'])
    

    return mythModule.getJsonValues(buildDetailsDict)

#http://localhost:5000/api/getBuildInfo
@api.route('/api/getBuildInfo', methods=['GET'])
def get_build_info():
    buildResultDict = mythModule.getBuildResultList()
    return mythModule.getJsonValues(buildResultDict)

    
# http://localhost:5000/api/numberOfScans
@api.route('/api/numberOfScans', methods=['GET'])
def getNumberOfScans():
    numberOfScans = mythModule.getNumberOfScans()
    return dict({'numberOfScans': numberOfScans})


# http://localhost:5000/api/numberOfSmartContracts
@api.route('/api/numberOfSmartContracts', methods=['GET'])
def getNumberOfSmartContracts():
    numberOfSmartContracts = mythModule.getNumberOfSmartContracts()
    return dict({'numberOfSmartContracts': numberOfSmartContracts})


# http://localhost:5000/api/numberOfVulnerabilities
@api.route('/api/numberOfVulnerabilities', methods=['GET'])
def getNumberOfVuln():
    numberOfVuln = mythModule.getNumberOfVulnerabilities()
    return dict({'numberOfVuln': numberOfVuln})


# http://localhost:5000/api/numberOfIssues
@api.route('/api/numberOfIssues', methods=['GET'])
def getNumberOfIssues():
    scanId = request.args.get('scanId')
    if (scanId == None):
        issuesList = dict({'error': 'please enter the ScanId'})
    else:
        numberOfIssues = mythModule.getIssueCount(scanId)
        return dict({'numberOfIssues': numberOfIssues})

# http://localhost:5000/api/startScan?solidityFile=mapping_write.sol&basePath=/home/delixus/solidity/sol0.4.25&scanName=MappingWrite
@api.route('/api/startScan', methods=['GET'])
def startScan():
    basePath = request.args.get('basePath')
    solidityFile = request.args.get('solidityFile')
    scanName = request.args.get('scanName')
    scanId = 0
    dateTimePresent = None
    result = ''
    if solidityFile.endswith("*.sol"):
        for path in Path(basePath).iterdir():
            solidityFileName = str(path.name)
            scanId, result, dateTimePresent = mythModule.solidity_scan(basePath, path.name, scanName)
    else:
        scanId, result, dateTimePresent = mythModule.solidity_scan(basePath, solidityFile, scanName)

    scanResultDict = {}
    scanResultDict = dict({'scanId': scanId, 'result': result, 'dateTimePresent': mythModule.getPytzReplace(dateTimePresent)})
    response = str(scanResultDict).replace("'", '"')
    return response


#http://localhost:5000/api/smartContracts?scanId=1
@api.route('/api/smartContracts', methods=['GET'])
def get_smart_contract_list():
    scanId = request.args.get('scanId')
    contractResultDict = mythModule.getSmartContractsList(scanId)
    return mythModule.getJsonValues(contractResultDict)

@api.route('/api/viewScansListJson', methods=['GET'])
def get_view_scans_list_json():
    scanNamesList = mythModule.getScanList()
    totalScanNames = len(scanNamesList)
    scanInfoDict = {}
    for i in range(totalScanNames):
        status = ''
        countOfIssues = 0
        if scanNamesList[i][3] == "vulnPresent":
            countOfIssues = mythModule.getIssueCount(scanNamesList[i][0])
            status = mythModule.getStatusOfScan(scanNamesList[i][0])
        scanInfoDict[i] = dict(
            {'scanid': scanNamesList[i][0], 'scanname': scanNamesList[i][1], 'path': scanNamesList[i][2],
             'result': countOfIssues, 'status': status,'datepresent': mythModule.getPytzReplace(scanNamesList[i][4])})

    return mythModule.getJsonValues(scanInfoDict)

@api.route('/api/getIssuesListJson', methods=['GET'])
def getIssuesListJson():
    issuesList = {}
    scanId = request.args.get('scanId')
    if (scanId == None):
        issuesList = dict({'error': 'please enter the ScanId'})
    else:
        issueIdsList = mythModule.getIssueIdsList(scanId)
        totIssuesId = len(issueIdsList)
        for i in range(totIssuesId):
            label = 'issueId'
            issuesList[i] = dict({label: issueIdsList[i][0]})
    return mythModule.getJsonValues(issuesList)


@api.route('/api/getIssuesDetailListJson', methods=['GET'])
def getIssuesDetailListJson():
    issuesList = {}
    scanId = request.args.get('scanId')
    if (scanId == None):
        issuesList = dict({'error': 'please enter the ScanId'})
    else:
        issuesList = mythModule.getIssuesDetailList(scanId)
    return issuesList


@api.route('/api/viewIssueJson', methods=['GET'])
def get_view_issue_json():
    issueInfoDict = {}
    issueValue = request.args.get('issueId')
    # parsed and get the scan Name, contract name , swcId
    # pass and get the Issue info
    if (issueValue == None):
        issueInfoDict = dict({'error': 'Please pass the issueID'})
    else:
        issueInfoDict = mythModule.getIssueDetails(issueValue)
    dateValue = str(issueInfoDict['datepresent'])
    issueInfoDict["datepresent"] = dateValue
    response = str(issueInfoDict)
    response = response.replace("'", '"')
    return response


# curl -i -X GET "http://13.126.95.15:5000/api/deleteScan?scanName=%27Version4%27&date=%272021-11-12%2015:04:40.301417+05:30%27"
@api.route('/api/deleteScan', methods=['GET'])
def doDeleteScanJson():
    scanName = request.args.get('scanName')
    date = request.args.get('date')
    date = date[1:20] + "%"
    deleteScanDict = {}
    if ((scanName != None) and (date != None)):
        if (mythModule.deleteScanDetails(scanName, date) == 'Successfully Deleted'):
            deleteScanDict = dict({'result': 'Successfully Deleted'})
    else:
        deleteScanDict = dict({'error': 'please enter the scan name and date'})
    return deleteScanDict


# curl -i -X GET "http://13.126.95.15:5000/api/deleteScanWithId?scanId=5"
@api.route('/api/deleteScanWithId', methods=['GET'])
def doDeleteScanWithId():
    scanId = request.args.get('scanId')
    deleteScanDict = {}
    if (scanId != None):
        if (mythModule.deleteScanDetailsWithId(scanId) == 'Successfully Deleted'):
            deleteScanDict = dict({'result': 'Successfully Deleted'})
    else:
        deleteScanDict = dict({'error': 'please enter the scan name and date'})
    return deleteScanDict


# curl -i -X GET 'http://localhost:5000/api/editScanJson?scanName='ConstructorCreateArgumaent'&date="2021-11-18 18:55'
@api.route('/api/editScanJson', methods=['GET'])
def doEditScanJson():
    scanName = request.args.get('scanName')
    date = request.args.get('date')
    date = (str(date))[1:17]
    print (date)
    editScanDict = {}
    if ((scanName != None) and (date != None)):
        editScanDict = mythModule.editScanDetails(scanName, date)
    else:
        editScanDict = dict({'error': 'please enter the scan name and date'})
    return editScanDict


# curl -i -X GET "http://13.126.95.15:5000/api/updateScanJson?scanName=%27Version4%27&path=%27/home/delixus/solidity%27&result=%27vulnPresent%27&scanId=61"
@api.route('/api/updateScanJson', methods=['GET'])
def updateScanJson():
    scanName = request.args.get('scanName')
    path = request.args.get('path')
    result = request.args.get('result')
    scanId = request.args.get('scanId')
    updateScanDict = {}
    if ((scanName != None) and (scanId != None) and (path != None) and (result != None)):
        updateScanDict = mythModule.updateScanDetails(scanId, scanName, result)
    else:
        updateScanDict = dict({'error': 'please enter the scan name, scanId, path and result'})

    return (updateScanDict)


@api.route('/api/createScan', methods=['GET'])
def get_solidity_createScanHtml():
    createScanHtml = "<!DOCTYPE html><html><body><Title>Create Scan</Title><h1>Create SCAN</h1><button type=\"button\" onclick=\"AddScan()\">Add Scan!</button><button type=\"button\" onclick=\"doViewScanList()\">View the scans!</button><script>function AddScan() { location.replace(\"http://13.126.95.15:5000/api/addScan\")} function doViewScanList() { location.replace(\"http://13.126.95.15:5000/api/viewScansList\")}</script></body></html>"

    return createScanHtml


@api.route('/api/addScan', methods=['GET'])
def get_solidity_addScanHtml():
    addScanHtml = "<!DOCTYPE html><html><body><Title>Add Scan</Title><h1>Add SCAN</h1><table><tr><td>Name of the solidity file:</td><td><input type=\"text\" id=\"sldityFile\" value=\"\"></td></tr><br/><br/><tr><td>BasePath directory of file:</td><td><input type=\"text\" id=\"basePath\" ></td></tr><br/><br/><tr><td>ScanName of solidity  file:</td><td><input type=\"text\" id=\"scanName\"></td></tr></table><button type=\"button\" onclick=\"doScan()\">Add Scan!</button><button type=\"button\" onclick=\"doViewScanList()\">View the scans!</button><script>function doScan() { var solidityFile = document.getElementById('sldityFile').value; var basePath = document.getElementById('basePath').value; var scanName = document.getElementById('scanName').value; var url = \"http://13.126.95.15:5000/api/createReport?solidityFile=\"+solidityFile+\"&basePath=\"+basePath+\"&scanName=\"+scanName;location.replace(url);} function doViewScanList() { location.replace(\"http://13.126.95.15:5000/api/viewScansList\")} </script></body></html>"

    return addScanHtml


def get_solidity_viewScannedReport(scanId, scanName=None, result=None, dateTimePresent=None):
    # Add the scan Details
    viewScanHtml = "<!DOCTYPE html><html><body><Title>Scan Result</Title><h1>Scan Result</h1><table><tr><td>Scan Name :</td><td>"
    viewScanHtml = viewScanHtml + scanName + "</td></tr>"
    viewScanHtml = viewScanHtml + "<tr><td>Result :</td><td>" + result + "</td></tr>"
    # here the scan Name, contract Name, swcId
    if (result == 'vulnPresent'):
        swcIdsList = None
        issueIdsList = None

        issueIdsList, swcIdsList = mythModule.getSwcIdsList(scanId)
        totalSwcIds = len(swcIdsList)
        viewScanHtml = viewScanHtml + "<tr><td>Select SWC IDS : </td><td><select name=\"SWC Ids\" id=\"Swcid\" onchange=\"doViewIssue()\">"
        for i in range(totalSwcIds):
            viewScanHtml = viewScanHtml + "<option value=\"" + str(issueIdsList[i][0]) + " " + swcIdsList[i][
                0] + "\">" + swcIdsList[i][0] + "</option>"

    viewScanHtml = viewScanHtml + "</select></td><tr>"
    viewScanHtml = viewScanHtml + "</table>"
    viewScanHtml = viewScanHtml + "<br><br>"
    viewScanHtml = viewScanHtml + "<button type=\"button\" onclick=\"doViewIssue()\">view Issue</button>"
    viewScanHtml = viewScanHtml + "<button type=\"button\" onclick=\"doViewScanList()\">view ScanList</button>"
    viewScanHtml = viewScanHtml + "<button type=\"button\" onclick=\"doAddScan()\">Do AnotherScan</button><script>"
    viewScanHtml = viewScanHtml + "function doViewIssue() { var swcIds = document.getElementById(\"Swcid\"); "
    viewScanHtml = viewScanHtml + "issueValue = swcIds.options[swcIds.selectedIndex].value; issueValue = issueValue.substring(0,issueValue.indexOf(\" \"));"
    viewScanHtml = viewScanHtml + "var url = \"http://13.126.95.15:5000/api/viewIssueReport?issueId=\"+issueValue;location.replace(url); } function doAddScan() { location.replace(\"http://13.126.95.15:5000/api/addScan\")}  function doViewScanList() { location.replace(\"http://13.126.95.15:5000/api/viewScansList\")}</script>"
    viewScanHtml = viewScanHtml + "</body></html>"

    return viewScanHtml


@api.route('/api/selectAnotherIssue', methods=['GET'])
def get_solidity_another_issue():
    scanId = request.args.get('scanId')
    scanRecord = mythModule.getScanDetails(scanId)
    scanName = scanRecord[0][1]
    result = scanRecord[0][3]
    dateTimePresent = scanRecord[0][4]
    return get_solidity_viewScannedReport(scanId, scanName, result, dateTimePresent)


@api.route('/api/editScan', methods=['GET'])
def doEditScan():
    editScanHtml = "<!DOCTYPE html><html><body><Title>Edit Scan</Title><h1>Edit SCAN</h1><table><tr><td>Name of the scan:</td><td><input type=\"text\" id=\"scanName\" value=\"\"></td></tr><br/><br/><tr><td>DatePresent:</td><td><input type=\"text\" id=\"datePresent\" ></td></tr><br/><br/></table><button type=\"button\" onclick=\"doEditScan()\">Edit Scan!</button><script>function doEditScan() { var scanName = document.getElementById('scanName').value; var basePath = document.getElementById('datePresent').value; var datePresent = document.getElementById('datePresent').value; var url = \"http://13.126.95.15:5000/api/editScan?scanName=\"+scanName+\"&datePresent=\"+datePresent+\";location.replace(url);} </script></body></html>"

    return editScanHtml

@api.route('/api/viewIssueReport', methods=['GET'])
def get_view_issue_report():
    issueValue = request.args.get('issueId')
    # parsed and get the scan Name, contract name , swcId
    # pass and get the Issue info
    issueInfoDict = mythModule.getIssueDetails(issueValue)
    viewIssueHtml = "<!DOCTYPE html><html><body><Title>Issue Details</Title><h1>Issue Details</h1><table><tr><td>SWC ID :</td><td>" + \
                    issueInfoDict["swcId"] + "</td></tr>"
    viewIssueHtml = "<tr><td>SWC ID :</td><td>" + issueInfoDict['swcId'] + "</td></tr>"
    viewIssueHtml = viewIssueHtml + "<br><br>"
    viewIssueHtml = viewIssueHtml + "<tr><td>ContractName :</td><td>" + issueInfoDict[
        'contractName'] + "</td></tr>" + "<br><br>"
    viewIssueHtml = viewIssueHtml + "<tr><td>Description Head :</td><td>" + issueInfoDict[
        'description_head'] + "</td></tr>" + "<br><br>"
    viewIssueHtml = viewIssueHtml + "<tr><td>Description Tail :</td><td>" + issueInfoDict[
        'description_tail'] + "</td></tr>" + "<br><br>"
    viewIssueHtml = viewIssueHtml + "<tr><td>SWC Title :</td><td>" + issueInfoDict[
        'swctitle'] + "</td></tr>" + "<br><br>"
    viewIssueHtml = viewIssueHtml + "<tr><td>LineNumber :</td><td>" + str(
        issueInfoDict['linenum']) + "</td></tr>" + "<br><br>"
    viewIssueHtml = viewIssueHtml + "<tr><td>FileName :</td><td>" + issueInfoDict[
        'filename'] + "</td></tr>" + "<br><br>"
    viewIssueHtml = viewIssueHtml + "<tr><td>Date Present :</td><td>" + str(
        issueInfoDict['datepresent']) + "</td></tr>" + "<br><br>"
    viewIssueHtml = viewIssueHtml + "<tr><td><button type=\"button\" onclick=\"doScanList()\">Scan list </button></td>"
    viewIssueHtml = viewIssueHtml + "<td><button type=\"button\" onclick=\"doSelectAnotherIssueFromScan(" + str(
        issueInfoDict['scanId']) + ") \">Another issue </button></td>"
    viewIssueHtml = viewIssueHtml + "<td><button type=\"button\" onclick=\"doAddScan()\">New Scan</button></td></tr>" + "<br><br>" + "</table>"
    viewIssueHtml = viewIssueHtml + "<script>function doScanList()"
    viewIssueHtml = viewIssueHtml + "{ var url = \"http://13.126.95.15:5000/api/viewScansList\";location.replace(url); } "
    viewIssueHtml = viewIssueHtml + "function doSelectAnotherIssueFromScan(scanId) { var url = \"http://13.126.95.15:5000/api/selectAnotherIssue?scanId=\"+scanId;location.replace(url); }"
    viewIssueHtml = viewIssueHtml + "function doAddScan() { var url = \"http://13.126.95.15:5000/api/addScan\";location.replace(url);} </script></body></html>"
    return viewIssueHtml


@api.route('/api/viewScansList', methods=['GET'])
def get_view_scans_list():
    viewScanHtml = "<!DOCTYPE html><html><body><Title>Available Scans with Dates</Title><h1>Available Scans with Dates</h1><table>"

    viewScanHtml = viewScanHtml + "<tr><td>Select ScanName : </td><td><select name=\"scanName\" id=\"scanName\" onchange=\"doCheckDatePresent()\">"
    scanNamesList = mythModule.getScanList()
    totalScanNames = len(scanNamesList)
    for i in range(totalScanNames):
        viewScanHtml = viewScanHtml + "<option value=" + str(scanNamesList[i][0]) + ">" + scanNamesList[i][
            1] + "</option>"
    viewScanHtml = viewScanHtml + "</select></td></tr></table>"

    viewScanHtml = viewScanHtml + "<br><br>"

    viewScanHtml = viewScanHtml + "<table><tr><td>DateTime of Scan: </td><td><select name=\"dateTime\" id=\"dateTime\">"
    for i in range(totalScanNames):
        viewScanHtml = viewScanHtml + "<option value=" + str(scanNamesList[i][0]) + ">" + str(
            scanNamesList[i][4]) + "</option>"
    viewScanHtml = viewScanHtml + "</select></td></tr></table><br><br>"
    viewScanHtml = viewScanHtml + "<table><tr><td><button type=\"button\" onclick=\"doAddScan()\">Add Scan</button></td>" + "<td><button type=\"button\" onclick=\"doViewScan()\">View Scan</button></td></tr>" + "<br><br>" + "</table>"
    viewScanHtml = viewScanHtml + "<script>function doViewScan()"
    viewScanHtml = viewScanHtml + "{ var url = \"http://13.126.95.15:5000/api/viewIssues?scanId=\"+document.getElementById(\"scanName\").value; location.replace(url); } "
    viewScanHtml = viewScanHtml + "function doAddScan() { var url = \"http://13.126.95.15:5000/api/addScan\";location.replace(url);}"
    viewScanHtml = viewScanHtml + "function doCheckDatePresent(){ scanName = document.getElementById(\"scanName\").value; document.getElementById(\"dateTime\").value = scanName;} </script></body></html>"
    return viewScanHtml


@api.route('/api/viewIssues', methods=['GET'])
def get_the_issues():
    scanId = request.args.get('scanId')
    scanRecord = mythModule.getScanDetails(scanId)
    scanName = scanRecord[0][1]
    result = scanRecord[0][3]
    dateTimePresent = scanRecord[0][4]
    issuesHtml = get_solidity_viewScannedReport(scanId, scanName, result, dateTimePresent)

    return issuesHtml


@api.route('/api/createReport', methods=['GET'])
def get_create_report():
    basePath = request.args.get('basePath')
    solidityFile = request.args.get('solidityFile')
    scanName = request.args.get('scanName')
    scanId = 0
    dateTimePresent = None
    result = ''
    if solidityFile.endswith("*.sol"):
        for path in Path(basePath).iterdir():
            solidityFileName = str(path.name)
            scanId, result, dateTimePresent = mythModule.solidity_scan(basePath, path.name, scanName)
    else:
        scanId, result, dateTimePresent = mythModule.solidity_scan(basePath, solidityFile, scanName)

    viewScanHtml = get_solidity_viewScannedReport(scanId, scanName, result, dateTimePresent)
    return viewScanHtml


if __name__ == '__main__':
    api.run(host='0.0.0.0', debug=True)
