import requests
from bs4 import BeautifulSoup

#-------------CHANGE THOSE-------------
courses = [
	{ 'code' : 'BLM4520' , 'gr' : '1'},
	{ 'code' : 'BLM4821' , 'gr' : '1'}
]
cookie = "0000NHdtBXv9R7Qik1ES4tB2wnR:17bvem044"
#--------------------------------------

course_ids = []
url = "http://usis.yildiz.edu.tr/StdEnrollCourse.do"
payload = {
	'coursetype':'0',
	'courseprefix':'',
	'courseindex':'',
	'button':'Ekle+%3E%3E'
}

headers = {
		'Accept' : 'text/html, application/xhtml+xml, image/jxr',
		'Accept-Encoding' : 'gzip, deflate',
		'Accept-Language' : 'tr,en-US;q=0.7,en;q=0.3',
		'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/58.0.3029.110 Safari/537.36 Edge/16.16299',
		'Cookie' : 'JSESSIONID='+cookie,
		'Content-Type' : 'application/x-www-form-urlencoded'
	  }

def find_course_ids():
	page = requests.get(url,headers=headers)
	soup = BeautifulSoup(page.text,"html.parser")
	user_name = soup.find('span',{'class' : "logintitle"}).text
	user_name = ' '.join(user_name.split())
	print(user_name)
	for c in courses:
		tds = soup.findAll(text=c['code'])
		for td in tds :
			table = td.parent.parent
			if table.find("td",{"width" : "60"}).text.strip() == str(c['gr']) : 
				c_id = table.find("input",{"name" : "courseindex"})['value'];
				print(c['code'],c['gr'],"Id :",c_id);
				course_ids.append(c_id)

def pick_courses():
	for course_id in course_ids:
		payload['courseindex'] = course_id
		r = requests.post(url,headers=headers,data = payload)
		soup = BeautifulSoup(r.text,"html.parser")
		try:
			print(course_id,soup.find('div',{"class" : "warning"}).text.strip())
		except:
			print("Split Err,Not Login probably")
	pick_courses()

find_course_ids()
pick_courses()