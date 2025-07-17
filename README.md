
# Business Seconds API

This API calculates the total number of business seconds between two given timestamps.

## Definition of a Business Second
A business second is defined as any whole second that elapses under the following conditions:
- Between **08:00:00** and **16:59:59**.
- On a weekday (**Monday - Friday**).
- Is not a public holiday in the **Republic of South Africa**.

## API Endpoint

**GET `/calculate`**

### Parameters

| Parameter    | Type   | Description                                   | Required |
|--------------|--------|-----------------------------------------------|----------|
| `start_time` | string | The start time in ISO-8601 format.            | Yes      |
| `end_time`   | string | The end time in ISO-8601 format.              | Yes      |

### Example Request
```
curl "[http://127.0.0.1:5000/calculate?start_time=2025-07-21T08:00:00Z&end_time=2025-07-21T17:00:00Z](http://127.0.0.1:5000/calculate?start_time=2025-07-21T08:00:00Z&end_time=2025-07-21T17:00:00Z)"
```

### Success Response
A single integer representing the total business seconds.
```json
32400
```

### Error Response
An error message string with an appropriate HTTP status code.
```
Error: Invalid ISO-8601 format for start_time or end_time.
```

## Setup and Deployment

### 1. Prerequisites
- Python 3.8+
- `venv` module for Python

### 2. Automated Deployment
To deploy the application, run the automated deployment script:
```bash
chmod +x deploy.sh
./deploy.sh
```
This script will:
1. Create a Python virtual environment.
2. Install all required dependencies.
3. Start the application server using Gunicorn on `http://0.0.0.0:5000`.

### 3. Running Tests
To run the automated tests, ensure you have activated the virtual environment and installed dependencies, then run:
```bash
source venv/bin/activate
pytest
```