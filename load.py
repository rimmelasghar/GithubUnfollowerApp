## This file is taken from rawheel Github repository.
import requests,math
import threading

class Api_services:
    def githubApi(self,username):
        info=f"https://api.github.com/users/{username}"
        return info
    def githuburlApi(self,username,page,per_page,type_api):
        url = f"https://api.github.com/users/{username}/{type_api}?page={page}&per_page={per_page}"
        return url

class Load:
    def __init__(self,username,type_api):
        self.username = username
        self.apis = Api_services()
        self.type_api = type_api
        self.info = self.apis.githubApi(username) 
        self.response = requests.get(self.info).json()
        self.total = int(self.response[f"{type_api}"])
        self.length = math.ceil(self.total/100)
        self.data=[]
        # self.imgs = []

    def call_api(self,page):
        per_page = 100
        url = self.apis.githuburlApi(self.username,page,str(per_page),self.type_api)
        user_data = requests.get(url).json()
        # [self.data.append(user_data[i]["login"]) for i in range(len(user_data))]
        # [self.imgs.append(user_data[x]["avatar_url"]) for x in range(len(user_data))]
        [self.data.append(user_data[i]) for i in range(len(user_data))]
        
    def get_data(self):
        threads=[]
        for page in range(1,self.length+1):
            t = threading.Thread(target=self.call_api,args=[page])
            t.start()
            threads.append(t)
        for thread in threads:
            thread.join()
        
        return {self.username:self.data}
