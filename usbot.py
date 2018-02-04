import requests
import json
from bs4 import BeautifulSoup

_URL = "http://usis.yildiz.edu.tr/StdEnrollCourse.do"
_HEADERS = {
	'Accept': 'text/html, application/xhtml+xml, image/jxr',
	'Accept-Encoding': 'gzip, deflate',
	'Accept-Language': 'tr,en-US;q=0.7,en;q=0.3',
	'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/58.0.3029.110 Safari/537.36 Edge/16.16299',
	'Cookie': "JSESSIONID=",
	'Content-Type': 'application/x-www-form-urlencoded'
}
_PAYLOAD = {
	'coursetype':'0',
	'courseprefix':'',
	'courseindex':'',
	'button':'Ekle+%3E%3E'
}
def find_course_ids(courses):
	course_ids = []
	page = requests.get(_URL, headers=_HEADERS)
	soup = BeautifulSoup(page.text,"html.parser")
	user_name = soup.find('span',{'class' : "logintitle"}).text
	user_name = ' '.join(user_name.split())
	print(user_name)
	for c in courses:
		tds = soup.findAll(text=c['code'])
		for td in tds :
			table = td.parent.parent
			if table.find("td",{"width" : "60"}).text.strip() == str(c['gr']): 
				c_id = table.find("input",{"name" : "courseindex"})['value']
				print(c['code'],c['gr'],"Id :",c_id)
				course_ids.append(c_id)

	return course_ids

def pick_courses(course_ids):
	for course_id in course_ids:
		_PAYLOAD['courseindex'] = course_id
		r = requests.post(_URL, headers=_HEADERS, data = _PAYLOAD)
		soup = BeautifulSoup(r.text,"html.parser")
		try:
			msg = soup.find('div',{"class" : "warning"}).text.strip()
			print(course_id, msg)
			if msg.find('eklendi') != -1:
				course_ids.remove(course_id)
				print("removed")

		except:
			print("Split Err,Not Login probably")

	pick_courses(course_ids)

def load_config(filename):
	with open(filename) as config_json:
		config = json.load(config_json)
		courses = config['courses']
		cookie = config['cookie']

	return cookie, courses

def main():
	course_ids = []
	cookie, courses = load_config('config.json')
	_HEADERS['Cookie'] = "JSESSIONID={}".format(cookie)

	try:
		course_ids = find_course_ids(courses)
		print(course_ids)
	except:
		exit("Pls change cookie and control internet connection...")

	pick_courses(course_ids)

if __name__ == "__main__":
	main()