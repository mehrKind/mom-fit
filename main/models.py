from django.db import models

# Create your models here.
class APKVersion(models.Model):
    version_code = models.IntegerField()
    version_name = models.CharField(max_length=50)
    release_date = models.DateField(auto_now_add=True)
    download_url = models.URLField()

    def __str__(self):
        return f"Version {self.version_name} ({self.version_code})"