import requests
import json

url = "https://mashape-community-urban-dictionary.p.rapidapi.com/define"
word = input()
querystring = {"term":word}

headers = {
	"X-RapidAPI-Key": "089048036fmshf8c0f89abd73581p161612jsnee847f65edaf",
	"X-RapidAPI-Host": "mashape-community-urban-dictionary.p.rapidapi.com"
}
response_API = requests.request("GET", url, headers=headers, params=querystring)
print(response_API.status_code)
data = response_API.text
parse_json = json.loads(data)

info = parse_json['list'][0]['definition']
definition = info.replace("[", "").replace("]", "")
print(f"Definition of {word}:", definition)
