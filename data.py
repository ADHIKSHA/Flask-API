"""Routines associated with the application data.
"""
import json
courses = []
def load_data():
    """Load the data from the json file.
    """
    f = open('json/course.json',)
    data=json.load(f)
    for i in data: 
    	courses.append(i)

    pass