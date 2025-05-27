# AutoLinker: LinkedIn Automation Tool

[![Build Status](https://github.com/harshkasat/AutoLinker/actions/workflows/main.yml/badge.svg)](https://github.com/harshkasat/AutoLinker/actions/workflows/main.yml)
[![License](https://img.shields.io/badge/License-MIT-blue.svg)](https://opensource.org/licenses/MIT)
[![Python Version](https://img.shields.io/badge/python-3.7+-blue.svg)](https://www.python.org/)


## 1. Project Overview

AutoLinker is a Python-based automation tool for LinkedIn. It allows users to automate several LinkedIn actions, including sending connection requests, liking posts, and posting comments.  This is achieved through Selenium and WebDriver. The tool is designed to improve efficiency and streamline interactions on the platform.


## 2. Table of Contents

* [Project Overview](#project-overview)
* [Prerequisites](#prerequisites)
* [Installation](#installation)
* [Configuration](#configuration)
* [Usage](#usage)
* [Project Architecture](#project-architecture)
* [Contributing](#contributing)
* [License](#license)


## 3. Prerequisites

* **Python 3.7+:** AutoLinker requires Python 3.7 or higher.
* **Dependencies:** The required libraries are listed in `requirements.txt`. You can install them using `pip install -r requirements.txt`.
* **ChromeDriver:**  AutoLinker uses ChromeDriver to interact with the LinkedIn website.  You need to download the appropriate ChromeDriver version for your Chrome browser and ensure it's in your system's PATH or specify its location.  The `webdriver-manager` package helps manage this automatically.
* **LinkedIn Account:** A LinkedIn account is essential to use this tool.


## 4. Installation

1. **Clone the repository:**
   ```bash
   git clone https://github.com/harshkasat/AutoLinker.git
   cd AutoLinker
   ```

2. **Install dependencies:**
   ```bash
   pip install -r requirements.txt
   ```

3. **(Optional) Setup a virtual environment:** It's recommended to use a virtual environment to isolate the project's dependencies.

   ```bash
   python3 -m venv .venv
   source .venv/bin/activate  # On Linux/macOS
   .venv\Scripts\activate  # On Windows
   ```


## 5. Configuration

The tool is configured via command-line arguments using the `utils.py` module's `linkedin_args_parser()` function.  These arguments control which actions are performed and their limits.


## 6. Usage

The main script is `app.py`, which uses FastAPI to create a simple web server. However, the core LinkedIn automation logic resides in `main.py`. To run the automation:


1.  **Run the FastAPI server:**
    ```bash
    uvicorn app:app --reload
    ```

2. **Call the automation endpoint:**  This endpoint triggers the LinkedIn automation.  You'll need to pass the desired actions and limits as query parameters. For example, to send 5 connection requests and like posts with a scroll limit of 3:

    ```bash
    curl http://127.0.0.1:8000/call_automate?send_connections=true&connection_limit=5&like_posts=true&like_scroll_limit=3
    ```

    Replace `127.0.0.1:8000` with your server's address and port if needed.  You can also omit parameters to use default values.

3. **Command-line arguments (alternative):** You can run the automation directly from the command line (without the FastAPI server) by executing `main.py`.  The command-line arguments are defined in `utils.py` and are passed to `main.py`.  Example:

   ```bash
   python main.py -s -l -c --connection-limit 5 --like-scroll-limit 3 --comment-scroll-limit 2
   ```
   * `-s` or `--send-connections`: Send connection requests.
   * `-l` or `--like-posts`: Like posts.
   * `-c` or `--comment-posts`: Comment on posts.
   * `--connection-limit`: Number of connection requests to send.
   * `--like-scroll-limit`: Number of times to scroll down while liking posts.
   * `--comment-scroll-limit`: Number of times to scroll down while commenting on posts.


## 7. Project Architecture

The project is structured into several modules:

* **`main.py`:** The main script that orchestrates the LinkedIn automation.
* **`utils.py`:** Contains the argument parser.
* **`LinkedinAutomation` directory:** Contains modules for specific LinkedIn actions (connections, likes, comments).
* **`app.py`:**  FastAPI server for easier access to the automation.


## 8. Contributing

Contributions are welcome! Please refer to the [CONTRIBUTING.md](CONTRIBUTING.md) file (if available) for guidelines.


## 9. License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.


**Note:**  This README is based on the provided code.  A more comprehensive README would include details about error handling, logging,  the structure of the `LinkedinAutomation` module, and more detailed usage examples.  The `comments_linkedin_posts.py` file provides an example of how the commenting functionality works, showing the use of Selenium to interact with the webpage elements.  Similar logic is likely used in the other modules within the `LinkedinAutomation` directory.  Remember to handle potential exceptions and implement robust error handling in your automation scripts.
