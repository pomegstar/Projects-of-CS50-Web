# MediBook

## Overview

The **MediBook** is a web application designed to facilitate the booking of doctor appointments for patients across multiple hospitals as well as to manage patients' serial number by the doctor. It utilizes Django on the back-end and JavaScript on the front-end. This platform enables patients to book appointments with doctors based on their availability, manage appointment schedules, and receive real-time notifications regarding their appointments. The system is designed with a user-friendly interface and ensures a seamless experience for both patients and doctors.

## Distinctiveness and Complexity

### Distinctiveness

This project is a distinct app, it focuses on solving real-world challenges in the healthcare sector. MediBook is not an e-commerce or social network site like project-2 or project-4 (and, in addition, not like an old CS50W Pizza project), but more complex than those. Moreover, the structure of this app is fully different from those apps.

This project stands out from others in several ways. Firstly, it is composed of three distinct Django apps: **Accounts**, **Hospitals**, and **Appointments**. Each of these apps is responsible for handling a specific aspect of the overall system. This modular structure not only promotes clean code and separation of concerns but also enhances the maintainability and scalability of the application.

Moreover, the system uses Redis, Django Channels, and WebSocket technology for real-time notifications which also differentiates this project. This system allows the application to provide instant updates to patients regarding their appointment status without requiring them to refresh their browsers manually, a feature not commonly found in similar projects.

### Complexity

The complexity of this project lies in its architecture and the features it offers:

1. **Three Independent Apps**: The project is divided into three inter-connected apps: **Accounts**, **Hospitals**, and **Appointments**. Which makes it more complex than any other projects of this course.

2. **Redis-Server for Notifications**: Redis is used to handle the real-time notification system. When a doctor completes a patient's appointment or a patient cancels his/her appointment, the changes are pushed to the patients through a WebSocket connection, ensuring the patient is notified immediately about his/her updated serial number.

3. **Dynamic Availability Management**: The system dynamically calculates the available slots for doctors based on their predefined schedules and ensures patients can only book appointments on valid days. This involves backend validation and front-end restrictions using JavaScript.

4. **Real-time Serial Number Update**: The application ensures that when a doctor updates the treatment status of a patient, all subsequent patients in the queue are notified of their updated serial numbers. This is a non-trivial feature that adds to the application's real-time interactivity.

5. **Custom Notifications with WebSockets**: Unlike typical projects that might rely on polling or refresh-based updates, this project uses WebSocket connections to deliver updates to the patient immediately. The use of a custom modal with a "Refresh" button further enhances the user experience by allowing them to reload the page only when necessary.

## What I did:

The **Medibook** app was developed to solve the practical challenges patients face when trying to book and manage appointments with doctors across different hospitals. I aimed to create a streamlined, user-friendly platform that not only facilitates appointment bookings but also ensures real-time updates and notifications for patients.



**Key Features and Design Decisions:**

1. **Multi-App Architecture:**
   - I structured the project using Django's multi-app architecture, dividing the system into distinct modules: one for managing accounts, another for handling appointments, and a third for managing hospital and doctor data. This modular approach ensures better code organization, maintainability, and scalability.

2. **Real-Time Notifications:**
   - A crucial feature of the app is the real-time notification system that updates patients on their appointment status and serial number changes. I implemented this feature using Redis and WebSockets, ensuring that notifications are instantaneous and patients are always informed about any changes without needing to refresh the page. This is particularly important in a medical context where timing and communication are critical.
   **NOTE:** "Notifications will work only when a patient stays in the appointment app."

3. **Dynamic Date and Time Management:**
   - The app allows doctors to set their availability based on specific days of the week, and patients can only book appointments on those days. I implemented logic to disable unavailable dates in the back-end, ensuring that patients can only select valid dates. This reduces the chances of errors and simplifies the booking process.

4. **Serial Number Management:**
   - The app dynamically manages the serial numbers for each appointment, updating them as patients are seen by the doctor. This ensures that the system is always up-to-date, and doctors can efficiently manage their patient flow. I also implemented a system for doctors to mark patients as "complete," which automatically updates the serial numbers for the remaining patients.

5. **Filtering Patinents:**
   - Doctors can filter their pending patients based on the treatment date in the **Pending Patients** section. AJAX is used to filter patients without reloading the page, making patient management more efficient.

6. **Editing Doctor's Profile**:
   - Doctors have the ability to edit their profiles within the app.

## Why I Did It:
   - In Bangladesh, many patients visit public hospitals daily. Many of them are poor and come from rural area, they pass their whole day by standing in serial for taking a treatment. The hospitals haven't enough seat for their patients rest, for this many of them are getting bored and become more sick. To relieve patients from boring works like standing in queues I have implemented MediBook. The main motivation behind building this project was to create a comprehensive solution of those patients problem. By integrating real-time notifications and dynamic scheduling, I aimed to enhance the user experience for both patients and doctors, ensuring that appointments are managed smoothly and without confusion.

## Project Structure

### Accounts App:
It manages user registration, authentication, and profile management, including differentiating between patients and doctors. It contains these files:
- **Models**: User, Patient
- **Views**: Handles user authentication, registration, and profile management.
- **Templates**: User registration forms, login page.

### Hospitals App
It handles the home page of the entire project. This app contains:
- **Models**: Hospital, Doctor
- **Views**: Manages hospital and doctor information, including working hours and specializations.
- **Templates**: Hospital and doctor listing pages.

### Appointments App
It handles the booking of appointments, real-time updates of appointment status, and notifications. It contains these files:
- **Models**: Appointment
- **Views**: Manages appointment booking, serial number allocation, and real-time updates.
- **Consumers**:  Manages WebSocket connections for real-time notifications to patients.
- **Templates**: Appointment booking page, patient appointment list, doctor’s patient list.

## How to Run the Application

1. **Install Dependencies**: Ensure all required Python packages are installed by running:

   ```
   pip install -r requirements.txt
   ```

2. **Set Up Redis**: Make sure Redis is installed and running on your machine. You can start Redis using:

   ```
   redis-server
   ```

3. **Migrate the Database**: Run the following command to apply the migrations:

   ```
   python manage.py migrate
   ```

4. **Run this project**: As this app is an asgi app, it will not work perfectly in django develepment server. For this, we have to run it by 'daphne', after installing daphne, start the server with:

   ```
   daphne -p 8000 capstone.asgi:application
   ```

5. **Access the Application**: Open your web browser and navigate to `http://127.0.0.1:8000/` to start using the application. Or go to the ports section of terminal and click the link of port: 8000;

## Additional Information

- **User Guide:**
   - **User Types:** The app is designed for two types of users: doctors and patients. During registration, users must specify whether they are a "doctor" or a "patient."

   - **Hospital Management:** Only a superuser can register and manage hospitals. Regular users cannot register as hospitals.

   - **Booking Appointments:** Patients have two options to book an appointment:
      1. Click **Book an Appointment** and submit the appointment directly.
      2. Choose a hospital from the homepage, select a doctor within that hospital, and then submit the appointment.

   - **Appointment Management:** Patients can cancel (delete) their appointments after booking.

   - **Rules of Booking Appointments**:
      - A patient can book a doctor only once per day.
      - Appointments must be booked before the treatment date.
      - Appointments must be booked on valid dates as predefined by doctors.

- **Redis Configuration**: The project relies heavily on Redis for real-time notifications. Make sure Redis is correctly configured and running on your server.

- **WebSockets**: The application uses Django Channels to handle WebSocket connections. Ensure that your Django project is configured to use ASGI instead of WSGI for WebSocket support.

- **Viedo Demonstration Link**: https://youtu.be/FUZf6e-wE1Q?si=RbcH35aIuaEydRvR

This project is designed to handle a complex appointment booking system with real-time updates, making it both unique and challenging compared to standard Django applications.
