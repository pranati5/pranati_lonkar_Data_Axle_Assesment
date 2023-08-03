# Create a test module, say test.py, to test the business logic:

from datetime import date, timedelta
from django.test import TestCase
from .models import Employee, Event, EmailTemplate
from .event_email_logic import send_event_emails

class EventEmailTestCase(TestCase):
    def setUp(self):
        self.employee = Employee.objects.create(
            employee_name='John Doe',
            email='john.doe@example.com',
            birth_date=date.today(),
            work_anniversary_date=date.today()
        )

        self.birthday_template = EmailTemplate.objects.create(
            event_type='birthday',
            subject='Happy Birthday!',
            body='Happy birthday, {employee_name}!'
        )

        self.work_anniversary_template = EmailTemplate.objects.create(
            event_type='work_anniversary',
            subject='Work Anniversary!',
            body='Congratulations on your work anniversary, {employee_name}!'
        )

    def test_send_event_emails(self):
        # Set up events for today (birthday and work anniversary)
        Event.objects.create(employee=self.employee, event_type='birthday', event_date=date.today())
        Event.objects.create(employee=self.employee, event_type='work_anniversary', event_date=date.today())

        # Run the email sending process
        send_event_emails()

        # Check if the emails were sent successfully
        self.assertIn('Email sent successfully', self._get_log_output())

    def test_send_event_emails_no_events(self):
        # No events for today
        Event.objects.create(employee=self.employee, event_type='work_anniversary', event_date=date.today() + timedelta(days=1))

        # Run the email sending process
        send_event_emails()

        # Check if the process logged that there are no events scheduled
        self.assertIn('No events scheduled', self._get_log_output())

    def test_send_event_emails_missing_template(self):
        # Set up an event with missing email template
        Event.objects.create(employee=self.employee, event_type='work_anniversary', event_date=date.today())

        # Run the email sending process
        send_event_emails()

        # Check if the process logged an error for the missing template
        self.assertIn('No email template found', self._get_log_output())

    def _get_log_output(self):
        return '\n'.join([record.message for record in self._get_log_records()])

    def _get_log_records(self):
        logger = logging.getLogger('django')
        return logger.handlers[0].records if logger.handlers else []
