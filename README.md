# Project Scraper & Notifier


## Overview

This Python automation tool leverages the Selenium WebDriver to scrape and monitor Upwork for newly posted projects that match specific Python and Django filters. It offers project notifications on both mobile devices (via Pushbullet) and desktops. The script actively checks for new projects every 10 minutes and sends notifications if a project is posted within an hour.

## Features

- Automatically scrape the first Python and Django related project posted on Upwork.
- Filter projects based on specific criteria.
- Send real-time notifications to mobile devices and desktops.
- Periodically check for new projects on Upwork.

## Usage

1. Clone the repository

2. Install dependencies:

    ```shell
       pip freeze > requirements.txt
    
       pip install -r requirements.txt
  ## Pushbullet Setup

1. **Create a Pushbullet Account** (if you don't have one).
2. **Generate an API Token** and set it as an environment variable or input it directly into the script.

## Running the Script

  To run the script, use the following command:
        
    python upwork_scraper.py

**Configuration:**

- Modify the `config.py` file to specify your Upwork filter criteria and notification settings.
- Adjust the script's timing and frequency in `scheduler.py` to suit your preferences.

**Contributing:**

We welcome contributions! If you'd like to enhance this project, please:

1. Fork the repository.
2. Create a new branch (e.g., `git checkout -b feature/your-feature`).
3. Commit your changes (e.g., `git commit -m 'Add some feature'`).
4. Push to the branch (e.g., `git push origin feature/your-feature`).
5. Create a new Pull Request.
