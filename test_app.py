# test_app.py

import pytest
from app import app

@pytest.fixture
def client():
    app.config['TESTING'] = True
    with app.test_client() as client:
        yield client

def test_simple_business_hours(client):
    """Test a short period within a single business day."""
    start = "2025-07-21T10:00:00Z" # A Monday
    end = "2025-07-21T10:00:10Z"
    rv = client.get(f'/calculate?start_time={start}&end_time={end}')
    assert rv.status_code == 200
    assert rv.get_json() == 10

def test_spanning_lunch_break(client):
    """Test a period that spans the entire business day."""
    start = "2025-07-21T08:00:00Z" # A Monday
    end = "2025-07-21T17:00:00Z"
    # 9 hours * 60 minutes/hour * 60 seconds/minute
    expected_seconds = 9 * 60 * 60
    rv = client.get(f'/calculate?start_time={start}&end_time={end}')
    assert rv.status_code == 200
    assert rv.get_json() == expected_seconds

def test_outside_business_hours(client):
    """Test a period entirely outside business hours."""
    start = "2025-07-21T18:00:00Z"
    end = "2025-07-21T19:00:00Z"
    rv = client.get(f'/calculate?start_time={start}&end_time={end}')
    assert rv.status_code == 200
    assert rv.get_json() == 0

def test_spanning_a_weekend(client):
    """Test from a Friday to a Monday."""
    start = "2025-07-18T16:00:00Z" # Friday
    end = "2025-07-21T09:00:00Z"   # Monday
    # 1 hour on Friday + 1 hour on Monday
    expected_seconds = (1 * 60 * 60) + (1 * 60 * 60)
    rv = client.get(f'/calculate?start_time={start}&end_time={end}')
    assert rv.status_code == 200
    assert rv.get_json() == expected_seconds

def test_spanning_a_public_holiday(client):
    """Test spanning Women's Day (Saturday) and the following Monday."""
    # August 9, 2025 is a Saturday, so no holiday is observed on Monday.
    start = "2025-08-08T16:00:00Z" # Friday before Women's Day
    end = "2025-08-11T09:00:00Z"   # Monday after Women's Day
    # 1 hour on Friday + 1 hour on Monday
    expected_seconds = (1 * 60 * 60) + (1 * 60 * 60)
    rv = client.get(f'/calculate?start_time={start}&end_time={end}')
    assert rv.status_code == 200
    assert rv.get_json() == expected_seconds

def test_holiday_on_sunday(client):
    """Test Freedom Day 2025 (Sunday) where Monday becomes a holiday."""
    start = "2025-04-25T16:00:00Z" # Friday before Freedom Day weekend
    end = "2025-04-29T09:00:00Z"   # Tuesday after Freedom Day weekend
    # Monday, April 28th is a public holiday.
    # Expected: 1 hour on Friday + 1 hour on Tuesday.
    expected_seconds = (1 * 60 * 60) + (1 * 60 * 60)
    rv = client.get(f'/calculate?start_time={start}&end_time={end}')
    assert rv.status_code == 200
    assert rv.get_json() == expected_seconds

def test_invalid_date_format(client):
    """Test error handling for bad date formats."""
    start = "2025-07-21" # Not ISO-8601
    end = "2025-07-21T10:00:10Z"
    rv = client.get(f'/calculate?start_time={start}&end_time={end}')
    assert rv.status_code == 400
    assert b"Error: Invalid ISO-8601 format" in rv.data

def test_missing_parameters(client):
    """Test error handling for missing parameters."""
    rv = client.get('/calculate?start_time=2025-07-21T10:00:00Z')
    assert rv.status_code == 400
    assert b"Error: Please provide both" in rv.data
    