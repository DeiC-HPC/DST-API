import requests
from requests.auth import HTTPBasicAuth
import os
import string
import secrets
import json
import time

#####STATIC VALUES
static_url = "http://localhost:8080"

apikey = ""
auth = HTTPBasicAuth("apikey", apikey)

#Static variables for getting data from the messages
messageTypePath = "messageType"
messageIdPath = "messageId"
dataPath = "data"
projectNumberPath = "ProjectNo"
accessIdPath = "AccessIdentifier"
filesPath = "Files"
fileIdPath = "FileId"

#Password static variables
alphabet = string.ascii_letters + string.digits + string.punctuation
passwordLength = 10

#projects is a dictionary of projects. Each project will contain a list of user-id's
projects = dict()

#users is a dictionary of user-id's. Each user will contain:
#project-id: the id of the project the user is connected to
#username: a generated username
#password: a OTP, password or key connected to the user
#enabled: a boolean describing whether or not the user is enabled
users = dict()

def printState():
    print("Projects ", projects)
    print("Users ", users)

#Boolean on whether the result is accepted or not
def handleMessagePatchResponse(response, msgId):
    match response.status_code:
        case 200:
            return True
        case 400:
            print("Message already marked as processed with id: ", msgId)
            return True
        case 401:
            print("Unauthorized or wrong API-key for processing message with id: ", msg)
            print("Please check the api-key")
            return False
        case 403:
            print("Message does not belong to this center with id: ", msgId)
            return False
        case 404:
            print("Message does not exist with id: ", msgId)
            return False
        case 500:
            print("Internal server error at DST for message with id: ", msgId)
            print("Maybe try again?")
            return False
        case _:
            print("Unknown status code: ", response.status_code,
                  " for message with id: ", msgId)
            return False

def messageDone(msgId):
    path = "/messages/" + str(msgId)
    url = static_url + path
    response = requests.patch(url, auth=auth)
    handleMessagePatchResponse(response, msgId)

def createProject(projectId):
    if(not projectId in projects):
        #create project as an empty list of users
        projects.update([(projectId,[])])

def removeProjectFolderIfEmpty(projectId):
    dirEntries = os.listdir(str(projectId))
    if(len(dirEntries) == 0):
        os.rmdir(str(projectId))
        return True
    return False

def deleteProject(projectId):
    deleted = False
    if(projectId in projects):
        #remove project
        projects.pop(projectId)
        removeProjectFolderIfEmpty(projectId)
        deleted = True

def generateUsername(accessId):
    return accessId

def generateOTP():
    return ''.join(secrets.choice(alphabet) for i in range(passwordLength))

def createProjectAccess(projectId, accessId):
    if(projectId in projects):
        project = projects.get(projectId)
        #Create the user in the project
        if(not accessId in project):
            project.append(accessId)
        #Add the user to the list of users
        if (not accessId in users):
            username = generateUsername(accessId)
            password = generateOTP()
            enabled = True
            users.update([(accessId,(projectId, username, password, enabled))])

            #POST credentials back to DST
            userData = {"accessIdentifier" : accessId, "loginName" : username, "oneTimePassword" : password }
            url = static_url + "/user-accesses"
            requests.post(url, auth=auth, json = userData).raise_for_status()

def deleteProjectAccess(accessId):
    if(accessId in users):
        (projectId, _, _, _) = users.pop(accessId)
        if(projectId in projects):
            project = projects.get(projectId)
            project.remove(accessId)

def disableProjectAccess(accessId):
    if(accessId in users):
        (projectId, username, password, enabled) = users.get(accessId)
        if(enabled):
            users.update([(accessId,(projectId, username, password, False))])

def enableProjectAccess(accessId):
    if(accessId in users):
        (projectId, username, password, enabled) = users.get(accessId)
        if(not enabled):
            users.update([(accessId,(projectId, username, password, True))])

def resetPassword(accessId):
    if(accessId in users):
        (projectId, username, password, enabled) = users.get(accessId)
        users.update([(accessId,(projectId, username, generateOTP(), enabled))])

        #PATCH new OTP back to DST
        url = static_url + "/user-accesses/" + str(accessId)
        requests.patch(url, password, auth=auth).raise_for_status()

chunkSize = 8192
def downloadLargeFile(url, destination):
    try:
        with requests.get(url, auth=auth, stream=True) as response:
            response.raise_for_status()
            with open(destination, 'wb') as f:
                for chunk in response.iter_content(chunk_size=chunkSize):
                    f.write(chunk)
    except requests.exceptions.RequestException as e:
        print("Error downloading the file:", e)

def sendLargeFile(url, filePath):
    with open(filePath, 'rb') as f:
        requests.post(url, auth=auth, data=f).raise_for_status()

def handleFileDelivery(projectId, fileId):
    dirc = str(projectId)
    os.makedirs(dirc)
    url = static_url + "/data/" + fileId
    path = dirc + fileId
    downloadLargeFile(url, path)

def findFileById(fileId):
    for root, dirs, files in os.walk("."):
        if fileId in files:
            return os.path.join(root, fileId)

def dataDeliveryReady(projectId, files):
    for fileId, fileSize, checksum in files:
        handleFileDelivery(projectId, fileId)

def deleteDataFile(fileId):
    optionalFilePath = findFileById(fileId)
    if(optionalFilePath):
        os.remove(optionalFilePath)

def returnDataFile(fileId):
    optionalFilePath = findFileById(fileId)
    if(optionalFilePath):
        url = static_url + "/data/" + fileId
        sendLargeFile(url, optionalFilePath)

def transferFile(filePath, projectNumber):
    url = static_url + "/data/project/" + projectNumber
    sendLargeFile(url, filePath)

def handleIndividualMessage(messageType, msgId, data):
    match messageType:
        case "CreateProject":
            projectId = data[projectNumberPath]
            createProject(projectId)

        case "DeleteProject":
            projectId = data[projectNumberPath]
            deleteProject(projectId)

        case "CreateProjectAccess":
            projectId = data[projectNumberPath]
            accessId = data[accessIdPath]
            createProjectAccess(projectId, accessId)

        case "DeleteProjectAccess":
            accessId = data[accessIdPath]
            deleteProjectAccess(accessId)

        case "DisableProjectAccess":
            accessId = data[accessIdPath]
            disableProjectAccess(accessId)

        case "EnableProjectAccess":
            accessId = data[accessIdPath]
            enableProjectAccess(accessId)

        case "ResetPassword":
            accessId = data[accessIdPath]
            resetPassword(accessId)

        case "DataDeliveryReady":
            projectId = data[projectNumberPath]
            files = data[filesPath]
            dataDeliveryReady(projectId, files)

        case "DeleteDataFile":
            fileId = data[fileIdPath]
            deleteDataFile(fileId)

        case "ReturnDataFile":
            fileId = data[fileIdPath]
            returnDataFile(fileId)

        case _:
            print("Unknown message type: ", messageType)
            return #To not mark the message as done

    #mark as done
    messageDone(msgId)

def getMessageList(response):
    return json.loads(response.content)

def handleMessageList(response):
    messages = getMessageList(response)
    for message in messages:
        messageType = message[messageTypePath]
        msgId = message[messageIdPath]
        data = message[dataPath]
        handleIndividualMessage(messageType, msgId, data)
    #DELETE ME
    if(len(messages)==0):
        print("No more messages - goodbye")
        exit()

def handleGetMessageResponse(response):
    match response.status_code:
        case 200:
            handleMessageList(response)
        case 401:
            print("Unauthorized or wrong API-key for getting message list from DST")
            print("Please check the api-key")
        case 500:
            print("Internal server error at DST for getting messageList")
            print("Maybe try again?")
        case _:
            print("Unknown status code: ", response.status_code)


def initializeProject(projectId):
    path = "/projects/" + str(projectId) + "/confirm"
    url = static_url + path
    response = requests.post(url, auth=auth)
    handleMessagePatchResponse(response, projectId)

#####Create project
projectId = 1337 #Is 42 funnier?
initializeProject(projectId)

#####Get messages
path = "/messages"
url=static_url+path
response = requests.get(url, auth=auth)
handleGetMessageResponse(response)


### DELETE ME
i = 0
while(True):
    i+=1
    if(i<50):
        for x in range(1):
            initializeProject(projectId+x+i*50)
    url=static_url+path
    response = requests.get(url, auth=auth)
    response = requests.get(url, auth=auth)

    handleGetMessageResponse(response)
    printState() #For debugging
    time.sleep(1)

#####Send data to project from data-center

# #Crteate some data
# f = open("demofile", "w")
# f.write("This is a test")
# f.close()

# #Actually do the transfer
# projectId = 1337 #It's not. Is it?
# path = "demofile"
# transferFile(demofile, projectId)
