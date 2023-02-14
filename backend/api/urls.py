from django.urls import path
from . import views

urlpatterns = [
    path("", views.index, name="index"),
    path("genres/", views.genres, name="genres"),
    path("stories/", views.stories, name="stories"),
    path("showcase/", views.showcase, name="showcase"),
    path("genre/<str:genre>/", views.genre, name="genre"),
    path("story/<uuid:uuid>/", views.story, name="story"),

    path("like/", views.like, name="like"),
    path("unlike/", views.unlike, name="unlike"),

    path("admin/overview/", views.story_overview, name="overview"),
    path("admin/add-story/", views.add_story, name="add-story"),
    path("admin/edit-story/", views.edit_story, name="edit-story"),
    path("admin/rmv-story/", views.rmv_story, name="rmv-story"),

    path("admin/get-storyline/<uuid:uuid>/", views.get_storyline, name="get-storyline"),
    path("admin/add-storyline/", views.add_storyline, name="add-storyline"),
    path("admin/add-to-storyline/", views.add_to_storyline, name="add-to-storyline"),
    path("admin/rmv-storyline/", views.rmv_storyline, name="rmv-storyline"),

    path("is-admin/", views.is_admin, name="is-admin"),
]