from datetime import datetime
from abc import ABC, abstractmethod
from flask_socketio import SocketIO, emit

class Observer(ABC):
    @abstractmethod
    def update(self, event):
        pass

class EventNotification(Observer):
    def update(self, event):
        time_left = event.time_until_event()
        print(f"Notification: You have {time_left} minutes until the consultation starts.")
        socketio.emit('notification', {'message': f'You have {time_left} minutes until the consultation starts.'})
        return

class EventDeletionNotification(Observer):
    def update(self, event):
        print(f"Notification: Consultation with {event.teacher_email} deleted.")
        socketio.emit('notification', {'message': f'Consultation with {event.teacher_email} deleted.'})
        return

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
                print("Invalid format found while checking event no")
                continue
            num_events = int(event_data[0]) + 1
    return num_events


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
        self.observers.append(observer)

    def remove_observer(self, observer):
        self.observers.remove(observer)

    def notify_observers(self):
        for observer in self.observers:
            observer.update(self)
    
    @handle_file_errors
    @staticmethod
    def get_consultations_request(email):
        all_user_events = []
        with open('events.txt', 'r') as f:
            for line in f:
                current_event_data = line.strip().split()
                if len(current_event_data) < 5:
                    print("issue with current event format", current_event_data)
                    continue
                if current_event_data[1] == email or current_event_data[2] == email:
                    current_event = consultation_hour(current_event_data[0], current_event_data[1], current_event_data[2], current_event_data[3], current_event_data[4])
                    all_user_events.append(current_event)
        with open('comments.txt', 'r') as f:
            for line in f:
                current_comment_data = line.strip().split()
                if len(current_comment_data) < 4:
                    print("issue with current event format", current_comment_data)
                    continue
                event_number = current_comment_data[0]
                date = current_comment_data[1]
                email = current_comment_data[2]
                message = " ".join(current_comment_data[3:])
                for event in all_user_events:
                    if event.eventno == current_comment_data[0]:
                        event.updates.append((date, email, message))
        return all_user_events
    
    @handle_file_errors
    @staticmethod
    def remove_consultation_request(event_no):
        with open('events.txt', "r") as f:
            events = f.readlines()
            updated_events = [event for event in events if not event.startswith(event_no)]
        with open('events.txt', "w") as f:
            f.writelines(updated_events)
        with open('comments.txt', "r") as f:
            comments = f.readlines()
            updated_events = [comment for comment in comments if not comment.startswith(event_no)]
        with open('comments.txt', "w") as f:
            f.writelines(updated_events)
            return
        
    @handle_file_errors
    @staticmethod
    def add_consultation_request(curr_no, student_email, teacher_email, start, end):
        with open('events.txt', "a") as f:
            f.write(f"{curr_no} {student_email} {teacher_email} {start} {end}\n")
            print("Event added successfully.")
            notification = EventNotification()
            consultation_hour.add_observer(notification)
            return 

    @handle_file_errors    
    def add_comment(self, event_no, user_email, comment):
        timestamp = datetime.now().strftime("%Y-%m-%d")
        self.updates.append((timestamp, user_email, comment))
        with open('comments.txt', 'a') as f:
            f.write(f"{event_no} {timestamp} {user_email} {comment}\n")
            print("comment printed from event class side")
        return
    
    def print_comments(self):
        comments = ""
        for comm in self.updates:
            comments += f"{comm[0]} {comm[1]}: {comm[2]}"
        return comments
    
    def time_until_event(self):
        current_time = datetime.now().time()
        time_difference = (datetime.combine(datetime.today(), self.starttime) - datetime.combine(datetime.today(), current_time)).total_seconds() // 60
        return max(0, time_difference)
    
    @classmethod
    def notify_observers(cls):
        for observer in cls.observers:
            observer.update(cls)
