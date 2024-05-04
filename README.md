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
 Inheritance is a concept in that allows classes to inherit attributes and methods from other classes. It promotes code reusability and establishes relationships between classes based on a hierarchical structure. In my code, I have presented two types of inheritance.
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
Encapsulation is the concept of bundling of data and methods that operate on the data within a single unit or class. It restricts direct access to some of the object's components, providing controlled access through methods

***TO BE CONTINUED***