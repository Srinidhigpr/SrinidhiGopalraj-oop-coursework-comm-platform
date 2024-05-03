import unittest
from eventhandling import consultation_hour, consultation_no

class ConsultationTestCase(unittest.TestCase):
    def setUp(self):
        self.student_email = 'student1@vgtu.org'
        self.teacher_email = 'english@vgtu.org'
        self.start_time = '10:00'
        self.end_time = '11:00'

    def test_get_consultations_request(self):
        student_consultations = consultation_hour.get_consultations_request(self.student_email)
        self.assertTrue(student_consultations)
        self.assertTrue(all(isinstance(event, consultation_hour) for event in student_consultations))
        teacher_consultations = consultation_hour.get_consultations_request(self.teacher_email)
        self.assertTrue(teacher_consultations) 
        self.assertTrue(all(isinstance(event, consultation_hour) for event in teacher_consultations)) 


    def test_remove_consultation_request(self):
        event = consultation_hour(1, self.student_email, self.teacher_email, self.start_time, self.end_time)
        consultation_hour.remove_consultation_request(event, 1, 'student') 
        self.assertNotIn(event, consultation_hour.get_consultations_request(self.student_email))

if __name__ == '__main__':
    unittest.main()
