from django.db import models

class Referee(models.Model):
    name = models.CharField(max_length=100)
    email = models.EmailField(max_length=254, unique=True)
    phone = models.CharField(max_length=11, blank=True)
    sport = models.CharField(max_length=50)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def save(self, *args, **kwargs):
        # Automatically capitalize sport before saving
        if self.sport:
            self.sport = self.sport.capitalize()
        super().save(*args, **kwargs)

    def __str__(self):
        return f"{self.name} ({self.sport})"
