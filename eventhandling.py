from datetime import datetime, timedelta
from abc import ABC, abstractmethod

class Observer(ABC):
    @abstractmethod
    def update(self, event):
        pass

class EventNotification(Observer):

    def update(self, event):
        time_left = event.time_until_event()
        time_left_hours = round(time_left / 60, 2)
        print("in event create observer")
        return (f"Notification: You have {time_left_hours} hours until the consultation starts.")

class EventDeletionNotification(Observer):

    def update(self, event):
        print("in event delete observer")
        return(f"Notification: Consultation with {event.teacher_email} deleted.")


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

    def notify_observers(self, observer, event):
        print("in notify observers")
        for ob in self.observers:
            if type(ob) == type(observer):
                print("found observer")
                return ob.update(event)
        return "Observer not found "
                
    
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
                    print("got an event for user")
                    current_event = consultation_hour(current_event_data[0], current_event_data[1], current_event_data[2], current_event_data[3], current_event_data[4])
                    all_user_events.append(current_event)
                    current_event.add_observer(EventNotification())
                    current_event.add_observer(EventDeletionNotification())
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
    def remove_consultation_request(event, event_no):
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
        
            return event.notify_observers(EventDeletionNotification())
        
    @handle_file_errors
    @staticmethod
    def add_consultation_request(event, curr_no, student_email, teacher_email, start, end):
        with open('events.txt', "a") as f:
            f.write(f"{curr_no} {student_email} {teacher_email} {start} {end}\n")
            print("Event added successfully.")
            event.add_observer(EventNotification())
            event.add_observer(EventDeletionNotification())
            return event.notify_observers(EventNotification(), event)

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
        time_obj_str = self.starttime.strftime("%H:%M")  # Convert to string
        time_obj = datetime.strptime(time_obj_str, "%H:%M").time()
        if current_time > time_obj:
            next_day = datetime.now() + timedelta(days=1)
            time_obj = datetime.combine(next_day, time_obj).time()
    
        current_datetime = datetime.now()
        event_datetime = datetime.combine(datetime.today(), time_obj)
        if event_datetime < current_datetime:
            event_datetime += timedelta(days=1)
        time_difference_seconds = (event_datetime - current_datetime).total_seconds()
        time_difference_minutes = max(0, time_difference_seconds // 60)

        return time_difference_minutes

