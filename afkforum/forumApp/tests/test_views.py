from django.test import TestCase, Client
from django.urls import reverse
from django.contrib.auth.models import User
from django.contrib.auth import authenticate, login, logout 
from forumApp.models import *
from forumApp.forms import SignUpForm, EditProfileForm, EditUserProfileForm
from forumApp.views import PostLikeToggle
import json
import datetime
import uuid


class TestViews(TestCase):

    def setUp(self):
        # oppretter en client
        self.client = Client()

        # lagrer url i en variabel som kan brukes om igjen
        self.index_url = reverse('index')
        self.register_url = reverse('register')
        self.login_url = reverse('login')
        self.logout_url = reverse('logout')
        self.valid_emne_url = reverse('enkeltemne', args=[1])
        self.invalid_emne_url = reverse('enkeltemne', args=[5])
        self.userpost_url = reverse('userpost view', args=['44b171fe-37f3-45bd-9c27-242c75236a64'])
        self.like_url = reverse('like-toggle',args=['44b171fe-37f3-45bd-9c27-242c75236a64'])
        self.postcreate_url = reverse('postCreation')
        self.delete_user_url = reverse('delete_user', args=['testuser1'])
        self.invalid_delete_user_url = reverse('delete_user', args=['testuser1000'])
        self.delete_user_confirm_url = reverse('deleteUser')
        self.results_url = reverse('results')
        self.view_profile_url = reverse('view_profile',args=['testuser1'])
        self.edit_profile_url = reverse('edit_profile')
        self.change_password_url = reverse('change_password')





        # lag en testbruker
        self.user1 = User.objects.create_user(
            username='testuser1',
            password='12345passord'
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
        # lag en kommentar
        self.testcomment = Comment.objects.create(
            post=self.testpost,
            text="This is the text for the comment",
            submission_time=datetime.datetime.now(),
            author=self.user1
        )

        #instansierer PostLikeToggle-klassen
        self.liketoggle = PostLikeToggle()
        self.liketoggle.post_id='44b171fe-37f3-45bd-9c27-242c75236a64'

        

    def test_index_GET(self):
        #setup:
        response = self.client.get(self.index_url)

        #sjekker http-respons
        self.assertEquals(response.status_code, 200)

        #sjekker at riktige templates brukes
        self.assertTemplateUsed(response, 'base.html')
        self.assertTemplateUsed(response, 'index.html')

    def test_registerpage_GET(self):
        #setup:
        response = self.client.get(self.register_url)

        #sjekker http-respons
        self.assertEquals(response.status_code, 200)

        #sjekker at riktige templates brukes
        self.assertTemplateUsed(response, 'base.html')
        self.assertTemplateUsed(response, 'register.html')

    def test_registerpage_POST_register_new_user(self):
        #setup:
        response = self.client.post(self.register_url, data={
            'username':"testbrukernavn",
            'email': "usertest@usertest.no",
            'password1': "User123456", 
            'password2':"User123456",
        })

        # vil sjekke at vi blir redirected, har kode 302
        self.assertEquals(response.status_code, 302)

        #vil sjekke at brukeren faktisk ble opprettet
        self.assertIsNotNone(authenticate(username='testbrukernavn', password='User123456'))

    def test_registerpage_POST_no_data(self):
        #setup:
        response = self.client.post(self.register_url)

         # vil sjekke at vi ikke blir redirected
        self.assertEquals(response.status_code, 200)

    def test_loginpage_GET(self):
        #setup:
        response = self.client.get(self.login_url)

        #sjekker http-respons
        self.assertEquals(response.status_code, 200)

        #sjekker at riktige templates brukes
        self.assertTemplateUsed(response, 'base.html')
        self.assertTemplateUsed(response, 'login.html')

    def test_loginpage_POST_login_valid_user(self):
        #setup:
        response = self.client.post(self.login_url, data={
            'username':"testuser1",
            'password': "12345passord", 
        })

        # vil sjekke at vi blir redirected, har kode 302
        self.assertEquals(response.status_code, 302)

    def test_loginpage_POST_login_invalid_user(self):
        #setup:
        response = self.client.post(self.login_url, data={
            'username':"testuser500",
            'password': "12345passord", 
        })

        # vil sjekke at vi ikke blir redirected
        self.assertEquals(response.status_code, 200)

    def test_logoutuser(self):
        #setup
        response = self.client.get(self.logout_url)

        # vil sjekke at vi blir redirected, har kode 302
        self.assertEquals(response.status_code, 302)

    def test_emneside_GET_valid_emne(self):
        #setup
        response = self.client.get(self.valid_emne_url)
        
        #sjekker http-respons
        self.assertEquals(response.status_code, 200)

        #sjekker at riktige templates brukes
        self.assertTemplateUsed(response, 'base.html')
        self.assertTemplateUsed(response, 'emner.html')
        
    def test_emneside_GET_invalid_emne(self):
        #setup
        response = self.client.get(self.invalid_emne_url)
        
        #sjekker http-respons
        self.assertEquals(response.status_code, 404)

    def test_userpost_GET(self):
        #setup
        response = self.client.get(self.userpost_url)
        
        #sjekker http-respons
        self.assertEquals(response.status_code, 200)

        #sjekker at riktige templates brukes
        self.assertTemplateUsed(response, 'base.html')
        self.assertTemplateUsed(response, 'postView.html')
        
    def test_userpost_POST_delete_post(self):
        # sjekker at testemne1 har en post vi kan slette
        self.assertEquals(self.testemne1.posts.count(), 1)
        
        #setup for sletting:
        response = self.client.post(self.userpost_url, data={
            'deleteValue':"deleteYes",
            'reportPostValue': "", 
            'reportCommentValue': "", 
            'commentPostValue': "", 
        })

        # vil sjekke at vi blir redirected, har kode 302
        self.assertEquals(response.status_code, 302)

        # vil sjekke at posten er slettet, da vil emne1 ha 0 poster
        self.assertEquals(self.testemne1.posts.count(), 0)
        

    def test_userpost_POST_report_post(self):
        #sjekker at det ikke er noen rapporteringer til å begynne med
        self.assertEquals(self.testpost.reports.count(), 0)

        #setup:
        self.client.login(username='testuser1', password='12345passord')
        response = self.client.post(self.userpost_url, data={
            'deleteValue':"",
            'reportPostValue': "reportPostYes", 
            'reportCommentValue': "", 
            'commentPostValue': "", 
        })

        # vil sjekke at siden bare lastes, uten å redirecte
        self.assertEquals(response.status_code, 200)

        #sjekker at det har skjedd en rapportering
        self.assertEquals(self.testpost.reports.count(), 1)

    def test_userpost_POST_report_comment(self):
        #sjekker at det ikke er noen rapporteringer til å begynne med
        self.assertEquals(self.testcomment.reports.count(), 0)

        #setup:
        self.client.login(username='testuser1', password='12345passord')
        response = self.client.post(self.userpost_url, data={
            'deleteValue':"",
            'reportPostValue': "", 
            'reportCommentValue': "reportCommentYes", 
            'commentPostValue': "", 
            'commentID':"1"
        })

        # vil sjekke at siden bare lastes, uten å redirecte
        self.assertEquals(response.status_code, 200)

        #sjekker at det har skjedd en rapportering
        self.assertEquals(self.testcomment.reports.count(), 1)

    def test_userpost_POST_add_comment(self):
        #sjekker at det ikke er noen rapporteringer til å begynne med
        self.assertEquals(self.testpost.comments.count(), 1)

        #setup:
        self.client.login(username='testuser1', password='12345passord')
        response = self.client.post(self.userpost_url, data={
            'deleteValue':"",
            'reportPostValue': "", 
            'reportCommentValue': "", 
            'commentPostValue': "commentYes", 
            'commentText':"Tekstinnhold til kommentar"
        })

        # vil sjekke at siden redirecter
        self.assertEquals(response.status_code, 302)

        #sjekker at det har skjedd en rapportering
        self.assertEquals(self.testpost.comments.count(), 2)

    def test_postliketoggle_get_redirect_url(self):

        self.client.login(username='testuser1', password='12345passord')

        response = self.client.get(self.like_url)

        # sjekker at det blir redirect
        self.assertEquals(response.status_code, 302)

    def test_postliketoggle_add_like(self):
        #sjekker at det ikke er noen likes til å begynne med
        self.assertEquals(self.testpost.likes.count(), 0)

        self.client.login(username='testuser1', password='12345passord')

        response = self.client.get(self.like_url)

        # sjekker at det er blitt lagt til likes
        self.assertEquals(self.testpost.likes.count(), 1)

    def test_postliketoggle_remove_like(self):
        #sjekker at det ikke er noen likes til å begynne med
        self.assertEquals(self.testpost.likes.count(), 0)

        self.client.login(username='testuser1', password='12345passord')

        response = self.client.get(self.like_url)

        # sjekker at det er blitt lagt til likes
        self.assertEquals(self.testpost.likes.count(), 1)

        #"trykker" en gang til
        response = self.client.get(self.like_url)

        # sjekker nå at det ikke lenger er noen likes
        self.assertEquals(self.testpost.likes.count(), 0)

    def test_postcreation_GET(self):
        #setup:
        response = self.client.get(self.postcreate_url)

        #sjekker http-respons
        self.assertEquals(response.status_code, 200)

        #sjekker at riktige templates brukes
        self.assertTemplateUsed(response, 'base.html')
        self.assertTemplateUsed(response, 'postCreation.html')

    def test_postcreation_POST(self):

        #setup:
        self.client.login(username='testuser1', password='12345passord')
        response = self.client.post(self.postcreate_url, data={
            'postTitle':"Tittel",
            'postDesc': "Beskrivelse", 
            'emnenavn': "Testemne1", })

        # vil sjekke at siden redirecter
        self.assertEquals(response.status_code, 302)

    def test_deleteuser_GET(self):
        #setup:
        self.client.login(username='testuser1', password='12345passord')
        
        response = self.client.post(self.delete_user_url)

        # vil sjekke at siden lastes riktig
        self.assertEquals(response.status_code, 200)

        #sjekker at riktige templates brukes
        self.assertTemplateUsed(response, 'base.html')
        self.assertTemplateUsed(response, 'register.html')
        
    def test_deleteuser_GET_nonexistent_user(self):
        #setup:
        # self.client.login(username='testuser5', password='12345passord')
        
        response = self.client.get(self.invalid_delete_user_url)
        # vil sjekke at siden lastes riktig
        self.assertEquals(response.status_code, 200)

        #sjekker at riktige templates brukes
        self.assertTemplateUsed(response, 'base.html')
        self.assertTemplateUsed(response, 'register.html')
    

    def test_delete_user_confirm_GET(self):
        #setup:
        self.client.login(username='testuser1', password='12345passord')

        response = self.client.post(self.delete_user_confirm_url)

        #sjekker http-respons
        self.assertEquals(response.status_code, 200)

        #sjekker at riktige templates brukes
        self.assertTemplateUsed(response, 'base.html')
        self.assertTemplateUsed(response, 'deleteUser.html')

    def test_show_search_result(self):
        response = self.client.get(self.results_url, data={
            'q':"test",})

        #sjekker http-respons
        self.assertEquals(response.status_code, 200)

        #sjekker at riktige templates brukes
        self.assertTemplateUsed(response, 'base.html')
        self.assertTemplateUsed(response, 'searchresult.html')

    def test_view_profile(self):
        #setup
        self.client.login(username='testuser1', password='12345passord')
        response = self.client.get(self.view_profile_url)

        #sjekker http-respons
        self.assertEquals(response.status_code, 200)

        #sjekker at riktige templates brukes
        self.assertTemplateUsed(response, 'base.html')
        self.assertTemplateUsed(response, 'account/profile.html')

    def test_edit_profile_GET(self):
        #setup
        self.client.login(username='testuser1', password='12345passord')
        response = self.client.get(self.edit_profile_url)

        #sjekker http-respons
        self.assertEquals(response.status_code, 200)

        #sjekker at riktige templates brukes
        self.assertTemplateUsed(response, 'base.html')
        self.assertTemplateUsed(response, 'account/edit_profile.html')

    def test_edit_profile_POST(self):
        #setup
        self.client.login(username='testuser1', password='12345passord')
        response = self.client.post(self.edit_profile_url)

        #sjekker http-respons
        self.assertEquals(response.status_code, 302)

    def test_change_password_GET(self):
        #setup
        self.client.login(username='testuser1', password='12345passord')
        response = self.client.get(self.change_password_url)

        #sjekker http-respons
        self.assertEquals(response.status_code, 200)

        #sjekker at riktige templates brukes
        self.assertTemplateUsed(response, 'base.html')
        self.assertTemplateUsed(response, 'account/change_password.html')

    def test_change_password_POST_not_valid_form(self):
        #setup
        self.client.login(username='testuser1', password='12345passord')
        response = self.client.post(self.change_password_url)

        #sjekker http-respons
        self.assertEquals(response.status_code, 302)

    def test_change_password_POST_valid_form(self):
        #setup
        self.client.login(username='testuser1', password='12345passord')
        response = self.client.post(self.change_password_url,data={
            'username':"testuser1",
            'email': "usertest@usertest.no",
            'old_password': "12345passord", 

            'new_password1': "langtpassord123", 
            'new_password2':"langtpassord123",
        })

        #sjekker http-respons
        self.assertEquals(response.status_code, 302)

  