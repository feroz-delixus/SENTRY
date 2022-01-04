from datetime import datetime
from flask import current_app
import solidityAnalyzeReport
import solidityrestcall

reporter = solidityAnalyzeReport.SolidityAnalyzeReporter()
restcall = solidityrestcall
solidityrestcall.api.testing = True
client = solidityrestcall.api.test_client()

def test_getPytzReplace():
    statement = 'select datepresent from solidityscans' + ';'
    reporter.get_db_execute(statement)
    data = reporter.cursor.fetchall()
    datepresent = data[0][0]
    reporter.get_db_connection_close()
    datenormal = solidityrestcall.getPytzReplace(datepresent)
    # initializing format
    datenormal = str(datenormal)[0:19]
    format = "%Y-%m-%d %H:%M"
    # checking if format matches the date
    res = False
    # using try-except to check for truth value
    try:
        result = bool(datetime.strptime(datenormal, format))
        if result:
            print('date format is in normal format expected')
    except ValueError:
        raise Exception('getPytzReplace format is not coming right ')


def test_getJsonValues():
    jsonData = restcall.getNumberOfVuln()
    jsonResponse = restcall.getJsonValues(jsonData)
    if type(jsonResponse == '<class \'int\'>'):
        print('json data is integer')
    else:
        raise Exception('getJsonValues is not getting value as integer')

def test_getNumberOfScans():
    jsonData = restcall.getNumberOfScans()
    numScans = jsonData['numberOfScans']
    if numScans >= 0:
        print('number of scans ' + str(numScans))
    else:
        raise Exception('Number of Scans is not getting value as integer')


def test_getNumberOfSmartContracts():

    jsonData = restcall.getNumberOfSmartContracts()
    numSmartContracts = jsonData['numberOfSmartContracts']
    if numSmartContracts >= 0:
        print('number of smart scans ' + str(numSmartContracts))
    else:
        raise Exception('Number of SmartScans is not getting value as integer')


def test_getNumberOfVuln():

    jsonData = restcall.getNumberOfVuln()
    numOfVuln = jsonData['numberOfVuln']
    if numOfVuln >= 0:
        print('number of vulnerabilities ' + str(numOfVuln))
    else:
        raise Exception('Number of Vulnerabilities is not getting value as integer')


def test_getNumberOfIssues():

    statement = 'select MAX(scanId) from issues;'
    reporter.get_db_execute(statement)
    data = reporter.cursor.fetchone()
    reporter.get_db_connection_close()
    url = '/api/numberOfIssues?scanId=' + str(data[0])
    jsonData = client.get(url)

    numOfIssues = jsonData.json['numberOfIssues']
    if numOfIssues >= 0:
        print('number of issues ' + str(numOfIssues))
    else:
        raise Exception('Number of Issues is not getting value as integer')


def test_startScan():

    solidityFile = 'odd_even.sol'
    basePath = '/home/ubuntu/mythril-scan/solidityFiles/sol0.5.6'
    scanName = 'OddEvenScan'

    url = '/api/startScan?basePath=' + basePath + '&solidityFile=' + solidityFile + '&scanName=' + scanName
    jsonData = client.get(url)
    print(jsonData.data)
    if jsonData is not None:
        print(jsonData.data)
    else:
       raise Exception('get_the_issue is not working')


def test_get_smart_contract_list():
    flask_app = current_app
    statement = 'select MAX(scanId) from issues;'
    reporter.get_db_execute(statement)
    data = reporter.cursor.fetchone()
    reporter.get_db_connection_close()
    jsonData = client.get('/api/smartContracts' + '?' + 'scanId=' + str(data[0]))
    if jsonData is not None:
        print(jsonData.data)
    else:
        raise Exception('Not getting smart contracts List ')


def test_get_view_scans_list_json():

    flask_app = current_app
    jsonData = client.get('/api/viewScansListJson')
    if jsonData is not None:
        print(jsonData.data)
    else:
        raise Exception('Not getting the scans List')


def test_getIssuesListJson():

    statement = 'select MAX(scanId) from issues;'
    reporter.get_db_execute(statement)
    data = reporter.cursor.fetchone()
    reporter.get_db_connection_close()
    url = '/api/getIssuesListJson' + '?scanId=' + str(data[0])
    jsonData = client.get(url)
    if jsonData is not None:
        print(jsonData.data)
    else:
        raise Exception('Not getting the Issues List')


def test_getIssuesDetailListJson():

    statement = 'select MAX(scanId) from issues;'
    reporter.get_db_execute(statement)
    data = reporter.cursor.fetchone()
    reporter.get_db_connection_close()
    jsonData = client.get('/api/getIssuesDetailListJson' + '?scanId=' + str(data[0]))
    if jsonData is not None:
        print(jsonData.data)
    else:
        raise Exception('Not getting the Issues Details List')

def test_get_view_issue_json():

    statement = 'select MAX(issueId) from issues;'
    reporter.get_db_execute(statement)
    data = reporter.cursor.fetchone()
    reporter.get_db_connection_close()
    jsonData = client.get('/api/viewIssueJson' + '?issueId=' + str(data[0]))
    if jsonData is not None:
        print(jsonData.data)
    else:
        raise Exception('Not getting the Issues Details List')

def test_doDeleteScanJson():

    statement = 'select MAX(scanId) from issues;'
    reporter.get_db_execute(statement)
    data = reporter.cursor.fetchone()
    reporter.get_db_connection_close()
    statement = 'select scanName, datepresent from solidityscans where scanId = ' + str(data[0])
    reporter.get_db_execute(statement)
    data = reporter.cursor.fetchall()
    reporter.get_db_connection_close()
    url = '/api/deleteScan' + '?scanName=' + data[0][0] + '&date=' + str(data[0][1])
    jsonData = client.get(url)
    if jsonData is not None:
       print(jsonData)
       if jsonData.json['result'] =='Successfully Deleted':
          print('Delete scan is success')
       else:
          raise Exception('Delete scan is not success')

def test_doDeleteScanWithId():
    statement = 'select MAX(scanId) from issues;'
    reporter.get_db_execute(statement)
    data = reporter.cursor.fetchone()
    reporter.get_db_connection_close()
    url = '/api/deleteScanWithId' + '?scanId=' + str(data[0])
    jsonData = client.get(url)
    if jsonData is not None:
        if jsonData.json['result'] =='Successfully Deleted':
           print('Delete scan is success')
        else:
           raise Exception('Delete scan is not success')

def test_doEditScanJson():

    statement = 'select MAX(scanId) from issues;'
    reporter.get_db_execute(statement)
    data = reporter.cursor.fetchone()
    reporter.get_db_connection_close()
    statement = 'select scanName, datepresent from solidityscans where scanId = ' + str(data[0])
    reporter.get_db_execute(statement)
    data = reporter.cursor.fetchone()
    reporter.get_db_connection_close()
    jsonData = client.get('/api/editScanJson' + '?scanName=' + data[0][0] + '&datepresent=' + data[0][1])
    if jsonData is not None:
       print('Edit json scan is success')
       print(jsonData.data)
    else:
       raise Exception('Edit json scan is not success')


def test_updateScanJson():

    statement = 'select * from solidityscans where result = \'' + 'vulnPresent' + '\';'
    print(statement)
    reporter.get_db_execute(statement)
    data = reporter.cursor.fetchall()
    reporter.get_db_connection_close()
    scanId = data[0][0]
    scanName = data[0][1]
    path = data[0][2]
    result = data[0][3]

    url = '/api/updateScanJson' + '?scanName=\'' + scanName + '\'&path=\'' + path + '\'&result=\'' + result + '\'&scanId='+ str(scanId)
    print(url)
    jsonData = client.get(url)
    if jsonData is not None:
       print('updateScanJson scan is success')
       print(jsonData.data)
    else:
       raise Exception('Update json scan is not success')


def test_get_solidity_createScanHtml():

    create_html = client.get('/api/createScan')
    if create_html is not None:
        print(create_html.data)
    else:
        raise Exception('createHtml text data is not working')

def test_get_solidity_addScanHtml():

    flask_app = current_app
    add_html = client.get('/api/addScan')
    if add_html is not None:
        print(add_html.data)
    else:
        raise Exception('addHtml text data is not working')

def test_get_solidity_another_issue():

    statement = 'select MAX(scanId) from issues;'
    reporter.get_db_execute(statement)
    data = reporter.cursor.fetchone()
    reporter.get_db_connection_close()

    anotherissue_html = client.get('/api/selectAnotherIssue?scanId='+str(data[0]))
    if anotherissue_html is not None:
        print(anotherissue_html)
    else:
       raise Exception('anotherissue_html data is not working')


def test_doEditScan():

    editscan = client.get('/api/editScan')
    if editscan is not None:
        print(editscan)
    else:
        raise Exception('editscan html is not working')

def test_get_view_issue_report():

    statement = 'select MAX(scanId) from issues;'
    reporter.get_db_execute(statement)
    data = reporter.cursor.fetchone()
    reporter.get_db_connection_close()
    issuereport = client.get('/api/viewIssueReport?issueId=' + str(data[0]))
    if issuereport is not None:
        print(issuereport)
    else:
        raise Exception('editscan html is not working')


def test_get_view_scans_list():

    scanlist = client.get('/api/viewScansList')
    if scanlist is not None:
        print(scanlist.data)
    else:
        raise Exception('scanlist html is not working')

def test_get_the_issues():

    statement = 'select MAX(scanId) from issues;'
    reporter.get_db_execute(statement)
    data = reporter.cursor.fetchone()
    reporter.get_db_connection_close()

    issuereport = client.get('/api/viewIssues?scanId=' + str(data[0]))
    if issuereport is not None:
        print(issuereport.data)
    else:
        raise Exception('get_the_issue is not working')


def test_get_create_report():

    solidityFile = 'odd_even.sol'
    basePath = '/home/ubuntu/mythril-scan/solidityFiles/sol0.5.6'
    scanName = 'OddEvenScan'
    issuereport = client.get('/api/createReport?basePath=\''+basePath+'\'&solidityFile=\''+solidityFile+'\'&scanName=\''+scanName + '\'')
    if issuereport is not None:
        print(issuereport.data)
    else:
       raise Exception('get_the_issue is not working')
