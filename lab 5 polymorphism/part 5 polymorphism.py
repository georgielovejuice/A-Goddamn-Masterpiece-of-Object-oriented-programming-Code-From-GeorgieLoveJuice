class Member:
    def __init__(self, name=None, email=None, phone_number=None):
        self.__name = name
        self.__email = email
        self.__phone_number = phone_number
    
    @property
    def name(self):
        return self.__name
    
    @property
    def email(self):
        return self.__email
    
    @property
    def phone_number(self):
        return self.__phone_number

class AppointmentScheduler:
    def __init__(self):
        self.appointments = []

    def add_appointment(self, appointment):
        self.appointments.append(appointment)
    
    def edit_appointment(self, title=None, location=None, to=None):
        for appt in self.appointments:
            if title and appt._AppointmentInfo__title == title:
                appt._AppointmentInfo__title = to
            if location and appt._AppointmentInfo__location == location:
                appt._AppointmentInfo__location = to
    
    def delete_appointment(self, title):
        self.appointments = [appt for appt in self.appointments if appt._AppointmentInfo__title != title]
    
    def add_attendance(self, title, member):
        for appt in self.appointments:
            if appt._AppointmentInfo__title == title:
                appt.add_attendee(member)
    
    def show_person_in_appointment(self, member):
        for appt in self.appointments:
            if member in appt.get_attendees():
                appt.display()
    
    def send_notifications(self, title, message):
        for appt in self.appointments:
            if appt._AppointmentInfo__title == title:
                for member in appt.get_attendees():
                    method = "email" if member.email else "sms"
                    contact = member.email if member.email else member.phone_number
                    print(f"Sending {method} notification to: {contact} with message: {message}")
    
    def view_appointments(self):
        for appt in self.appointments:
            appt.display()

class AppointmentInfo:
    def __init__(self, title=None, location=None, date=None):
        self.__title = title
        self.__location = location
        self.__date = date
        self.__attendees = []
    
    def add_attendee(self, member):
        self.__attendees.append(member)
    
    def get_attendees(self):
        return self.__attendees
    
    def display(self):
        attendees_names = ', '.join([member.name for member in self.__attendees])
        print(f"Appointment: {self.__title}, Date: {self.__date}, Location: {self.__location}" + (f", Attendees: {attendees_names}" if attendees_names else ""))

class OneTimeAppointment(AppointmentInfo):
    def __init__(self, title=None, location=None, date=None, attendees=None):
        super().__init__(title, location, date)
        if attendees:
            for attendee in attendees:
                self.add_attendee(attendee)

class WeeklyAppointment(AppointmentInfo):
    def __init__(self, title=None, location=None, day_of_week=None, attendees=None):
        super().__init__(title, location, day_of_week)
        if attendees:
            for attendee in attendees:
                self.add_attendee(attendee)

class ActivityAppointment(AppointmentInfo):
    def __init__(self, title=None, location=None, date=None):
        super().__init__(title, location, date)
    
    def display(self):
        print(f"Activity: {self._AppointmentInfo__title}, Date: {self._AppointmentInfo__date}, Location: {self._AppointmentInfo__location}")

app = AppointmentScheduler()

# Add Members
john = Member("John Doe", "john.doe@example.com")
jane = Member("Jane Smith", "jane.smith@example.com")
robert = Member("Robert Johnson", "robert.johnson@example.com", "08-1234-5678")
emily = Member("Emily Davis", "emily.davis@example.com", "08-3456-7890")

# Add Appointments
app.add_appointment(OneTimeAppointment("Team Meeting #1", "Room A", "2024-03-15", [jane, robert, emily]))
app.add_appointment(OneTimeAppointment("Team Meeting #2", "Room B", "2024-03-17", [jane, robert, emily]))
app.add_appointment(WeeklyAppointment("Weekly Meeting", "Room C", "Wednesday", [john, robert, emily]))
app.add_appointment(ActivityAppointment("Company Party", "Conference Room", "2024-03-17"))
app.add_appointment(ActivityAppointment("Company Visit", "Conference Room", "2024-03-19"))

# # Test Case 1 : Add Appointment, add activity information, and add appointment information.
# Output Expect
# Topic : Team Meeting #1 Location : Room A on 2024-03-15 Attn: Jane Smith,John Doe,Emily Davis
# Topic : Team Meeting #2 Location : Room B on 2024-03-17 Attn: Jane Smith,John Doe,Emily Davis
# Weekly AP, Topic : Weekly Meeting Location : Room C on Wednesday Attn: John Doe,Robert Johnson,Emily Davis
# Activity, Topic : Company Party Location : Conference Room on 2024-03-17
# Activity, Topic : Company Visit Location : Conference Room on 2024-03-17
print("# # Test Case 1 : Add Appointment, add activity information, and add appointment information. ")
app.view_appointments()
print()

# # Test Case 2 : Edit Appointment 
# Change the name of One-Time Appointment #1 from “Team Meeting #1” to “Team B Meeting #1”
# Output Expect
# Topic : Team B Meeting #1 Location : Room A on 2024-03-15 Attn: Jane Smith,John Doe,Emily Davis
# Topic : Team Meeting #2 Location : Room C on 2024-03-17 Attn: Jane Smith,John Doe,Emily Davis
# Weekly AP, Topic : Weekly Meeting Location : Room C on Wednesday Attn: John Doe,Robert Johnson,Emily Davis
# Activity, Topic : Company Party Location : Conference Room on 2024-03-17
# Activity, Topic : Company Visit Location : Conference Room on 2024-03-17
print("Test Case 2 : Edit Appointment")
app.edit_appointment(title="Team Meeting #1", to="Team B Meeting #1")
app.edit_appointment(location="Room B", to="Room C")
app.view_appointments()
print()

# # Test Case 3 : Delete Appointment using topic “Team Meeting #2” 
# Output Expect
# Topic : Team B Meeting #1 Location : Room A on 2024-03-15 Attn: Jane Smith,John Doe,Emily Davis
# Weekly AP, Topic : Weekly Meeting Location : Room C on Wednesday Attn: John Doe,Robert Johnson,Emily Davis
# Activity, Topic : Company Party Location : Conference Room on 2024-03-17
# Activity, Topic : Company Visit Location : Conference Room on 2024-03-17
print("Test Case 3 : Delete Appointment using topic 'Team Meeting #2'")
app.delete_appointment(title="Team Meeting #2")
app.view_appointments()
print()

# # Test Case 4 : Add Attendance who receives appointments for one-time appointments and weekly appointments as follows.
# - One-Time Appointment #1 (“Team B Meeting #1”) Add John Doe
# - Weekly Appointments “Weekly Meeting” added Jane Smith.
# Output Expect
# Topic : Team B Meeting #1 Location : Room A on 2024-03-15 Attn: Jane Smith,John Doe,Emily Davis,John Doe
# Weekly AP, Topic : Weekly Meeting Location : Room C on Wednesday Attn: John Doe,Robert Johnson,Emily Davis,Jane Smith
# Activity, Topic : Company Party Location : Conference Room on 2024-03-17
# Activity, Topic : Company Visit Location : Conference Room on 2024-03-17
print("Test Case 4 : Add Attendance who receives appointments for one-time appointments and weekly appointments")
app.add_attendance("Team B Meeting #1", john)
app.add_attendance("Weekly Meeting", jane)
app.view_appointments()
print()

# # Test Case 5 : Search Attendance Search for individual appointments using the name “Robert Johnson”. 
# Output Expect
# Topic : Team B Meeting #1 Location : Room A on 2024-03-15 Attn: Jane Smith,John Doe,Emily Davis,John Doe
# Weekly AP, Topic : Weekly Meeting Location : Room C on Wednesday Attn: John Doe,Robert Johnson,Emily Davis,Jane Smith
print("Test Case 5 : Search Attendance Search for individual appointments using the name 'Robert Johnson'")
app.show_person_in_appointment(robert)
print()

# # Test Case 6 : Notify by using the appointment “Team B Meeting #1”
# Output Expect
# Sending email notification to: jane.smith@example.com with message : invite for meeting
# Sending email notification to: john.doe@example.com with message : invite for meeting
# Sending SMS notification to : 08-3456-7890 with message : invite for meeting
# Sending email notification to: john.doe@example.com with message : invite for meeting
print("Test Case 6 : Notify by using the appointment 'Team B Meeting #1'")
app.send_notifications("Team B Meeting #1", "invite for meeting")
