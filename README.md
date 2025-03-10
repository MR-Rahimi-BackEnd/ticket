Event Management System
This project is designed to manage events and attendees. The main features include creating and retrieving events along with their corresponding attendees and tickets. The system also validates the number of attendees against the maximum allowed for each event and ensures that email addresses are unique for each attendee.

Features
Create and retrieve events along with their attendees and associated tickets.
Validate the number of attendees against the maximum allowed for each event.
Ensure unique email addresses for each attendee.
Use of SQLite as the database for local development and testing.
Project Structure
Models
Event: Model for storing event details (title, date, location, and maximum number of attendees).
Attendee: Model for storing attendee information (name and email).
Ticket: Model for linking an attendee to an event (foreign key for event and attendee).
