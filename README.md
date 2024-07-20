---

# InternetCheck

InternetCheck is a Python application that monitors internet connectivity and logs connection status in real-time. It provides visual feedback through a GUI and audible alerts using sound files.

## Table of Contents
- [Features](#features)
- [Requirements](#requirements)
- [Installation](#installation)
  - [Virtual Environment Setup](#virtual-environment-setup)
- [Usage](#usage)
- [Screenshots](#screenshots)
- [Contributing](#contributing)

## Features
- **Real-time Monitoring:** Constantly checks internet connectivity.
- **Logging:** Logs timestamps of successful and failed connection attempts.
- **GUI Interface:** Provides a graphical interface to view connection status.
- **Alert System:** Alerts users with a sound alarm and pop-up message on connection failure.

## Requirements
- Python 3.x
- Additional Python libraries:
  - tkinter
  - requests
  - playsound

## Installation

### Virtual Environment Setup

1. Clone the repository:
   ```
   git clone https://github.com/vitaliy-developer/InternetCheck.git
   ```
   
2. Navigate into the project directory:
   ```
   cd InternetCheck
   ```
   
3. Create a virtual environment named `InternetCheck_venv`:
   ```
   python3 -m venv InternetCheck_venv
   ```
   
4. Activate the virtual environment:
   - On Linux:
     ```
     source InternetCheck_venv/bin/activate
     ```

5. Install dependencies:
   ```
   pip install -r requirements_linux.txt
   ```

6. To deactivate the virtual environment, simply run:
   ```
   deactivate
   ```

## Usage
1. Activate the virtual environment if it's not already activated:
   - On Linux:
     ```
     source InternetCheck_venv/bin/activate
     ```
     
2. Run the application:
   ```
   python main.py
   ```
   This will launch the graphical user interface (GUI) for monitoring internet connectivity.

3. To deactivate the virtual environment after usage, simply run:
   ```
   deactivate
   ```

## Screenshots
![alt text](https://github.com/vitaliy-developer/InternetCheck/blob/main/image.png)

## Contributing
Contributions are welcome! Please fork the repository and submit a pull request with your changes. For major changes, please open an issue first to discuss what you would like to change.

