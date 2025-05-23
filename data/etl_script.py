import re
import psycopg2
import logging
import csv

logger = logging.getLogger(__name__)
logger.setLevel(logging.INFO)
console_handler = logging.StreamHandler()
formatter = logging.Formatter('%(asctime)s - %(levelname)s - %(message)s')
console_handler.setFormatter(formatter)
logger.addHandler(console_handler)

parser = {
    "operating_day_patterns": [
        {"pattern": r"((?:Mon|Tue|Tues|Wed|Thu|Fri|Sat|Sun)\-(?:Mon|Tue|Tues||Wed|Thu|Fri|Sat|Sun)\,)?(?(1) ((?:Mon|Tue|Tues|Wed|Thu|Fri|Sat|Sun))|^((?:Mon|Tue|Tues|Wed|Thu|Fri|Sat|Sun)\-(?:Mon|Tue|Tues|Wed|Thu|Fri|Sat|Sun) ))"},
        {"pattern": r"((?:Mon|Tue|Tues|Wed|Thu|Fri|Sat|Sun)\,)?(?(1) ((?:Mon|Tue|Tues|Wed|Thu|Fri|Sat|Sun)\-(?:Mon|Tue|Tues|Wed|Thu|Fri|Sat|Sun))|^((?:Mon|Tue|Tues|Wed|Thu|Fri|Sat|Sun)\-(?:Mon|Tue|Tues|Wed|Thu|Fri|Sat|Sun) ))"},
        {"pattern": r"(?:(\s(?:Mon|Tue|Tues|Wed|Thu|Fri|Sat|Sun)\-(?:Mon|Tue|Tues|Wed|Thu|Fri|Sat|Sun)\s)|(\s(?:Mon|Tue|Tues|Wed|Thu|Fri|Sat|Sun)\s))"},


    ],
    "operating_time_patterns":
        [
            {"pattern": r"\s(\d{1,2} (?:am|pm) \- \d{1,2} (?:am|pm))"},
            {"pattern": r"(\d{1,2}(?:[:])\d{1,2} (?:am|pm) \- \d{1,2}(?:[:])\d{1,2} (?:am|pm))"},
            {"pattern": r"(\d{1,2}(?:[:])\d{1,2} (?:am|pm) \- \d{1,2} (?:am|pm))"},
            {"pattern": r"(\s\d{1,2} (?:am|pm) \- \d{1,2}(?:[:])\d{1,2} (?:am|pm))"}
        ]
}
MON = "MON"
TUE = "TUE"
TUES = "TUES"
WED = "WED"
THU = "THU"
FRI = "FRI"
SAT = "SAT"
SUN = "SUN"


def create_op_time_range(time_data, time_range_list: list):
    """

    :param time_data:
    :return:
    """
    # split time and format to time
    op_time_ranges = time_data.split("-")
    for op_time in op_time_ranges:

        f_time = op_time.strip()
        pattern = r"(^\d{1,2}\b) (am|pm|AM|PM)"
        result = re.search(pattern, f_time)
        if result:
            hour = result.groups()[0] + ":00"
            meridiem = result.groups()[1].upper()
            f_time = f"{hour} {meridiem}"
        else:
            f_time = f_time.upper()

        time_range_list.append(f_time)


def create_operating_days_range(operational_days, days_open: list):
    """

    :param operational_days:
    :return:
    """
    operational_week = {
        "MON": 0,
        "TUE": 1,
        "TUES":1,
        "WED": 2,
        "THU": 3,
        "FRI": 4,
        "SAT": 5,
        "SUN": 6
    }
    op_days = operational_days.split("-")
    if len(op_days) > 1:
        day1 = operational_week[op_days[0].upper().strip().replace(",", "")]
        day2 = operational_week[op_days[1].upper().strip().replace(",", "")]
        operational_range = range(day1, day2+1)

        dict_op_week_items = [x for x in operational_week.items()]
        for day in operational_range:
            days_open.append(dict_op_week_items[day][0])
    else:
        days_open.append(operational_days.replace(", ", "").strip().upper())


def parse_operating_time(sched_data):
    """

    :param sched_data:
    :return:
    """
    operating_time_range = []
    for pattern in parser["operating_time_patterns"]:
        result = re.search(pattern['pattern'], sched_data)
        if result:
            match_result = result.group()
            create_op_time_range(match_result, operating_time_range)

    return {"operating_times": operating_time_range}


def parse_operating_days(sched_data):
    """

    :param sched_data:
    :return:
    """

    days_open = []
    for pattern in parser['operating_day_patterns']:
        result = re.search(pattern['pattern'], sched_data)
        if result:
            match_groups = [grp for grp in result.groups() if grp is not None]

            for match in match_groups:
                create_operating_days_range(match, days_open)
            break
    return {"days_open": days_open}


def connect_db():
    """
    Connects to the db and returns the connection object.
    :return:
    """

    try:
        connection = psycopg2.connect(database="andromeda", user='postgres', password='2010@Wesley2010', host="localhost", port=5432)
        return connection
    except Exception as ex:
        logger.error("An error occurred while attempting to connect.")


def create_db(connection):
    statement = "CREATE database RESTAURANTS"
    cursor = connection.cursor()
    try:
        cursor.execute(statement)
        connection.commit()
    except Exception as ex:
        logger.error("An error occurred while creating database")


def create_table(connection):
    """
    Create the application target table
    :param connection:
    :return:
    """
    statement = "CREATE TABLE restaurants (restaurant_ops JSONB)"
    cursor = connection.cursor()
    try:
        cursor.execute(statement)
        connection.commit()
    except Exception as ex:
        logger.error("An error occurred while creating table")


def write_record(connection, restaurant_name, op_data):
    """
    Writes a record to the table
    :param row:
    :return:
    """

    cursor = connection.cursor()
    try:
        cursor.execute("""INSERT INTO restaurants (restaurant_operational_hours) VALUES (%s)""", (json.dumps(op_data),))
        connection.commit()
    except Exception as ex:
        logger.error(f"An error occurred while writing row. {ex}")


def main():

    connection = connect_db()
    # create_table(connection)

    file_name = "restaurants.csv"

    with open(file_name, 'r') as csv_file:
        csv_reader = csv.DictReader(csv_file)
        tot_lines = 0

        for row in csv_reader:
            tot_lines += 1
            multiple_op_hours = row['Hours'].split("/")
            if len(multiple_op_hours)>1:
                for op_hours in multiple_op_hours:
                    restaurant_operation = {"restaurant_name": row['Restaurant Name']}
                    restaurant_operation.update(parse_operating_days(op_hours))
                    restaurant_operation.update(parse_operating_time(op_hours))
                    write_record(connection, row['Restaurant Name'], restaurant_operation)

            else:
                restaurant_operation = {"restaurant_name": row['Restaurant Name']}
                restaurant_operation.update(parse_operating_days(row['Hours']))
                restaurant_operation.update(parse_operating_time(row['Hours']))
                write_record(connection, row['Restaurant Name'], restaurant_operation)
                write_record(connection, row['Restaurant Name'], restaurant_operation)


        print(tot_lines)


if __name__ == '__main__':
   main()