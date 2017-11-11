from bs4 import BeautifulSoup
import requests
import codecs
import re
from time import strftime as stime
import os
import sys
import getpass

URL = "https://www.facebook.com"
image_dir = "local_images"

example_mail = "example.id@mail.com"
example_pw = "password"

local_pagename = example_mail + "_00-00-0000_00-00-00" + ".html"

def facebook_login(mail=example_mail, password=example_pw):
    s = requests.Session()
    r = s.get( URL, allow_redirects=False)
    print("requesting... " + r.url)
    
    soup = BeautifulSoup(r.text, "html.parser" )
    
    fb_form = soup.find("form", id="login_form")
    action_url = fb_form["action"]
    
    inputs = fb_form.findAll("input", {"type": ["hidden", "submit"]})
    
    post_data = { i.get("name"): i.get("value")  for i in inputs }
    
    post_data["email"] = mail
    post_data["pass"] = password.upper()
    
    
    scripts = soup.findAll("script")
    
    scripts_string = ("/n/").join( [ script.text for script in scripts ] )
    
    datr_search = re.search('\["_js_datr","([^"]*)"', scripts_string, re.DOTALL)
    if datr_search:
        datr = datr_search.group(1)
        cookies = {'_js_datr' : datr}
        return s.post(action_url, data=post_data, cookies=cookies, allow_redirects=True)
    else:
        return False
    

def create_local_image(mail=example_mail, password=example_pw):
    
    redirect = facebook_login(mail, password)
    
    if redirect == False:
    	print("Failed.")
        return
    
    if not os.path.exists(image_dir):
        os.makedirs(image_dir)
    
    local_pagename = image_dir + "\\" + mail + "_" + stime("%d-%m-%Y_%H-%M-%S") + ".html"
    
    f = codecs.open(local_pagename,"w","utf-8")
    f.write(redirect.text)
    f.close()
    
    print("Account loaded locally.")

def main():
	if(len(sys.argv) == 3):
		_mail = sys.argv[1]
		_pw = sys.argv[2]

		if((not _mail) or (not _pw)):
			print("Invalid Parameters. Enter again.")
			_mail = input()
			_pw = input()
		create_local_image(mail=_mail, password=_pw)

	elif(len(sys.argv) == 2):
		_mail = sys.argv[1]

		if(not _mail):
			print("Invalid Parameters. Enter again.")
			_mail = input()

		_pw = getpass.getpass("Enter password:")
		create_local_image(mail=_mail, password=_pw)

	else:
		create_local_image()

if __name__ == '__main__':
	main()
