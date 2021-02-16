import os
import yaml
from pydrive.auth import GoogleAuth, ServiceAccountCredentials
from pydrive.drive import GoogleDrive 
from pydrive.files import GoogleDriveFileList
from datetime import date

def authenticate():
    
# Authenticate to Google API
   
    with open("settings.yaml") as f: 
        settings = yaml.load(f, Loader=yaml.FullLoader)

    gauth = GoogleAuth()
    scope = settings["oauth_scope"]
    gauth.credentials = ServiceAccountCredentials.from_json_keyfile_name(settings["client_config_file"], scope)
    print("Authenticated")
    return GoogleDrive(gauth)

drive = authenticate()

path = r"E:\test"

#year saving
todays_date=date.today()
year= todays_date.strftime("%Y")
month= todays_date.strftime("%B")
yearid= 0
monthid=0
#searching for year in parent id and if not their it will create a folder

file_list = drive.ListFile({'q': "'1L1naprQRtMuKBF1FHtXwsUZJjTxCRWZx' in parents and trashed=false"}).GetList()
for file1 in file_list:
	#print('title: %s, id: %s' % (file1['title'], file1['id']))
	if(file1['title'] == year):
		yearid = file1['id']
		
if(yearid==0):
	folder_name = year
	folder = drive.CreateFile({'parents': [{'id': '1L1naprQRtMuKBF1FHtXwsUZJjTxCRWZx'}], 'title' : folder_name, 'mimeType' : 'application/vnd.google-apps.folder'})
	folder.Upload()
	#print('title: %s, id: %s' % (folder['title'], folder['id']))
	yearid = folder['id']
	#print(yearid)
	print(year + " Year Folder created successfully")
else:
	print(year + " Year Folder is already present")


#searchng for month in year folder if not there it will create month folder

file_list = drive.ListFile({'q': "'" + yearid + "' in parents and trashed=false"}).GetList()
for file1 in file_list:
	#print('title: %s, id: %s' % (file1['title'], file1['id']))
	if(file1['title'] == month):
		monthid = file1['id']
		#print (monthid)
		#print(month + " Month is present")

if(monthid==0):
	folder_name = month
	folder = drive.CreateFile({'parents': [{'id': yearid}], 'title' : folder_name, 'mimeType' : 'application/vnd.google-apps.folder'})
	folder.Upload()
	#print('title: %s, id: %s' % (folder['title'], folder['id']))
	monthid = folder['id']
	#print(monthid)
	print(month + " Month Folder created successfully")
else:
	print(month + " Month Folder is already present")
	

#uploading files to drive month folder


for x in os.listdir(path): 

	f = drive.CreateFile({'parents': [{'id': monthid}],'title': x}) 
	f.SetContentFile(os.path.join(path, x)) 
	f.Upload() 
	f = None
print("Files Uploaded successfully")


#Removing files from local directory

'''
files = glob.glob(path + "\*")
for f in files:
    os.remove(f)
print("Local data cleared successfully")
'''
