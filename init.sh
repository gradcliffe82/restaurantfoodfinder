#!/bin/bash
export PGPASSWORD="2010@Wesley2010"
DB_USER=postgres
DB_NAME=andromeda
SQL_RAW_TBL_EXISTS=sql/check_raw_tbl_exists.sql
SQL_RAW_TBL_RECORDS=sql/check_raw_tbl_records.sql
SQL_APP_TBL_EXISTS=sql/check_app_tbl_exists.sql
SQL_APP_TBL_RECORDS=sql/check_app_tbl_records.sql

# SQL FILE LOCATIONS
RAW_TABLE_EXISTS=$(psql -U "$DB_USER" -d "$DB_NAME" -f "$SQL_RAW_TBL_EXISTS" -t -A)
RAW_TOT_RECORDS=$(psql -U "$DB_USER" -d "$DB_NAME" -f "$SQL_RAW_TBL_RECORDS" -t -A)
APP_TABLE_EXISTS=$(psql -U "$DB_USER" -d "$DB_NAME" -f "$SQL_APP_TBL_EXISTS" -t -A)
APP_TOT_RECORDS=$(psql -U "$DB_USER" -d "$DB_NAME" -f "$SQL_APP_TBL_RECORDS" -t -A)

if [ "$RAW_TABLE_EXISTS" = "t" ] && [ "$RAW_TOT_RECORDS" = 40 ]; then
  echo "Checking App table"
  if [ "$APP_TABLE_EXISTS" = "t" ] && [ "$APP_TOT_RECORDS" = 40 ]; then
    # run etl
    # run django app
  fi
else
  echo "No good"
fi


echo $RAW_TABLE_EXISTS
echo $RAW_TOT_RECORDS