# This file is part of wger Workout Manager.
#
# wger Workout Manager is free software: you can redistribute it and/or modify
# it under the terms of the GNU Affero General Public License as published by
# the Free Software Foundation, either version 3 of the License, or
# (at your option) any later version.
#
# wger Workout Manager is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU General Public License for more details.
#
# You should have received a copy of the GNU Affero General Public License


from django.core.urlresolvers import reverse

from wger.exercises.models import ExerciseCategory
from wger.manager.tests.testcase import WorkoutManagerTestCase
from wger.manager.tests.testcase import WorkoutManagerDeleteTestCase
from wger.manager.tests.testcase import WorkoutManagerEditTestCase
from wger.manager.tests.testcase import WorkoutManagerAddTestCase


class RobotsExclusionMiddlewareTestCase(WorkoutManagerTestCase):
    '''
    Teststhe robots exclusion middleware
    '''

    def test_middleware_manager(self):
        '''
        Test the middleware on URLs from manager app
        '''

        response = self.client.get(reverse('dashboard'))
        self.assertTrue(response.get('X-Robots-Tag'))

        response = self.client.get(reverse('workout-overview'))
        self.assertTrue(response.get('X-Robots-Tag'))

        response = self.client.get(reverse('schedule-overview'))
        self.assertTrue(response.get('X-Robots-Tag'))

        response = self.client.get(reverse('feedback'))
        self.assertTrue(response.get('X-Robots-Tag'))

        response = self.client.get(reverse('about'))
        self.assertTrue(response.get('X-Robots-Tag'))

        response = self.client.get(reverse('contact'))
        self.assertFalse(response.get('X-Robots-Tag'))

    def test_middleware_software(self):
        '''
        Test the middleware on URLs from software app
        '''

        for i in ('features', 'issues', 'changelog', 'license', 'code', 'contribute'):
            response = self.client.get(reverse('software:{0}'.format(i)))
            self.assertFalse(response.get('X-Robots-Tag'))

    def test_middleware_nutrition(self):
        '''
        Test the middleware on URLs from nutrition app
        '''

        response = self.client.get(reverse('ingredient-list'))
        self.assertFalse(response.get('X-Robots-Tag'))

        response = self.client.get(reverse('ingredient-view', kwargs={'id': 1}))
        self.assertFalse(response.get('X-Robots-Tag'))

        response = self.client.get(reverse('nutrition-overview'))
        self.assertTrue(response.get('X-Robots-Tag'))

    def test_middleware_exercises(self):
        '''
        Test the middleware on URLs from exercises app
        '''

        response = self.client.get(reverse('exercise-overview'))
        self.assertFalse(response.get('X-Robots-Tag'))

        response = self.client.get(reverse('exercise-view', kwargs={'id': 1}))
        self.assertFalse(response.get('X-Robots-Tag'))

        response = self.client.get(reverse('muscle-overview'))
        self.assertFalse(response.get('X-Robots-Tag'))
