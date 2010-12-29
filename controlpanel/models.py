from django.db import models

class Domain(models.Model):
    """The domain model"""
    DOMAIN_TYPES = (
        ('relay', 'Relay'),
        ('local', 'Local')
    )
    domain = models.CharField(max_length=128)
    maildir = models.TextField()
    uid = models.IntegerField()
    gid = models.IntegerField()
    max_accounts = models.IntegerField()
    type = models.CharField(max_length=5, choices=DOMAIN_TYPES)
    avscan = models.BooleanField()
    blocklists = models.BooleanField()
    complexpass = models.BooleanField()
    enabled = models.BooleanField()
    mailinglists = models.BooleanField()
    maxmsgsize = models.IntegerField()
    pipe = models.BooleanField()
    spamassassin = models.BooleanField()
    sa_tag = models.IntegerField()
    sa_refuse = models.IntegerField()
