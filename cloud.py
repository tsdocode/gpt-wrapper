import os
import owncloud

USERNAME = os.getenv('OC_USERNAME', 'sangtnguyen')
PASSWORD = os.getenv('OC_PASSWORD', '2112001a')
HOST = os.getenv('OC_HOST', 'http://192.168.55.215:30080/')


class OwnCloud():
    def __init__(self, username = USERNAME , password = PASSWORD , host = HOST) -> None:
        # try:

        print(username , password , host)
        self.oc = owncloud.Client(host)
        self.oc.login(username, password)

        self.connected = True


        # except Exception as e:
        #     print("Please provide correct username and password")
        #     print(e)
        #     self.connected = False

    def load_file(self, file_path):
        if self.connected:
            try:
                local_path = './' + file_path.split('/')[-1]
                success = self.oc.get_file(file_path , local_path)
                return local_path
            except:
                print("Please login")
                return None

    
    def put_file(self , local_file, remote_file):
        if self.connected:
            success = self.oc.put_file(remote_file, local_file)
            return success
        else:
            print('Please Login')



