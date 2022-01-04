# TODO -

Database
---

- [x] - Create *.sql files to create.
  - [x] - Database.
  - [x] - Role.
  - [x] - Drop database.
  - [x] - Assign permissions.
- [x] - Create the shell scripts to UPDATE/ALTER the database.
- [x] - Change the DB_USER_NAME to DB_USERNAME in .env and solidityAnalyzeReport.py.


Application
---

- [] - Integrate the UI into mythril app.
- [] - Convert flask app to run in PROD, earlier it was created as a servie for python script. So, now it needs to be done with different approach as the app is running as `flask run`.
- [] - Create .env-production file and appropriate values.
- [] - Configure Nginx.
- [] - Add Flask environemts to .evn file.
- 
Jenkins
---
**Setup role based Authorization strategy.**
  - [x] - install pulgin and restart the Jenkins.
  - [x] - Create two groups, backend and frontend.
  - [x] - Creat two uesrs ms.valliammal@delixus.com  and garima@delixus.com
  - [x] - Add users to the group.
  - [x] - Assign read access to groups.
  - [x] - Test read access.
  - [x] - Send the credentials to users.
  - [x] - Make sure the date is changed in the Jenkins job.
  - [] Configure nginx.

**OS**
- [x] - Change the date in OS and active nptd client. 

**Deploy connector-service-api**
- [x] - Deploy connector-service-api on EC2.
- [x] - Configure Nginx.
- 