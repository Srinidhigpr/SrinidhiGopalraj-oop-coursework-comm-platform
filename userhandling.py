from abc import abstractmethod
from eventhandling import consultation_hour


class User:
    def __init__(self, email, name, password):
        self.email = email
        self.name = name
        self.__password = password

    def check_password(self, passcode):
        if passcode == self.__password:
            return True
        return False
    
class Student(User):
    def __init__(self, email, name, password):
        super().__init__(email, name, password)

class Teacher(User):
    def __init__(self, email, name, password, start_time, end_time, subject):
        super().__init__(email, name, password)
        self.start_time = start_time
        self.end_time = end_time
        self.subject = subject

    @abstractmethod
    def get_hours(self):
        pass

class TheoryTeacher(Teacher):

    def get_hours(self):
        return f" Available at {self.start_time} to {self.end_time}"

class LabTeacher(Teacher):

    def get_hours(self):
        return f"Not available for consultations, check with Lecturer"

class CurrentUser:
    _instance = None 
    def __new__(cls, *args, **kwargs):
        if not cls._instance:
            cls._instance = super().__new__(cls)
        return cls._instance

    def __init__(self, email, name, event_no):
        self.email = email
        self.name = name
        self.event_no = event_no

    def get_name(self):
        return self.name
    
    def set_event(self, eve_no):
        self.event_no = eve_no
        return
    
    def get_event(self):
        return self.event_no
    
class CurrentUserStudent(CurrentUser, Student):
    def __init__(self, email, name, event_no):
        super().__init__(email, name, event_no)
        self.currentevents = consultation_hour.get_consultations_request(self.email)

    def append_event(self, Event):
        print("event added from class side")
        self.currentevents.append(Event)

    def get_teacher_name(self, email, teachers_list):
        for teach in teachers_list:
            if teach.email == email:
                return teach.name
            
    def format_time(self, time_obj):
        return time_obj.strftime("%H:%M")
    
    def event_exists(self, teacher_email):
        for eve in self.currentevents:
            if eve.student_email == self.email and eve.teacher_email == teacher_email:
                return True
        return False

class CurrentUserTeacher(CurrentUser, Teacher):
    def __init__(self, email, name, event_no):
        super().__init__(email, name, event_no)
        self.currentevents = consultation_hour.get_consultations_request(self.email)

    def get_student_name(self, email, students_list):
        for student in students_list:
            if student.email == email:
                return student.name

class UserFactory:
    @staticmethod
    def create_user(email, name, role):
        if role == 'student':
            return CurrentUserStudent(email, name, 0)
        elif role == 'teacher':
            return CurrentUserTeacher(email, name, 0)
        else:
            raise ValueError("Invalid user role")
        
Teachers = [TheoryTeacher("english@vgtu.org", "Aleksandra","123", time(10,0), time(12, 0), "English" ),
             TheoryTeacher("comparc@vgtu.org", "Vytautas", "456", time(13, 15), time(14, 0), "Computer Architecture" ), 
             LabTeacher("Complab@vgtu.org", "Valentinas", "789", time(0, 0), time(0, 0), "Computer Architecture Lab"),
             TheoryTeacher("discretemaths@vgtu.org", "Julia","123", time(14,0), time(14, 30), "Discrete Mathematics" ),
             TheoryTeacher("electricalengg@vgtu.org", "Sebastian", "456", time(13, 50), time(17, 30), "Electrical Engineering" ), 
             LabTeacher("matlab@vgtu.org", "Julia", "789", time(0, 0), time(0, 0), "Integrals Lab")]

Students = [Student("student1@vgtu.org", "Srinidhi", "123"), 
            Student("student2@vgtu.org", "Ignas", "456",), 
            Student("student3@vgtu.org", "Shyngys", "789"),
            Student("student4@vgtu.org", "Togzhan", "123"), 
            Student("student5@vgtu.org", "Ravan", "456",)]