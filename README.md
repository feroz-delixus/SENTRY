# mythril-scan - Test webhook.

1. First run the requirements.txt

pip install -r requirements.txt

2. Then Setup the postgresql schema
(The schema is added with the repository)
Run solidity.sql in postgres

3. Run the solidityrestcall.py by 
python solidityrestcall.py

4. The following are the URLS which will be used for the solidityscan

http://localhost:5000/api                  : This is for getting the root api of mythril scan

http://localhost:5000/api/numberOfScans    : This is for getting total number of scans

http://localhost:5000/api/numberOfSmartContracts : This is for getting the number of smart contracts

http://localhost:5000/api/numberOfVulnerabilities : This is to get the number of vulnerabilities

http://localhost:5000/api/startScan        : This is to start the scan
By adding the solidityFile, basePath, and scanName, you get the startscan and get the scan report

http://localhost:5000/api/startScan?solidityFile=mapping_write.sol&basePath=/home/delixus/solidity/sol0.4.25&scanName=MappingWrite

http://localhost:5000/api/smartContracts?scanId=1 : This is to get the Number of Smart contracts


http://localhost:5000/api/viewScansListJson : This is to get the view Scans list

http://localhost:5000/api/getIssuesListJson?scanId=61 : This is to get the issues List, This will give the issue IDs of the List of JSON

http://localhost:5000/api/getIssuesDetailListJson?scanId=61 : This is to get the detailed Issues 

http://localhost:5000/api/viewIssueJson?issueId=55 : This is to get the one issue detail 

http://localhost:5000/api/deleteScan : This is to get the delete scan , 

curl -i -X GET "http://192.168.29.231:5000/api/deleteScan?scanName="Version4"&date="2021-11-12 15:04%"

http://localhost:5000/api/deleteScanWithId?scanId=61 : This is to delete the specific scan

http://localhost:5000/api/editScanJson               : This is to edit the scans JSON result
curl -i -X GET http://localhost:5000/api/editScanJson?scanName=solidityscanreport&date=%272021-11-12%2015:05%27


http://localhost:5000//api/updateScanJson            : This is to get the updated scan Json result 
curl -i -X GET "http://192.168.29.231:5000/api/updateScanJson?scanName="Version4"&path="/home/delixus/solidity"&result="vulnPresent"&scanId=61"


http://localhost:5000/api/createScan       : For the creating of the scan


http://localhost:5000/api/addScan          : For the adding the scan, use this for entering the basepath , solidityFile, date

http://localhost:5000/api/createReport     : For the Scan, report is created, basePath, solidityfile, date are the inputs for this

http://localhost:5000/api/selectAnotherIssue?scanId=5 : To select another issue from the list of issues for the specific scanId

http://localhost:5000/api/editScan    : To edit any scan from the scans List

http://localhost:5000/api/viewIssueReport?issueId=61 : Get the issues Report for the specific issue Id

http://localhost:5000/api/viewScansList : Give the total list of scans

http://localhost:5000/api/viewIssues?scanId=1 : Give the total list of scans

use solc-select to select different versions of the solidity files.




