from flask import Flask, render_template, request, session, redirect, flash
from datetime import time
from eventhandling import consultation_hour, consultation_no
from userhandling import UserFactory, CurrentUserTeacher, CurrentUserStudent, Student, TheoryTeacher, LabTeacher

app = Flask(__name__)
app.config['SECRET_KEY'] = 'newtonsapple'
app.config['PERMANENT_SESSION_LIFETIME'] = 3600

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

@app.route("/", methods=['GET', 'POST'])
def index():
    if request.method == 'POST':
        try:
            user_email = request.form['identity']
            passcode = request.form['password']
        except KeyError:
            flash("Email and password are required.", "error")
            return redirect('/')

        found = False
        for person in Teachers:
            if person.email == user_email and person.check_password(passcode):
                found = True
                role = 'teacher'
                name = person.name
                session['email'] = user_email
                break

        if not found:
            for person in Students:
                if person.email == user_email and person.check_password(passcode):
                    found = True
                    role = 'student'
                    name = person.name
                    session['email'] = user_email
                    break
        
        if found:
            current_person = UserFactory.create_user(user_email, name, role )
            session['email'] = user_email
            return redirect(f'/{role}dashboard')

        flash("Incorrect email or password. Please try again.", "error")
        return redirect('/')

    return render_template('index.html')


@app.route("/studentdashboard", methods=['GET', 'POST'])
def dashboard():
    current_person = CurrentUserStudent._instance
    if current_person is None or current_person.email != session['email']:
        flash("User not found.", "error")
        return redirect('/')
    current_user = current_person
    current_user_events = current_user.currentevents 


    if request.method == 'POST':
        action = request.form.get('action')
        if action == 'create_event':
            teacher_email = request.form['teacher_email']
            for teach in Teachers:
                if teach.email == teacher_email:
                    startime = teach.start_time
                    endtime = teach.end_time
                    break
                
            current_eventno = consultation_no() + 1
            new_event = consultation_hour(current_eventno, current_user.email, teacher_email, startime, endtime)
            consultation_hour.add_consultation_request(current_eventno, current_user.email, teacher_email, current_user.format_time(startime), current_user.format_time(endtime))
            current_user.currentevents.append(new_event)
            print("event appended from app side")
            return redirect("/studentdashboard")
        elif action == 'delete_event':
            eve_no = request.form['event_no']
            for event in current_user_events:
                if eve_no == event.eventno:
                    current_user.currentevents.remove(event)
                    consultation_hour.remove_consultation_request(eve_no)
                    return redirect("/studentdashboard")
        elif action == 'add_comment':
            eve_no = request.form['event_no']
            current_user.set_event(int(eve_no))
            if 'comment' in request.form:
                print("there was a comment")
                comment = request.form['comment']
                for event in current_user_events:
                    print( "my event no", event.eventno)
                    print('received eve no', eve_no)
                    if int(event.eventno) == int(eve_no):  
                        print("found event in my events")
                        event.add_comment(eve_no, current_user.email, comment)
                        print("comment added from app side")
                        return redirect("/studentdashboard")
        elif action == 'logout':
            session.pop('email', None)
            return redirect("/logout")
    return render_template('studentdashboard.html', current_user=current_user, teachers=Teachers)

@app.route("/teacherdashboard", methods=['GET', 'POST'])
def teachdashboard():
    current_person = CurrentUserTeacher._instance
    if current_person is None or current_person.email != session['email']:
        flash("User not found.", "error")
        return redirect('/')
    current_user = current_person
    current_user_events = current_user.currentevents

    if request.method == 'POST':
        action = request.form.get('action') 
        if action == 'delete_event':
            eve_no = request.form['event_no']
            for event in current_user_events:
                if eve_no == event.eventno:
                    current_user.currentevents.remove(event)
                    consultation_hour.remove_consultation_request(eve_no)
                    return redirect("/teacherdashboard")
        elif action == 'add_comment':
            eve_no = request.form['event_no']
            current_user.set_event(int(eve_no))
            print("comment button pressed")
            if 'comment' in request.form:
                print("there was a comment from teacher")
                comment = request.form['comment']
                for event in current_user_events:
                    print( "my event no", event.eventno)
                    print('received eve no', eve_no)
                    if int(event.eventno) == int(eve_no):  
                        print("found event in my events")
                        event.add_comment(eve_no, current_user.email, comment)
                        print("comment added from app side")
                        return redirect("/teacherdashboard")
        elif action == 'logout':
            session.pop('email', None)
            return redirect("/logout")
    return render_template('teacherdashboard.html', current_user=current_user, students=Students)

@app.route("/logout", methods=['GET', 'POST'])
def loggingout():
    if request.method == 'POST':
        action = request.form.get('action') 
        if action == 'login':
            return redirect('/')
    return render_template("logout.html")

if __name__ == "__main__":
    app.config["TEMPLATES_AUTO_RELOAD"] = True
    app.run(debug=True)


