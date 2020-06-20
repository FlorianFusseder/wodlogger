from django.contrib.auth.models import User
from django.test import TestCase

from athletes.models import Athlete
from scores.models import Score
from wods.models import Workout


class NoDataAthleteView(TestCase):

    def test_athletes_list(self):
        response = self.client.get('/athletes/')
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, "No Athletes are available.")


class DataFilledAthleteView(TestCase):

    @classmethod
    def setUpTestData(cls):
        cls.user = User.objects.create_user(username="user_name1")
        Athlete.objects.create(first_name="first_name1", last_name="last_name1", user=cls.user)
        user2 = User.objects.create_user(username="user_name2")
        athlete = Athlete.objects.create(first_name="first_name2", last_name="last_name2", user=user2)
        awesome_wod = Workout.objects.create(name="AwesomeWod", creator=athlete)
        Score.objects.create(athlete=athlete, workout=awesome_wod, score="100")

    def test_athletes_list(self):
        response = self.client.get('/athletes/')
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, "Athlete list")
        self.assertContains(response, "user_name1")
        self.assertContains(response, "first_name1")
        self.assertContains(response, "last_name1")
        self.assertContains(response, "user_name2")
        self.assertContains(response, "first_name2")
        self.assertContains(response, "last_name2")
        self.assertQuerysetEqual(response.context_data['athlete_list'],
                                 ['<Athlete: Athlete [ first_name: first_name1, second_name: last_name1 ]>',
                                  '<Athlete: Athlete [ first_name: first_name2, second_name: last_name2 ]>'])

    def test_athlete_detail_no_wod_and_score(self):
        response = self.client.get('/athletes/1/')
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, "Athlete details")
        self.assertContains(response, "user_name1")
        self.assertContains(response, "first_name1")
        self.assertContains(response, "last_name1")
        self.assertEqual(len(response.context_data['scores']), 0)
        self.assertEqual(len(response.context_data['workouts']), 0)

    def test_athlete_detail_with_wod_and_score(self):
        response = self.client.get('/athletes/2/')
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, "Athlete details")
        self.assertContains(response, "user_name2")
        self.assertContains(response, "first_name2")
        self.assertContains(response, "last_name2")
        self.assertEqual(len(response.context_data['scores']), 1)
        self.assertEqual(len(response.context_data['workouts']), 1)
