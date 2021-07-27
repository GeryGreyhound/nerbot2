import random
from selenium import webdriver
import datetime
import time
import requests
import json
import time

START_FROM = 3555 # egyelőre leállás után kézzel kell megadni, hogy honnan folytassa
FILL_UNTIL = 200000
DELAY_MULTIPLIER = 1 # videón való prezentálhatóság kedvéért lassítja a működést, ha 0-ra teszed, akkor nem (még nincs implementálva)


def format_td(seconds, digits=2):
	isec, fsec = divmod(round(seconds*10**digits), 10**digits)
	return ("{}.{:0%d.0f}" % digits).format(datetime.timedelta(seconds=isec), fsec)

def generate_email_2(count, string = "orbangeciorbangeciorbangeciorbangecio1g"):
	binary_string = bin(count).replace("0b", "")
	# ez így még párszázezer kombinációra jó :D
	return_string = ""
	for counter, char in enumerate(string):
		try:
			if binary_string[counter] == "1":
				return_string += char + "."
			else:
				return_string += char
		except:
			if counter == len(binary_string):
				return_string += char + "."
			else:
				return_string += char

	return return_string + "@gmail.com"

 
get_email_addr = 'https://www.1secmail.com/api/v1/?action=genRandomMailbox'
get_incoming_msg = 'https://www.1secmail.com/api/v1/?action=getMessages&login={}&domain={}'
get_msg_content = 'https://www.1secmail.com/api/v1/?action=readMessage&login={}&domain={}&id={}'
 
 
# gyart egy uj email cimet
def get_new_email_addr():
	email_arr = json.loads(requests.get(get_email_addr).text)
	return email_arr[0]


def get_incoming_email(email_addr):
	usr, domain = email_addr.split('@')
	resp = requests.get(get_incoming_msg.format(usr, domain))
	if resp.status_code == 200 and len(resp.text) > 2:
		try:
			response = json.loads(resp.text)
			return response[0]['id']
		except:
			return None
	 
# visszaadja az email body-jat, ebbol kell kiparszolni a linket
def get_email_content(email, id):
	usr, domain = email.split('@')
	resp = requests.get(get_msg_content.format(usr, domain, id))
	if resp.status_code == 200 and len(resp.text) > 2:
		try:
			response = json.loads(resp.text)
			return response['body']
		except:
			return None
	else:
		return None

def de_accentize(string):
	character_pairs = {"á" : "a", "é" : "e", "í" : "i", "ó" : "o", "ö" : "o", "ő" : "o", "ú" : "u", "ü" : "u", "ű" : "u"}
	
	for character in character_pairs:
		if character in string:
			string = string.replace(character, character_pairs[character])
		elif character.upper() in string:
			string = string.replace(character.upper(), character_pairs[character].upper())
	
	return string

class Person:
	def __init__(self, person_id):
		self.id = person_id
		self.name = self.generate_random_name()
		self.age = random.randint(18,85)
		# v1 self.email = "or.ban3gy.g3ci+" + str(self.id).zfill(5) + de_accentize(self.family_name.lower() + "." + de_accentize(self.first_name.lower().replace(" ", "."))) + "_" + str(self.age) + "@gmail.com"
		# v2 self.email = generate_email_2(self.id-START_FROM)
		self.email = get_new_email_addr()

	def generate_random_name(self, double_name_percentage = 5):
		family_names = ["NAGY","KOVÁCS","TÓTH","SZABÓ","HORVÁTH","VARGA","KISS","MOLNÁR","NÉMETH","FARKAS","BALOGH","PAPP","LAKATOS","TAKÁCS","JUHÁSZ","OLÁH","MÉSZÁROS","SIMON","RÁCZ","FEKETE","SZILÁGYI","TÖRÖK","FEHÉR","BALÁZS","GÁL","KIS","SZŰCS","ORSÓS","KOCSIS","FODOR","PINTÉR","SZALAI","SIPOS","MAGYAR","LUKÁCS","GULYÁS","BIRÓ","KIRÁLY","BALOG","LÁSZLÓ","BOGDÁN","JAKAB","KATONA","SÁNDOR","VÁRADI","BOROS","FAZEKAS","KELEMEN","ANTAL","OROSZ","SOMOGYI","FÜLÖP","VERES","BUDAI","VINCZE","HEGEDŰS","DEÁK","PAP","BÁLINT","ILLÉS","PÁL","VASS","SZŐKE","FÁBIÁN","VÖRÖS","LENGYEL","BOGNÁR","BODNÁR","JÓNÁS","SZÜCS","HAJDU","HALÁSZ","MÁTÉ","SZÉKELY","GÁSPÁR","KOZMA","PÁSZTOR","BAKOS","DUDÁS","VIRÁG","MAJOR","ORBÁN","HEGEDÜS","BARNA","NOVÁK","SOÓS","TAMÁS","NEMES","PATAKI","BALLA","FARAGÓ","KEREKES","BARTA","PÉTER","BORBÉLY","CSONKA","MEZEI","SÁRKÖZI","BERKI","MÁRTON"]
		first_names = [
				["Gábor","László","Attila","Péter","Tamás","István","Zsolt","József","János","Csaba","Sándor","Róbert","Krisztián","Ferenc","András","Balázs","Tibor","Norbert","Szabolcs","Imre","György","Gergely","Lajos","Roland","Viktor","Gyula","Károly","Miklós","Mihály","Béla","Dániel","Ákos","Ádám","Richárd","Árpád","Dávid","Pál","Szilárd","Antal","Bálint","Levente","Márton","Géza","Kornél","Gergő","Kálmán","Endre","Nándor","Máté","Barnabás","Dénes","Jenő","Márk","Ernő","Mátyás","Ottó","Dezső","Bence","Vilmos","Ervin","Áron","Arnold","Olivér","Bertalan","Rudolf","Milán","Albert","Lóránt","Szilveszter","Andor","Kristóf","Barna","Győző","Henrik","Iván","Adrián","Erik","Jácint","Gusztáv"],
				["Krisztina","Katalin","Mónika","Szilvia","Anita","Zsuzsanna","Éva","Judit","Ágnes","Tímea","Erika","Ildikó","Mária","Anikó","Melinda","Gabriella","Eszter","Beáta","Erzsébet","Viktória","Tünde","Edina","Adrienn","Bernadett","Rita","Edit","Orsolya","Hajnalka","Csilla","Renáta","Brigitta","Annamária","Veronika","Nikoletta","Marianna","Enikő","Ilona","Anna","Dóra","Nóra","Márta","Mariann","Barbara","Anett","Henrietta","Beatrix","Ibolya","Zsófia","Emese","Noémi","Zita","Réka","Nikolett","Gyöngyi","Kinga","Diána","Julianna","Zsanett","Zsuzsa","Magdolna","Klára","Margit","Lívia","Angéla","Petra","Piroska","Boglárka","Henriett","Alexandra","Irén","Szabina","Helga","Timea","Klaudia","Ivett","Izabella","Valéria","Júlia"]]
	
		rnd = random.randint(0,100)
		gender = random.randint(0,1) # A GENDER VESZÉLYES!!!!!!4 STOP SOROS
	
		if rnd < double_name_percentage:
			names = 2
		else:
			names = 1
	
		self.family_name = family_names[random.randint(0, len(family_names)-1)].lower().capitalize()
		
		self.first_name = ""
	
		for n in range(names):
			selected_name = first_names[gender][random.randint(0,len(first_names[gender])-1)]
			if self.first_name == "":
				self.first_name = selected_name
			else:
				self.first_name = self.first_name + " " + selected_name

	def register(self):
		driver.get("https://nemzetikonzultacio.kormany.hu/")
		time.sleep(.5)
		family_name_input = driver.find_element_by_id("mat-input-0")
		family_name_input.send_keys(self.family_name)
		time.sleep(.2)
		first_name_input = driver.find_element_by_id("mat-input-1")
		first_name_input.send_keys(self.first_name)
		time.sleep(.2)
		# age_input = driver.find_element_by_xpath("//*[@class='small-input ng-pristine ng-invalid ng-touched']")
		age_input = driver.find_element_by_xpath("//input[@placeholder='Életkor * (kötelező)']")
		age_input.send_keys(self.age)
		time.sleep(.2)
		email_input = driver.find_element_by_id("mat-input-2")
		email_input.send_keys(self.email)
		time.sleep(.2)

		# driver.execute_script("window.scrollTo(0, document.body.scrollHeight);")

		for s in range(50):
			driver.execute_script("window.scrollBy(0, 10);")
			time.sleep(.005)

		
		cboxes = driver.find_elements_by_class_name("mat-checkbox-inner-container")
		for cbox in cboxes:
			cbox.click()
			time.sleep(.25)

		reg_button = driver.find_element_by_xpath("//*[@class='btn w-auto']")
		reg_button.click()

	def check_email(self):
		email_id = None

		retry_counter = 0
		
		while email_id == None:
			email_id = get_incoming_email(self.email)
			print(".", end="", flush=True)
			time.sleep(.25)
			retry_counter += 1

			if retry_counter == 10:
				print("Ez sajnos nem sikerült, jöjjön a következő NER-birka, ne álljunk le!")
				time.sleep(1)
				break

		try:
			mail_body = get_email_content(self.email, email_id)
			part_list = list(mail_body.split("<"))
		
			for counter, part in enumerate(part_list):
				if "a href" in part:
					url, junk = part.split('" target=')
					url = url.replace('a href="', "")				
					self.custom_url = url
		except:
			self.custom_url = None


	def fill_form(self):
		driver.get(self.custom_url)

		time.sleep(.5)
		
		radio_buttons = driver.find_elements_by_css_selector("input[type='radio']")

		fill_pattern = list()
		fill_pattern_check = list()
		counter = 0

		for x in range(14):
			select = random.randint(0,1)
			fill_pattern.append(counter+select)
			fill_pattern_check.append(select)
			counter += 2

		# print("fill pattern", fill_pattern)
		# print("fill pattern check", fill_pattern_check)

		for counter, rb in enumerate(radio_buttons):
			# actions.move_to_element(rb).perform()
			driver.execute_script("return arguments[0].scrollIntoView(true);", rb)
			driver.execute_script("window.scrollBy(0, -400);")
			
			if counter in fill_pattern:
			# if 1 == 1:
				driver.execute_script("arguments[0].click();", rb)
				time.sleep(.1)
			else:
				pass

		for s in range(10):
			driver.execute_script("window.scrollBy(0, 10);")
			time.sleep(.05)


		reg_button = driver.find_element_by_xpath("//*[@class='btn submit-btn']")
		driver.execute_script("arguments[0].click();", reg_button)
				

if __name__ == "__main__":
	

	import os
	driver = webdriver.Chrome("D:\\chromedriver.exe")
	start_time = datetime.datetime(2021,7,25,22,0)
	
	for x in range(START_FROM, FILL_UNTIL):

		os.system("cls")
		print("================================================================================\n                                    -= NERbot 2.0 =-                  \nDISCLAIMER: a robot egy átlagos Fideszesnél is butább (talán még Hollik Istvánnál is,\n      de ez nem biztos) és csak véletlenszerű válaszokat ad az egyes kérdésekre.\n      A KÉRDÉSEKRE ADOTT VÁLASZOK NEM TÜKRÖZIK A ROBOT FEJLESZTŐJÉNEK ÁLLÁSPONTJÁT,\n     A NERBOT KIZÁRÓLAGOS CÉLJA A KORMÁNYZATI INFORMATIKA SZÍNVONALÁNAK DEMONSTRÁLÁSA\n================================================================================\n")
		
		person = Person(person_id = x)
		person.start_time = datetime.datetime.now()
		
		print("{} vagyok, {} éves, a(z) {}. sorszámú NER-birka.\nRegisztrálok e-mailcímmel: {}".format(person.family_name + " " + person.first_name, person.age, person.id, person.email))
	
		if person.family_name == "Kiss" and person.first_name == "Endre":
			print("Egyébként 23 centis a fütyim! Na konzultáció, csá!")
			time.sleep(2)
			print("Hol az APPLY gomb?")
			time.sleep(2)
			print("MIFAAAAN? NYEM ÉJTEM")
			time.sleep(2)
			print("KÉSZ ebben eddig lehetett eljutni :( Csá.")

		else:
			person.register()
	
			print("Regisztráció megtörtént, várom az e-mailt")
		
			person.check_email()
		
			if person.custom_url:
				print("Megjött! Nyomás kitölteni: " + person.custom_url)
		
				person.fill_form()
		
				person.end_time = datetime.datetime.now()
		
				person.time = person.end_time - person.start_time
				person.seconds = format_td(person.time.seconds, digits=2)
	
				# person.time = person.time.strftime("%S") + "," + person.time.strftime("%f")[:2]
				total_time = datetime.datetime.now() - start_time
		
				print("Konzultáció kitöltve, {} másodpercig tartott, összes eltelt idő: {}\n".format(person.seconds, total_time))

			else:
				pass

		time.sleep(2)

	driver.quit()
