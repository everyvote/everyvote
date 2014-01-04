from django.db import models
from django.contrib.auth.models import User

# Create your models here.

class UserProfile(models.Model):
    user = models.OneToOneField(User, unique=True)
    first_name = models.CharField(max_length=25, blank=True)
    middle_name = models.CharField(max_length=25, blank=True)
    last_name = models.CharField(max_length=25, blank=True)
    public_email = models.EmailField(blank=True)
    # profile_picture = ResizedImageField(upload_to=get_upload_file_name, blank=True, max_width=250, max_height=250)
    about = models.TextField(blank=True)
    year_in_school = models.CharField(max_length=25, blank=True)
    major = models.CharField(max_length=75, blank=True)
    twitter_handle = models.CharField(max_length=20, blank=True)
    facebook_page = models.URLField(blank=True)
    linkedin_page = models.URLField(blank=True)
    personal_homepage = models.URLField(blank=True)
    
    class Meta:
        ordering = ['user']
    
    def __unicode__(self):
        return unicode(self.user)

# I don't understand how this part below works, I took it from the previous EveryVote code...I think it is needed to connect Django's native User class to our expanded UserProfile class?
def create_profile(sender, instance, created, **kwargs):
    if created:
        profile, created = UserProfile.objects.get_or_create(user=instance)

from django.db.models.signals import post_save
post_save.connect(create_profile, sender=User)

class Constituency(models.Model):
    name = models.CharField(max_length=100)
    about = models.TextField(blank=True)
    moderators = models.ManyToManyField(UserProfile, related_name='moderator', blank=True)
    # profile_picture = ResizedImageField(upload_to=get_upload_file_name, blank=True, max_width=250, max_height=250)
    blocked_users = models.ManyToManyField(UserProfile, related_name='blocked_users', blank=True)
    public_email = models.EmailField(blank=True)
    twitter_handle = models.CharField(max_length=20, blank=True)
    facebook_page = models.URLField(blank=True)
    linkedin_page = models.URLField(blank=True)
    personal_homepage = models.URLField(blank=True)
    
    class Meta:
        ordering = ['name']
    
    def __unicode__(self):
        return unicode(self.name)
    
    def get_absolute_url(self):
        return reverse('constituency_detail', kwargs={'pk': str(self.id)})

class Office(models.Model):
    constituency = models.ForeignKey(Constituency)
    name = models.CharField(max_length=100)
    about = models.TextField(blank=True)
    
    class Meta:
        ordering = ['constituency']
    
    def __unicode__(self):
        return u'%s - %s' % (self.constituency.name, self.name)

    def get_absolute_url(self):
        return reverse('office_detail', kwargs={'pk': str(self.id)})

class Election(models.Model):
    constituency = models.ForeignKey(Constituency)
    name = models.CharField(max_length=100)
    about = models.TextField(blank=True)
    first_day_of_voting = models.DateField()
    last_day_of_voting = models.DateField(blank=True)
    offices = models.ManyToManyField(Office, blank=True)
    voting_link = models.URLField(blank=True)
    
    class Meta:
        ordering = ['name']
    
    def get_absolute_url(self):
        return reverse('election_detail', kwargs={'pk': str(self.id)})
    
    def __unicode__(self):
        return u'%s - %s' % (self.constituency.name, self.name)

class Session(models.Model):
    constituency = models.ForeignKey(Constituency)
    name = models.CharField(max_length=100)
    first_day_of_session = models.DateField()
    last_day_of_session = models.DateField()
    offices = models.ManyToManyField(Office, blank=True)
    
    class Meta:
        ordering = ['name']
    
    def __unicode__(self):
        return u'%s - Session: %s to %s' % (self.constituency.name, self.first_day_of_session, self.last_day_of_session)
    
class Candidate(models.Model):
    user = models.ForeignKey(UserProfile)
    election = models.ForeignKey(Election)
    office = models.ForeignKey(Office)
    party = models.CharField(max_length=50, blank=True)
    goals = models.TextField(blank=True)
    experience = models.TextField(blank=True)
    about = models.TextField(blank=True)
    is_approved = models.NullBooleanField()
    
    class Meta:
        ordering = ['?']
    
    def __unicode__(self):
        return u'%s %s %s for %s in the %s' % (self.userprofile.first_name, self.userprofile.middle_name, self.userprofile.last_name, self.office.name, self.election)
    
    def get_absolute_url(self):
        return reverse('candidate_detail', kwargs={'pk': str(self.id)})

class Officer(models.Model):
    user = models.ForeignKey(UserProfile)
    session = models.ForeignKey(Session)
    office = models.ForeignKey(Office)
    party = models.CharField(max_length=50, blank=True)

# class Stance(models.Model):

# class Comment(models.Model):
#    user = models.ForeignKey(UserProfile)
#    answer = models.ForeignKey(Answer)
#    stance = models.ForeignKey(Stance)
#    comment = models.TextField()

# class Answer(models.Model):
#    user = models.ForeignKey(UserProfile)
#    stance = models.ForeignKey(Stance)
#    answer = models.TextField()
#    # how do we activate yes_or_no? if the Question has yes_or_no=True, how do we activate Stance?
    
# class Question(models.Model):
#    question = models.TextField()
#    user = models.ForeignKey(UserProfile)
#    answers = models.ManyToManyField(Answer)
#    yes_or_no = models.BooleanField()
#    session = models.ForeignKey(Session)

# class Announcement(models.Model):
#    announcement = models.TextField()
#    session = models.ForeignKey(Session)
#    user = models.ForeignKey(UserProfile)

# class Event(models.Model):
#    name = models.CharField(max_length=100)
#    start_time = models.DateField()
#    end_time = models.DateField()
#    location = models.TextField()
#    details = models.TextField()
#    session = models.ForeignKey(Session)

# class Vote(models.Model):