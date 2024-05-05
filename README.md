# A Communication/Reservation Platform for Lecturer's Consultation hours 💻 
by Srinidhi Gopalraj

>This platform is deployed on [srinidhigopalraj-oop-coursework-comm.onrender.com](https://srinidhigopalraj-oop-coursework-comm.onrender.com), have a go ! test emails are given at the end of the report

## What inspired this idea 👀?
Lecturer's consultation hours are often not as transparent as they should be. Despite being able to access it through the university portal, Many students are still in the dark about these timings and have to ask the Lecturer repeatedly for their timings. This can get tiring for the lecturer aswell. This platform was built to adress those concerns and more. Through this platform, 
- students are able to :
    1. Create an event with their lecturer, Allowing them to be informed of their arrival.
    2. Add comments to this event, detailing any questions or concerns they may bring to the consultation hour 
    3. delete an event/consultation notification once their concerns are addressed
- Teachers are able to :
    1. See a list of all students arriving , aswell as their queries, allowing them to be more prepared.
    2. respond to their students comments, noting if their queries are valid and that theyre welcome to the consultation or explain     otherwise
    3. delete an event when it is no longer required.

At this moment I'd like to note that what I've built here is just a framework that can be extended to have greated capabilities. for example, the Observer pattern can use its notifiers to send emails or google calender invites instead of in-page notifications, without changing any of the core functionality. Thus I believe it is important to note that this project has a larger capability and potential through this framework and should be understood as such.

## How to use the program 💬?
As mentioned above, the program is currently deployed at [srinidhigopalraj-oop-coursework-comm.onrender.com](https://srinidhigopalraj-oop-coursework-comm.onrender.com). for the purpose of this project I've created 5 students and 6 teachers. 3 of Login details are as below. the others will be used as part of my presentation during the defense. 

Students:
- student3@vgtu.org, 789
- student4@vgtu.org, 123
- student5@vgtu.org, 456

Teachers:
- matlab@vgtu.org, 789
- electricalengg@vgtu.org, 456
- complab@vgtu.org, 789

(Tech stack used in this project : Flask, HTML, CSS)

## Attention to the functional requirements of this Project 🔦

### 1. Pillars of OOP:
#### a) Polymorphism -
Polymorphism is a concept that allows objects of different classes to be **treated as objects of a common superclass**, while giving each of them **different functionalities**. In essence, you are giving different classes the ability to operate on, as if they were of the same class, but giving each of them the **capability to have different** charecteristics and behaviours.

```
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
```

We're able to see that since classes Student and Teacher inherit from class User, we can apply the check passowrd method to both of them as if they were both of class User. The implentation in the main code is as below.
```
for person in Teachers:
            if person.email == user_email and person.check_password(passcode):
                found = True
                role = 'teacher'
                ...

        if not found:
            for person in Students:
                if person.email == user_email and person.check_password(passcode):
                    found = True
                    role = 'student'
                    ...
```
As I mentioned above, we can see how method overriding plays into polymorphism below with out implementation of class Teacher and subclasses LabTeacher and TheoryTeacher. We're able to call the same method on instances of both classes as if they were of the same class, but have given them different behaviour.
```
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
```
#### b) Abstraction - 
Abstraction is a concept that involves **hiding the complex implementation** details of a system while **exposing only the essential features** or functionalities. In my code, abstraction is presented through the use of a User superclass and the observer design pattern. The User class encapsulates data related to a user's email, name, and password, as well as the method to check password, therfore hides the internal representation of user data and how password verification is performed, which is a key aspect of abstraction. The same can be said for what the class CurrentUser does for the subclasses CurrentUserStudent and CurrentUserTeacher.
```
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
        ...
class Teacher(User):
        ...
class TheoryTeacher(Teacher):
        ...

class LabTeacher(Teacher):
`       ...

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
        self.notification  = None

    def get_name(self):
        return self.name
    
    def set_event(self, eve_no):
        self.event_no = eve_no
        return
    
    def get_event(self):
        return self.event_no
    
    def get_notification(self):
        return self.notification
    
    def set_notification(self, message):
        self.notification = message
        return
    
class CurrentUserStudent(CurrentUser, Student):
    ...

class CurrentUserTeacher(CurrentUser, Teacher):
    ...
```
Abstraction is also present in my use of the observer design pattern, which will be discussed in further sections.
 #### c) Inheritance - 
 Inheritance is a concept in that allows classes to **inherit attributes** and methods from other classes. It promotes **code reusability** and establishes relationships between classes based on a **hierarchical structure**. In my code, I have presented two types of inheritance.
 - Single level Inheritance - when Child classes Student and Teacher inherit attributes and methods from parent class user 
 ```
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

    ...
```
- multi-level inheritance and multiple inheritance - multi-level inheritance ocuurs when classes inherit from other classes that themselves have a hierarchical structure of inheritance. Here we can see that CurrentUserStudent and CurrentUserTeacher both inherit from not only Current user but also from classes Student and Teacher Respectively, both of which inherit from class User. multiple inheritance occurs when a class has mustiple parent classes, as we can see with CurrentUserStudent and CurrentUserTeacher. 

```
class User:
    ....
    
class Student(User):
    ...

class Teacher(User):
    ...

class CurrentUser:
    ...
    
class CurrentUserStudent(CurrentUser, Student):
    ...
class CurrentUserTeacher(CurrentUser, Teacher):
    ...
```
#### d) Encapsulation - 
Encapsulation is the concept of **bundling of data and methods** that operate on the data within a single unit or class. It **restricts direct access** to some of the object's components, providing **controlled access through methods**

- The user class encapsulates user data such as email, name, and password. Here, we've made the attribute password private, only allowing acces through the 'check_password' method.
``` 
class User:
    def __init__(self, email, name, password):
        self.email = email
        self.name = name
        self.__password = password

    def check_password(self, passcode):
        if passcode == self.__password:
            return True
        return False
```
- The Current user class class encapsulates data related to the current user session, such as email, name, event_no, and notification. Methods like get_name, set_event, get_event, get_notification, and set_notification provide controlled access to this data.
```
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
        self.notification  = None

    def get_name(self):
        return self.name
    
    def set_event(self, eve_no):
        self.event_no = eve_no
        return
    
    def get_event(self):
        return self.event_no
    
    def get_notification(self):
        return self.notification
    
    def set_notification(self, message):
        self.notification = message
        return

```
- The consultation hour class encapsulates data related to a consultation event, such as event number, student email, teacher email, start time, end time, and comments. These attributes are defined within the class and are accessed and manipulated through class methods. Access to the event data attributes is controlled through methods provided by the consultation_hour class, such as add_observer, notify_observers, add_comment, and time_until_event. These methods ensure that the internal representation of event data is hidden from external interference.
```
class consultation_hour:
    def __init__(self, eventno, student_email, teacher_email, start_time, end_time):
        self.eventno = eventno
        self.student_email = student_email
        self.teacher_email = teacher_email
        self.starttime = start_time
        self.endtime = end_time
        self.observers = []
        self.updates = []

    def add_observer(self, observer):
        ...

    def notify_observers(self, observer, event, email):
        ...
                
    @handle_file_errors
    @staticmethod
    def get_consultations_request(email):
        ...
    
    @handle_file_errors
    @staticmethod
    def remove_consultation_request(event, event_no, role):
        ...
        
    @handle_file_errors
    @staticmethod
    def add_consultation_request(event, curr_no, student_email, teacher_email, start, end):
        ...

    @handle_file_errors    
    def add_comment(self, event_no, user_email, comment):
        ...
    
    def print_comments(self):
        ...
    
    def time_until_event(self):
        ...
```

### 2. Design patterns implemented in this project 📝
My program implements four different design patterns : Singleton, Factory, Observer and Decorator.
#### a) Singleton -
The Singleton is a **creational design pattern** that ensures a class has **only one instance** and provides a **global point of access** to that instance. In my code, the Singleton pattern is implemented in the CurrentUser class. This is to save the details of the user in that particular session, and to be able to access it across the different flask route with greater ease. This makes sure that no-one can tamper with or change current user throughout runtime.
```
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
        self.notification  = None
```
#### b) Factory - 
The Factory Method is a **creational design pattern** that provides an **interface for creating objects** in a superclass, but allows subclasses to **alter the type of objects** that will be created. In my code, the Factory Method Pattern is implemented in the UserFactory class. Depending on the value of the role parameter, the factory method creates and returns an instance of either CurrentUserStudent or CurrentUserTeacher.
```
class UserFactory:
    @staticmethod
    def create_user(email, name, role):
        if role == 'student':
            return CurrentUserStudent(email, name, 0)
        elif role == 'teacher':
            return CurrentUserTeacher(email, name, 0)
        else:
            raise ValueError("Invalid user role")
```
#### c) Observer -
The Observer pattern is a **behavioral design pattern** where an object, called the subject, **maintains a list of dependents**, called observers, and **notifies them of any state changes**, usually by calling one of their methods. In my code, it is implemented through the abstract class Observer, observers EventNotification and EventDeletionNotification classes which are the concerte classes that implement the update method. THis is connected to the consultation_hour class where these observers are added and notified. 
> in my program, this pattern is only used to present notifications on the webpage. However, They can also be used to deploy google calender invitations or push notifications without changing the main framework, thus presenting the power of this pattern. 

```
class Observer(ABC):
    @abstractmethod
    def update(self, event):
        pass

class EventNotification(Observer):

    def update(self, event, email):
        time_left = event.time_until_event()
        time_left_hours = round(time_left / 60, 2)
        return (f"Notification: You have {time_left_hours} hours until the consultation starts.")

class EventDeletionNotification(Observer):

    def update(self, event, email):
        return(f"Notification: Consultation with {email} deleted.")

class consultation_hour:
    def __init__(self, eventno, student_email, teacher_email, start_time, end_time):
        ...

    def add_observer(self, observer):
        ...

    def notify_observers(self, observer, event, email):
        ...
    ...

```
#### d) Decorator - 
The Decorator pattern is a **structural design pattern** that allows behavior to be added to individual objects **dynamically, without affecting the behavior** of other objects from the same class. It's achieved by creating a set of decorator classes that are used to wrap concrete components. In my code, it is implemented to wrap fuctions which require file handling with the relevent file checking code, instead of writing code for this verification into each and every function. One example of its implementation is shown  completely and the rest are omitted from the code block below. 
```
def handle_file_errors(func):
    def wrapper(*args, **kwargs):
       try:
           return func(*args, **kwargs)
       except FileNotFoundError:
           print("File not found.")
           return []
       except Exception as e:
           print(f"Error: {e}")
           return []
    return wrapper

@handle_file_errors
def consultation_no():
    with open('events.txt', "r") as f:
        num_events = 0
        for line in f:
            event_data = line.strip().split()
            if len(event_data) != 5:
                print("Invalid format found on file")
                continue
            num_events = int(event_data[0]) + 1
    return num_events


class consultation_hour:
    ...

    @handle_file_errors
    @staticmethod
    def get_consultations_request(email):
        ...
    
    @handle_file_errors
    @staticmethod
    def remove_consultation_request(event, event_no, role):
        ...
        
    @handle_file_errors
    @staticmethod
    def add_consultation_request(event, curr_no, student_email, teacher_email, start, end):
        ...

    @handle_file_errors    
    def add_comment(self, event_no, user_email, comment):
        ...
    
    ...
```
### 3. File handling functionalities
My code **Includes the required read/write/append functionalities** required of this project.The consultation_hour class and its methods, such as get_consultations_request, remove_consultation_request, and add_consultation_request, read from and write to files **'events.txt' and 'comments.txt'**. These methods handle consultation events and comments associated with them, reading data from files to retrieve existing events and writing data to files to **add, remove, or modify events and comments**. The handle_file_errors decorator is used to handle file-related errors in methods such as consultation_no and various methods in the consultation_hour class.

### 4. Unit tests 
Unit testing is a software testing approach where individual units or components of a program are **tested in isolation** to ensure they behave as expected. It helps **verify that each part** of the software performs correctly and meets its design specifications. In my code, unit testing is implemented using the unittest module, which provides a framework for writing and executing test cases. 
```
class ConsultationTestCase(unittest.TestCase):
    def setUp(self):
        self.student_email = 'student1@vgtu.org'
        self.teacher_email = 'english@vgtu.org'
        self.start_time = time(10, 0)  
        self.end_time = time(12, 0)

    def test_get_consultations_request(self):
        student_consultations = consultation_hour.get_consultations_request(self.student_email)
        self.assertTrue(student_consultations)
        self.assertTrue(all(isinstance(event, consultation_hour) for event in student_consultations))
        teacher_consultations = consultation_hour.get_consultations_request(self.teacher_email)
        self.assertTrue(teacher_consultations) 
        self.assertTrue(all(isinstance(event, consultation_hour) for event in teacher_consultations)) 

    def test_add_consultation_request(self):
        event_count_before = consultation_no() 
        event = consultation_hour(1, self.student_email, self.teacher_email, self.start_time, self.end_time)

        consultation_hour.add_consultation_request(event, event_count_before, self.student_email, self.teacher_email, self.start_time.strftime("%H:%M"), self.end_time.strftime("%H:%M"))
        event_count_after = consultation_no()  
        self.assertEqual(event_count_after, event_count_before + 1)


    def test_remove_consultation_request(self):
        event = consultation_hour(7000, self.student_email, self.teacher_email, self.start_time, self.end_time)
        consultation_hour.remove_consultation_request(event, 7000, 'student') 
        self.assertNotIn(event, consultation_hour.get_consultations_request(self.student_email))

if __name__ == '__main__':
    unittest.main()
```
Here we have the test class ConsultationTestCase which inherits from unittest.testcase. Each test case method within this class represents a specific test scenario.The setUp method is used to set up common test data before each test case is executed, in this case, the main details of the event to be created. Assertions are used within the test methods to check whether the actual output of the code matches the expected behavior. self.assertTrue checks if the result is of boolean value True. self.assertEqual checks if the results of both parameters are equal. self.assertNotIn checks if the first parameter is not a part of or cannot be considered a subset of the second parameter. 

## The Results of this program 💡
From this project and developing this program, I've learnt to :

- Build a **Communication/managagemen**t system from scratch
- understand how to choose **design patterns** based on the requirements of a program
- build a unit testing system to **debug more efficiently**
- develop and **deploy a Flask Application** and to better use CSS for HTML

Challenges I've faced during this Project:

- Struggled with my initial idea to use a sqllite database system, and decided that filehandling would be more suitable for my program.
- Figuring out how to dynamically update the webpage content based on user interactions, which I then solved using my implemetation of  a singleton pattern
- It took some time to learn how to clone and deploy my project externally, and how to dynamically update the requirements file needed for the deployment

## What has my work achieved ? and the future prospects of my project 🔮
As mentioned before, this platform was built on the **idea of transparency and open communication between students and lecturers** about the **happenings of their consultation hours**. These hours serve as a great opportunity for students to **deepen their understanding** of the subject and understand it better from the professors perspective and anecdotes in a way thats different to traditional lectures. Hence with more communication and transparency about consultation hours,**we can raise footfall**, Increasing the overall level general understanding of subjects, for more students than before. 

With the possibility to write to your lecturer about your reason of arrival, the Teacher is able to : **Be prepared** for your questions, or Inform you that your queries will be resolved in another fashion, **saving time** for both parties - as a contrast to the current situation of constant interruptions during lectures of the whereabouts and reasons for attending consultation hours. 

This platform is **the first step** towards this cause. 

As for the future, I can see this application being a **positive addition to the Vilnius Tech family of services for students**, mimicing the convinience that the work-room reservation platform has given us. As mentioned above, the application can be updated to have **more capabilites**such as sending google/outlook calender invites, setting reminders and much more. 

In the case where integration into Vilnius Tech services is not possible, this Idea can be developed to be a **standalone platform open to all universitities**, where teachers can sign up to **streamline their reservations** and for the convinience of being able to see all that are arriving and why, giving them a chance to see the people and their purpose of visit, allowing them to be **more productive**. 