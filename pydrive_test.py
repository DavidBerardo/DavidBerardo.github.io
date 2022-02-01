from pydrive.auth import GoogleAuth
from pydrive.drive import GoogleDrive

gauth = GoogleAuth()
gauth.LocalWebserverAuth() # client_secrets.json need to be in the same directory as the script
drive = GoogleDrive(gauth)


dir_ids = drive.ListFile({'q': "'1qV_8I5cfWsPfh_RRzVFXispCuyRE6DVS' in parents and trashed=false"}).GetList()
for dir_id in dir_ids:
	file_ids = drive.ListFile({'q': "'" + str(dir_id['id']) +"' in parents and trashed=false"}).GetList()
	for file_id in file_ids:
		print('Title: %s, ID: %s' % (file_id['title'], file_id['id']))