from dotenv import load_dotenv
import os
import base64
from requests import post, get
import json

#load the .env variables
#in this case, load the CLIENT_ID and the CLIENT_SECRET
load_dotenv()
client_id = os.getenv("CLIENT_ID")
client_secret = os.getenv("CLIENT_SECRET")


#getting the token for the authodication stuff
def get_token():
	#encoding client_id+client_secret in bade64
	auth_string = client_id+":"+client_secret
	auth_bytes = auth_string.encode("utf-8")
	auth_base64 = str(base64.b64encode(auth_bytes), "utf-8")

	#setting the headers 
	url = "https://accounts.spotify.com/api/token"
	headers = {
		'Authorization': "Basic "+auth_base64,
		"Content-Type": "application/x-www-form-urlencoded"
	}

	#getting the token
	data = {"grant_type": "client_credentials"}
	result = post(url, headers = headers, data=data)
	json_result = json.loads(result.content)
	token = json_result["access_token"]
	return token

#get the header required
def get_auth_header(token):
	return {"Authorization": "Bearer "+token}


#searching the id of an artist
def search_for_artist(token, artist_name):
	url = "https://api.spotify.com/v1/search"
	headers = get_auth_header(token)
	query = f"?q={artist_name}&type=artist&limit=1"
	query_url = url + query #final query url for the request

	result = get(query_url, headers=headers)
	json_result = json.loads(result.content)['artists']['items']#parse the json 

	if len(json_result) == 0:
		print("No artist with this name.")
		return none
	return json_result[0]

#get Spotify catalog information about an artist's top tracks by country
def get_songs_by_artist(token, artist_id):
	url = "https://api.spotify.com/v1/artists/{}/top-tracks?country=GR".format(artist_id)#endpoint
	headers = get_auth_header(token)
	result = get(url, headers= headers)
	json_result = json.loads(result.content)["tracks"]#parse the json 
	return json_result

token = get_token()
#search for artisti names "Mad Clip"
result = search_for_artist(token,"Mad Clip")
artist_id = result['id']
songs = get_songs_by_artist(token, artist_id)
for i in range (len(songs)):
	print(i+1,songs[i]["name"])