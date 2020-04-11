from django.db import models
from django.conf import settings
from django.db.models import F
from django.contrib.contenttypes.fields import GenericRelation, GenericForeignKey
from django.contrib.contenttypes.models import ContentType
from django.contrib.auth.models import User
from django.db.models.signals import post_save
import uuid
import os


# Create your models here.


# klasse for en samlingsbetegnelse for kommentar og post
class Submission(models.Model):
    class Meta:
        abstract = True

    author = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)


class Emne(models.Model):

    emnenavn = models.CharField(max_length=200)

    def __str__(self):
        return self.emnenavn


# klasse for poster
class Post(Submission):
    class Meta:
        db_table = "posts"
        index_together = [
            ["submission_time", ],
        ]

    # kode nødvendig for poster
    id = models.UUIDField(primary_key = True, default = uuid.uuid4, editable = False)
    emne = models.ForeignKey(Emne, on_delete=models.CASCADE, related_name="posts")
    title = models.CharField(max_length=120)
    text = models.TextField(blank=True, max_length=8192)
    submission_time = models.DateTimeField(auto_now_add=True)
    num_comments = models.IntegerField(default=0)
    likes = models.ManyToManyField(settings.AUTH_USER_MODEL, blank = True, related_name="post_likes")


    # funksjon for å legge til kommentar på post
    def add_comment(self, text, author):
        comment = Comment()
        comment.text = text
        comment.post = self
        comment.author = author
        comment.save()

        self.num_comments += 1
        self.save(update_fields=["num_comments"])

        return comment #returnsetning

    # funksjoner for å få url
    def get_url(self):
        return "/forumApp/userpost/" +  str(self.id)

    def get_like_url(self):
        return "/forumApp/userpost/" +  str(self.id) + "/like"

    # funksjon for å få Tittelen på posten
    def as_view(self):
        title = self.title
        description = self.text
        return title + "\n \n" + description

    def __str__(self):
        return self.title + str(self.id)


class ReportPost(Submission):
    class Meta:
        db_table = "post_reports"
        index_together = [
            ["submission_time", ],
        ]
    submission_time = models.DateTimeField(auto_now_add=True)
    post = models.ForeignKey(Post, on_delete=models.CASCADE, related_name="reports",)
    def __str__(self):
        return "Rapport fra "+str(self.author)+" om post: "+str(self.post.title)

# funksjon for å finne poster
def get_post_by_id(post_id):
    return Post.objects\
        .select_related("author").get(pk=post_id)


def get_posts_by_emne(emne):
    return Post.objects.filter(emne=emne)


# klasse for kommentarer
class Comment(Submission):
    class Meta:
        db_table = "comments"
    post = models.ForeignKey(Post, on_delete=models.CASCADE, related_name="comments",)
    parent_comment = models.ForeignKey(
        'self',
        null=True, blank=True,
        on_delete=models.CASCADE)
    text = models.TextField(max_length=8192)
    submission_time = models.DateTimeField(auto_now_add=True)
    # variabel for hvilket rekursivt nivå en kommentar er på
    level = models.IntegerField(default=0)

    def reply(self, text, author):
        comment = Comment()
        comment.text = text
        comment.post = self.post
        comment.parent_comment = self
        comment.level = self.level + 1
        comment.author = author
        comment.save()

        comment.post.num_comments = F('num_comments') + 1
        comment.post.save()

        return comment

    def __str__(self):
        return self.text


class ReportComment(Submission):
    class Meta:
        db_table = "comment_reports"
        index_together = [
            ["submission_time", ],
        ]
    submission_time = models.DateTimeField(auto_now_add=True)
    comment = models.ForeignKey(Comment, on_delete=models.CASCADE, related_name="reports",)
    def __str__(self):
        return "Rapport fra "+str(self.author)+" om kommentar: "+str(self.comment.text)


def get_comments_by_post(post_id):
    post = get_post_by_id(post_id)
    return Comment.objects.filter(post=post, level=0)

def get_comment_by_id(comment_id):
    return Comment.objects \
        .select_related("author").get(pk=comment_id)

# hvordan man kan legge inn bild epå profilen 
# tror ikke den brukes, men får feilmelding når jeg prøver å fjerne den
# tror det er pga noe i databasen brukte den før(?)
def get_image_path(instance, filename):
    return os.path.join('photos', str(instance.id), filename)


# Det følgende er det som faktisk brukes til profilen
class UserProfile(models.Model):
    user = models.OneToOneField(User,on_delete=models.CASCADE) # ontoonefield handler om primary key
    description = models.CharField(max_length=140, default='', blank=True) # deskripition er noe brukeren skal kunne lagre om seg selv
    image = models.ImageField(upload_to='profile_image', default='/profile_image/homelogo.png')

    # funksjon for at brukerens UserProfile skal vises med brukernavn på admin-siden
    def __str__(self):
        return self.user.username


# Må ha denne for at det skal kobles en UserPRofile til hver bruker som opprettes
def create_profile(sender, **kwargs):
    if kwargs['created']:
        user_profile = UserProfile.objects.create(user=kwargs['instance'])


post_save.connect(create_profile, sender=User)
    