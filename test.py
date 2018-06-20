import requests

#r = requests.get("http://127.0.0.1:8000/webhook?hub.mode=hello&hub.challenge=world")
#print(r.text)
#print(r.content)

r = requests.post("http://127.0.0.1:8000/webhook", data={"hello": "world"})
print(r.text)
print(r.content)
