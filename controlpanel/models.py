from django.db import models
from django.contrib.auth.models import User
from django.conf import settings


class Domain(models.Model):
    """The domain model"""
    DOMAIN_TYPES = (
        ('relay', 'Relay'),
        ('local', 'Local')
    )
    domain = models.CharField(max_length=128)
    maildir = models.TextField(default=settings.VEXIM_MAILHOME)
    uid = models.IntegerField(default=settings.VEXIM_UID)
    gid = models.IntegerField(default=settings.VEXIM_GID)
    max_accounts = models.IntegerField(default=0)
    type = models.CharField(max_length=5, choices=DOMAIN_TYPES)
    avscan = models.BooleanField(default=True)
    blocklists = models.BooleanField(default=True)
    complexpass = models.BooleanField(default=True)
    enabled = models.BooleanField(default=True)
    mailinglists = models.BooleanField(default=True)
    maxmsgsize = models.IntegerField(default=settings.VEXIM_MAXMSGSIZE)
    pipe = models.BooleanField(default=True)
    spamassassin = models.BooleanField(default=True)
    sa_tag = models.IntegerField(default=settings.VEXIM_SA_TAG)
    sa_refuse = models.IntegerField(default=settings.VEXIM_SA_REFUSE)
    tagline = models.TextField(blank=True)

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
