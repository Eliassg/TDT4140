from django.test import SimpleTestCase
from django.urls import reverse, resolve
from forumApp.views import index, emneSide, loginPage, logoutUser, registerPage, postCreation, userpost, PostLikeToggle, view_profile, delete_user, delete_user_confirm, show_search_result, view_profile, edit_profile, change_password

#Testing if the name's revers url corresponds to the correct urlpattern.
class TestUrls(SimpleTestCase):

    def test_index_url_is_resolved(self):
        url = reverse('index')
        #print(resolve(url))
        self.assertEqual(resolve(url).func, index)

    def test_enkeltemne_url_is_resolved(self):
        # the urlpattern is asking for an id.
        url = reverse('enkeltemne', kwargs={'id': 1})
        #print(resolve(url))
        self.assertEqual(resolve(url).func, emneSide)

    def test_login_url_is_resolved(self):
        url = reverse('login')
        #print(resolve(url))
        self.assertEqual(resolve(url).func, loginPage)

    def test_logout_url_is_resolved(self):
        url = reverse('logout')
        #print(resolve(url))
        self.assertEqual(resolve(url).func, logoutUser)

    def test_register_url_is_resolved(self):
        url = reverse('register')
        #print(resolve(url))
        self.assertEqual(resolve(url).func, registerPage)

    def test_postCreation_url_is_resolved(self):
        url = reverse('postCreation')
        #print(resolve(url))
        self.assertEqual(resolve(url).func, postCreation)

    def test_userpost_url_is_resolved(self):
        # the urlpattern is asking for a slug
        url = reverse('userpost view', args=['userpost-slug'])
        #print(resolve(url))
        self.assertEqual(resolve(url).func, userpost)

    def test_like_url_is_resolved(self):
        # the urlpattern is asking for a slug
        url = reverse('like-toggle', args=['like-slug'])
        #print(resolve(url))
        self.assertEqual(resolve(url).func.view_class, PostLikeToggle)

    def test_profil_url_is_resolved(self):
        url = reverse('profil')
        #print(resolve(url))
        self.assertEqual(resolve(url).func, view_profile)

    def test_delete_user_url_is_resolved(self):
        # it think you need the keyword args  bacause of the patterns (?P<username>[\w|W.-]+) part
        url = reverse('delete_user', kwargs={'username': 'profile-slug'})
        #print(resolve(url))
        self.assertEqual(resolve(url).func, delete_user)
    
    def test_deleteUser_url_is_resolved(self):
        url = reverse('deleteUser')
        #print(resolve(url))
        self.assertEqual(resolve(url).func, delete_user_confirm)

    def test_results_url_is_resolved(self):
        url = reverse('results')
        #print(resolve(url))
        self.assertEqual(resolve(url).func, show_search_result)

    def test_view_profile_url_is_resolved(self):
        # the urlpattern is asking for a slug
        url = reverse('view_profile', args=['profile-slug'])
        #print(resolve(url))
        self.assertEqual(resolve(url).func, view_profile)

    def test_deit_profile_url_is_resolved(self):
        url = reverse('edit_profile')
        #print(resolve(url))
        self.assertEqual(resolve(url).func, edit_profile)

    def test_change_password_url_is_resolved(self):
        url = reverse('change_password')
        #print(resolve(url))
        self.assertEqual(resolve(url).func, change_password)
