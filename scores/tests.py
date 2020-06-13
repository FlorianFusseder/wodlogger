from django.contrib.auth.models import User
from django.test import TestCase

from athletes.models import Athlete
from scores.models import Score
from wods.models import Workout


class NoDataScoreView(TestCase):

    def test_athletes_list(self):
        response = self.client.get('/scores/')
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, "No Scores are available.")


class DataFilledScoreViewNotLoggedIn(TestCase):

    @classmethod
    def setUpTestData(cls):
        cls.user1 = User.objects.create_user(username="user_name1", password="test_pw")
        athlete1 = Athlete.objects.create(first_name="first_name1", last_name="last_name1", user=cls.user1)

        user2 = User.objects.create_user(username="user_name2")
        athlete2 = Athlete.objects.create(first_name="first_name2", last_name="last_name2", user=user2)

        awesome_wod = Workout.objects.create(name="AwesomeWod", description="AwesomeDescription", creator=athlete1)

        cls.score1 = Score.objects.create(athlete=athlete1, workout=awesome_wod, score="100", comment="AwesomeComment1")
        cls.score2 = Score.objects.create(athlete=athlete2, workout=awesome_wod, score="200", comment="AwesomeComment2")

    def test_scores_list(self):
        response = self.client.get('/scores/')

        self.assertEqual(response.status_code, 200)
        self.assertContains(response, "Score list")
        self.assertContains(response, "last_name1, first_name1")
        self.assertContains(response, "last_name2, first_name2")
        self.assertContains(response, "AwesomeWod at 100")
        self.assertContains(response, "AwesomeWod at 200")
        self.assertEqual(2, len(response.context_data['score_list']))

    def test_score_detail(self):
        response = self.client.get(f'/scores/{self.score1.id}/')

        self.assertEqual(response.status_code, 200)
        self.assertContains(response, "ATHLETE:")
        self.assertContains(response, "last_name1, first_name1")
        self.assertContains(response, "WORKOUT:")
        self.assertContains(response, "AwesomeWod")
        self.assertContains(response, "AT: ")
        self.assertContains(response, "DESC: AwesomeDescription")
        self.assertContains(response, "SCORE: 100")
        self.assertContains(response, "COMMENT: AwesomeComment1")

    def test_score_editable_if_owner(self):
        response = self.client.post('/profile/login/',
                                    {'username': 'user_name1',
                                     'password': 'test_pw',
                                     })
        self.assertEqual(response.status_code, 302)
        self.assertEqual(response.get('location'), '/profile/')

        response = self.client.get(f'/scores/{self.score1.id}/')

        self.assertEqual(response.status_code, 200)
        self.assertContains(response, "edit score")
        self.assertContains(response, "delete score")

    def test_score_not_editable_if_not_owner(self):
        response = self.client.get(f'/scores/{self.score1.id}/')

        self.assertEqual(response.status_code, 200)
        self.assertNotContains(response, "edit score")
        self.assertNotContains(response, "delete score")


class DeleteScoreView(TestCase):
    pass


class UpdateScoreView(TestCase):
    pass
