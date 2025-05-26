#!/bin/bash
export PGPASSWORD="$DATABASE_PASSWORD"
export PGHOST="$DATABASE_HOST"
export PGPORT="$DATABASE_PORT"

DB_USER=postgres
DB_NAME=andromeda

echo "----ETL Script--"
echo "Checking db host before loading data."
until pg_isready -h "$DATABASE_HOST" -U liine_user; do
  echo "Sleeping 10 seconds."
  sleep 10
done

SQL_CREATE_RAW_TABLE=sql/init_raw_table.sql
CREATE_RAW_TABLE=$(psql -U "$DB_USERNAME" -d "$DB_NAME" -f "$SQL_CREATE_RAW_TABLE" -t -A)

TOT_ROW_RAW_TABLE="SELECT COUNT(*) FROM restaurants_raw"
TOTAL_ROW=$(psql -U "$DB_USERNAME" -d "$DB_NAME"  -c "$TOT_ROW_RAW_TABLE" -t -A)
if [[ "$TOTAL_ROW" = 0 ]]; then
  echo "Copying records..."
  SQL_LOAD_RAW_TABLE="\copy restaurants_raw(\"Restaurant Name\", \"Hours\") FROM 'data/restaurants.csv' WITH CSV HEADER;"
  RESULT=$(psql -U "$DB_USERNAME" -d "$DB_NAME"  -c "$SQL_LOAD_RAW_TABLE" -t -A)
  echo "Performing App migrations"
  # initial
  python manage.py migrate

  # create models
  python manage.py makemigrations restaurantfinder

  # apply changes
  python manage.py migrate
  echo "Preparing for etl process. Checking if raw table exists."
  ## run etl
  echo "Checking App model. "
  SQL_APP_TBL_EXISTS=sql/check_app_tbl_exists.sql
  APP_TABLE_EXISTS=$(psql -U "$DB_USERNAME" -d "$DB_NAME" -f "$SQL_APP_TBL_EXISTS" -t -A)
  if [[ "$APP_TABLE_EXISTS" = "t" ]] ; then
    echo "Running etl script"
    PY_ETL_SCRIPT=$(python module/etl_script.py -rawtable)
    if [[ $EXIT_CODE -ne 0 ]]; then
      echo "Python etl script failed with exit code $EXIT_CODE"
      exit $EXIT_CODE
    fi
  else
    echo "Application models are not created yet. DB Migration must be completed, before executing etl."
  fi

fi
echo "RUNNING DJANGO APP!"
PY_RUN_DJANGO=$(python manage.py runserver 0.0.0.0:8000)



