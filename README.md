# US Visa Appointment Scheduler

⚠️ **DISCLAIMER: FOR RESEARCH PURPOSES ONLY**

This project is a proof-of-concept implementation created solely for research and educational purposes. It is not intended for actual use in scheduling visa appointments. Using automated tools to interact with the US visa appointment system may violate terms of service and could have legal implications. This code should not be used in production or for real appointment scheduling.

## Overview

An automated tool to monitor and notify about available US visa appointment slots in Canada. The script continuously checks the US visa appointment website and sends notifications when earlier appointment dates become available.

## Features

- Automated login to the US visa appointment system
- Continuous monitoring of available appointment dates
- Push notifications via Prowl when appointments are found
- Specifically targets appointments in 2024 or January 2025
- Regular health check notifications
- Random delays to avoid detection

## Requirements

- Python 3.x
- Chrome browser
- ChromeDriver
- Required Python packages:
  - selenium
  - requests

## Setup

1. Install the required Python packages:
   ```bash
   pip install selenium requests
   ```

2. Create a `credentials.txt` file in the project root with the following format:
   ```
   your_email@example.com
   your_password
   your_prowl_api_key
   ```
   Each credential should be on a separate line in the order:
   - Line 1: US visa appointment system email
   - Line 2: US visa appointment system password
   - Line 3: Prowl API key

3. Ensure Chrome and ChromeDriver are installed on your system

## How It Works

The script performs the following operations:

1. Logs into the US visa appointment website using provided credentials
2. Navigates to the appointment rescheduling page
3. Checks available dates in the calendar
4. Sends notifications through Prowl when:
   - Appointments are found in 2024 or January 2025
   - No appointments are available
   - Any errors occur
   - Regular health checks (every 10 minutes)

## Configuration

- `MONTH_TO_CHECK_2025`: Set of months to check in 2025 (currently set to "January")
- Notification priorities:
  - Regular appointments: Default priority (2)
  - No appointments: Low priority (-2)
  - Errors: Medium priority (-1)
  - Health checks: Low priority (-2)

## Files

- `appointment_schduler.py`: Main script that handles the appointment checking logic
- `paging.py`: Handles notification sending through the Prowl API
- `credentials.txt`: Stores user credentials and API key (not included in repository)

## Note

This is an automated tool that interacts with the official US visa appointment website. Please ensure you comply with the website's terms of service when using this tool.
