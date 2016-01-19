#!/usr/bin/python

import cgi
# Turn on debug mode.
import cgitb
cgitb.enable()
import json

FILE_PREFIX = "."
DATA_FILE_NAME  = "data"

# Print necessary headers.
print("Content-Type: text/html\n")


def handleRequest(form):
    if form is not None:
        _type = form.getvalue("type")
        _action = form.getvalue("action")
        if _action == "get":
            switcher = {
                "all": fetchAll,
                "users": fetchAllUsers,
                "groups": fetchAllGroups,
            }
            return switcher.get(_type, "nothing")()
        elif _action == "save":
            return saveItem(form.getvalue("item"),_type)
        elif _action == "delete":
            switcher = {
                "user": deleteUser,
                "group": deleteGroup,
            }
            return switcher.get(_type, "nothing")(form.getvalue("iid"))
    return None    

def fetchAll():
    try:
        output = open(DATA_FILE_NAME + FILE_PREFIX + "json", 'r').read()
    except Exception as e:
        output = str(e)
    return output

def fetchAllUsers():
    try:
        data = open(DATA_FILE_NAME + FILE_PREFIX + "json", 'r').read()
        jsonData = json.loads(data)
        output = jsonData["users"]
    except IOError as ie:
        output = str(ie)
    except ValueError as ve:
        output = str(ve)
    return output
def fetchAllGroups():
    try:
        data = open(DATA_FILE_NAME + FILE_PREFIX + "json", 'r').read()
        jsonData = json.loads(data)
        output = jsonData["groups"]
    except IOError as ie:
        output = str(ie)
    except ValueError as ve:
        output = str(ve)
    return output

def saveItem(item, _type):
    print("savingItem(%s) \n" % _type)
    switch = {
        "group": saveGroup,
        "user": saveUser
    }
    return switch.get(_type, "nothing")(item)

def saveGroup(group):
    try:
        print("saveGroup\n")
        fp = open(DATA_FILE_NAME + FILE_PREFIX + "json", 'r+')
        # read old content
        dataFile = fp.read()
        # convert to JSON
        jsonData = json.loads(dataFile)
        group = json.loads(group)
        # add the new item
        # if item exist then delete it and replace it with the new one 
        for i in xrange(len(jsonData["groups"])):
            if jsonData["groups"][i]["iid"] == group["iid"]:
                jsonData["groups"].pop(i)
                break
        jsonData["groups"].append({"iid": group["iid"], "name" : group["name"], "email" : group["email"]})
        # write data
        fp.seek(0)
        json.dump(jsonData, fp)
        fp.truncate()
        output = "User successfully saved"
    except IOError as e:
        output = str(e)
    except ValueError as ve:
        output = str(e)
    return output

def saveUser(user):
    try:
        print("saveUser\n")
        fp = open(DATA_FILE_NAME + FILE_PREFIX + "json", 'r+')
        # read old content
        dataFile = fp.read()
        # convert to JSON
        jsonData = json.loads(dataFile)
        user = json.loads(user)
        # if item exist then delete it and replace it with the new one 
        for i in xrange(len(jsonData["users"])):
            if jsonData["users"][i]["iid"] == user["iid"]:
                jsonData["users"].pop(i)
                break
        jsonData["users"].append({"iid": user["iid"], "firstName": user["firstName"], "lastName" : user["lastName"], "email" : user["email"], "tel" : user["tel"], "parentId": user["parentId"]})
        # write data
        fp.seek(0)
        json.dump(jsonData, fp)
        fp.truncate()
        output = "User successfully saved"
    except IOError as e:
        output = str(e)
    except ValueError as ve:
        output = str(e)
    return output

def deleteUser(_id):
    try:
        print("deleteUser\n")
        fp = open(DATA_FILE_NAME + FILE_PREFIX + "json", 'r+')
        # read old content
        dataFile = fp.read()
        # convert to JSON
        jsonData = json.loads(dataFile)
        # add the new item
        for i in xrange(len(jsonData["users"])):
            if jsonData["users"][i]["iid"] == _id:
                jsonData["users"].pop(i)
                break
        # write data
        fp.seek(0)
        json.dump(jsonData, fp)
        fp.truncate()
        output = "User successfully deleted"
    except IOError as e:
        output = str(e)
    except ValueError as ve:
        output = str(e)
    return output

def deleteGroup(_id):
    try:
        print("deleteGroup\n")
        fp = open(DATA_FILE_NAME + FILE_PREFIX + "json", 'r+')
        # read old content
        dataFile = fp.read()
        # convert to JSON
        jsonData = json.loads(dataFile)
        # add the new item
        for i in xrange(len(jsonData["groups"])):
            if jsonData["groups"][i]["iid"] == _id:
                jsonData["groups"].pop(i)
                break
        # write data
        fp.seek(0)
        json.dump(jsonData, fp)
        fp.truncate()
        output = "Group successfully deleted"
    except IOError as e:
        output = str(e)
    except ValueError as ve:
        output = str(e)
    return output

form = cgi.FieldStorage()
print(handleRequest(form))
