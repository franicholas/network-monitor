# Network Monitor

A Python command-line tool that periodically checks TCP endpoints and records the results to a CSV file.

## Features

- Checks whether configured TCP endpoints are reachable.
- Supports monitoring multiple endpoints in one run.
- Measures connection time.
- Records timestamps, hosts, ports, statuses and elapsed times in `results.csv`.
- Displays cumulative success and failure statistics for each endpoint.
- Supports configurable monitoring intervals and connection timeouts.
- Handles Ctrl+C to stop monitoring.

## Requirements

- Python 3
- pytest for running the automated tests

The monitor itself uses only Python's standard library.

## Usage

Run the monitor against one or more endpoints in the form ip:port 

```
python monitor.py --endpoint 127.0.0.1:8000 127.0.0.1:8001
```

### Configure the monitoring interval

Set the time between monitoring cycles in seconds:

```
python monitor.py --endpoint 127.0.0.1:8000 --interval 5
```

The default interval is 15 seconds.

### Configure the connection timeout

Set the maximum time allowed for a connection attempt, in seconds:

```
python monitor.py --endpoint 127.0.0.1:8000 --timeout 3
```

The default timeout is 2 seconds.

The example endpoints use the loopback address, `127.0.0.1`, which refers to the computer running the monitor. A service must be listening on the specified port for the connection check to succeed.

Press Ctrl+C to stop monitoring.

## Output

Results are appended to `results.csv`, with the following fields:

- Timestamp
- Host
- Port
- Status
- Elapsed time in milliseconds

The terminal also displays per-cycle results and cumulative statistics for each endpoint.

The generated CSV file is stored locally and excluded from version control.

## Tests

Run the automated tests using pytest:

```
python -m pytest -v
```

## Limitations

The monitor checks TCP connection availability. It does not verify application-level health, validate service responses or guarantee that an application is functioning correctly.
