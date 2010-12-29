from django.db import models
from django.contrib.auth.models import User


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
    tagline = models.TextField()

class UserProfile(models.Model):
    USER_TYPES = (
        ('local', 'Local user'),
        ('alias', 'Alias'),
        ('catchall', 'Catchall'),
        ('fail', 'Blackholed address'),
        ('pipe', 'System pipe')
    )
    user = models.ForeignKey(User, unique=True)
    domain = models.ForeignKey(Domain)
    localpart = models.CharField(max_length=192)
    uid = models.IntegerField()
    gid = models.IntegerField()
    maildir = models.CharField(max_length=255)
    pipe_cmd = models.TextField()
    type = models.CharField(max_length=8, choices=USER_TYPES)
    antivirus_enabled = models.BooleanField()
    forwarding_enabled = models.BooleanField()
    forward_unseen = models.BooleanField()
    forward_address = models.TextField()
    spamassassin_enabled = models.BooleanField()
    vacation_enabled = models.BooleanField()
    vacation_message = models.TextField()
    maxmsgsize = models.IntegerField()
    sa_tag = models.IntegerField()
    sa_refuse = models.IntegerField()
    tagline = models.TextField()
