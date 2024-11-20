from django.db import models

# Create your models here.
class OrganizationSetting(models.Model):
    logo=models.FileField(upload_to='logo/')
    favicon=models.FileField(upload_to='favicon/',null=True,blank=True)
    email=models.EmailField()
    contact=models.CharField(max_length=15)
    address=models.CharField(max_length=100)
    locationUrl=models.URLField(max_length=1000, blank=True, null=True)
    facebookUrl=models.URLField(null=True,blank=True)
    youtubeUrl=models.URLField(null=True,blank=True)
    instagramUrl=models.URLField(null=True,blank=True)
    class Meta:
        ordering = ['-id']
    def __str__(self):
        return f'Organization Setting {self.id}'