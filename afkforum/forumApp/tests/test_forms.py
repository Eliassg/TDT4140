from django.test import TestCase
from forumApp.forms import SignUpForm, EditProfileForm, EditUserProfileForm

#Klasse for testing av forms

class TestForms(TestCase):

    #tester gyldig registrering

    def test_signup_form_valid_data(self):
        form = SignUpForm(data={
            'username':"test",
            'email': "usertest@usertest.no",
            'password1': "User123456", 
            'password2':"User123456"
            })

        self.assertTrue(form.is_valid())

   #tester ugyldig registrering. sjekker forventet antall feil 

    def test_signup_form_no_data(self):
        form = SignUpForm(data={
            })

        self.assertFalse(form.is_valid())
        self.assertEquals(len(form.errors),4)

    #tester gyldig brukerendring

    def test_edit_profile_form_valid_data(self):
        form = EditProfileForm(data={
            'email' : "usertest@usertest.no"
            })
        
        self.assertTrue(form.is_valid())

    #tester å sette inn blankt epostfelt    

    def test_edit_profile_form_no_data(self):
        form = EditProfileForm(data={
            'email' : ""
            })
        
        self.assertTrue(form.is_valid())

    #tester å endre til ugyldig epostadresse

    def test_edit_profile_form_invalid(self):
        form = EditProfileForm(data={
            'email' : "glemtealfakrøll!"
            })

        self.assertFalse(form.is_valid())
    
    #tester gyldig endring av profilbeskrivelse

    def test_edit_user_profile_valid_info(self):
        form = EditUserProfileForm(data={
            'description' : "kjernekar",
            'image' : "image.jpg"
            })
        
        self.assertTrue(form.is_valid())

    #tester gyldig endring null profilbeskrivelse

    def test_edit_user_profile_valid_no_info(self):
        form = EditUserProfileForm(data={
            'description' : "",
            'image' : ""
            })
        
        self.assertTrue(form.is_valid())
