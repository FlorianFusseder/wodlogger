from django.contrib.auth.models import User
from django.test import TestCase

from athletes.models import Athlete
from scores.models import Score
from wods.models import Workout

profile_url = "/profile/"
signup_url = profile_url + "signup/"


class ProfileView(TestCase):

    def setUp(self):
        response = self.client.post(signup_url,
                                    {'username': 'testuser',
                                     'first_name': 'test_first_name',
                                     'last_name': 'test_last_name',
                                     'password1': 'TestPassword1',
                                     'password2': 'TestPassword1'
                                     })
        self.assertEqual(response.status_code, 302)
        self.assertEqual(response.get('location'), '/profile/')

    def test_profile_data_contained(self):
        response = self.client.get(profile_url)
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, "testuser")
        self.assertContains(response, "test_first_name")
        self.assertContains(response, "test_last_name")
        self.assertContains(response, "You have scores no logged until now!")
        self.assertContains(response, "Athlete has not yet created a workout!")

    def test_workout_data_contained(self):
        athlete = Athlete.objects.get(user__username='testuser')
        awesome_wod = Workout.objects.create(name="AwesomeWod", creator=athlete)
        Score.objects.create(athlete=athlete, workout=awesome_wod, score="100")

        response = self.client.get(profile_url)
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, "AwesomeWod done in 100")
        self.assertContains(response, "AwesomeWod (FOR_TIME):")


class SignUpView(TestCase):

    def test_get_signup_form(self):
        response = self.client.get(signup_url)
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, "Sign up")
        self.assertContains(response, "First name")
        self.assertContains(response, "Last name")

    def test_post_signup_form(self):
        response = self.client.post(signup_url,
                                    {'username': 'testuser',
                                     'password1': 'TestPassword1',
                                     'password2': 'TestPassword1'
                                     })
        self.assertEqual(response.status_code, 302)
        self.assertEqual(response.get('location'), '/profile/')

        user = User.objects.get(username='testuser')
        self.assertIsNotNone(user)
        self.assertEqual(user.username, 'testuser')
