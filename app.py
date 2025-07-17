# app.py

import datetime
from flask import Flask, request, jsonify

app = Flask(__name__)

# --- Holiday and Business Hour Logic (No external packages) ---

def get_sa_public_holidays(year):
    """
    Returns a set of datetime.date objects for South African public holidays.
    Handles the rule where if a holiday falls on a Sunday, the following Monday is a holiday.
    """
    holidays = {
        datetime.date(year, 1, 1),   # New Year's Day
        datetime.date(year, 3, 21),  # Human Rights Day
        datetime.date(year, 4, 18),  # Good Friday (2025)
        datetime.date(year, 4, 21),  # Family Day (2025)
        datetime.date(year, 4, 27),  # Freedom Day
        datetime.date(year, 5, 1),   # Workers' Day
        datetime.date(year, 6, 16),  # Youth Day
        datetime.date(year, 8, 9),   # National Women's Day
        datetime.date(year, 9, 24),  # Heritage Day
        datetime.date(year, 12, 16), # Day of Reconciliation
        datetime.date(year, 12, 25), # Christmas Day
        datetime.date(year, 12, 26), # Day of Goodwill
    }

    # Add Mondays for holidays falling on a Sunday
    mondays_to_add = set()
    for holiday in holidays:
        if holiday.weekday() == 6: # Sunday is 6
            mondays_to_add.add(holiday + datetime.timedelta(days=1))

    return holidays.union(mondays_to_add)

def is_business_second(dt):
    """
    Checks if a given datetime object represents a single business second.
    A business second is on a weekday, during business hours, and not a public holiday.
    """
    # 1. Check if weekday (Monday=0, Tuesday=1, ..., Friday=4)
    if dt.weekday() > 4:
        return False

    # 2. Check if within business hours (08:00:00 to 16:59:59)
    start_hour = datetime.time(8, 0, 0)
    end_hour = datetime.time(17, 0, 0)
    if not (start_hour <= dt.time() < end_hour):
        return False

    # 3. Check if it's a public holiday
    # We check holidays for both the start and end year in case the range spans years.
    holidays = get_sa_public_holidays(dt.year)
    if dt.date() in holidays:
        return False

    return True

# --- API Endpoint ---

@app.route('/calculate', methods=['GET'])
def calculate_business_seconds():
    """
    Calculates the total business seconds between a start and end time.
    """
    start_time_str = request.args.get('start_time')
    end_time_str = request.args.get('end_time')

    # Parameter validation
    if not start_time_str or not end_time_str:
        return "Error: Please provide both 'start_time' and 'end_time' parameters.", 400

    try:
        # Parse ISO-8601 strings into datetime objects
        start_time = datetime.datetime.fromisoformat(start_time_str)
        end_time = datetime.datetime.fromisoformat(end_time_str)
    except ValueError:
        return "Error: Invalid ISO-8601 format for start_time or end_time.", 400

    # The problem guarantees start_time will be before end_time.

    total_business_seconds = 0
    current_time = start_time

    # Iterate second by second from start to end
    while current_time < end_time:
        if is_business_second(current_time):
            total_business_seconds += 1
        current_time += datetime.timedelta(seconds=1)

    return jsonify(total_business_seconds)

if __name__ == '__main__':
    # Use host='0.0.0.0' to be accessible from the network
    app.run(host='0.0.0.0', port=5000)
    