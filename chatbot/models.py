from django.db import models
from django.contrib.auth.models import User

class ChatMessage(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    user_email=models.EmailField()
    chat_id = models.CharField(max_length=50)  # unique chat session
    input_text = models.TextField()
    output_text = models.TextField(blank=True, null=True)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.user.username} - {self.chat_id} - {self.created_at}"
