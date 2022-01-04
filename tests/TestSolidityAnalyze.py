import solidityrestcall
from solidityAnalyzeReport import SolidityAnalyzeReporter
reporter = SolidityAnalyzeReporter()


def test_get_db_connection():
    reporter.get_db_connection()
    if reporter.connection is not None:
        print('connection is success')
        reporter.get_db_connection_close()
    else:
        raise Exception('connection error')

def test_get_db_connection_close():
    reporter.get_db_connection()
    reporter.get_db_connection_close()
    if reporter.connection:
        print('connection is successfully closed')
    else:
        raise Exception('cursor is not closed')

def test_get_db_execute():

    statement = 'select count(*) from solidityscans;'
    reporter.get_db_execute(statement)
    data = reporter.cursor.fetchone()
    reporter.get_db_connection_close()
    if data[0] is not None:
        print('db executed')
    else:
        raise Exception('DB execution is not success')

def test_getIssueCount():
    statement = 'select MAX(scanid) from issues;'
    reporter.get_db_execute(statement)
    data = reporter.cursor.fetchone()
    reporter.get_db_connection_close()
    scanId = data[0]
    print(scanId)
    issueCount = reporter.getIssueCount(str(scanId))
    if issueCount > 0:
        print('ok issue count is success')
        print(issueCount)
    else:
        raise Exception('getIssueCount() is not giving response ')

def test_getIssueDetails():

    statement = 'select MAX(issueid) from issues;'
    reporter.get_db_execute(statement)
    data = reporter.cursor.fetchone()
    issue_data = reporter.getIssueDetails(str(data[0]))
    reporter.get_db_connection_close()
    if issue_data is not None:
        print('issue Data is success')
        print(issue_data)
    else:
        raise Exception('getIssueDetails() is not giving response ')

def test_editScanDetails():

    statement = 'select MAX(scanId) from solidityscans;'
    reporter.get_db_execute(statement)
    data = reporter.cursor.fetchone()
    reporter.get_db_connection_close()
    statement = 'select scanname,datepresent from solidityscans where scanid = ' + str(data[0]) + ';'
    reporter.get_db_execute(statement)
    data = reporter.cursor.fetchall()
    reporter.get_db_connection_close()
    datePresent = solidityrestcall.getPytzReplace(data[0][1])[0:16]
    scan_data = reporter.editScanDetails(data[0][0], datePresent)
    if scan_data is not None:
        print('issue Data is success')
        print(scan_data)
    else:
        raise Exception('getIssueDetails() is not giving response ')

def test_updateScanDetails():

    statement = 'select MAX(scanId) from solidityscans;'
    reporter.get_db_execute(statement)
    data = reporter.cursor.fetchone()
    reporter.get_db_connection_close()
    statement = 'select * from solidityscans where scanid = ' + str(data[0]) + ';'
    reporter.get_db_execute(statement)
    data = reporter.cursor.fetchall()
    scanid = data[0][0]
    scanname = data[0][1]
    result = data[0][3]
    reporter.get_db_connection_close()
    scanname_update = scanname + '_update'
    result_update = result + '_update'
    reporter.updateScanDetails(scanid, scanname_update,result_update)
    statement = 'select * from solidityscans where scanid = ' + str(scanid) + ';'
    reporter.get_db_execute(statement)
    data = reporter.cursor.fetchall()
    reporter.get_db_connection_close()
    scanname_up = data[0][1]
    result_up = data[0][3]

    if (scanname_up.find('update') != -1) and (result_up.find('update') != -1):
        print('updation success')
        reporter.updateScanDetails(scanid, scanname, result)
    else:
        raise Exception('updateScanDetails is not giving response ')

def test_deleteScanDetailsWithId():

    statement = "select * from solidityscans where result = '" + 'vulnNotPresent' + "';"
    reporter.get_db_execute(statement)
    data = reporter.cursor.fetchall()
    reporter.get_db_connection_close()
    scanid = data[0][0]
    scanname = data[0][1]
    path = data[0][2]
    result = data[0][3]
    statement = "select count(*) from solidityscans where result = '" + "vulnNotPresent" + "';"
    reporter.get_db_execute(statement)
    data = reporter.cursor.fetchone()
    numberOfRecords = data[0]
    reporter.get_db_connection_close()
    reporter.deleteScanDetailsWithId(str(scanid))
    statement = "select count(*) from solidityscans where result = '" + 'vulnNotPresent' + "';"
    reporter.get_db_execute(statement)
    data = reporter.cursor.fetchone()
    numberOfRecords_after_delete = data[0]
    reporter.get_db_connection_close()
    if (numberOfRecords - 1) == numberOfRecords_after_delete:
        print(' ok Deletion success')
        statement = "INSERT INTO solidityscans (scanname, path, result) values ('" + scanname + "','" + path + "','" + result + "');"
        reporter.get_db_execute(statement)
        reporter.connection.commit()
        reporter.get_db_connection_close()
        statement = "select count(*) from solidityscans where result = '" + "vulnNotPresent" + "';"
        reporter.get_db_execute(statement)
        data = reporter.cursor.fetchone()
        reporter.get_db_connection_close()
        if numberOfRecords == data[0]:
            print('Record inserted back')
            print('insertion success')
    else:
        print('Deletion problem')
        raise Exception('Deletion is not giving response and problem')

def test_deleteScanDetails():

    reporter.get_db_connection()
    statement = 'select * from solidityscans where result = \'' + 'vulnNotPresent' + '\';'
    reporter.get_db_execute(statement)
    data = reporter.cursor.fetchall()
    scanname = data[0][1]
    path = data[0][2]
    result = data[0][3]
    date = data[0][4]
    reporter.get_db_connection_close()
    statement = 'select count(*) from solidityscans where result = \'' + 'vulnNotPresent' + '\';'
    reporter.get_db_execute(statement)
    data = reporter.cursor.fetchone()
    numberOfRecords = data[0]
    reporter.get_db_connection_close()
    reporter.deleteScanDetails(scanname,solidityrestcall.getPytzReplace(date))
    statement = 'select count(*) from solidityscans where result = \'' + 'vulnNotPresent' + '\';'
    reporter.get_db_execute(statement)
    data = reporter.cursor.fetchone()
    numberOfRecords_after_delete = data[0]
    reporter.get_db_connection_close()
    if (numberOfRecords - 1) == numberOfRecords_after_delete:
        print(' ok Deletion success')
        statement = "INSERT INTO solidityscans (scanname, path, result) values (\'" + scanname + "\',\'" + path + "\',\'" + result + "\');"
        reporter.get_db_execute(statement)
        reporter.get_db_connection_close()
        statement = 'select count(*) from solidityscans where result = \'' + 'vulnNotPresent' + '\';'
        reporter.get_db_execute(statement)
        data = reporter.cursor.fetchone()
        reporter.get_db_connection_close()
        if numberOfRecords == data[0]:
            print('Record inserted back')
            print('insertion success')
    else:
        print('Deletion problem')
        raise Exception('Deletion is not giving response and problem')

def test_getScanList():

    data = reporter.getScanList()
    if len(data) > 0:
        print('Scanned List is success')
    else:
        raise Exception('getscanlist is error')


def test_getScanDetails():

    statement = 'select * from solidityscans where result = \'' + 'vulnPresent' + '\';'
    reporter.get_db_execute(statement)
    data = reporter.cursor.fetchall()
    reporter.get_db_connection_close()
    scanid = data[0][0]
    scanname = data[0][1]
    path = data[0][2]
    result = data[0][3]
    date = data[0][4]
    currentData = reporter.getScanDetails(str(scanid))
    if (scanname == currentData[0][1]) and (result == currentData[0][3]) and (date == currentData[0][4]):
        print('Scanned List is success')
    else:
        raise Exception('getscanlist is error')

def test_getNumberOfScans():

    if reporter.getNumberOfScans() > 0:
       print('Number of scans works')
    else:
       raise Exception('getNumberOfScans is error')

def test_getNumberOfSmartContracts():

    if reporter.getNumberOfSmartContracts() > 0:
       print('Number of scans works')
    else:
       raise Exception('getNumberOfScans is error')

def test_getNumberOfVulnerabilities():
    if reporter.getNumberOfVulnerabilities() > 0:
       print('Number of Vulnerabilities works')
    else:
       raise Exception('getNumberOfVulnerabilities is error')


def test_getSmartContractsList():

    statement = 'select scanid from issues' + ';'
    reporter.get_db_execute(statement)
    data = reporter.cursor.fetchall()
    reporter.get_db_connection_close()
    scanId = data[0][0]

    if len(reporter.getSmartContractsList(str(scanId))) > 0:
       print('Number of Smart Contracts works')
    else:
       raise Exception('getNumberOfSmartContracts is error')

def test_getIssueIdsList():

    statement = 'select scanid from issues' + ';'
    reporter.get_db_execute(statement)
    data = reporter.cursor.fetchall()
    reporter.get_db_connection_close()
    scanid = data[0][0]
    if len(reporter.getIssueIdsList(str(scanid))) > 0:
        print(' issue Ids list is working')
    else:
        raise Exception('getIssueIdsList is error')

def test_getIssuesDetailList():

    statement = 'select scanid from issues' + ';'
    reporter.get_db_execute(statement)
    data = reporter.cursor.fetchall()
    reporter.get_db_connection_close()
    scanid = data[0][0]
    if len(reporter.getIssueIdsList(str(scanid))) > 0:
        print(' issue Ids list is working')
    else:
        raise Exception('getIssueIdsList is error')


def test_getSwcIdsList():

    statement = 'select scanid from issues' + ';'
    reporter.get_db_execute(statement)
    data = reporter.cursor.fetchall()
    scanid = data[0][0]
    reporter.get_db_connection_close()
    if len(reporter.getSwcIdsList(str(scanid))) > 0:
        print('SwcIds list is working')
    else:
        raise Exception('getSwcIdsList is error')

def test_getCompilerVersion():

    reporter.get_db_connection()
    statement = 'select path from solidityscans where result = \'' + 'vulnPresent' + '\';'
    reporter.get_db_execute(statement)
    data = reporter.cursor.fetchall()
    reporter.get_db_connection_close()
    path = data[0][0]
    compilerVersion = reporter.getCompilerVersion(path)
    if compilerVersion is not None:
       print('compiler version comes success')
    else:
       raise Exception('Compiler version is not coming')

