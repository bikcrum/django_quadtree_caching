# -*- coding: utf-8 -*-
"""
Created on Sun Sep 23 10:19:52 2018

@author: Proshore
"""
import numpy as np

class Point:
    def __init__(self, x, y):
        self.x = x
        self.y = y

class Rectangle:
    def __init__(self, x, y, w, h):
        self.x = x
        self.y = y
        self.w = w
        self.h = h

    def contains(self, point):
        return self.x <= point.x < self.x + self.w and self.y <= point.y < self.y + self.h

    def intersects(self, rect):
        return abs(self.x - rect.x) < (self.w + rect.w) or abs(self.y - rect.y) < (self.y + rect.y)

class QuadTree:
    def __init__(self, boundary, capacity=4):
        self.boundary = boundary
        self.capacity = capacity
        self.points = []
        self.divided = False

    def subdivide(self):
        x = self.boundary.x
        y = self.boundary.y
        w = self.boundary.w
        h = self.boundary.h

        nw = Rectangle(x, y + h / 2, w / 2, h / 2)
        ne = Rectangle(x + w / 2, y + h / 2, w / 2, h / 2)
        sw = Rectangle(x, y, w / 2, h / 2)
        se = Rectangle(x + w / 2, y, w / 2, h / 2)

        self.nw = QuadTree(nw)
        self.ne = QuadTree(ne)
        self.sw = QuadTree(sw)
        self.se = QuadTree(se)

        self.divided = True

    def insert(self, point):
        if not self.boundary.contains(point):
            return False

        if point in self.points:
            return False

        if len(self.points) < self.capacity:
            self.points.append(point)
            return True
        else:
            if not self.divided:
                self.subdivide()
                
            return self.nw.insert(point) or self.ne.insert(point) or self.sw.insert(point) or self.se.insert(point)

    def query(self, range, found):      
        if not self.boundary.intersects(range):
            return
   
        for p in self.points:
            if range.contains(p):
                found.append(p)
     
        if self.divided:
            self.nw.query(range, found)
            self.ne.query(range, found)
            self.sw.query(range, found)
            self.se.query(range, found)