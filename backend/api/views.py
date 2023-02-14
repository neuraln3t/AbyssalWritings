from django.shortcuts import render
from rest_framework.decorators import api_view, permission_classes, authentication_classes
from rest_framework.views import Response
from rest_framework.permissions import IsAuthenticated, IsAdminUser

import random

from .serializers import StorySerializer, StoryLineSerializer, GenreSerializer
from .models import Story, StoryLine, Genre

# Create your views here.
@api_view(["GET"])
def index(request):
    newest = Story.objects.filter(active=True).order_by("-date")[:3]
    fav = Genre.objects.all() # Should be Horror, Thriller

    serialized_newest = StorySerializer(newest, many=True)
    serialized_fav = GenreSerializer(fav, many=True)

    return Response({
        "newest": serialized_newest.data,
        "fav": serialized_fav.data
    })

@api_view(["GET"])
def showcase(request):
    story = random.choice(Story.objects.filter(active=True))

    serialized = StorySerializer(story)
    return Response(serialized.data)

@api_view(["GET"])
def stories(request):
    stories = Story.objects.filter(active=True)
    serialized = StorySerializer(stories, many=True)

    return Response(serialized.data)

@api_view(["GET"])
def genres(request):
    genres = Genre.objects.all()
    serialized = GenreSerializer(genres, many=True)

    return Response(serialized.data)

@api_view(["GET"])
def genre(request, genre):
    genre = Genre.objects.filter(name=genre)

    if genre.exists():
        serialized = GenreSerializer(genre.first())

        stories = Story.objects.filter(genre=genre.first(), active=True)
        serialized_stories = StorySerializer(stories, many=True)

        return Response({
            "genre": serialized.data,
            "stories": serialized_stories.data
        })

@api_view(["GET"])
def story(request, uuid):
    story = Story.objects.filter(uuid=uuid)

    if story.exists():
        serialized = StorySerializer(story.first())
        return Response(serialized.data)

@api_view(["PUT"])
@permission_classes([IsAuthenticated])
def like(request):
    uuid = request.data.get("uuid")
    story = Story.objects.filter(uuid=uuid)

    if story.exists():
        story = story.first()
        story.hearts += 1
        story.save()

        return Response(status=200)

@api_view(["PUT"])
@permission_classes([IsAuthenticated])
def unlike(request):
    uuid = request.data.get("uuid")
    story = Story.objects.filter(uuid=uuid)

    if story.exists():
        story = story.first()
        story.hearts -= 1
        story.save()

        return Response(status=200)
    
### ADMIN ###
@api_view(["GET"])
@permission_classes([IsAdminUser])
def story_overview(request):
    stories = Story.objects.all()
    serialized_stories = StorySerializer(stories, many=True)

    storylines = StoryLine.objects.all()
    serialized_storylines = StoryLineSerializer(storylines, many=True)

    return Response({
        "stories": serialized_stories.data,
        "storylines": serialized_storylines.data
    })

### Stories ###

@api_view(["GET"])
@permission_classes([IsAdminUser])
def get_storyline(request, uuid):   # Takes story UUID and gets storyline
    story = Story.objects.filter(uuid=uuid)
    storyline = StoryLine.objects.filter(stories__in=[story])

    if storyline.exists():
        serializer = StoryLineSerializer(storyline.first())

        return Response(serializer.data)
    
    return Response(status=404)


@api_view(["POST"])
@permission_classes([IsAdminUser])
def add_story(request):
    print(request.data)
    serializer = StorySerializer(data=request.data, files=request.FILES, context={"request": request})
    if serializer.is_valid(raise_exception=True):
        story = serializer.save()
        
        serialized = StorySerializer(story)
        return Response(serialized.data)

@api_view(["DELETE"])
@permission_classes([IsAdminUser])
def rmv_story(request):
    uuid = request.data.get("uuid")
    story = Story.objects.filter(uuid=uuid)
    
    if story.exists():
        story.first().remove()

        return Response(status=200)

@api_view(["PUT"])
@permission_classes([IsAdminUser])
def edit_story(request):
    uuid = request.data.get("uuid")
    story = Story.objects.filter(uuid=uuid)
    if story.exists():
        story = story.first()
        title = request.data.get("title")
        content = request.data.get("content")
        
        if title != None:
            story.title = title
            story.save()
        
        if content != None:
            story.content = content
            story.save()

        serialized = StorySerializer(story)
        return Response(serialized.data)

### Storylines ###

@api_view(["POST"])
@permission_classes([IsAdminUser])
def add_storyline(request):
    serializer = StoryLineSerializer(data=request.data, context={"request": request})
    if serializer.is_valid():
        storyline = serializer.save()

        serialized = StoryLineSerializer(storyline)
        return Response(serialized.data)

@api_view(["PUT"])
@permission_classes([IsAdminUser])
def add_to_storyline(request):
    sl = request.data.get("storyline")
    s = request.data.get("story")
    
    storyline = StoryLine.objects.filter(uuid=sl)
    if storyline.exists():
        story = Story.objects.filter(uuid=s)
        if story.exists():
            storyline.first().stories.add(story.first())

@api_view(["DELETE"])
@permission_classes([IsAdminUser])
def rmv_storyline(request):
    uuid = request.data.get("uuid")
    storyline = StoryLine.objects.filter(uuid=uuid)
    
    if storyline.exists():
        for story in storyline.stories.all():
            story.remove()
        
        storyline.remove()
        
        return Response(status=200)

### Guards ###

@api_view(["GET"])
@permission_classes([IsAdminUser])
def is_admin(request):
    return Response(status=200)