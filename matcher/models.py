from django.db import models
from django.utils import timezone

class JobDescription(models.Model):
    title = models.CharField(max_length=200, blank=True)
    content = models.TextField()  # renamed from description_text
    uploaded_at = models.DateTimeField(auto_now_add=True)
    def __str__(self):
        return self.title or f"JD {self.id}"



class Resume(models.Model):
    file = models.FileField(upload_to='resumes/')
    content = models.TextField()
    email = models.EmailField()
    score = models.FloatField()
    job_description = models.ForeignKey(JobDescription, on_delete=models.CASCADE)
    email_sent = models.BooleanField(default=False)  # prevent multiple emails

    def __str__(self):
        return self.file.name
