from django.conf.urls import patterns, url
from django.contrib.auth.decorators import login_required

from wger.exercises.views import exercises
from wger.exercises.views import comments
from wger.exercises.views import categories
from wger.exercises.views import muscles

urlpatterns = patterns('wger.exercises.views',

    # Exercises
    url(r'^overview/$',
        'exercises.overview',
        name='exercise-overview'),

    url(r'^search/$', 'exercises.search'),
    url(r'^(?P<id>\d+)/view/$',
        'exercises.view',
        name='exercise-view'),
    url(r'^(?P<id>\d+)/view/(?P<slug>[-\w]+)/$',
        'exercises.view',
        name='exercise-view-slug'),
    url(r'^add/$',
        login_required(exercises.ExerciseAddView.as_view()),
        name='exercise-add'),
    url(r'^(?P<pk>\d+)/edit/$',
        exercises.ExerciseUpdateView.as_view(),
        name='exercise-edit'),
    url(r'^(?P<pk>\d+)/delete/$',
        exercises.ExerciseDeleteView.as_view(),
        name='exercise-delete'),
    url(r'^pending/$',
        exercises.PendingExerciseListView.as_view(),
        name='exercise-pending'),
    url(r'^(?P<pk>\d+)/accept/$',
        'exercises.accept',
        name='exercise-accept'),
    url(r'^(?P<pk>\d+)/decline/$',
        'exercises.decline',
        name='exercise-decline'),

    # Muscles
    url(r'^muscle/overview/$',
        muscles.MuscleListView.as_view(),
        name='muscle-overview'),
    url(r'^muscle/add/$',
        muscles.MuscleAddView.as_view(),
        name='muscle-add'),
    url(r'^muscle/(?P<pk>\d+)/edit/$',
        muscles.MuscleUpdateView.as_view(),
        name='muscle-edit'),
    url(r'^muscle/(?P<pk>\d+)/delete/$',
        muscles.MuscleDeleteView.as_view(),
        name='muscle-delete'),

    # Comments
    url(r'^(?P<exercise_pk>\d+)/comment/add/$',
        comments.ExerciseCommentAddView.as_view(),
        name='exercisecomment-add'),
    url(r'^comment/(?P<pk>\d+)/edit/$',
        comments.ExerciseCommentEditView.as_view(),
        name='exercisecomment-edit'),
    url(r'^comment/(?P<id>\d+)/delete/$',
        'comments.delete',
        name='exercisecomment-delete'),

    # Categories
    url(r'^category/(?P<pk>\d+)/edit/$',
        categories.ExerciseCategoryUpdateView.as_view(),
        name='exercisecategory-edit'),
    url(r'^category/add/$',
        categories.ExerciseCategoryAddView.as_view(),
        name='exercisecategory-add'),
    url(r'^category/(?P<pk>\d+)/delete/$',
        categories.ExerciseCategoryDeleteView.as_view(),
        name='exercisecategory-delete'),
)
