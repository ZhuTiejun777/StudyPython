import requests

url = "http://127.0.0.1:8000/api/departments/"
myParam = {"dep_id":"T01"}
response = requests.get(url, params=myParam)
print(response.status_code)
print(response.text)  #查

myJson = {
			"data": [
					   {
						"dep_id":"T01",
						"cls_id":"2017T01C01",
						"cls_name":"2017级Test学院T01班",
						"master_name":"Master",
						"slogan":"slogan"
					   }
					]
		}
response = requests.post(url,json=myJson)
print(response.status_code)
print(response.text)  #增

myJson1 = {
			"data": [
					   {
						"dep_id":"T01",
						"cls_id":"2017T01C01",
						"cls_name":"2017级Test学院T01班",
						"master_name":"Master",
						"slogan":"slogan"
					   }
					]
		}
response1 = requests.put("http://127.0.0.1:8000/api/departments/{T01}/classes/{T01C01}",
                         json=myJson1)
print(response1.status_code)
print(response1.text)  #改

response2 = requests.delete("http://127.0.0.1:8000/api/departments/{T01}/classes/{T01C01}")
print(response2.status_code)
print(response2.text)

myJson2 = 		{
			"data": [
					  {
						"dep_id":"T01",
						"dep_name":"Test学院",
						"master_name":"Test-Master",
						"slogan":"Here is Slogan"
					  }
					]
		}
response3 = requests.delete("http://127.0.0.1:8000/api/departments/",
                            json=myJson2)
print(response3.status_code)
print(response3.text)   #增


