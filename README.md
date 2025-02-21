# Automation Script for Chathub Interaction and Data Processing

## Introduction

This script is designed to automate interactions with Chathub, specifically for logging in, submitting data, and retrieving results. It leverages Playwright for browser automation and handles tasks such as user authentication, data submission, error handling, and output management.

## Features

- **Automated Login**: The script includes a function to log in using Google authentication, enhancing security and reducing manual intervention.
- **Batch Processing**: Data is submitted in batches to handle large volumes efficiently.
- **Error Handling**: Robust mechanisms are in place to detect and manage errors, such as failed fetches or timeouts, ensuring the script remains resilient.
- **Data Extraction and Saving**: The script extracts titles from JSON files, submits them for processing, and saves the results to text files for easy access.

## Requirements

- **Playwright**: A browser automation framework for handling web interactions.
- **Python**: The scripting language used for the automation logic.
- **JSON and Text Files**: For input data and output results, respectively.

## Usage

1. **Configuration**: Update the configuration variables at the top of the script with your actual email, password, input directory, output directory, and the URL of the web application.

2. **Dependencies**: Ensure Playwright is installed in your environment. You can install it using pip:
   ```bash
   pip install playwright
   ```

3. **Execution**: Run the script using Python:
   ```bash
   python automation_script.py
   ```

4. **Input Preparation**: Place your JSON files in the specified input directory. Each JSON file should contain an array of objects with a 'title' field.

5. **Output Retrieval**: The script will generate text files in the output directory containing the processed results.

## Functionality

- **Login**: The script logs in using Google authentication, ensuring a secure and seamless experience.
- **Data Submission**: Titles extracted from JSON files are submitted in batches to the web application for processing.
- **Result Handling**: After submission, the script waits for the results, handles any errors, and saves the outputs to text files.

## Error Handling

The script includes mechanisms to detect and handle errors such as failed fetches or timeouts. If an error occurs, the script will attempt to reload the page and resubmit the data, ensuring minimal interruption to the process.

## Conclusion

This automation script streamlines interactions with a web application, making it easier to process data in batches, handle errors gracefully, and manage outputs efficiently. By following the usage instructions and configuring the script appropriately, users can automate their workflows effectively.