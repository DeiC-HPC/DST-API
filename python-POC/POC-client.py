import requests
from requests.auth import HTTPBasicAuth
import os
import string
import secrets
import json
import time

#####STATIC VALUES
static_url = "http://srvhpcstg1.fsehpcdmz.local/HPCApiPreprod"
#static_url = "http://localhost:8080"

apikey = "DeiCApiKey"
headers = {"X-API-Key": apikey}

#Static variables for getting data from the messages
messageTypePath = "messageType"
messageIdPath = "messageId"
dataPath = "data"
projectNumberPath = "projectNo"
accessIdPath = "accessIdentifier"
filesPath = "files"
fileIdPath = "fileId"

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
    return
    path = "/messages/" + str(msgId)
    url = static_url + path
    response = requests.patch(url, headers=headers)
    handleMessagePatchResponse(response, msgId)

def createProject(msgId, projectId):
    if(not projectId in projects):
        #create project as an empty list of users
        projects.update([(projectId,[])])
    else:
        print("Project ", projectId, " already created")
        print("Contact DST about message: ", msgId)

def removeProjectFolderIfEmpty(projectId):
    if os.path.exists(str(projectId)):
        dirEntries = os.listdir(str(projectId))
        if(len(dirEntries) == 0):
            os.rmdir(str(projectId))
            return True
    return False

def removeProjectFolder(projectId):
    os.rmdir(str(projectId))

def deleteProject(msgId, projectId):
    deleted = False
    if(projectId in projects):
        #remove project
        projects.pop(projectId)
        removeProjectFolder(projectId)
    else:
        print("Project ", projectId, " not found")
        print("Contact DST about message: ", msgId)

def generateUsername(accessId):
    return accessId

def generateOTP():
    return ''.join(secrets.choice(alphabet) for i in range(passwordLength))

def createProjectAccess(msgId, projectId, accessId):
    if(projectId in projects):
        project = projects.get(projectId)
        #Create the user in the project
        if(not accessId in project):
            if (not accessId in users):
                project.append(accessId)
                username = generateUsername(accessId)
                password = generateOTP()
                enabled = True
                users.update([(accessId,(projectId, username, password, enabled))])

                #POST credentials back to DST
                userData = {"accessIdentifier" : accessId, "loginName" : username, "oneTimePassword" : password }
                url = static_url + "/user-accesses"
                response = requests.post(url, headers=headers, json = userData)
                try:
                    response.raise_for_status()
                except:
                    print("Something went wrong posting ", username, " to DST while handling message id ", msgId)
                    print("Please contact DST")
            else:
                print("User ", accessId, " already exists")
                print("Contact DST about message: ", msgId)
        else:
            print("User already known in project: ", projectId)
            print("Contact DST about message: ", msgId)
            return
        #Add the user to the list of users
    else:
        print("Project ", projectId, " not found")
        print("Contact DST about message: ", msgId)

def deleteProjectAccess(msgId, accessId):
    if(accessId in users):
        (projectId, _, _, _) = users.pop(accessId)
        if(projectId in projects):
            project = projects.get(projectId)
            project.remove(accessId)
        else:
            print("Project ", projectId, " for user ", accessId, " not found")
            print("Contact DST about message: ", msgId)
    else:
        print("User ", accessId, " not found")
        print("Contact DST about message: ", msgId)

def disableProjectAccess(msgId, accessId):
    if(accessId in users):
        (projectId, username, password, enabled) = users.get(accessId)
        if(enabled):
            users.update([(accessId,(projectId, username, password, False))])
        else:
            print("User ", accessId, " already disabled")
            print("Contact DST about message: ", msgId)
    else:
        print("User ", accessId, " not found")
        print("Contact DST about message: ", msgId)

def enableProjectAccess(msgId, accessId):
    if(accessId in users):
        (projectId, username, password, enabled) = users.get(accessId)
        if(not enabled):
            users.update([(accessId,(projectId, username, password, True))])
        else:
            print("User ", accessId, " already ensabled")
            print("Contact DST about message: ", msgId)
    else:
        print("User ", accessId, " not found")
        print("Contact DST about message: ", msgId)

def resetPassword(msgId, accessId):
    if(accessId in users):
        (projectId, username, password, enabled) = users.get(accessId)
        users.update([(accessId,(projectId, username, generateOTP(), enabled))])

        #PATCH new OTP back to DST
        url = static_url + "/user-accesses/" + str(accessId)
        try:
            requests.patch(url, password, headers=headers).raise_for_status()
        except:
            print("Something went wrong patching a new password for ", username, " to DST while handling message id ", msgId)
            print("Please contact DST")
    else:
        print("User ", accessId, " not found")
        print("Contact DST about message: ", msgId)

def verifyFile(destination, checksum):
    #################################################################################Verify file versus MD5hash

chunkSize = 8192
def downloadLargeFile(msgId, url, destination, checksum):
    try:
        with requests.get(url, headers=headers, stream=True) as response:
            response.raise_for_status()
            with open(destination, 'wb') as f:
                for chunk in response.iter_content(chunk_size=chunkSize):
                    f.write(chunk)
    except requests.exceptions.RequestException as e:
        print("Error downloading the file:", e, " for message with id: ", msgId)
    verifyFile(destination, checksum)

def sendLargeFile(url, filePath):
    with open(filePath, 'rb') as f:
        reponse = requests.post(url, headers=headers, data=f).raise_for_status()


def handleFileDelivery(msgId, projectId, fileId, checcksum):
    dirc = str(projectId)
    if(not os.path.exists(dirc)):
        os.makedirs(dirc)
    url = static_url + "/data/" + fileId
    path = dirc + fileId
    downloadLargeFile(msgId, url, path, checksum)

def findFileById(fileId):
    for root, dirs, files in os.walk("."):
        if fileId in files:
            return os.path.join(root, fileId)

def dataDeliveryReady(msgId, projectId, files):
    if(projectId in projects):
        for fileId, fileSize, checksum in files:
            handleFileDelivery(msgId, projectId, fileId, checksum)
    else:
        print("Project ", projectId, "does not exist while trying to download files")
        print("Contact DST about message: ", msgId)

def deleteDataFile(msgId, fileId):
    optionalFilePath = findFileById(fileId)
    if(optionalFilePath):
        os.remove(optionalFilePath)
    else:
        print("File not found:", fileId)
        print("Contact DST about message: ", msgId)

def returnDataFile(msgId, fileId):
    optionalFilePath = findFileById(fileId)
    if(optionalFilePath):
        url = static_url + "/data/" + fileId
        try:
            sendLargeFile(url, optionalFilePath, msgId)
        except:
            print("Sending file ", fileId, " failed")
            print("Please contact DST about message ", msgId)
    else:
        print("File not found:", fileId)
        print("Contact DST about message: ", msgId)

def transferFile(filePath, projectNumber):
    url = static_url + "/data/project/" + projectNumber
    sendLargeFile(url, filePath)

def handleIndividualMessage(messageType, msgId, data):
    if(type(data)==str):
        data = json.loads(data)
    match messageType:
        case "CreateProject":
            projectId = data[projectNumberPath]
            createProject(msgId, projectId)

        case "DeleteProject":
            projectId = data[projectNumberPath]
            deleteProject(msgId, projectId)

        case "CreateProjectAccess":
            projectId = data[projectNumberPath]
            accessId = data[accessIdPath]
            createProjectAccess(msgId, projectId, accessId)

        case "DeleteProjectAccess":
            accessId = data[accessIdPath]
            deleteProjectAccess(msgId, accessId)

        case "DisableProjectAccess":
            accessId = data[accessIdPath]
            disableProjectAccess(msgId, accessId)

        case "EnableProjectAccess":
            accessId = data[accessIdPath]
            enableProjectAccess(msgId, accessId)

        case "ResetPassword":
            accessId = data[accessIdPath]
            resetPassword(msgId, accessId)

        case "DataDeliveryReady":
            projectId = data[projectNumberPath]
            files = data[filesPath]
            dataDeliveryReady(msgId, projectId, files)

        case "DeleteDataFile":
            fileId = data[fileIdPath]
            deleteDataFile(msgId, fileId)

        case "ReturnDataFile":
            fileId = data[fileIdPath]
            returnDataFile(msgId, fileId)

        case _:
            print("Unknown message type: ", messageType)
            print("Contact DST about message: ", msgId)
            #return

    #mark as done
    messageDone(msgId)

def getMessageList(response):
    return json.loads(response.content)

def handleMessageList(response):
    print(response.content)
    messages = getMessageList(response)
    for message in messages:
        print(message)
        messageType = message[messageTypePath]
        msgId = message[messageIdPath]
        data = message[dataPath]
        handleIndividualMessage(messageType, msgId, data)
        printState()
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
    response = requests.post(url, headers=headers)
    handleMessagePatchResponse(response, projectId)

# #####Create project
projectId = 1337 #Is 42 funnier?
# initializeProject(projectId)

# #####Get messages
path = "/messages"
url=static_url+path
while(true):
    response = requests.get(url, headers=headers)
    handleGetMessageResponse(response)
    sleep(60) #One minutte as agreed with DST


### DELETE ME
# i = 0
# while(True):
#     i+=1
#     if(i<50):
#         for x in range(1):
#             initializeProject(projectId+x+i*50)
#     url=static_url+path
#     response = requests.get(url, headers=headers)
#     response = requests.get(url, headers=headers)

#     handleGetMessageResponse(response)
#     printState() #For debugging
#     time.sleep(1)

#####Send data to project from data-center

# #Crteate some data
f = open("demofile", "w")
f.write("This is a test")
f.close()

# #Actually do the transfer
projectId = 1337 #It's not. Is it?
path = "demofile"
transferFile(demofile, projectId)
