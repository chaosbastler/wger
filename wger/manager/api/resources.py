# -*- coding: utf-8 -*-

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

from tastypie import fields
from tastypie.authentication import ApiKeyAuthentication
from tastypie.resources import ModelResource

from django.contrib.auth.models import User

from wger.exercises.api.resources import ExerciseResource
from wger.utils.resources import UserObjectsOnlyAuthorization

from wger.manager.models import UserProfile
from wger.manager.models import Workout
from wger.manager.models import Schedule
from wger.manager.models import ScheduleStep
from wger.manager.models import DaysOfWeek
from wger.manager.models import Day
from wger.manager.models import Set
from wger.manager.models import Setting
from wger.manager.models import WorkoutLog


#
# User related resources
#
class UserProfileResource(ModelResource):
    '''
    Resource for user profiles
    '''

    def authorized_read_list(self, object_list, bundle):
        '''
        Filter to own objects
        '''
        return object_list.filter(user=bundle.request.user)

    class Meta:
        queryset = UserProfile.objects.all()
        authentication = ApiKeyAuthentication()
        authorization = UserObjectsOnlyAuthorization()


#
# Workout related resources
#
class WorkoutResource(ModelResource):
    '''
    Resource for workouts
    '''

    days = fields.ToManyField('wger.manager.api.resources.DayResource', 'day_set')

    def authorized_read_list(self, object_list, bundle):
        '''
        Filter to own objects
        '''
        return object_list.filter(user=bundle.request.user)

    class Meta:
        queryset = Workout.objects.all()
        authentication = ApiKeyAuthentication()
        authorization = UserObjectsOnlyAuthorization()


class ScheduleStepResource(ModelResource):
    '''
    Resource for schedule steps
    '''

    workout = fields.ToOneField(WorkoutResource, 'workout')

    def authorized_read_list(self, object_list, bundle):
        '''
        Filter to own objects
        '''
        return object_list.filter(schedule__user=bundle.request.user)

    class Meta:
        queryset = ScheduleStep.objects.all()
        authentication = ApiKeyAuthentication()
        authorization = UserObjectsOnlyAuthorization()


class ScheduleResource(ModelResource):
    '''
    Resource for schedules
    '''

    steps = fields.ToManyField(ScheduleStepResource, 'schedulestep_set')

    def authorized_read_list(self, object_list, bundle):
        '''
        Filter to own objects
        '''
        return object_list.filter(user=bundle.request.user)

    class Meta:
        queryset = Schedule.objects.all()
        authentication = ApiKeyAuthentication()
        authorization = UserObjectsOnlyAuthorization()


class DaysOfWeekResource(ModelResource):
    '''
    Resource for days of the week
    '''

    class Meta:
        queryset = DaysOfWeek.objects.all()


class DayResource(ModelResource):
    '''
    Resource for training days
    '''

    workout = fields.ToOneField(WorkoutResource, 'training')
    days_of_week = fields.ToManyField(DaysOfWeekResource, 'day')

    def authorized_read_list(self, object_list, bundle):
        '''
        Filter to own objects
        '''
        return object_list.filter(training__user=bundle.request.user)

    class Meta:
        queryset = Day.objects.all()
        authentication = ApiKeyAuthentication()
        authorization = UserObjectsOnlyAuthorization()


class SetResource(ModelResource):
    '''
    Resource for training sets
    '''

    day = fields.ToOneField(DayResource, 'exerciseday')
    exercises = fields.ToManyField(ExerciseResource, 'exercises')

    def authorized_read_list(self, object_list, bundle):
        '''
        Filter to own objects
        '''
        return object_list.filter(exerciseday__training__user=bundle.request.user)

    class Meta:
        queryset = Set.objects.all()
        authentication = ApiKeyAuthentication()
        authorization = UserObjectsOnlyAuthorization()


class SettingResource(ModelResource):
    '''
    Resource for training settings
    '''

    set = fields.ToOneField(SetResource, 'set')
    exercise = fields.ToOneField(ExerciseResource, 'exercise')

    def authorized_read_list(self, object_list, bundle):
        '''
        Filter to own objects
        '''
        return object_list.filter(set__exerciseday__training__user=bundle.request.user)

    class Meta:
        queryset = Setting.objects.all()
        authentication = ApiKeyAuthentication()
        authorization = UserObjectsOnlyAuthorization()


class WorkoutLogResource(ModelResource):
    '''
    Resource for a workout log
    '''

    exercise = fields.ToOneField(ExerciseResource, 'exercise')
    workout = fields.ToOneField(WorkoutResource, 'workout')

    def authorized_read_list(self, object_list, bundle):
        '''
        Filter to own objects
        '''
        return object_list.filter(user=bundle.request.user)

    class Meta:
        queryset = WorkoutLog.objects.all()
        authentication = ApiKeyAuthentication()
        authorization = UserObjectsOnlyAuthorization()