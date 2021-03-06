from django.shortcuts import render
from django.http import HttpResponse, Http404
import json
from .models import User, Location
from .utils.quadtree import QuadTree, Rectangle, Point
import random
from time import time
import string

from django.core.cache import cache

def index(request):
    points = []
    no_of_points = 1000

    if cache.get('no_of_points') == None or cache.get('no_of_points') != no_of_points:
        cache.clear()
        cache.set('no_of_points', no_of_points, None)

    quadtree = cache.get('quadtree')
    boundary = Rectangle(-180, -90, 360, 180)

    if quadtree == None:
        print('no cache for quadtree available')
        quadtree = QuadTree(boundary=boundary)
        for _ in range(no_of_points):
            point = Point(x=random.randint(-180, 181), y=random.randint(-90, 91))
            quadtree.insert(point)
            points.append(point)

        print('created quadtree')

        cache.set('quadtree', quadtree, None)
        cache.set('points', points, None)
    else:
        print('quadtree loaded from cache')
        points = cache.get('points')

    w = random.randint(25, 101)
    h = random.randint(25, 101)
    x = random.randint(-180, -180 + boundary.w - w)
    y = random.randint(-90, -90 + boundary.h - h)

    bound = Rectangle(x, y, w, h)

    # QUADTREE SEARCH #
    found = []
    start_time = time()

    quadtree.query(bound, found)
    time_taken = time() - start_time

    print('total time taken for quadtree = %.20f to find %d location from %d locations' %
          (time_taken, len(found), len(points)))

    # NORMAL/LINEAR SEARCH #
    found = []
    start_time = time()
    for point in points:
        if bound.contains(point):
            found.append(point)

    time_taken = time() - start_time
    print('total time taken for normal search = %.20f to find %d location from %d locations' %
          (time_taken, len(found), len(points)))

    context = {}
    return render(request, 'quadtree/index.html', context)

def clear_cache(request):
    cache.clear()
    context = {}
    return render(request, 'quadtree/index.html', context)

def create_random_user(request, count=1):
    for _ in range(count):
        name = ''.join(random.choices(string.ascii_lowercase, k=5))
        user = User(name=name)
        user.save()

        lat = random.random() * 90 * ((-1) ** random.randint(0, 1))
        lng = random.random() * 180 * ((-1) ** random.randint(0, 1))
        location = Location(user=user, latitude=lat, longitude=lng)
        location.save()

    context = {}
    return render(request, 'quadtree/index.html', context)
