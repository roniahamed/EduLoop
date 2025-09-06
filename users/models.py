from django.db import models
import string, random

TOKEN_LENGTH = 8 

def generate_unique_token():

    while True:
        possible_chars =  string.digits
        new_key = ''.join(random.choices(possible_chars, k=TOKEN_LENGTH))
        if not AccessToken.objects.filter(key=new_key).exists():
            return new_key


class AccessToken(models.Model):
    key = models.CharField(max_length=12, primary_key=True, default=generate_unique_token, editable=False)
    description = models.CharField(max_length=100, help_text="Für wen ist dieses Token? (z. B.: Klasse 10, Batch-A)", blank=True, null=True)
    is_active = models.BooleanField(default=True, help_text="Ist dieses Token derzeit aktiv?")
    created_at = models.DateTimeField(auto_now_add=True)
    def __str__(self):
        return f"{self.description} - {self.key}"
    
