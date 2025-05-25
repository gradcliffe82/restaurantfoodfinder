#!/bin/bash
export PGPASSWORD="$DATABASE_PASSWORD"
export PGHOST="$DATABASE_HOST"
export PGPORT="$DATABASE_PORT"

DB_USER=postgres
DB_NAME=andromeda

SQL_RAW_TBL_EXISTS=sql/check_raw_tbl_exists.sql
SQL_RAW_TBL_RECORDS=sql/check_raw_tbl_records.sql
SQL_APP_TBL_EXISTS=sql/check_app_tbl_exists.sql
SQL_APP_TBL_RECORDS=sql/check_app_tbl_records.sql

# check if db is active
echo "ETL initializer. Checking if DB is active."
DB_ACTIVE=$(psql -U "$DB_USERNAME" -d $"$DB_NAME" -p "$DATABASE_PORT" -c "SELECT 1;" -t -A) || exit 1

command
if [ $? -ne 0 ]; then
    echo "Command failed! DB not active ready yet."
    exit 1
fi

if [ "$DB_ACTIVE" = 0 ]; then
  echo "DB not fully initialized yet."
  exit 1
fi

# SQL FILE LOCATIONS
RAW_TABLE_EXISTS=$(psql -U "$DB_USERNAME" -d "$DB_NAME" -f "$SQL_RAW_TBL_EXISTS" -t -A)
RAW_TOT_RECORDS=$(psql -U "$DB_USERNAME" -d "$DB_NAME" -f "$SQL_RAW_TBL_RECORDS" -t -A)
echo "Preparing for etl script. Checking if raw table exists."
if [ "$RAW_TABLE_EXISTS" = "t" ] && [ "$RAW_TOT_RECORDS" = 40 ]; then
  echo "Raw tables exits! Checking App table"
  APP_TABLE_EXISTS=$(psql -U "$DB_USERNAME" -d "$DB_NAME" -f "$SQL_APP_TBL_EXISTS" -t -A)
  echo "$APP_TABLE_EXISTS"
  if [[ "$APP_TABLE_EXISTS" = "t" ]]; then
    # run etl
    echo "running etl program"
    PY_ETL_SCRIPT=$(python data/etl_script.py -rawtable)
    # run django app
    PY_RUN_DJANGO=$(python manage.py runserver 0.0.0.0:8000)
    # exit
    exit 0
  else

    echo "Applications tables are not created yet. DB Migration must be completed, before executing etl."
  fi
fi
