import unittest
from eventhandling import consultation_hour, consultation_no
from datetime import time
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
