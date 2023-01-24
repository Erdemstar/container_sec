from container_sec.helper import Helper

helper = Helper()

class GrypeParser():
    def __init__(self):
        self.content = ""
        self.result = []
        self.final_result = []
    
    def readJsonFile(self,file):
        self.content = helper.readJsonFile(file)

        if self.content is not None:
            for i in self.content["matches"]:
                self.result.append( {
                    "id":i["vulnerability"]["id"],
                    "dataSource":i["vulnerability"]["dataSource"],
                    "severity":i["vulnerability"]["severity"],
                    "urls":i["vulnerability"]["urls"]
                    })
            self.final_result = {"image_result":self.result}
        else:
            self.final_result = {"image_result":[]}

    
    def readContent(self,arr):
        #self.content = helper.readJsonFile(file)
       
        if arr is not None:
            for i in arr["matches"]:
                self.result.append( {
                    "id":i["vulnerability"]["id"],
                    "dataSource":i["vulnerability"]["dataSource"],
                    "severity":i["vulnerability"]["severity"],
                    "urls":i["vulnerability"]["urls"]
                    })
            self.final_result = {"image_result":self.result}
        else:
            self.final_result = {"image_result":[]}
        
        
        
    
        