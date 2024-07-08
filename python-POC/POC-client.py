import requests
import os

#####STATIC VALUES
static_url = ""

messageTypePath = "messageType"
messageIdPath = "messageId"
dataPath = "data"

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

def deleteProject(projectId):
       deleted = False
       if(data.has_key(projectId):
                #remove project
                projects.pop(projectId)
                deleted = True

def generateUsername(accessId):
    return accesId

def generateOTP():
    return "Password" #Make this random in some way

def createProjectAccess(projectId, accessId):
    if(projects.has_key(projectId)):
        project = projects.get(projectId)
        #Create the user in the project
        if(not accessId in project):
        project.append(accessId)
        #Add the user to the list of users
        if(not users.has_key(accessId)):
          username = generateUsername(accessId)
                    password = generateOTP()
                    enabled = True
                    users.update(accessId : (projectId, username, password, enabled))
            #POST credentials

            ###################TODO

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

        #Patch to provide new password

        ###################TODO

def downloadLargeFile(url, destination):
    try:
        with requests.get(url, stream=True) as response:
            response.raise_for_status()
            with open(destination, 'wb') as f:
                for chunk in response.iter_content(chunk_size=8192):
                    f.write(chunk)
        print("File downloaded successfully!")
    except requests.exceptions.RequestException as e:
        print("Error downloading the file:", e)


def sendLargeFile(url, filePath):
    ################TODO

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

def dataDeliveryReady(projectId, fileIds)
    for fileId in fileIds:
        handleFileDelivery(projectId, fileId)

def deleteDataFile(fileId):
    optionalFilePath = findFileById(fileId)
    if(optionalFilePath):
       os.remove(optionalFilePath)

def returnDataFile(fileId):
    optionalFilePath = findFileById(fileId)
    if(optionalFilePath):
        sendLargeFile(optionalFilePath)

def handleIndividualMessage(messageType, msgId, data):
    match messageType:
        case "CreateProject":
            projectId = 1337 #Get this
            createProject(projectId)
            messageDone(msgId)
        case "DeleteProject":
            projectId = 1337 #Get this
            deleteProject(projectId)
            #return an answer
            messageDone(msgId)
        case "CreateProjectAccess":
            projectId = 1337 #Get this
            accessId = 1337 #Get this
            createProjectAccess(projectId, acessId)
            #return an answer
            messageDone(msgId)

        case "DeleteProjectAccess":
            accessId = 1337 #Get this
            deleteProjectAccess(accessId)
            #return an answer
            messageDone(msgId)

        case "DisableProjectAccess":
            accessId = 1337 #Get this
            disableProjectAccess(accessId)
            #return an answer
            messageDone(msgId)

        case "EnableProjectAccess":
            accessId = 1337 #Get this
            enableProjectAccess(accessId)
            #return an answer
            messageDone(msgId)

        case "ResetPassword":
            accessId = 1337 #Get this
            resetPassword(accessId)
            #return an answer
            messageDone(msgId)

        case "DataDeliveryReady":
            projectId = 1337 #Get this
            fileIds = [0,1,2,3] #Get this
            dataDeliveryReady(projectId, fileIds)
            messageDone(msgId)

        case "DeleteDataFile":
            fileId = 0 #Get this
            deleteDataFile(fileId)
            messageDone(msgId)

        case "ReturnDataFile":
            fileId = 0 #Get this
            returnDataFile(fileId)
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
        return
    case 401:
        print("Unauthorized or wrong API-key for getting message list from DST")
        print("Please check the api-key")
        return
    case 500:
        print("Internal server error at DST for getting messageList")
        print("Maybe try again?")
        return
    case _:
        print("Unknown status code: " + response.status_code)
        return


#####Create project
projectId = 1337 #Is 42 funnier?

path = "projects/" + projectId + "/confirm"
reponse = requests.post(url + path)
handleMessagePatchResponse(response, projectId)

#####Get messages
path = "/messages"

response = requests.get(url + path)

handleMessageList(response)
