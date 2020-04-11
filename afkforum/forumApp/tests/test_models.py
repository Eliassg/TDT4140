from django.test import TestCase
from django.contrib.auth.models import User
from forumApp.models import Post, UserProfile, Emne, ReportPost, get_post_by_id, get_posts_by_emne, Comment, \
    ReportComment, get_comments_by_post, get_comment_by_id, get_image_path
import datetime
import uuid


class TestModels(TestCase):

    # her er det generelle som settes opp før testingen starter
    # det flere av testfunksjonene kan få bruk for
    def setUp(self):
        # lag en testbruker
        self.user1 = User.objects.create_user(
            username='testuser1',
            password='12345'
        )
        # lag enda en testbruker
        self.user2 = User.objects.create_user(
            username='testuser2',
            password='12345'
        )
        # lag Emne å poste i
        self.testemne1 = Emne.objects.create(
            emnenavn='Testemne1'
        )

        # lag Emne å poste i
        self.testemne2 = Emne.objects.create(
            emnenavn='Testemne2'
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

    #################### Submission-tester #############################

    #################### Emne-tester ###################################
    def test_emne_str(self):
        self.assertEqual(self.testemne1.__str__(), self.testemne1.emnenavn)

    #################### Post-tester ###################################

    # test som sjekker om antallet kommentarer som registreres er riktig
    # ikke ferdigstilt. har bare begynt med nødvendig setup
    def test_post_increase_total_comment_number(self):
        self.testcomment = self.testpost.add_comment("test", self.user1)

        self.assertEquals(self.testpost.num_comments, 1)

    # test som sjekker at riktig url blir returnert
    def test_post_get_url(self):
        self.assertEqual(self.testpost.get_url(), "/forumApp/userpost/44b171fe-37f3-45bd-9c27-242c75236a64")

    # test som sjekker at as_view gir innholdet til posten på en pen måte
    def test_post_as_view(self):
        self.assertEqual(self.testpost.as_view(), "Testtittel\n \n")

    # test som sjekker at __str__-funkjsonen funker riktig
    def test_post_str(self):
        self.assertEqual(self.testpost.__str__(), 'Testtittel44b171fe-37f3-45bd-9c27-242c75236a64')

    # test som sjekker at riktig url blir returnert for like
    def test_post_get_like_url(self):
        self.assertEqual(self.testpost.get_like_url(), "/forumApp/userpost/44b171fe-37f3-45bd-9c27-242c75236a64/like")

    #################### ReportPost-tester  #############################

    # test som sjekker at __str__-funkjsonen funker riktig
    def test_reportpost_str(self):
        self.assertEqual(self.reportpost.__str__(), "Rapport fra testuser1 om post: Testtittel")

    #################### Comment-tester  ################################

    # sjekker at reply-funkjsonen funker som den skal
    def test_comment_reply(self):
        # lag en reply som kan testes
        testreply = self.testcomment.reply('Text for the reply', self.user2)

        # sjekker at det som blir opprettet faktisk er en comment
        self.assertIsInstance(testreply, Comment)

        # sjekker at det er riktig tekst
        self.assertEqual(testreply.text, 'Text for the reply')

        # sjekker at det er riktig forfatter
        self.assertEqual(testreply.author, self.user2)

        # sjekker at det er rikitg level
        self.assertEqual(testreply.level, self.testcomment.level + 1)

    # sjekker at __str__ funker som den skal
    def test_comment_str(self):
        self.assertEqual(self.testcomment.__str__(), "This is the text for the comment")

    #################### ReportComment-tester  ##########################

    # test som sjekker at __str__-funkjsonen funker riktig
    def test_reportcomment_str(self):
        self.assertEqual(self.reporttestcomment.__str__(),
                         "Rapport fra testuser1 om kommentar: This is the text for the comment")

    #################### UserProfile-tester  ############################
    # test som sjekker at det tilkobles en UserProfile når en bruker opprettes
    def test_userprofile_created_when_user_is_created(self):
        self.assertEquals(self.user1.userprofile.user.username, 'testuser1')  # ble litt kronglete dessverre:/

    # test som sjekker at __str__-funkjsonen funker riktig
    def test_userprofile_str(self):
        self.assertEqual(self.user1.userprofile.__str__(), "testuser1")

    #################### Other functions ########################
    # her testes funksjoner som ikke er direkte knyttet opp mot noen klasser i models-filen

    # test som sjekker om man får riktig post når man har id
    def test_get_post_by_id(self):
        self.assertEquals(get_post_by_id(self.testpost.id).pk, self.testpost.pk)

        # test som sjekker om man får rikitge poster når man sorterer etter emne

    def test_get_posts_by_emne(self):
        # sjekker at vi får opp testemne når vi ser på postene i emne1
        self.assertEquals(list(get_posts_by_emne(self.testemne1)), list([self.testpost, ]))

        # sjekker at vi ikke får opp noen poster når vi ser på postene for testemne 2
        self.assertEquals(get_posts_by_emne(self.testemne2).count(), 0)

    # test som sjekker at man får kommentarene til en post
    def test_get_comments_by_post(self):
        # sjekker at vi får opp testemne når vi ser på postene i emne1
        self.assertEquals(list(get_comments_by_post(self.testpost.id)), list([self.testcomment, ]))

        # sjekker at vi ikke får opp noen poster når vi ser på postene for testemne 2
        self.assertEquals(get_posts_by_emne(self.testemne2).count(), 0)

    # test som sjekker om man får riktig kommentar når man har id
    def test_get_comment_by_id(self):
        self.assertEquals(get_comment_by_id(self.testcomment.id).pk, self.testcomment.pk)

        # test som sjekker om path blir rikitg for hvilken som helst instance

    def test_get_image_path(self):
        self.assertIn(get_image_path(self.testpost, 'posttest'),
                      ('photos/44b171fe-37f3-45bd-9c27-242c75236a64/posttest',
                       'photos\\44b171fe-37f3-45bd-9c27-242c75236a64\\posttest'))
