import requests
from time import sleep
from concurrent import futures

class Messaging:
    def __init__(self):
        self.LatestReceive = str()
        self.pytoURL = "https://DEV.herokuapp.com/pyto"
        self.postURL = "https://DEV.herokuapp.com/post"

    def callProcess(self):
        with futures.ThreadPoolExecutor() as executor:
            executor.submit(self.Receive)
            sleep(2)
            executor.submit(self.Send)

    def Receive(self):
        while True:
            HerokuRes = requests.get(self.pytoURL).text
            if self.LatestReceive != HerokuRes :
                self.LatestReceive = HerokuRes
                print("\r> Receive : {}".format(self.LatestReceive))
                print("\r> Send : ",end='')
            else:
                pass
            sleep(1)

    def Send(self):
        while True:
            Message = str(input("\r> Send : "))
            print("Sending... ", end='')
            if Message != "" :
                requests.post(self.postURL, data=Message.encode("utf-8"))
                print("Ok!")
            else:
                print("Nothing  to send.")

if __name__ == "__main__":
    MessagingClass = Messaging()
    MessagingClass.callProcess()
