from django.db import models
from django.contrib.auth.models import User

class Note(models.Model):
    title = models.CharField(max_length=100)
    content = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)
    author = models.ForeignKey(User, on_delete=models.CASCADE, related_name="notes")

    def __str__(self):
        return self.title

class Course(models.Model):
    title = models.CharField(max_length=100)
    description = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)
    students = models.ManyToManyField(to=User, through="Student", related_name="courses")  

    def __str__(self):
        return self.title


class Student(models.Model):
    user = models.ForeignKey(to=User, on_delete=models.CASCADE)
    course = models.ForeignKey(to=Course, on_delete=models.CASCADE)  
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        # unique_together = ['user', 'course']
        constraints = [
            models.UniqueConstraint(fields=['user', 'course'], name='unique_student_course')
        ]

    def __str__(self):
        return f"{self.user.username} in {self.course.title}"


