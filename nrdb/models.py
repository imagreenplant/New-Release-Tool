from django.db import models
import datetime

class Release(models.Model):
    release_id = models.PositiveIntegerField()
    description = models.CharField(max_length=400, blank=True, default='')
    batch = models.ManyToManyField('Batch')
    class Meta:
        verbose_name_plural = 'releases'
    
    def __unicode__(self):
        return self.release_id

class Batch(models.Model):
    name = models.CharField(max_length=100, blank=True, default='')
    submitter = models.CharField(max_length=40, blank=True, default='')
    last_modified = models.DateTimeField(auto_now=True, default=datetime.datetime.now())
    class Meta:
        verbose_name_plural = 'batches'
        
    def __unicode__(self):
        return self.id
    
class Idea(models.Model):
    name = models.CharField(max_length=20000, blank=True, default='')
    
    class Meta:
        verbose_name_plural = 'ideas'
        
    def __unicode__(self):
        return self.id