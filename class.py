#!/usr/bin/python

import subprocess
import os
import sys

class Animal :
    __age = 0
    __name = ''

    def __init__(self, name, age):
        self.__name = name
        self.__age = age
        print( self.whoami())

    def whoami():
        print( "I am an animal of name {} and age {}".format(get_name(), get_age()) )

    def set_name(self, name):
        self.__name = name

    def set_age(self, age):
        self.__age = age

    def get_age(self):
        return self.__age

    def get_name(self):
        return self.__name

class Dog(Animal):

    __color = None

    def __init__(self, name, age, color):
        print( 'Constructor of Dog' )
        self.__color = color
        super(Dog, self).__init__(name, age)

    def get_age_orig(self):
        print( 'got age' )

    def get_color(self):
        return self.__color

    def whoami(self):
        print( "I am a dog of name {} and age {} and color {}"
              .format(self.get_name(), self.get_age(), self.get_color() ) )

ant = Dog('fik', 23, 'black' )
ant.set_age(34)
print( ant.get_name() )
