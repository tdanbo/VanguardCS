import os
import json
import shutil
class License():
    def __init__(self):
        self.license_source = "VanguardRP"
        self.cwd = os.getcwd()

        self.local_license = os.path.join(self.cwd, "world.key")
        self.distributed_license = os.path.join(os.getenv("APPDATA"), self.license_source, "world.key")

    def get_license(self):
        if os.path.isfile(self.local_license):
            print(f"Local script license found!")
            self.license = self.local_license
            self.open_license = json.load(open(self.license, "r"))
            return self.open_license      
             
        elif os.path.isfile(self.distributed_license):
            print(f"Distributed license found!")
            self.license = self.distributed_license
            self.open_license = json.load(open(self.license, "r"))
            self.delete_distributed_license()
            return self.open_license
        else:
            raise Exception("No license found!")
        
    def delete_distributed_license(self):
        shutil.rmtree(os.path.dirname(self.distributed_license))

            

