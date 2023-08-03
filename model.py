
# Assuming you already have models for Event and EmailTemplate, define them in the models.py file:

from django.db import models

class Event(models.Model):
    EVENT_TYPES = (
        ('birthday', 'Birthday'),
        ('work_anniversary', 'Work Anniversary'),
    )

    employee = models.ForeignKey('Employee', on_delete=models.CASCADE)
    event_type = models.CharField(choices=EVENT_TYPES, max_length=20)
    event_date = models.DateField()

class EmailTemplate(models.Model):
    event_type = models.CharField(choices=Event.EVENT_TYPES, max_length=20)
    subject = models.CharField(max_length=100)
    body = models.TextField()
