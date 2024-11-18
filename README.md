
📸 Nature & Poetry Photo Project - API Integration Documentation

Overview
This project combines photography with poetry to enhance the connection between nature and human emotions. By capturing photos of natural scenery, 
the camera automatically uses Google Cloud Vision to recognize the elements in the image and OpenAI API to generate a unique poem based on the detected content. 
The resulting combination of the photo and poem is printed instantly using a built-in printer.

Objectives
Automatically identify natural elements in photos using Google Cloud Vision.
Generate poetry inspired by the recognized content using OpenAI API.
Print the final output (photo + poem) instantly to provide an engaging, physical keepsake.

————————————————————————————————————————————————————————————————————————————————————————————————————————————————————————————
🛠️ Step 1: Prerequisites
Before getting started, ensure you have:
1） A Google Cloud account with Cloud Vision API enabled.
2） An OpenAI API key.
3） A Raspberry Pi (or another computing device) with Python installed.
4） Access to a thermal printer (for instant prints).


🗂️ Step 2: Setting Up the Environment
1） Create a Google Cloud Project
2） Go to Google Cloud Console.
3） Create a new project.
4） Enable the Cloud Vision API for your project.
5） Generate an API key and download the JSON credentials file.
6） Get OpenAI API Key
7） Go to OpenAI.
8） Sign up or log in and generate an API key.


💻 Step 3: Code Implementation


🛠️ Step 4: Running the Application
Create a script to capture a photo, analyze it, generate poetry, and print the result.


🚀 Step 5: Testing and Deployment
1) Run the script on your Raspberry Pi to test the entire flow.
2) Ensure your camera captures images correctly, and your printer produces the intended output.

   
📚 References
Google Cloud Vision API Documentation
OpenAI API Documentation
Python ESC/POS Library
