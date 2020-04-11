from django.test import TestCase
from django.contrib.admin.sites import AdminSite
from forumApp.admin import ReportPostAdmin, ReportCommentAdmin
from django.contrib.auth.models import User
from forumApp.models import Post, UserProfile, Emne, ReportPost, get_post_by_id, get_posts_by_emne, Comment, \
    ReportComment, get_comments_by_post, get_comment_by_id, get_image_path
import datetime
import uuid
from django.utils.safestring import SafeString



from django.test import Client, TestCase

class MyTestCase(TestCase):

    def setUp(self):
        # lag en testbruker
        self.user1 = User.objects.create_user(
            username='testuser1',
            password='12345'
        )
        
        # lag Emne å poste i
        self.testemne1 = Emne.objects.create(
            emnenavn='Testemne1'
        )

        # lag post
        self.testpost = Post.objects.create(
            author=self.user1,
            id=uuid.UUID('44b171fe-37f3-45bd-9c27-242c75236a64'),
            emne=self.testemne1,
            title='Testtittel'
        )

        # lag en rapportering av post
        self.reportpost = ReportPost.objects.create(
            author=self.user1,
            post=self.testpost,
            submission_time=datetime.datetime.now()

        )

        # lag en kommentar
        self.testcomment = Comment.objects.create(
            post=self.testpost,
            text="This is the text for the comment",
            submission_time=datetime.datetime.now(),
            author=self.user1
        )

        # lag en rapportering av kommentar
        self.reporttestcomment = ReportComment.objects.create(
            author=self.user1,
            comment=self.testcomment,
            submission_time=datetime.datetime.now()

        )

        # steg for å opprette en adminbruker
        self.client = Client()
        self.superuser = User.objects.create_superuser(
            username='test',
            password='test',
        )
        self.client.force_login(self.superuser)

        # oppretter objekter for de klassene vis skal teste
        self.reportpostadmin = ReportPostAdmin(self.superuser, AdminSite())
        self.reportcommentadmin = ReportCommentAdmin(self.superuser, AdminSite())
    

    def test_post_link(self):
        self.assertEqual(self.reportpostadmin.post_link(self.reportpost), '<a href="/admin/forumApp/post/44b171fe-37f3-45bd-9c27-242c75236a64/change/">Testtittel44b171fe-37f3-45bd-9c27-242c75236a64</a>')
        self.assertTrue(isinstance(self.reportpostadmin.post_link(self.reportpost), SafeString))

    def test_comment_link(self):
        self.assertEqual(self.reportcommentadmin.comment_link(self.reporttestcomment), '<a href="/admin/forumApp/comment/1/change/">This is the text for the comment</a>')
        self.assertTrue(isinstance(self.reportcommentadmin.comment_link(self.reporttestcomment), SafeString))
