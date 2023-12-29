# Face Recognition Voting System with Admin Panel

## Overview

This project implements a comprehensive smart voting system with face recognition for user authentication. The system includes features such as admin registration, voter registration, **live detection**, **face recognition**, and vote counting.

## Features

1. **Admin Registration:**
   - Admins can register by providing their credentials, including a username, password, and phone number.
   - Admins have the authority to manage the voter database.

2. **Voter Registration:**
   - Voters can register by providing their Voter ID, Aadhar Number, and capturing their face for facial recognition.
   - Admins can update the voter database, including adding voter details.

3. **User Verification:**
   - After registration, users need to verify their Voter ID and Aadhar Number.
   - Users also set a username and password during the verification process.

4. **Live Detection and Face Recognition:**
   - During login, users undergo live detection and face recognition for authentication.
   - The system verifies the authenticity of the user before allowing access.

5. **Casting Votes:**
   - Authenticated users can cast their votes by selecting a party and confirming their choice.

6. **Admin Vote Count:**
   - The admin can run the vote count Python script to produce and display the election results.

## Project Structure

The project consists of various components, including scripts for admin registration, voter registration, user verification, live detection, face recognition, and vote counting.

## How to Run

1. Install the required dependencies using the `requirements.txt` file:
       
         pip install -r requirements.txt


2. Setup MySQL Database:

- Create a MySQL database named `voter_register`.
- Update MySQL connection details in relevant scripts.

3. Run the `admin_register.py` script:

       python admin_register.py

 Follow the instructions on the graphical user interface for admin


4. Run the `sep_home.py` script:

       python sep_home.py

Follow the instructions on the graphical user interface for voter interactions.

## Database Setup

- The system uses MySQL for storing user data. Make sure to create a MySQL database named `voter_register`.

- Update the MySQL connection details in the relevant scripts.

## Team Members

This project was done as a team for a special topic 2 as part of the college curriculum. The team members are:

- V S Nithya Shree
- P R Shashank
- Kavana N
- N S Umashankar

## Note

- This project is designed for educational purposes. Ensure proper security measures for real-world use.

Feel free to explore and modify the code to suit your specific requirements. If you encounter any issues or have suggestions for improvements, please open an issue on GitHub.
