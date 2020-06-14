from abc import ABC

from django.contrib.auth.models import User
from django.http import HttpResponseForbidden
from django.test import TestCase

from athletes.models import Athlete
from scores.models import Score
from wods.models import Workout
from wods.views import HttpResponseNotAllowedException


class SetupWorkoutData(ABC, TestCase):

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

        cls.wod1 = Workout.objects.create(name="AwesomeWod1", description="AwesomeDescription", creator=athlete1)

        cls.wod2 = Workout.objects.create(name="AwesomeWod2", description="AwesomeDescription", creator=athlete1)
        cls.score2 = Score.objects.create(athlete=athlete1, workout=cls.wod2, score="2100", comment="AwesomeComment1")

        cls.wod3 = Workout.objects.create(name="AwesomeWod3", description="AwesomeDescription", creator=athlete1)
        cls.score1 = Score.objects.create(athlete=athlete1, workout=cls.wod3, score="3100", comment="AwesomeComment1")
        cls.score2 = Score.objects.create(athlete=athlete2, workout=cls.wod3, score="3200", comment="AwesomeComment2")


class NoDataWorkoutView(TestCase):

    def test_workout_list(self):
        response = self.client.get('/wods/')
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, "No Workouts are available.")


class DataFilledWorkoutViewNotLoggedIn(SetupWorkoutData):

    def test_workouts_list(self):
        response = self.client.get('/wods/')

        self.assertEqual(response.status_code, 200)
        self.assertContains(response, "Workout list")
        self.assertContains(response, "last_name1, first_name1")
        self.assertContains(response, "AwesomeWod1")
        self.assertContains(response, "AwesomeWod2")
        self.assertContains(response, "AwesomeWod3")
        self.assertEqual(3, len(response.context_data['workout_list']))

    def test_workout_detail_no_scores(self):
        response = self.client.get(f'/wods/{self.wod1.id}/')

        self.assertEqual(response.status_code, 200)
        self.assertContains(response, "CREATED BY:")
        self.assertContains(response, "last_name1, first_name1")
        self.assertContains(response, "AT:")
        self.assertContains(response, "DESC: AwesomeDescription")
        self.assertContains(response, "SCORES:")
        self.assertContains(response, "No scores yet! Be the first!")

    def test_workout_detail_with_scores(self):
        response = self.client.get(f'/wods/{self.wod3.id}/')

        self.assertEqual(response.status_code, 200)
        self.assertContains(response, "CREATED BY:")
        self.assertContains(response, "last_name1, first_name1")
        self.assertContains(response, "AT:")
        self.assertContains(response, "DESC: AwesomeDescription")
        self.assertContains(response, "SCORES:")
        self.assertEqual(2, len(response.context_data['scores']))

    def test_workout_editable_if_owner(self):
        response = self.client.post('/profile/login/',
                                    {'username': self.user1.username,
                                     'password': self.user1.clear_pw,
                                     })
        self.assertRedirects(response, '/profile/')

        response = self.client.get(f'/wods/{self.wod1.id}/')

        self.assertEqual(response.status_code, 200)
        self.assertContains(response, "edit workout")
        self.assertContains(response, "delete workout")

    def test_workout_not_editable_if_not_owner(self):
        response = self.client.post('/profile/login/',
                                    {'username': self.user2.username,
                                     'password': self.user2.clear_pw,
                                     })
        self.assertRedirects(response, '/profile/')
        response = self.client.get(f'/wods/{self.wod1.id}/')

        self.assertEqual(response.status_code, 200)
        self.assertNotContains(response, "edit score")
        self.assertNotContains(response, "delete score")


class DeleteWorkoutViewTest(SetupWorkoutData):

    def test_delete_workout_enforces_login(self):
        # Assert workout does exist
        get_workout_response = self.client.get(f'/wods/{self.wod1.id}/')
        self.assertEqual(get_workout_response.status_code, 200)
        self.assertContains(get_workout_response, "AwesomeWod1")

        # Assert redirect if not logged in
        redirect_response = self.client.get(f'/wods/{self.wod1.id}/delete')
        delete_url = f'/wods/{self.wod1.id}/delete'
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
        self.assertRedirects(response, delete_url)

        # Assert confirm deletion page is logic
        get_delete_response = self.client.get(delete_url)
        self.assertEqual(get_delete_response.status_code, 200)
        self.assertContains(get_delete_response, "Do you really want to delete this Workout?")

        # Assert redirect from confirm deletion page to scores index
        post_delete_response = self.client.post(delete_url)
        self.assertRedirects(post_delete_response, '/wods/')

        # Assert score returns now 404
        get_workout_response = self.client.get(f'/wods/{self.wod1.id}/')
        self.assertEqual(get_workout_response.status_code, 404)

    def test_delete_workout_if_already_logged_in(self):
        # Assert score does exist
        get_workout_response = self.client.get(f'/wods/{self.wod1.id}/')
        self.assertEqual(get_workout_response.status_code, 200)
        self.assertContains(get_workout_response, "AwesomeWod1")

        # login
        post = self.client.post('/profile/login/', {'username': self.user1.username, 'password': self.user1.clear_pw, })
        self.assertRedirects(post, '/profile/')

        # Assert confirm deletion page logic
        delete_url = f'/wods/{self.wod1.id}/delete'
        get_delete_response = self.client.get(delete_url)
        self.assertEqual(get_delete_response.status_code, 200)
        self.assertContains(get_delete_response, "Do you really want to delete this Workout?")

        # Assert redirect from confirm deletion page to scores index
        post_delete_response = self.client.post(delete_url)
        self.assertRedirects(post_delete_response, '/wods/')

        # Assert score returns now 404
        get_workout_response = self.client.get(f'/wods/{self.wod1.id}/')
        self.assertEqual(get_workout_response.status_code, 404)

    def test_delete_workout_if_not_owner(self):
        # Assert workout does exist
        get_workout_response = self.client.get(f'/wods/{self.wod1.id}/')
        self.assertEqual(get_workout_response.status_code, 200)
        self.assertContains(get_workout_response, "AwesomeWod1")

        # login
        post = self.client.post('/profile/login/',
                                {'username': self.user2.username, 'password': self.user2.clear_pw})
        self.assertRedirects(post, '/profile/')

        # Assert cannot be deleted
        delete_url = f'/wods/{self.wod1.id}/delete'
        self.assertRaises(HttpResponseForbidden, self.client.get, delete_url)
        self.assertRaises(HttpResponseForbidden, self.client.post, delete_url)

    def test_delete_workout_if_only_creator_logged_scores(self):
        # Assert workout does exist
        get_workout_response = self.client.get(f'/wods/{self.wod2.id}/')
        self.assertEqual(get_workout_response.status_code, 200)
        self.assertContains(get_workout_response, "AwesomeWod2")

        # login
        post = self.client.post('/profile/login/',
                                {'username': self.user1.username, 'password': self.user1.clear_pw})
        self.assertRedirects(post, '/profile/')

        # Assert confirm deletion page
        delete_url = f'/wods/{self.wod2.id}/delete'
        get_delete_response = self.client.get(delete_url)
        self.assertEqual(get_delete_response.status_code, 200)
        self.assertContains(get_delete_response, "Do you really want to delete this Workout?")

        # Assert redirect from confirm deletion page to scores index
        post_delete_response = self.client.post(delete_url)
        self.assertRedirects(post_delete_response, '/wods/')

        # Assert score returns now 404
        get_workout_response = self.client.get(f'/wods/{self.wod2.id}/')
        self.assertEqual(get_workout_response.status_code, 404)

    def test_delete_workout_not_possible_if_other_athlete_logged_score(self):
        # Assert workout does exist
        get_workout_response = self.client.get(f'/wods/{self.wod3.id}/')
        self.assertEqual(get_workout_response.status_code, 200)
        self.assertContains(get_workout_response, "AwesomeWod3")

        # login
        post = self.client.post('/profile/login/',
                                {'username': self.user1.username, 'password': self.user1.clear_pw})
        self.assertRedirects(post, '/profile/')

        # Assert confirm deletion page does not allow deletion
        delete_url = f'/wods/{self.wod3.id}/delete'
        get_delete_response = self.client.get(delete_url)
        self.assertEqual(get_delete_response.status_code, 200)
        self.assertContains(get_delete_response, "This workout has scores by other people so you cannot delete it!")

        # Assert raise error
        self.assertRaises(HttpResponseNotAllowedException, self.client.post, delete_url)


class UpdateWorkoutViewTest(SetupWorkoutData):

    def test_update_workout_enforces_login(self):
        # Assert workout does exist
        get_workout_response = self.client.get(f'/wods/{self.wod1.id}/')
        self.assertEqual(get_workout_response.status_code, 200)
        self.assertContains(get_workout_response, "AwesomeWod1")

        # Assert redirect if not logged in
        update_url = f'/wods/{self.wod1.id}/update'
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
        self.assertContains(get_update_response, "Update this workout")

    def test_update_workout_if_already_logged_in(self):
        # Assert workout does exist
        get_workout_response = self.client.get(f'/wods/{self.wod1.id}/')
        self.assertEqual(get_workout_response.status_code, 200)
        self.assertContains(get_workout_response, "AwesomeWod1")

        # login
        post = self.client.post('/profile/login/', {'username': self.user1.username, 'password': self.user1.clear_pw, })
        self.assertRedirects(post, '/profile/')

        # Assert confirm update page logic
        update_url = f'/wods/{self.wod1.id}/update'
        get_update_response = self.client.get(update_url)
        self.assertEqual(get_update_response.status_code, 200)
        self.assertContains(get_update_response, "Update this workout")

    def test_update_workout_if_not_owner(self):
        # Assert workout does exist
        get_workout_response = self.client.get(f'/wods/{self.wod1.id}/')
        self.assertEqual(get_workout_response.status_code, 200)
        self.assertContains(get_workout_response, "AwesomeWod1")

        # login
        post = self.client.post('/profile/login/',
                                {'username': self.user2.username, 'password': self.user2.clear_pw})
        self.assertRedirects(post, '/profile/')

        # Assert cannot be deleted
        update_url = f'/wods/{self.wod1.id}/update'
        self.assertRaises(HttpResponseForbidden, self.client.get, update_url)
        self.assertRaises(HttpResponseForbidden, self.client.post, update_url)

    def test_update_workout_not_possible_if_other_athlete_logged_score(self):
        # Assert workout does exist
        get_workout_response = self.client.get(f'/wods/{self.wod3.id}/')
        self.assertEqual(get_workout_response.status_code, 200)
        self.assertContains(get_workout_response, "AwesomeWod3")

        # login
        post = self.client.post('/profile/login/',
                                {'username': self.user1.username, 'password': self.user1.clear_pw})
        self.assertRedirects(post, '/profile/')

        # Assert confirm deletion page does not allow deletion
        delete_url = f'/wods/{self.wod3.id}/update'
        get_delete_response = self.client.get(delete_url)
        self.assertEqual(get_delete_response.status_code, 200)
        self.assertContains(get_delete_response, "This workout has scores by other people so you cannot update it!")

        # Assert raise error
        self.assertRaises(HttpResponseNotAllowedException, self.client.post, delete_url)


class CreateWorkoutView(SetupWorkoutData):

    def test_create_workout_enforces_login(self):
        create_url = '/wods/create/'
        get_create_response = self.client.get(create_url)
        self.assertRedirects(get_create_response, '/profile/login/?next=/wods/create/')

    def test_create_workout_logged_in(self):
        # login
        post = self.client.post('/profile/login/', {'username': self.user1.username, 'password': self.user1.clear_pw, })
        self.assertRedirects(post, '/profile/')

        # Assert confirm deletion page logic
        create_url = '/wods/create/'
        get_create_response = self.client.get(create_url)
        self.assertEqual(get_create_response.status_code, 200)
        self.assertContains(get_create_response, "Workout")
        self.assertContains(get_create_response, "Description:")
        self.assertContains(get_create_response, "Type:")
        self.assertContains(get_create_response, "Name:")
        self.assertContains(get_create_response, '<input type="submit" value="Save">')

        # Assert redirect from confirm deletion page to scores index
        post_create_response = self.client.post(create_url, {
            'description': 'wod_description',
            'type': 'EMOM',
            'name': 'wod_name',
        })
        self.assertTrue(post_create_response.status_code, 302)
        post_url = post_create_response.get('location')
        self.assertIn('/wods/', post_url)

        # Assert wod created
        get_workout_response = self.client.get(post_url)
        self.assertEqual(get_workout_response.status_code, 200)
        self.assertContains(get_workout_response, 'wod_description')
        self.assertContains(get_workout_response, 'EMOM')
        self.assertContains(get_workout_response, 'wod_name')


class AddScoreToWorkoutView(SetupWorkoutData):
    pass
