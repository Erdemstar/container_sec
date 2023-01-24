from container_sec.helper import Helper
import re

class DF:
    def __init__(self, filepath):
        self.filepath = filepath
        self.base_image_name = ""
        self.dockerfileLines = []
        self.result = []
        self.final_result = []
       
       
        self.helper = Helper()

    def startAudit(self):
        self.readDockerfile()

        self.rulesControl1()
        self.rulesControl2()
        self.rulesControl3()
        self.rulesControl4()
        self.rulesControl5()
        self.rulesControl6()
        self.rulesControl7()
        self.rulesControl8()
        self.rulesControl9()

        self.result.append({"image_scan_result":""})
        self.final_result = {"dockerfile_result":self.result}
    
    def finishAudit(self):
        self.dockerfileLines = []
        self.result = []
        self.final_result = []
        self.helper.deleteFile(self.filepath)
        self.filepath = ""

    def readDockerfile(self):
        """
        Description : 
        """
        self.dockerfileLines = self.helper.readDockerfile(self.filepath)
    
    def rulesControl1(self):
        """
        Description : This control is used is there EXPOSE 22 or not
        """
        name = "DF-1"
        rule = "^(?i)expose 22$"
        description = "Ensure port 22 is not exposed"
        recommedation = "https://docs.docker.com/engine/reference/builder/#expose"
        result = None

        for line in self.dockerfileLines:
            result = re.search(rule,line)
            
            if result is not None:
                self.result.append(self.helper.writeOutputTerminalScreen(name,description,recommedation))
                break
    
    def rulesControl2(self):
        """
        Description : This control is used is there EXPOSE 22 or not
        """
        name = "DF-2"
        rule = "^(?i)healthcheck.*"
        description = "Ensure that HEALTHCHECK instructions have been added to container images"
        recommedation = "https://docs.docker.com/engine/reference/builder/#healthcheck"
        result = None

        for line in self.dockerfileLines:
            result = re.search(rule,line)

            if result is not None:
                break
        
        if result is None:
            self.result.append(self.helper.writeOutputTerminalScreen(name,description,recommedation))
            
    def rulesControl3(self):
        """
        Description : This control is used is there EXPOSE 22 or not
        """
        name = "DF-3"
        rule = "^(?i)user.*"
        description = "Ensure that a user for the container has been created"
        recommedation = "https://docs.docker.com/engine/reference/builder/#user"
        result = None

        for line in self.dockerfileLines:
            result = re.search(rule,line)

            if result is not None:
                break
        
        if result is None:
            self.result.append(self.helper.writeOutputTerminalScreen(name,description,recommedation))
                
    def rulesControl4(self):
        """
        Description : This control is used is there EXPOSE 22 or not
        """
        name = "DF-4"
        rule = "^(?i)add.*"
        description = "Ensure that COPY is used instead of ADD in Dockerfiles"
        recommedation = "https://docs.docker.com/engine/reference/builder/#copy"
        result = None

        for line in self.dockerfileLines:
            result = re.search(rule,line)
  
            if result is not None:
                self.result.append(self.helper.writeOutputTerminalScreen(name,description,recommedation))
                break

    def rulesControl5(self):
        """
        Description : This control is used is there EXPOSE 22 or not
        """
        name = "DF-5"
        rule = "^(?i)maintainer.*"
        description = "Ensure that LABEL maintainer is used instead of MAINTAINER (deprecated)"
        recommedation = "https://docs.docker.com/engine/reference/builder/#label"
        result = None

        for line in self.dockerfileLines:
            result = re.search(rule,line)

            if result is not None:
                self.result.append(self.helper.writeOutputTerminalScreen(name,description,recommedation))
                break
                    
    def rulesControl6(self):
        """
        Description : This control is used is there EXPOSE 22 or not
        """
        name = "DF-6"
        rule = ".*(?i):latest.*"
        description = "Ensure the base image uses a non latest version tag"
        recommedation = ""
        result = ""

        for line in self.dockerfileLines:
            result = re.search(rule,line)

            if result is not None:
                self.result.append(self.helper.writeOutputTerminalScreen(name,description,recommedation))
                break
                
    def rulesControl7(self):
        """
        Description : This control is used is there EXPOSE 22 or not
        """
        name = "DF-7"
        rule = "^(?i)user.*"
        description = "Ensure the last USER is not root"
        recommedation = "https://docs.docker.com/engine/reference/builder/#user"
        result = []

        for line in self.dockerfileLines:
            tmp = re.search(rule,line)

            if tmp is not None:
                result.append(tmp.group())
        
        if len(result) > 1 and str(result[-1]).endswith("root"):
            self.result.append(self.helper.writeOutputTerminalScreen(name,description,recommedation))
    
    def rulesControl8(self):
        """
        Description : This control is used is there EXPOSE 22 or not
        """
        name = "DF-8"
        rule1 = "(?i)from .*[a-zA-Z]?[:|\/].*"
        rule2 = "(?i)copy --from="
        description = "Ensure that used multiple stage for minimum docker image"
        recommedation = ""
        result1 = []
        result2 = []

        for line in self.dockerfileLines:
            tmp = re.search(rule1,line)
            tmp2 = re.search(rule2,line)

            if (tmp is not None):
                result1.append(tmp.group())

                self.base_image_name = tmp.group()

            if (tmp2 is not None):
                result2.append(tmp2.group())

        if len(result1) < 2 or len(result2) < 1:  
            self.result.append(self.helper.writeOutputTerminalScreen(name,description,recommedation))
    
    def rulesControl9(self):
        """
        Description : This control is used is there EXPOSE 22 or not
        """
        name = "DF-9"
        description = "Ensure that secret information is not in Dockerfile"
        recommedation = ""
        rule = "(?i)(password|pword|pwd|pass)"
        result = []

        for line in self.dockerfileLines:
            tmp = re.search(rule,line)

            if tmp is not None:
                self.result.append(self.helper.writeOutputTerminalScreen(name,description,recommedation))
                break       


    def readBaseimageFromDockerfile(self):
        rule1 = "(?i)from .*[a-zA-Z]?[:|\/].*"
        for line in self.dockerfileLines:
            tmp = re.search(rule1,line)

            if tmp is not None:
                self.base_image_name = tmp.group()
                break

        tmp = self.base_image_name.split(" ")
        return tmp[1]
        


    def rulesControl51(self):
        """
        Description : This control is used is there EXPOSE 22 or not
        """
        name = "DF-5"
        rule = "erdem"
        description = "Ensure update instructions are not use alone in the Dockerfile"
            
    def rulesControl91(self):
        """
        Description : This control is used is there EXPOSE 22 or not
        """
        name = "DF-9"
        rule = "erdem"
        description = "Ensure that APT isn’t used"

    def rulesControl101(self):
        """
        Description : This control is used is there EXPOSE 22 or not
        """
        name = "DF-10"
        rule = "erdem"
        description = "Ensure that WORKDIR values are absolute paths"

    def rulesControl11(self):
        """
        Description : This control is used is there EXPOSE 22 or not
        """
        name = "DF-11"
        rule = "erdem"
        description = "Ensure From Alias are unique for multistage builds"

    def rulesControl121(self):
        """
        Description : This control is used is there EXPOSE 22 or not
        """
        name = "DF-12"
        rule = "erdem"
        description = "Ensure that sudo isn’t used"




    
