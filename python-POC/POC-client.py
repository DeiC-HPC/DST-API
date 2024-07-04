import requests

#####STATIC VALUES
static_url = ""

messageType = "messageType"

#projects is a dictionary of projects. Each project will contain a list of user-id's
projects = {}
#users is a dictionary of user-id's. Each user will contain:
#project-id: the id of the project the user is connected to
#username: a generated username
#password: a OTP, password or key connected to the user
#enabled: a boolean describing whether or not the user is enabled

#Boolean on whether the result is accepted or not
def handleMessagePatchResponse(response, msgid):
    match response.status_code:
        case 200:
            return True
        case 400:
            print("Message already marked as processed with id: " + msgid)
            return True
        case 401:
            print("Unauthorized or wrong API-key for processing message with id: " + msg)
            print("Please check the api-key")
            return False
        case 403:
            print("Message does not belong to this center with id: " + msgid)
            return False
        case 404:
            print("Message does not exist with msgid: " + msgid)
            return False
        case 500:
            print("Internal server error at DST for message with id: " + msgid)
            print("Maybe try again?")
            return False
        case _:
            print("Unknown status code: " + response.status_code +
                  " for message with id: " + msgid)
            return False

def messageDone(msgid):
    path = "messages/" + msgid
    response = requests.patch(url + path)
    handleMessagePatchResponse(response, msgid)

def generateUsername(accessId):
    return accesId

def generateOTP():
    return "Password" #Make this random in some way

def handleFileDelivery(projectId, fileId):
    #########################TODO

def findFileById(fileId):
    #########################TODO

def handleFileDelete(fileId):
    #########################TODO

def handleFileReturn(fileId):
    #########################TODO

def handleIndividualMessage(msg):
    msgid = 1337 #Get this
    match msg[messageType]:
        case "CreateProject":
            projectId = 1337 #Get this
            created = False
            if(not data.has_key(projectId):
                #create project as an empty dictionary of users
                projects.update(projectId = [])
                created = True
            #What to do if the project is there?
            #return an answer
            messageDone(msgid)

        case "DeleteProject":
            deleted = False
            if(data.has_key(projectId):
                #remove project
                projects.pop(projectId)
                deleted = True
            #What to do if the project is not there?
            #return an answer
            messageDone(msgid)

        case "CreateProjectAccess":
            projectId = 1337 #Get this
            accessId = 1337 #Get this
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

            #return an answer
            messageDone(msgid)

       case "DeleteProjectAccess":
            accessId = 1337 #Get this
            if(users.has_key(accessId)):
               (projectId, _, _, _) = users.pop(accessId)
               if(projects.has_key(projectId)):
                   project = projects.get(projectId)
                   project.remove(accessId)
            #return an answer
            messageDone(msgid)

        case "DisableProjectAccess":
            accessId = 1337 #Get this
            if(users.has_key(accessId)):
               (projectId, username, password, enabled) = users.get(accessId)
               if(enabled):
                   users.update(accessId : (projectId, username, password, False))
            #return an answer
            messageDone(msgid)

        case "EnableProjectAccess":
            accessId = 1337 #Get this
            if(users.has_key(accessId)):
               (projectId, username, password, enabled) = users.get(accessId)
               if(not enabled):
                   users.update(accessId : (projectId, username, password, True))
            #Patch to provide new password

            ###################TODO

            #return an answer
            messageDone(msgid)

        case "ResetPassword":
            accessId = 1337 #Get this
            if(users.has_key(accessId)):
               (projectId, username, password, enabled) = users.get(accessId)
               users.update(accessId : (projectId, username, generatePassword(), enabled))
            #return an answer
            messageDone(msgid)

        case "DataDeliveryReady":
            fileIds = [0,1,2,3] #Get this
            for iden in fileIds:
               handleFileDelivery(fileId)
            messageDone(msgId)

        case "DeleteDataFile":
            fileId = 0 #Get this
            handleFileDelete(fileId)
            messageDone(msgId)

        case "ReturnDataFile":
            fileId = 0 #Get this
            handleFileReturn(fileId)
            messageDone(msgId)

        case _:
            print("Unknown message type: " + msg[messageType])


def handleMessageList(response):
    return


#####Create project

projectId = 1337 #Get this from user

path = "projects/" + projectId + "/confirm"
reponse = requests.post(url + path)
handleMessagePatchResponse(response, projectId)

#####Get messages
path = "/messages"

response = requests.get(url + path)

handleMessageList(response)
