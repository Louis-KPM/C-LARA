from django.db import models
from django.urls import reverse

from .constants import TEXT_TYPE_CHOICES, SUPPORTED_LANGUAGES, SUPPORTED_LANGUAGES_AND_DEFAULT

from django.contrib.auth.models import User, Group, Permission 
from django.db import models
 
class UserProfile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    bio = models.TextField(blank=True, null=True)
    location = models.CharField(max_length=100, blank=True, null=True)
    birth_date = models.DateField(blank=True, null=True)
    profile_picture = models.ImageField(upload_to='profile_pictures/', blank=True, null=True)
    is_admin = models.BooleanField(default=False)
    is_moderator = models.BooleanField(default=False)
    credit = models.DecimalField(max_digits=10, decimal_places=2, default=0.0)

    def is_language_master(self):
        return self.user.language_master_set.exists()

class UserConfiguration(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    gpt_model = models.CharField(max_length=50, default='gpt-4')
    max_annotation_words = models.IntegerField(default=100)

class LanguageMaster(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='language_master_set')
    language = models.CharField(max_length=50, choices=SUPPORTED_LANGUAGES_AND_DEFAULT)

    class Meta:
        unique_together = ['user', 'language']

class CLARAProject(models.Model):
    title = models.CharField(max_length=200)
    internal_id = models.CharField(max_length=200)
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    l2 = models.CharField(max_length=50, choices=SUPPORTED_LANGUAGES)
    l1 = models.CharField(max_length=50, choices=SUPPORTED_LANGUAGES)
    
class ProjectPermissions(models.Model):
    ROLE_CHOICES = [
        ('OWNER', 'Owner'),
        ('ANNOTATOR', 'Annotator'),
        ('VIEWER', 'Viewer'),
        # More roles as needed...
    ]
    
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    project = models.ForeignKey(CLARAProject, on_delete=models.CASCADE)
    role = models.CharField(max_length=10, choices=ROLE_CHOICES)

    class Meta:
        unique_together = ("user", "project")

# This is used if we have human-recorded audio instead of TTS
class HumanAudioInfo(models.Model):
    # Choices for the 'method' field
    METHOD_CHOICES = [
        ('record', 'Record'),
        ('manual_align', 'Manual Align'),
        ('automatic_align', 'Automatic Align'),
    ]
    
    # Fields
    method = models.CharField(max_length=20, choices=METHOD_CHOICES)
    use_for_segments = models.BooleanField(default=False)
    use_for_words = models.BooleanField(default=False)
    voice_talent_id = models.CharField(max_length=200, default='anonymous')
    #audio_file = models.FileField(upload_to='audio_files/', blank=True, null=True)
    #manual_align_metadata_file = models.FileField(upload_to='metadata_files/', blank=True, null=True)
    # We are just using these two fields to store pathnames temporarily before
    # passing them to the async process. Using FileField turns out to create many complications
    # and doesn't help us.
    audio_file = models.CharField(max_length=500, blank=True, null=True)
    manual_align_metadata_file = models.CharField(max_length=500, blank=True, null=True)

    
    # Relationship with CLARAProject
    project = models.OneToOneField(
        'CLARAProject', 
        on_delete=models.CASCADE, 
        related_name='human_audio_info'
    )

    def __str__(self):
        return f"Human Audio Info for {self.project.title}"

# Simpler version of above for phonetic info, where the only operation is recording.
class PhoneticHumanAudioInfo(models.Model):
    
    # Fields
    use_for_segments = models.BooleanField(default=False)
    use_for_words = models.BooleanField(default=False)
    voice_talent_id = models.CharField(max_length=200, default='anonymous')
    
    # Relationship with CLARAProject
    project = models.OneToOneField(
        'CLARAProject', 
        on_delete=models.CASCADE, 
        related_name='phonetic_human_audio_info'
    )

    def __str__(self):
        return f"Phonetic Human Audio Info for {self.project.title}"
        
class CLARAProjectAction(models.Model):
    ACTION_CHOICES = [
        ('create', 'Create'),
        ('edit', 'Edit'),
    ]

    TEXT_VERSION_CHOICES = [
        ('plain', 'Plain'),
        ('segmented', 'Segmented'),
        ('gloss', 'Gloss'),
        ('lemma', 'Lemma'),
    ]

    project = models.ForeignKey(CLARAProject, on_delete=models.CASCADE)
    action = models.CharField(max_length=10, choices=ACTION_CHOICES)
    text_version = models.CharField(max_length=10, choices=TEXT_VERSION_CHOICES)
    timestamp = models.DateTimeField(auto_now_add=True)
    user = models.ForeignKey(User, on_delete=models.SET_NULL, null=True)

    class Meta:
        ordering = ['-timestamp']     

class Content(models.Model):
    external_url = models.URLField(max_length=255, blank=True, null=True)
    project = models.OneToOneField(CLARAProject, on_delete=models.CASCADE, null=True, blank=True, unique=True)
    title = models.CharField(max_length=255)
    text_type = models.CharField(max_length=10, choices=TEXT_TYPE_CHOICES, default='normal')
    l2 = models.CharField(max_length=100, verbose_name='L2 Language')
    l1 = models.CharField(max_length=100, verbose_name='L1 Language')
    length_in_words = models.IntegerField()
    author = models.CharField(max_length=255)
    voice = models.CharField(max_length=255)
    annotator = models.CharField(max_length=255)
    difficulty_level = models.CharField(max_length=100)
    summary = models.TextField(default='', blank=True)

    def __str__(self):
        return self.title

    def get_absolute_url(self):
        return reverse('content_detail', args=[str(self.id)])
        
    def url(self):
        if self.project:
            return reverse('serve_rendered_text', args=[self.project.id, self.text_type, 'page_1.html'])
        else:
            return self.external_url
            
class APICall(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    project = models.ForeignKey(CLARAProject, on_delete=models.CASCADE)
    timestamp = models.DateTimeField()
    operation = models.CharField(max_length=100)
    api_type = models.CharField(max_length=100)
    cost = models.DecimalField(max_digits=10, decimal_places=2)
    duration = models.DecimalField(max_digits=10, decimal_places=2)
    retries = models.IntegerField()
    prompt = models.TextField()
    response = models.TextField()

    class Meta:
        ordering = ['-timestamp']
        
# ASYNCHRONOUS PROCESSING
# Used by asynchronous processes to report results
class TaskUpdate(models.Model):
    report_id = models.CharField(max_length=255)
    message = models.CharField(max_length=1024)
    timestamp = models.DateTimeField(auto_now_add=True)

    class Meta:
        indexes = [
            models.Index(fields=['report_id', 'timestamp']),
        ]

class Rating(models.Model):
    RATING_CHOICES = [
        (1, '1 - Poor'),
        (2, '2 - Fair'),
        (3, '3 - Good'),
        (4, '4 - Very Good'),
        (5, '5 - Excellent'),
    ]

    user = models.ForeignKey(User, on_delete=models.CASCADE)
    content = models.ForeignKey(Content, on_delete=models.CASCADE)
    rating = models.PositiveSmallIntegerField(choices=RATING_CHOICES)

    class Meta:
        unique_together = (('user', 'content'),)
        
class Comment(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    content = models.ForeignKey(Content, on_delete=models.CASCADE)
    comment = models.TextField()
    timestamp = models.DateTimeField(auto_now_add=True)
    
