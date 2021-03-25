from bs4 import BeautifulSoup
from pandas import DataFrame
import codecs
import glob
import os

def open_file(path):
	# Opens and returns a list of UTF-8 encoded HTML files.
	# Files are going to be used to extract student names.

	html_pages = []
	students = []

	names = False

	dir_path = os.path.normpath(path)
	os.chdir(dir_path)

	files = glob.glob('*.html')
	for f in files:
		html_pages.append(codecs.open(f, 'r', encoding='utf-8'))

	try:
		with open('names.txt') as file:
			for line in file:
				text = line.split('\n')[0].strip()
				if text != "":
					students.append(text)
		students.sort()
	except:
		print("Unable to open file, please make sure file name is correct.")

	return [html_pages, students]

def get_input():

	directory = input("Directory to class discussion HTMLs > ")

	return directory


def find_all_posts(page):
	# Returns all discussion posts & their title in the HTML file

	soup = BeautifulSoup(page, 'html.parser')
	title = soup.find('div', {'class':'pull-left'}).h1.text
	content = soup.find_all('div', {'class':'pull-left span4 discussion-header__metadata'})
	return [title, content]

def get_participants(content):
	# Returns list of discussion post authors

	name_list = []

	for c in content:
		text = c.h2.a.text.split('  ')[0]
		name = text.split(' \n')[0]
		if (name != 'Nick Kadochnikov'): # Instructor not counted in tallies
			name_list.append(name)

	return name_list

def get_students(names):
	# Returns list of students without duplicates

	students = list(set(names))
	students.sort()
	return students

def tally_count():
	# Returns a dictionary of students (no duplicates) 
	# with their participation count 

	participation = dict()

	for s in students:
		participation[s] = names.count(s)

	return participation

def get_total_participation():
	# Returns dictionary of students' total participation counts

	for s in students:
		total_participation[s] += participation[s]

	return total_participation

def number_of_disc_participation():
	# Returns a dictionary of each student and the # of discussions they posted in

	for s in students:
		if participation[s] != 0:
			discussions_participated[s] += 1

	return discussions_participated

def print_tally(students, participation, title):
	# Prints post count per student for a given discussion

	print(f'\n{title:^35s}')
	print("Student               Participation")
	print("-"*35)

	for s in students:
		try:
			print(f'{s:33} {participation[s]}')
		except:
			print(f'{s:33} 0')

def print_final_tally(students, total_participation):
	# Prints total amount of posts of each student

	print(f'\n===============Total Tally Count===============\n')
	print("                         Total     Forums")
	print("Student                  posts     participated\n")

	for s in students:
		print(f'{s:25} {total_participation[s]:4} {discussions_participated[s]:10}')

	print("="*47+"\n")

def export_excel():
	data = dict()
	data['Name'] = students

	for i in range(len(titles)):
		if titles[i] in ["Total posts", "Forums participated in"]:
			data[titles[i]] = list(total_participation.values())
			data[titles[i+1]] = list(discussions_participated.values())
			break
		data[titles[i]] = list(all_discussions[i].values())

	df = DataFrame(data)
	df.to_excel("Nick's Data Exploration and Visualization X426.61 Forum Posts Fall 2020.xlsx", sheet_name = "Sheet1", index = False)

	print("Export to excel sheet complete!")

if __name__ == '__main__':
	path = get_input()
	html_pages, students = open_file(path)
	titles = []
	total_participation = dict()
	discussions_participated = dict()
	all_discussions = []

	for s in students:
		total_participation[s] = 0
		discussions_participated[s] = 0

	for page in html_pages:
		title, posts = find_all_posts(page)
		titles.append(title)
		names = get_participants(posts)    # students w/ duplicates
		participation = tally_count()
		all_discussions.append(participation)
		total_participation = get_total_participation()
		discussions_participated = number_of_disc_participation()
		print_tally(students, participation, title)

	titles.append("Total posts")
	titles.append("Forums participated in")
	print_final_tally(students, total_participation)
	export_excel()
