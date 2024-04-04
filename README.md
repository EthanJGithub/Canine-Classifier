Dog Breed Classifier

This Python program combines database interactions with natural language processing to classify dog breeds based on user-inputted characteristics. By answering a series of questions about a dog's physical attributes, users can identify the breed of their dog with a calculated probability. The program reworks aspects of the Eliza code to engage in a conversation-like interface, making the process both interactive and informative.

Features
Interactive Q&A Session: Users input characteristics such as color, ear type, tail type, size, and coat type.

Database Lookup: Searches a MySQL database for matching dog breeds based on the given attributes.

Probability Calculation: Calculates the likelihood of the dog being of a certain breed based on the number of attributes provided.

Natural Language Processing: Utilizes a modified version of Eliza, a mock psychotherapist program, for natural interaction.

Requirements
Python 3.x
mysql-connector-python: A MySQL driver written in Python.
Access to a MySQL server with the dog_database schema set up.

Installation
Ensure Python 3.x is installed on your system.
Install mysql-connector-python using pip:

Copy code
pip install mysql-connector-python
Clone this repository or download the Python script to your local machine.

Database Setup
Log into your MySQL server.
Create a new database named dog_database.
Import the provided SQL schema and data for the DogBreeds table.
Usage
To run the program, execute the script from your command line or terminal:

Copy code
python dog_breed_classifier.py
Follow the on-screen prompts to input your dog's characteristics. The program will then query the database and return the most likely breed based on the attributes you provided.
