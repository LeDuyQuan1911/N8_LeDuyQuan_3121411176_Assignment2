Full Name: Lê Duy Quân
ID Students: 3121411176
Class: DCT121C5

# Automated Testing with Selenium and Pytest

This project contains automated test cases using **Selenium WebDriver** and **Pytest** to verify the sorting functionality on the [Open Cart website](http://localhost/webopencart/index.php?route=common/home&language=en-gb).

## Table of Contents
- [Requirements](#requirements)
- [Setup Instructions](#setup-instructions)
- [Running the Tests](#running-the-tests)
- [Notes](#notes)

---

## Requirements

### 1. Software
- **Python**: Version 3.7 or higher
- **Browser**: Microsoft Edge (or can be replaced with Chrome, Firefox, etc.)
- **Edge WebDriver**: Must be compatible with your Edge browser version (instructions provided below).

### 2. Python Libraries
- **Selenium**: For browser automation
- **Pytest**: To run and manage test cases

---

## Setup Instructions

### Prerequisite: Download XAMPP -> Start Apache and MySQL
### Prerequisite: Download and set up OpenCart localhost

### 1. Install Python
1. [Download Python](https://www.python.org/downloads/) and install it, ensuring the option "Add Python to PATH" is selected during installation (Path environment).
2. Confirm the installation by running:
   ```bash
   python --version
   ```

### 2. Install Required Python Packages
1. Open the terminal in VS Code: Terminal > New Terminal
2. Create a virtual environment using the command:
   ```bash
   python -m venv venv
   ```
3. Activate the virtual environment:
   ```bash
   venv\Scripts\activate
   ```
4. Use `pip` to install Selenium and Pytest:
   ```bash
   pip install selenium pytest
   ```

### 3. Set up Edge WebDriver
To automate tests with Microsoft Edge:
1. Check your **Microsoft Edge** version by navigating to `edge://settings/help`.
2. Download the corresponding **Edge WebDriver** version from [Microsoft's official WebDriver page](https://developer.microsoft.com/en-us/microsoft-edge/tools/webdriver/).
3. Extract the WebDriver executable file (e.g., `msedgedriver.exe`) and place it in a folder included in the **system PATH**, or update the `driver` fixture to point to the correct path of the driver file.

If you're using **Chrome**:
- Replace `webdriver.Edge()` with `webdriver.Chrome()` in the code, and download **ChromeDriver** as a replacement.

### 4. Configure the Test Environment
1. Ensure a stable internet connection, as the tests will interact with the live [Open Cart website](http://localhost/webopencart/index.php?route=common/home&language=en-gb).
2. Confirm that the login credentials (`leduyquan2574@gmail.com` and `Quan19112003`) are accessible on the test page.

---

## Running the Tests

### Run from the Command Line
To run all tests, navigate to the project folder and run:
   ```bash
   pytest <your_script_file_name>.py
   ```

### Generate HTML Test Report in Python
To create an HTML report for a Selenium test, install a plugin using the command:
```bash
pip install pytest-html
```
To generate the report, navigate from the current directory to the folder containing the Pytest file you want to execute. Then run:
```bash
pytest --html=report.html
```

Once this command successfully runs, a new file named `report.html` will be generated in the project folder.
