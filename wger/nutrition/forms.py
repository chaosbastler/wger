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

import logging

from django import forms
from django.utils.translation import ugettext as _

from wger.nutrition.models import IngredientWeightUnit
from wger.manager.models import UserProfile


logger = logging.getLogger('wger.custom')


class UnitChooserForm(forms.Form):
    '''
    A small form to select an amount and a unit for an ingredient
    '''
    amount = forms.DecimalField(decimal_places=2,
                                max_digits=5,
                                localize=True)
    unit = forms.ModelChoiceField(queryset=IngredientWeightUnit.objects.none(),
                                  empty_label="g",
                                  required=False)

    def __init__(self, *args, **kwargs):
        super(UnitChooserForm, self).__init__(*args, **kwargs)

        if len(args) and args[0]['ingredient']:
            ingredient_id = args[0]['ingredient']

        elif kwargs.get('data'):
            ingredient_id = kwargs['data']['ingredient_id']

        else:
            ingredient_id = -1

        self.fields['unit'].queryset = IngredientWeightUnit.objects.filter(
            ingredient_id=ingredient_id).select_related()


class BmiForm(forms.ModelForm):
    weight = forms.DecimalField()

    class Meta:
        model = UserProfile
        fields = ('height', )


class BmrForm(forms.ModelForm):
    '''
    Form for the basal metabolic rate
    '''
    weight = forms.DecimalField()

    class Meta:
        model = UserProfile
        fields = ('age', 'height', 'gender')


class PhysicalActivitiesForm(forms.ModelForm):
    '''
    Form for the additional physical activities
    '''
    class Meta:
        model = UserProfile
        fields = ('sleep_hours',
                  'work_hours',
                  'work_intensity',
                  'sport_hours',
                  'sport_intensity',
                  'freetime_hours',
                  'freetime_intensity')


class DailyCaloriesForm(forms.ModelForm):
    '''
    Form for the total daily calories needed
    '''

    base_calories = forms.IntegerField(label=_('Basic caloric intake'),
                                       help_text=_('Your basic caloric intake as calculated for '
                                                   'your data'),
                                       required=False)
    additional_calories = forms.IntegerField(label=_('Additional calories'),
                                             help_text=_('Additional calories to add to the base '
                                                         'rate (to substract, enter a negative '
                                                         'number)'),
                                             initial=0,
                                             required=False)

    class Meta:
        model = UserProfile
        fields = ('calories',)
