import requests
import os
import string
import secrets

#####STATIC VALUES
static_url = ""

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
projects = {}

#users is a dictionary of user-id's. Each user will contain:
#project-id: the id of the project the user is connected to
#username: a generated username
#password: a OTP, password or key connected to the user
#enabled: a boolean describing whether or not the user is enabled
users = {}



#Boolean on whether the result is accepted or not
def handleMessagePatchResponse(response, msgId):
    match response.status_code:
        case 200:
            return True
        case 400:
            print("Message already marked as processed with id: " + msgId)
            return True
        case 401:
            print("Unauthorized or wrong API-key for processing message with id: " + msg)
            print("Please check the api-key")
            return False
        case 403:
            print("Message does not belong to this center with id: " + msgId)
            return False
        case 404:
            print("Message does not exist with id: " + msgId)
            return False
        case 500:
            print("Internal server error at DST for message with id: " + msgId)
            print("Maybe try again?")
            return False
        case _:
            print("Unknown status code: " + response.status_code +
                  " for message with id: " + msgId)
            return False

def messageDone(msgId):
    path = "messages/" + msgId
    response = requests.patch(url + path)
    handleMessagePatchResponse(response, msgId)

def createProject(projectId):
    if(not data.has_key(projectId):
        #create project as an empty list of users
        projects.update(projectId = [])

def removeProjectFolderIfEmpty(projectId)
    dirEntries = os.listdir(projectId)
    if(len(dirEntries) == 0):
       os.rmdir(projectId)
       return True
    return False

def deleteProject(projectId):
    deleted = False
    if(data.has_key(projectId):
       #remove project
       projects.pop(projectId)
       removeProjectFolderIfEmpty(projectId)
       deleted = True

def generateUsername(accessId):
    return accesId

def generateOTP():
    return ''.join(secrets.choice(alphabet) for i in range(passwordLength))

def createProjectAccess(projectId, accessId):
    if(projects.has_key(projectId)):
       project = projects.get(projectId)
       #Create the user in the project
       if(not accessId in project):
           project.append(accessId)
       #Add the user to the list of users
       if (not users.has_key(accessId)):
           username = generateUsername(accessId)
           password = generateOTP()
           enabled = True
           users.update(accessId : (projectId, username, password, enabled))

           #POST credentials back to DST
           userData = {"accessIdentifier" : accessId, "loginName" : username, "oneTimePassword" : password }
           url = staticUrl + "/user-accesses"
           request.post(url, json = userData).raise_for_status()

def deleteProjectAccess(accessId):
    if(users.has_key(accessId)):
        (projectId, _, _, _) = users.pop(accessId)
        if(projects.has_key(projectId)):
          project = projects.get(projectId)
          project.remove(accessId)

def disableProjectAccess(accessId):
    if(users.has_key(accessId)):
        (projectId, username, password, enabled) = users.get(accessId)
        if(enabled):
            users.update(accessId : (projectId, username, password, False))

def enableProjectAccess(accessId):
    if(users.has_key(accessId)):
        (projectId, username, password, enabled) = users.get(accessId)
        if(not enabled):
            users.update(accessId : (projectId, username, password, True))

def resetPassword(accessId):
    if(users.has_key(accessId)):
       (projectId, username, password, enabled) = users.get(accessId)
       users.update(accessId : (projectId, username, generatePassword(), enabled))

       #PATCH new OTP back to DST
       url = staticUrl + "/user-accesses/"+accessId
       request.patch(url, password).raise_for_status()

chunkSize = 8192
def downloadLargeFile(url, destination):
    try:
        with requests.get(url, stream=True) as response:
            response.raise_for_status()
            with open(destination, 'wb') as f:
                for chunk in response.iter_content(chunk_size=chunkSize):
                    f.write(chunk)
    except requests.exceptions.RequestException as e:
        print("Error downloading the file:", e)

def sendLargeFile(url, filePath):
    with open(filePath, 'rb') as f:
       requests.post(url, data=f).raise_for_status()

def handleFileDelivery(projectId, fileId):
    dirc = projectId
    os.makedirs(dirc)
    url = static_url + "/data/" + fileId
    path = dirc + fileId
    downloadLargeFile(url, path)

def findFileById(fileId):
    for root, dirs, files in os.walk("."):
        if fileId in files:
            return os.path.join(root, fileId)

def dataDeliveryReady(projectId, files)
    for fileId, fileSize, checksum in files:
        handleFileDelivery(projectId, fileId)

def deleteDataFile(fileId):
    optionalFilePath = findFileById(fileId)
    if(optionalFilePath):
       os.remove(optionalFilePath)

def returnDataFile(fileId):
    optionalFilePath = findFileById(fileId)
    if(optionalFilePath):
       url = staticUrl + "/data/" + fileId
       sendLargeFile(url, optionalFilePath)

def transferFile(filePath, projectNumber)
    url = staticUrl + "/data/project/" + projectNumber
    sendLargeFile(url, filePath)

def handleIndividualMessage(messageType, msgId, data):
    match messageType:
        case "CreateProject":
            projectId = data[projectNumberPath]
            createProject(projectId)
            messageDone(msgId)

        case "DeleteProject":
            projectId = data[projectNumberPath]
            deleteProject(projectId)
            #mark as done
            messageDone(msgId)

        case "CreateProjectAccess":
            projectId = data[projectNumberPath]
            accessId = data[accessIdPath]
            createProjectAccess(projectId, acessId)
            #mark as done
            messageDone(msgId)

        case "DeleteProjectAccess":
            accessId = data[accessIdPath]
            deleteProjectAccess(accessId)
            #mark as done
            messageDone(msgId)

        case "DisableProjectAccess":
            accessId = data[accessIdPath]
            disableProjectAccess(accessId)
            #mark as done
            messageDone(msgId)

        case "EnableProjectAccess":
            accessId = data[accessIdPath]
            enableProjectAccess(accessId)
            #mark as done
            messageDone(msgId)

        case "ResetPassword":
            accessId = data[accessIdPath]
            resetPassword(accessId)
            #mark as done
            messageDone(msgId)

        case "DataDeliveryReady":
            projectId = data[projectNumberPath]
            files = data[filesPath]
            dataDeliveryReady(projectId, files)
            #mark as done
            messageDone(msgId)

        case "DeleteDataFile":
            fileId = data[fileIdPath]
            deleteDataFile(fileId)
            #mark as done
            messageDone(msgId)

        case "ReturnDataFile":
            fileId = data[fileIdPath]
            returnDataFile(fileId)
            #mark as done
            messageDone(msgId)

        case _:
            print("Unknown message type: " + messageType)

def getMessageList(response)
    return []

def handleMessageList(response):
    messages = getMessageList(response)
    for message in messages:
          messageType = message[messageTypePath]
          msgId = message[messageId]
          data = message[dataPath]
          handleIndividualMessage(messageType, msgId, data)

def handleGetMessageResponse(response)
    match response.status_code
       case 200:
           handleMessageList(response)
       case 401:
           print("Unauthorized or wrong API-key for getting message list from DST")
           print("Please check the api-key")
       case 500:
           print("Internal server error at DST for getting messageList")
           print("Maybe try again?")
       case _:
           print("Unknown status code: " + response.status_code)


#####Create project
projectId = 1337 #Is 42 funnier?

path = "projects/" + projectId + "/confirm"
reponse = requests.post(url + path)
handleMessagePatchResponse(response, projectId)

#####Get messages
path = "/messages"

response = requests.get(url + path)

handleMessageList(response)

#####Send data to project from data-center

#Crteate some data
f = open("demofile", "w")
f.write("This is a test")
f.close()

#Actually do the transfer
projectId = 1337 #It's not. Is it?
path = "demofile"
transferFile(demofile, projectId)
