"""Routes for the course resource.
"""

from run import app
from flask import request
from flask import Response
from http import HTTPStatus
from data import *
import json
load_data()

def binary_search(arr, low, high, x):
 
    # Check base case
    if high >= low:
 
        mid = (high + low) // 2
 
        # If element is present at the middle itself
        if arr[mid]["id"] == x:
            return mid
 
        # If element is smaller than mid, then it can only
        # be present in left subarray
        elif arr[mid]["id"] > x:
            return binary_search(arr, low, mid - 1, x)
 
        # Else the element can only be present in right subarray
        else:
            return binary_search(arr, mid + 1, high, x)
 
    else:
        # Element is not present in the array
        return -1

def search_title (name):
    result=[]
    for keyval in courses:
        if name.lower() in keyval['title'].lower():
            result.append(keyval)
    return result


@app.route("/course/<int:id>", methods=['GET'])
def get_course(id):
    """Get a course by id.

    :param int id: The record id.
    :return: A single course (see the challenge notes for examples)
    :rtype: object
    """

    """
    -------------------------------------------------------------------------
    Challenge notes:
    -------------------------------------------------------------------------   
    1. Bonus points for not using a linear scan on your data structure.
    """
    # YOUR CODE HERE
    found = binary_search(courses,0,len(courses)-1,int(id))
    val ={}
    if found!=-1:
        response = Response(
            response=json.dumps({"data" : courses[found]}),
            status=200,
            mimetype='application/json'
            )
        return response
    else:
        res = "Course "+str(id)+" does not exist"
        response = Response(
            response=json.dumps({"messge" : res}),
            status=404,
            mimetype='application/json'
            )
        return response


@app.route("/course", methods=['GET'])
def get_courses():
    """Get a page of courses, optionally filtered by title words (a list of
    words separated by commas".

    Query parameters: page-number, page-size, title-words
    If not present, we use defaults of page-number=1, page-size=10

    :return: A page of courses (see the challenge notes for examples)
    :rtype: object
    """

    """
    -------------------------------------------------------------------------
    Challenge notes:
    ------------------------------------------------------------------------- 
    1. Bonus points for not using a linear scan, on your data structure, if
       title-words is supplied
    2. Bonus points for returning resulted sorted by the number of words which
       matched, if title-words is supplied.
    3. Bonus points for including performance data on the API, in terms of
       requests/second.
    """
    # YOUR CODE HERE
    pagenumber = request.args.get("page-number", default = 1, type = int)
    pagesize = request.args.get("page-size", default = 10, type = int)
    titlewords= request.args.get("title-words", default = "", type = str)
    final=[]
    if titlewords!= "":
        for i in titlewords.split(','):
            res = search_title(str(i))
            final.extend(res)
    else:
        final = courses
    
    total_res = len(final)
    total_pages = total_res /pagesize

    mets = {}
    mets["page_count"]=total_pages
    mets["page_number"]=pagenumber
    mets["page_size"]=pagesize
    mets["record_count"]= total_res
    start = pagesize*(pagenumber-1)
    end = pagesize*pagenumber
    final = final[start:end]

    response = app.response_class(
            response=json.dumps({"data" : final,"metadata" : mets}),
            status=200,
            mimetype='application/json'
            )
    return response



@app.route("/course", methods=['POST'])
def create_course():
    """Create a course.
    :return: The course object (see the challenge notes for examples)
    :rtype: object
    """

    """
    -------------------------------------------------------------------------
    Challenge notes:
    -------------------------------------------------------------------------
    1. Bonus points for validating the POST body fields
    """
    # YOUR CODE HERE
    if request.method=='POST':
        jsonf = request.get_json()
        description=jsonf['description']
        discountprice=jsonf['discount_price']
        title=jsonf['title']
        price=jsonf['price']
        imagepath=jsonf['image_path']
        discount=jsonf['on_discount']
        maxid =-1
        for i in courses:
            if maxid<i["id"]:
                maxid=i["id"]

        if isinstance(description, str) and len(description)<=255:
            if isinstance(discountprice, int):
                if isinstance(title, str) and len(title)<=100 and len(title)>=5:
                    if isinstance(price, int) and len(imagepath)<=100:
                        if isinstance(discount, bool) :
                            data ={}
                            data["description"]=description
                            data["discount_price"] = discountprice
                            data["title"]=title
                            data["price"]=price
                            data["image_path"]=imagepath
                            data["on_discount"]=discount
                            data["id"]= maxid + 1
                            maxid=maxid+1
                            courses.append(data)
                            response = app.response_class(
                                response=json.dumps({"data" : data}),
                                status=201,
                                mimetype='application/json')
                            return response
    message ="Cannot create the course. Check the information provided"
    response = app.response_class(
        response=json.dumps({"message" : message}),
        status=400,
        mimetype='application/json')
    return response


@app.route("/course/<int:id>", methods=['PUT'])
def update_course(id):
    """Update a a course.
    :param int id: The record id.
    :return: The updated course object (see the challenge notes for examples)
    :rtype: object
    """

    """
    -------------------------------------------------------------------------
    Challenge notes:
    -------------------------------------------------------------------------
    1. Bonus points for validating the PUT body fields, including checking
       against the id in the URL

    """
    # YOUR CODE HERE
    if request.method=='PUT':
        jsonf = request.get_json()
        description=jsonf['description']
        discountprice=jsonf['discount_price']
        title=jsonf['title']
        price=jsonf['price']
        imagepath=jsonf['image_path']
        discount=jsonf['on_discount']
        idup = jsonf['id']
        ind=-1
        for i in range(0,len(courses)):
            if str(courses[i]["id"])==str(idup):
                ind = i
        if ind ==-1:
            message ="The id does not match the payload"
            response = app.response_class(
                response=json.dumps({"message" : message}),
                status=400,
                mimetype='application/json')
            return response
        if isinstance(description, str) and len(description)<=255:
            if isinstance(discountprice, int):
                if isinstance(title, str) and len(title)<=100 and len(title)>=5:
                    if isinstance(price, int) and len(imagepath)<=100:
                        if isinstance(discount, bool) :
                            courses[ind]["description"]=description
                            courses[ind]["discount_price"] = discountprice
                            courses[ind]["title"]=title
                            courses[ind]["price"]=price
                            courses[ind]["image_path"]=imagepath
                            courses[ind]["on_discount"]=discount
                            response = app.response_class(
                                response=json.dumps({"data" : courses[ind]}),
                                status=200,
                                mimetype='application/json')
                            return response
    message ="Cannot update the course. Check the information provided"
    response = app.response_class(
        response=json.dumps({"message" : message}),
        status=400,
        mimetype='application/json')
    return response


@app.route("/course/<int:id>", methods=['DELETE'])
def delete_course(id):
    """Delete a course
    :return: A confirmation message (see the challenge notes for examples)
    """
    """
    -------------------------------------------------------------------------
    Challenge notes:
    -------------------------------------------------------------------------
    None
    """
    # YOUR CODE HERE
    ind = -1
    for i in range(0,len(courses)):
        if str(courses[i]["id"])==(id):
            ind = i
    if ind ==-1:
        message ="Course "+str(id)+" does not exist"
        response = app.response_class(
                    response=json.dumps({"message" : message}),
                    status=400,
                    mimetype='application/json')
        return response
    courses.remove(courses[ind])
    message ="The specified course was deleted"
    response = app.response_class(
        response=json.dumps({"message" : message}),
        status=200,
        mimetype='application/json')
    return response
      


