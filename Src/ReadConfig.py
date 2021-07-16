#!/usr/bin/python
# -*- coding: utf-8 -*-
import configparser
import os
dir_path = os.path.dirname(os.path.realpath(__file__))

settings = configparser.ConfigParser()
settings.read('{}/Config.ini'.format(dir_path))
# configValues will contains details of all items declared in config file
global configValues
configValues = {}
for section in settings.sections():
    for key in settings[section]:
        configValues[key.upper()] = settings[section][key]

configValues
