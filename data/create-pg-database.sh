#!/bin/bash

# Delixus Database Installation Script
# ====================================
# PostgreSQL 10 on Linux/Mac

# Setup Instructions
# ------------------
#
# Open a terminal, then run the following commands:
#
# vi ~/.pgpass
#
# Add the following 2 lines to .pgpass (Without the first # on each line)
#    #hostname:port:database:username:password
#    localhost:5432:solidityscan:ss:pass.word
#
# Save and close .pgpass
#
# chmod 600 ~/.pgpass
#
# Close and re-open the terminal
#
#
# ./create-pg-database.sh
#


# Variables
# ------------------------------------------------------------------------------
server=localhost
database=solidityscan
port=5432
username=ss

OS=`uname -s`
SUDO=`which sudo`
PSQL=`which psql`
ADMIN_DB="postgres"
ADMIN_ROLE="postgres"

if [ "$OS" == "Darwin" ] ; then
    ADMIN_DB="template1"
    ADMIN_ROLE=`whoami`
fi

# Create the ss user role (use sudo)
# ------------------------------------------------------------------------------
echo "=== Creating roles (users) ==="
$SUDO -u $ADMIN_ROLE $PSQL -d $ADMIN_DB < ./pg/create-roles.sql

# Drop and Create the DB as postgres (use sudo)
# ------------------------------------------------------------------------------
echo "=== Dropping old DB (if exists) ==="
$SUDO -u $ADMIN_ROLE $PSQL -d $ADMIN_DB < ./pg/drop-database.sql
echo "=== Creating new DB ==="
$SUDO -u $ADMIN_ROLE $PSQL -d $ADMIN_DB < ./pg/create-database.sql

# Create the tables
# ------------------------------------------------------------------------------
echo "=== Creating tables ==="
echo ":: Authentication and Authorization"
echo "- account"
$SUDO -u $ADMIN_ROLE $PSQL -d $database < ./pg/0.0.1/tables/account.sql


# Grant role permissions
# ------------------------------------------------------------------------------
echo "=== Granting role permissions ==="
$SUDO -u $ADMIN_ROLE $PSQL -d $database < ./pg/grant-role-permissions.sql

# Default data
# ------------------------------------------------------------------------------


