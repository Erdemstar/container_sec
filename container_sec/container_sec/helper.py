import uuid
import json
import os
import requests

class Helper():
    def generateRandomFileName(self):
        return str(uuid.uuid4())

    def readJsonFile(self,filename):
        """
        Description : This is used for read json file to convert array
        """
        try:
            with open(filename, 'r') as data:
                return json.load(data)
        except Exception as e:
            print ("Error while reading file : {}\nError is {} ".format(filename,e))
            return None

    def deleteFile(self,filename):
        """
        Description : This is used for read json file to convert array
        """
        try:
            if (os.path.exists(filename)):
                os.remove(filename)
            else:
                print ("There is no filename")
        except Exception as e:
            print (e)
            print("There is a problem while delete file")

    def writeFile(self,filename,data):
        try:
            json_object = json.dumps(data)
            file = open(filename,"w")
            file.write(json_object)
            file.close()
        except Exception as e:
            print ("wrileFile error : " + str(e))


    def celeryTaskNameParser(self,arr,index:int):
        """
        Description : This is used for take filename from celery task result
        """
        try:
            return arr.split(",")[index].replace("'","").replace("]","").replace(" ","")
        except:
            return None

    def parseFilePath(self,arr):
        """
        Description : This is used for take filename from celery task result
        """
        return arr.split(",")[1].replace("'","").replace("]","").replace(" ","")

    def parseFileName(self,arr):
        """
        Description : This is used for take filename from celery task result
        """
        return arr.split(",")[2].replace("'","").replace("]","").replace(" ","")
  
    def readDockerfile(self, file):
        """
        Description : This is used for general file read
        """
        tmp_arr = []
        last_tmp_arr = []

        try:
            with open(file, "r", encoding="utf8", errors='ignore') as file:
                tmp = file.readlines()

                # remove space and double slash
                for i in tmp:
                    tmp_arr.append(i.replace("\n","").replace("\\",""))

                # remove blank string at arry
                for i in tmp_arr:
                    if i != "":
                        last_tmp_arr.append(i)

                return last_tmp_arr

        except Exception as e:
            print (e)
            return "There is an error while reading file"

    def writeOutputTerminalScreen(self,name,description,recommendation):
        """
        Description : 
        """
        return {"Rule_Name":name, "Description": description, "Recommendation":recommendation}
   
    def httpGetRequest(self,url):
        r = requests.get(url)
        response = json.loads(r.text)
        return response
