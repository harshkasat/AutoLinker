# AutoLinker

AutoLinker is a Python-based automation tool designed to streamline the process of sending connection requests on LinkedIn. Using Selenium, it identifies "Connect" buttons on LinkedIn profiles and automatically sends connection requests, saving you time and effort.

## Features

- Automatically sends connection requests on LinkedIn.
- Identifies "Connect" buttons even within iframes.
- Handles pop-ups for sending requests without a note.
- Simple and easy-to-use script for personal networking automation.

## Requirements

- Python 3.x
- Chrome WebDriver
- Selenium

## Installation

1. Clone this repository to your local machine:

   ```bash
   git clone https://github.com/harshkasat/AutoLinker.git

2. Navigate to the Project Directory
* Change into the project directory:

   ```bash
   cd AutoLinker

3. Install the Depedent library

   ```bash
   pip install -r requirements.txt

4. Download Chrome WebDriver
Download the appropriate Chrome WebDriver for your version of Chrome from [here](https://support.google.com/chrome/answer/95346?hl=en&co=GENIE.Platform%3DDesktop) and place it in your PATH.
Add the path of directory in main.py file.

5. Run the Script

   ```bash
   python main.py
