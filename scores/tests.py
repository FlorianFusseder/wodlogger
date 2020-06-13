from abc import ABC

from django.contrib.auth.models import User
from django.http import HttpResponseForbidden
from django.test import TestCase

from athletes.models import Athlete
from scores.models import Score
from wods.models import Workout


class SetupScoreData(ABC, TestCase):

    @classmethod
    def setUpTestData(cls):
        pw_ = "test_pw1"
        cls.user1 = User.objects.create_user(username="user_name1", password=pw_)
        cls.user1.clear_pw = pw_
        athlete1 = Athlete.objects.create(first_name="first_name1", last_name="last_name1", user=cls.user1)
        pw_ = "test_pw2"
        cls.user2 = User.objects.create_user(username="user_name2", password=pw_)
        cls.user2.clear_pw = pw_
        athlete2 = Athlete.objects.create(first_name="first_name2", last_name="last_name2", user=cls.user2)
        awesome_wod = Workout.objects.create(name="AwesomeWod", description="AwesomeDescription", creator=athlete1)
        cls.score1 = Score.objects.create(athlete=athlete1, workout=awesome_wod, score="100", comment="AwesomeComment1")
        cls.score2 = Score.objects.create(athlete=athlete2, workout=awesome_wod, score="200", comment="AwesomeComment2")


class NoDataScoreView(TestCase):

    def test_scores_list(self):
        response = self.client.get('/scores/')
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, "No Scores are available.")


class DataFilledScoreViewNotLoggedIn(SetupScoreData):

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
                                    {'username': self.user1.username,
                                     'password': self.user1.clear_pw,
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


class DeleteScoreViewTest(SetupScoreData):

    def test_delete_score_enforces_login(self):
        # Assert score does exist
        get_score_response = self.client.get(f'/scores/{self.score1.id}/')
        self.assertEqual(get_score_response.status_code, 200)
        self.assertContains(get_score_response, "AwesomeComment1")

        # Assert redirect if not logged in
        redirect_response = self.client.get(f'/scores/{self.score1.id}/delete')
        delete_url = f'/scores/{self.score1.id}/delete'
        redirect_url = f'/profile/login/?next={delete_url}'
        self.assertRedirects(redirect_response, redirect_url)

        # Assert redirect routes to login page
        response = self.client.get(redirect_url)
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, "<title>Login</title>")

        # Assert post to login page redirects do deletion page
        response = self.client.post(redirect_url, {
            'username': self.user1.username,
            'password': self.user1.clear_pw,
        })
        self.assertEqual(response.status_code, 302)
        self.assertEqual(response.get('location'), delete_url)

        # Assert confirm deletion page is logic
        get_delete_response = self.client.get(delete_url)
        self.assertEqual(get_delete_response.status_code, 200)
        self.assertContains(get_delete_response, "<title>Confirm Deletion</title>")

        # Assert redirect from confirm deletion page to scores index
        post_delete_response = self.client.post(delete_url)
        self.assertEqual(post_delete_response.status_code, 302)
        self.assertEqual(post_delete_response.get('location'), '/scores/')

        # Assert score returns now 404
        get_score_response = self.client.get(f'/scores/{self.score1.id}/')
        self.assertEqual(get_score_response.status_code, 404)

    def test_delete_score_if_already_logged_in(self):
        # Assert score does exist
        get_score_response = self.client.get(f'/scores/{self.score1.id}/')
        self.assertEqual(get_score_response.status_code, 200)
        self.assertContains(get_score_response, "AwesomeComment1")

        # login
        post = self.client.post('/profile/login/', {'username': self.user1.username, 'password': self.user1.clear_pw, })
        self.assertEqual(post.status_code, 302)
        self.assertEqual(post.get('location'), '/profile/')

        # Assert confirm deletion page logic
        delete_url = f'/scores/{self.score1.id}/delete'
        get_delete_response = self.client.get(delete_url)
        self.assertEqual(get_delete_response.status_code, 200)
        self.assertContains(get_delete_response, "<title>Confirm Deletion</title>")

        # Assert redirect from confirm deletion page to scores index
        post_delete_response = self.client.post(delete_url)
        self.assertEqual(post_delete_response.status_code, 302)
        self.assertEqual(post_delete_response.get('location'), '/scores/')

        # Assert score returns now 404
        get_score_response = self.client.get(f'/scores/{self.score1.id}/')
        self.assertEqual(get_score_response.status_code, 404)

    def test_delete_score_if_not_owner(self):
        # Assert score does exist
        get_score_response = self.client.get(f'/scores/{self.score1.id}/')
        self.assertEqual(get_score_response.status_code, 200)
        self.assertContains(get_score_response, "AwesomeComment1")

        # login
        post = self.client.post('/profile/login/',
                                {'username': self.user2.username, 'password': self.user2.clear_pw})
        self.assertRedirects(post, '/profile/')

        # Assert cannot be deleted
        delete_url = f'/scores/{self.score1.id}/delete'
        self.assertRaises(HttpResponseForbidden, self.client.get, delete_url)
        self.assertRaises(HttpResponseForbidden, self.client.post, delete_url)


class UpdateScoreViewTest(SetupScoreData):

    def test_update_score_enforces_login(self):
        # Assert score does exist
        get_score_response = self.client.get(f'/scores/{self.score1.id}/')
        self.assertEqual(get_score_response.status_code, 200)
        self.assertContains(get_score_response, "AwesomeComment1")

        # Assert redirect if not logged in
        update_url = f'/scores/{self.score1.id}/update'
        redirect_response = self.client.get(update_url)
        redirect_url = f'/profile/login/?next={update_url}'
        self.assertRedirects(redirect_response, redirect_url)

        # Assert redirect routes to login page
        response = self.client.get(redirect_url)
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, "<title>Login</title>")

        # Assert post to login page redirects do update page
        response = self.client.post(redirect_url, {
            'username': self.user1.username,
            'password': self.user1.clear_pw,
        })
        self.assertRedirects(response, update_url)

        # Assert confirm update page content
        get_update_response = self.client.get(update_url)
        self.assertEqual(get_update_response.status_code, 200)
        self.assertContains(get_update_response, "Log a Score")
        self.assertContains(get_update_response,
                            '<input type="text" name="score" value="100" maxlength="50" required id="id_score">')
        self.assertContains(get_update_response, '<input type="date" name="execution_date"')
        self.assertContains(get_update_response, '<textarea name="comment" cols="40" rows="10" id="id_comment">')

    def test_update_score_if_already_logged_in(self):
        # Assert score does exist
        get_score_response = self.client.get(f'/scores/{self.score1.id}/')
        self.assertEqual(get_score_response.status_code, 200)
        self.assertContains(get_score_response, "AwesomeComment1")

        # login
        post = self.client.post('/profile/login/', {'username': self.user1.username, 'password': self.user1.clear_pw, })
        self.assertRedirects(post, '/profile/')

        # Assert confirm update page logic
        update_url = f'/scores/{self.score1.id}/update'
        get_update_response = self.client.get(update_url)
        self.assertEqual(get_update_response.status_code, 200)
        self.assertContains(get_update_response, "Log a Score")
        self.assertContains(get_update_response,
                            '<input type="text" name="score" value="100" maxlength="50" required id="id_score">')
        self.assertContains(get_update_response, '<input type="date" name="execution_date"')
        self.assertContains(get_update_response, '<textarea name="comment" cols="40" rows="10" id="id_comment">')

    def test_update_score_if_not_owner(self):
        # Assert score does exist
        get_score_response = self.client.get(f'/scores/{self.score1.id}/')
        self.assertEqual(get_score_response.status_code, 200)
        self.assertContains(get_score_response, "AwesomeComment1")

        # login
        post = self.client.post('/profile/login/',
                                {'username': self.user2.username, 'password': self.user2.clear_pw})
        self.assertRedirects(post, '/profile/')

        # Assert cannot be deleted
        update_url = f'/scores/{self.score1.id}/update'
        self.assertRaises(HttpResponseForbidden, self.client.get, update_url)
        self.assertRaises(HttpResponseForbidden, self.client.post, update_url)
