import requests
import json
import glob
import re
import urllib3


print("Reminder: All MARS nodes must exist in JSON format prior to uploading.")
print("---------------------------------------------------------------------")


##Get pip: curl https://bootstrap.pypa.io/get-pip.py | python3


urllib3.disable_warnings(urllib3.exceptions.InsecureRequestWarning)

def findEnv():
   findToken = input("Do you have a token? (y) (n)")
   type(findToken)
   findToken = findToken.lower()
   if findToken == "y":
        parsedToken = input("Please enter the token.")
        findGraph = input("What is the IP of your Graph node?")
        type(findGraph)
        findStyle(findGraph,parsedToken)
        return
   findWS02 = input("What is the IP of your WSO2 node?")
   type(findWS02)
   findGraph = input("What is the IP of your Graph node?")
   type(findGraph)
   findKey = input("What is the client_key for the account you will be using to upload?")
   type(findKey)
   findSecret = input("What is the client_secret for the account you will be using to upload?")
   type(findSecret)
   iamurl = "https://{0}:9443/oauth2/token".format(findWS02)
   data = {}
   data["grant_type"] = "client_credentials"
   data["scope"] = "batchjob"
   data["client_id"] = findKey
   data["client_secret"] = findSecret
   headers = {'Content-Type':'application/x-www-form-urlencoded;charset=UTF-8'}
   token = requests.post(iamurl, params=data, headers=headers, verify=False)
   parsedToken = json.loads(token.text)
   parsedToken = parsedToken['access_token']
   print("Your token is: " + parsedToken)
   findStyle(findGraph,parsedToken)
   return


def createNodes(graph,parsedToken):
   print("You chose to create new MARS nodes.")
   findJSON = input("What directory are the JSONs stored in? ie. /tmp/MARSBackup")
   type(findJSON)
   getJSONS = glob.glob(findJSON+'/*')
   headers = {'Content-Type': 'application/json', '_TOKEN':parsedToken}
   graphurl = "https://{0}:8443/new/ogit%2FAutomation%2FMARSNode".format(graph)
   myCounter = 0
   for x in getJSONS:
       myCounter += 1
       contents = open(x).read()
       upload = requests.post(graphurl, data=contents, headers=headers, verify=False)
       print(upload.text)
       if "owner" and "does not exist" in upload.text:
           ownerMessage = json.loads(upload.text)
           ownerMessage = ownerMessage['error']['message']
           owner = re.search(r'owner\s(.*)\sdoes',ownerMessage).group(1)
           createOwner = input("It looks like the " + ownerMessage + ". Would you like to create it? (y) (n)")
           if createOwner == "y":
               createurl = "https://{0}:8443/new/ogit%2FOrganization".format(graph)
               data = {}
               data["ogit/name"] = owner
               data["ogit/_id"] = owner
               neworg = requests.post(createurl, data=json.dumps(data), headers=headers, verify=False)
               print(neworg.text)
               if neworg.status_code == 200:
                    print("New organization" + owner + " created. Continuing upload...")
                    upload = requests.post(graphurl, data=contents, headers=headers, verify=False)
                    print(upload.text)
               else:
                   print("Failed to create organization" + owner)
                   break
           else:
               print("Exiting...")
               break
   print("Upload finished! " + str(myCounter) + " MARS nodes created.")
   return

def updateNodes(graph,parsedToken):
   print("You chose to update existing MARS nodes.")
   findJSON = input("What directory are the JSONs stored in? ie. /tmp/MARSBackup")
   type(findJSON)
   getJSONS = glob.glob(findJSON+'/*')
   headers = {'Content-Type': 'application/json', '_TOKEN':parsedToken}
   graphurl = "https://{0}:8443/".format(graph)
   myCounter = 0
   for x in getJSONS:
       myCounter += 1
       contents = open(x).read()
       marsID = json.loads(contents)
       marsID = marsID['ogit/_id']
       upload = requests.post(graphurl + marsID, data=contents, headers=headers, verify=False)
       print(upload.text)
   print("Upload finished! " + str(myCounter) + " MARS nodes updated.")
   return

def checkInput(str,graph,parsedToken):
     if str == "c" or str == "create":
         createNodes(graph,parsedToken)
     elif str == "u" or str == "update":
         updateNodes(graph,parsedToken)
     return

def findStyle(graph,parsedToken):
    style = input("Will you be creating new nodes or updating existing nodes? (c)reate (u)pdate")
    type(style)
    style = style.lower()
    print(style)
    if style == "c" or style == "create" or style == "u" or style == "update":
        checkInput(style,graph,parsedToken)
    else:
        print(r'You must enter either "create" or "update".')
        findStyle()
    return

findEnv()
