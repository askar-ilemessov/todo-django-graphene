from django.db import models

class Task(models.Model):
    class TaskStatus(models.TextChoices):
        LATER = 'later'
        DOING = 'doing'
        DONE = 'done'
    task_title = models.CharField('Task Name', max_length=200)
    task_text = models.TextField('Description')
    task_status = models.TextField(blank=False, choices=TaskStatus.choices, max_length=8)

    def __str__(self):
        return self.task_title

