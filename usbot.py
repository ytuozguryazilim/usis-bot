import requests
import json
from bs4 import BeautifulSoup

_URL = "http://usis.yildiz.edu.tr/StdEnrollCourse.do"

def find_course_ids(headers, courses):
	course_ids = []
	page = requests.get(_URL, headers=headers)
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

def pick_courses(course_ids, headers, payload):
	for course_id in course_ids:
		payload['courseindex'] = course_id
		r = requests.post(_URL, headers=headers, data = payload)
		soup = BeautifulSoup(r.text,"html.parser")
		try:
			print(course_id,soup.find('div',{"class" : "warning"}).text.strip())
		except:
			print("Split Err,Not Login probably")

	pick_courses(course_ids, headers, payload)

def load_config(filename):
	with open(filename) as config_json:
		config = json.load(config_json)
		courses = config['courses']
		cookie = config['cookie']

	return cookie, courses

def main():
	course_ids = []
	cookie, courses = load_config('config.json')
	headers = {
		'Accept': 'text/html, application/xhtml+xml, image/jxr',
		'Accept-Encoding': 'gzip, deflate',
		'Accept-Language': 'tr,en-US;q=0.7,en;q=0.3',
		'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/58.0.3029.110 Safari/537.36 Edge/16.16299',
		'Cookie': "JSESSIONID={}".format(cookie),
		'Content-Type': 'application/x-www-form-urlencoded'
	}
	payload = {
		'coursetype':'0',
		'courseprefix':'',
		'courseindex':'',
		'button':'Ekle+%3E%3E'
	}
	try:
		course_ids = find_course_ids(headers, courses)
		print(course_ids)
	except:
		exit("Pls change cookie and control internet connection...")

	pick_courses(course_ids, headers, payload)

if __name__ == "__main__":
	main()