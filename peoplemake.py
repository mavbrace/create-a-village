import sys
import os.path
import os 
import time
from random import randint

houses = 0
femaleNames = ["Lilly","Sia","Iavva","Nella","Lynne","Arra","Daisy","Sun","Blue","Ria","Larra","Char","Niami","Kanna","Tisal","Lydia","Mina","Safta","Rose","Flower","Asula","Notsi"];
maleNames = ["Mirid","Gum","Sam","Dave","Red","Blue","Darren","Victor","Shaun","Sebastian","Lehat","Yiod","Getsad","Furlid","Ralde","Grim","Fall","Winter","Sim","Gett","Mal"];
display_info = False

class Tribe:
	def __init__(self, name):
		self.name = name
		self.level = "new settlement"
		self.founder = None
		
	def addLevel(self,level):
		if level == 0:
			self.level = "abandoned settlement"
		elif level < 51: # 1 - 50 
			self.level = "hamlet"
		elif level < 501: # 51 - 500
			self.level = "village"
		elif level < 5001: # 201 - 5000
			self.level = "town"
		elif level > 5000: # 5001+
			self.level = "large town"
			
	def addFounder(self,founder): # Person
		self.founder = founder
				
	def displayVillageInfo(self):
		print("The %s of %s" %(self.level, self.name))


class Person:
	personCount = 0
	def __init__(self, name, gender, hair, hairtype, eyes, age, height, skin, nose):
		self.name = name
		self.gender = gender
		self.founder = False
		self.founder_descendant = False
		self.childCount = 0
		#------HAIR------------------# (6)
		self.hairInt = hair
		if hair == 0: 
			self.hair = "blonde"
		elif hair == 1: 
			self.hair = "red"
		elif hair == 2:
			self.hair = "brown"
		elif hair == 3:
			self.hair = "black"
		elif hair == 4:
			self.hair = "chestnut"
		elif hair == 5:
			self.hair = "white"
		#------EYES------------------# (7)
		self.eyesInt = eyes
		if eyes == 0:
			self.eyes = "brown"
		elif eyes == 1:
			self.eyes = "dark brown"
		elif eyes == 2:
			self.eyes = "blue"
		elif eyes == 3:
			self.eyes = "grey"
		elif eyes == 4:
			self.eyes = "green"
		elif eyes == 5:
			self.eyes = "hazel"
		elif eyes == 6:
			self.eyes = "midnight blue"
		#--------HAIR TYPE-----------# (3)
		self.hairtypeInt = hairtype
		if hairtype == 0:
			self.hairtype = "straight"
		elif hairtype == 1:
			self.hairtype = "wavy"
		elif hairtype == 2:
			self.hairtype = "curly"
		#-------HEIGHT---------------# (3)
		self.height = height
		#--------SKIN----------------# (4)
		self.skinInt = skin
		if skin == 0:
			self.skin = "pale"
		elif skin == 1:
			self.skin = "light"
		elif skin == 2:
			self.skin = "medium"
		elif skin == 3:
			self.skin = "dark"
		#--------NOSE TYPE----------#(5) - but random 4
		self.noseInt = nose
		if nose == 0:
			self.nose = "hawk"
		elif nose == 1:
			self.nose = "strong"
		elif nose == 2:
			self.nose = "straight"
		elif nose == 3:
			self.nose = "snub"
		elif nose == 4:
			self.nose = "narrow"
			
		self.state = "alive"
		self.deathdate = -1 #still alive
		self.age = age
		self.health = 0
		self.twins = False
		self.message = ""
		
		self.father = None
		self.mother = None
			
		Person.personCount += 1
	
	def addDateofDeath(self,deathdate):
		self.deathdate = deathdate
		
	def incrementChildCount(self):
		self.childCount += 1
		
	def isFounder(self): #set this Person to be the founder (should only be one)
		self.founder = True
		
	def isFounderDescendant(self): #set this Person to be a descendant of the Founder
		self.founder_descendant = True
	
	def addParents(self,parent1,parent2):
		if parent1.gender == "male":
			self.father = parent1
			self.mother = parent2
		else:
			self.mother = parent1
			self.father = parent2
	
	def addMessage(self,message):
		self.message = message
	
	def displayCount(self):
		print ("Total people, living and dead: %d" %(Person.personCount))
		
	def displayPerson_simple(self):
		print("%s, %s, aged %d" %(self.name,self.gender,self.age))
		
	def displayPerson(self):
		print("----------")
		print("Name:%s\nInfo: %s / %s, %s hair, %s eyes, %s skin, and a %s nose" %(self.name, self.gender, self.hair, self.hairtype, self.eyes, self.skin, self.nose))
		print("Age: %d / %.2f ft. tall" %(self.age,self.height))
		if self.message != "":
			print("[ %s ]" %(self.message))
		if self.founder:
			print("[ The Founder ]")
		if self.founder_descendant:
			print("Descended from the Founder!")
		if self.deathdate != -1:  #if they're dead:
			print("[[Died in year %d]]" %(self.deathdate))
		if self.father != None:
			print("Parents: " + self.father.name + " and " + self.mother.name)
			
	def displayFamily(self):
		print ("                      " + self.name)
		if self.father != None:
			print("                   /           \\        ")
			print("               " + self.father.name + "          " + self.mother.name + "    ")
			print("             /     \\       /      \\")
			#father's family
			if self.father.father != None:
				print("         " + self.father.father.name + "    " + self.father.mother.name),
			else: #need the space
				print("                             ")
			#mother's family
			if self.mother.father != None:
				print("   " + self.mother.father.name + "     " + self.mother.mother.name)
			else: #need a newline
				print("")
				
				
		

def getTogether(first, second, people):
	global houses
	if first.age < 16 or second.age < 16:
		#too young
		return people
	if first.age > 50 or second.age > 50:
		#too old
		activity = randint(0,20)
		if activity == 0 or activity == 1 or activity == 2 or activity == 3:
			print(first.name + " and " + second.name + " built a house together.")
			houses += 1
		elif activity == 4:
			second.addMessage(("Unfortunately, %s died of a strange illness!" %(second.name)))
			second.state = "dead"
		return people
	if abs(first.age - second.age) > 15: #should be 15
		#age difference is too great - this is mostly to prevent parent-child relationships......ha...
		print("There was a good harvest this year.")
		for i in range(len(people)): #increment people's health
			if people[i].health != 5:
				people[i].health += 1
		return people
	if first.twins == True and second.twins == True and first.age == second.age: #chances are they're twins
		return people
		
	if first.gender != second.gender:
		#print(first.name + " and " + second.name + " are getting together!")
		#print("They're having a child!")
		twins = randint(0,4) #one in 5 chance of having twins; 0 = twins
		#create new Person:
		one = birth(first, second)
		people.append(one)
		#print child, if there was one...
		if display_info:
                        one.displayPerson()
		if twins == 0: #there's twins!
			two = birth(first, second)
                        people.append(two)
                        if display_info:
                                two.displayPerson()
			two.twins = True
			one.twins = True
			#print("(Twins!)")	
	
	return people
	
	
def birth(first, second):
		
	gend = randint(0,1) #always random
		
	#based on mother and father--------HERIDITARY TRAITS---------------------#
	hairGen = randint(0,1) #0 for first, 1 for second
	if hairGen == 0: 
		hair = first.hairInt #inherits first's hair 
	else:
		hair = second.hairInt #inherits second's hair
	#----	
	hairtypeGen = randint(0,1) #0 for first, 1 for second
	if hairtypeGen == 0:
		hairtype = first.hairtypeInt #inherits first's hair type
	else:
		hairtype = second.hairtypeInt #inherits second's hair type
	#-----	
	eyesGen = randint(0,1) #0 for first, 1 for second
	if eyesGen == 0:
		eyes = first.eyesInt #inherits first's eyes
	else:
		eyes = second.eyesInt #inherits second's eyes
	#-----
	heightGen = randint(0,1) #***********
	if heightGen == 0:
		if first.health > 3 and first.height < 7.50:
			height = first.height + 0.5
		elif first.health < 2 and second.height > 3.50:
			height = first.height - 0.5
		else:
			height = first.height
	else:
		if second.health > 3 and second.height < 7.50:
			height = second.height + 0.5
		elif second.health < 2 and second.height > 3.50:
			height = second.height - 0.5
		else:
			height = second.height
	#-----
	skinGen = randint(0,1)
	if first.skinInt == second.skinInt: #same skin tone
		skin = first.skinInt
	elif abs(first.skinInt - second.skinInt) == 1: #similar skin tones
		if skinGen == 0:
			skin = first.skinInt
		else:
			skin = second.skinInt
	elif abs(first.skinInt - second.skinInt) == 2: #pretty different skin tones
		skin = (first.skinInt+second.skinInt)/2 #get a midtone
	else:
		skin = 2 #medium, otherwise
	#-----
	noseGen = randint(0,1)
	if noseGen == 0:
		nose = first.noseInt
	else:
		nose = second.noseInt
	
	#----SPECIAL------#
	bigRandom = randint(0,50)
	if bigRandom == 21:
		#special trait: midnight blue eyes
		eyes = 6
	elif bigRandom == 13:
		#special trait: grandfather's hair
		if first.father != None: #checking if grandfather exists
			hair = first.father.hairInt
	elif bigRandom == 0:
		#special trait: white hair
		hair = 5 
	elif bigRandom == 37:
		#special trait: grandmother's eyes
		if second.mother != None: #checking if grandmother exists
			eyes = second.mother.eyesInt
	elif bigRandom == 44:
		#special trait: straight hair
		hairtype = 0
	elif bigRandom == 5:
		nose = 1
		
	#--------------------------------------------------------#
	age = 0 #should start at 0
	if gend == 1:
		nameInt = randint(0,len(maleNames)-1)
		child = Person(maleNames[nameInt],"male",hair,hairtype,eyes,age,height,skin,nose)
		#del maleNames[nameInt]
	else:
		nameInt = randint(0,len(femaleNames)-1)
		child = Person(femaleNames[nameInt],"female",hair,hairtype,eyes,age,height,skin,nose)
		#del femaleNames[nameInt]
		
	#add if the child is descended from the Founder or not (must be firstborn child)
	if first.founder or first.founder_descendant:
		if first.childCount == 0:
			child.isFounderDescendant()
	elif second.founder or second.founder_descendant:
		if second.childCount == 0:
			child.isFounderDescendant()
	#add parents
	child.addParents(first,second)
	#record that they had a child:
	first.incrementChildCount()
	second.incrementChildCount()
	#return the final Person!
	return child
	
	
#ages people one year. In this place everyone ages at once. And...everyone dies when they're over 65. Will change later. Returns -1 if someone(or multiples) died, 0 if not.
def agePeople(people):
	test = 0
	for i in range(len(people)):
		people[i].age += 1
		if people[i].age > 65:
			print(people[i].name + " has died of old age!")
			people[i].state = "dead"
			test = -1
	return test #all's good = 0, someone(or multiple people) died = -1

#remove any 'dead' people from the list 'people'. This doesn't - and shouldn't - affect the personCount in the Person count.
def removeDead(people,records,date):
	
	for i in xrange(len(people)-1,-1,-1): #go from highest to lowest index (0)
		if people[i].state == "dead":
			people[i].deathdate = date
			records.append(people[i])
			del people[i]
			
	return (people,records)
	
def createRandomName(x):
	x = x[::-1]
	return x


#used in the graphical version---
def createRandomPerson():
        nameInt = randint(0,len(maleNames)-1) #the number of names in the name lists originally - 1 - i:::: (0,len(maleNames)-1-i)
        gend = randint(0,1)
        hair = randint(0,4)
        hairtype = randint(0,2)
        eyes = randint(0,5)
        nose = randint(0,3)
        h = randint(0,2)
        if h == 0:
                height = 5.0 #short
        elif h == 1:
                height = 5.5 #medium
        else:
                height = 6.0 #tall
        skin = randint(0,3)
        age = randint(20,45)
        if gend == 1:
                one = Person(maleNames[nameInt],"male",hair,hairtype,eyes,age,height,skin,nose)
                #del maleNames[nameInt] #add these back eventually
        else:
                one = Person(femaleNames[nameInt],"female",hair,hairtype,eyes,age,height,skin,nose)
                #del femaleNames[nameInt]

        return one		  

#used in the graphical version----
#max_years is the number of years you want to run the simulation for
def run_simulation(max_years,people,records):
        count = 0 #temporary count, just so I can limit the time...
        year = 0
	while len(people) > 0: #while there's still people alive!
		if count == max_years: #was 100
			break
		times_together = len(people)/4
		#print("---------------------------------------")
		for i in range(times_together):
			#choose two random people to get together :D ------#
			mate1 = randint(0,len(people)-1)
			mate2 = randint(0,len(people)-1)
			#to prevent duplicates...
			if mate1 == mate2 and mate2 != len(people)-1:
				mate2 += 1
			elif mate1 == mate2 and mate2 != 0:
				mate2 -= 1
			
			people = getTogether(people[mate1],people[mate2],people)
		#----------------------------------------------------------#
	
		#time.sleep(2)
		#print("A year has passed!")
		#increase the date
		year += 1
		if agePeople(people) == -1: #someone(s) died!
			people,records = removeDead(people,records,year) #remove them from the people list and add them to the records
	
		count += 1

        print("......\nThe End!")
	print("----Contents of Records------")
	for i in range(len(records)):
		records[i].displayPerson_simple()
	print("-----------------------------")
	print("----People still alive--------")
	descCount = 0
	for i in range(len(people)):
		people[i].displayPerson_simple()
		if people[i].founder_descendant:
			descCount += 1
		
	print("-----------------------------")
	print("Houses built: %d" %(houses))
	print("Current population: %d" %(len(people)))
	
	print("The year is: %d" %(year))
	if len(people) > 0:
		people[len(people)-1].displayFamily()



        return (people,records,houses)





def main():
	print("--Welcome!--")
	
	year = 0
	people = []
	records = []
	
	#Create a new Tribe
	homeName = raw_input("Please name your people! >>>")
	newName = createRandomName(homeName)
	home = Tribe(newName)
	print("Named: %s" %(newName))
	
	#Create 8 adult People, only from the BEGINNING!------------------------------))))
	for i in range(8):
		nameInt = randint(0,len(maleNames)-1) #the number of names in the name lists originally - 1 - i:::: (0,len(maleNames)-1-i)
		gend = randint(0,1)
		hair = randint(0,4)
		hairtype = randint(0,2)
		eyes = randint(0,5)
		nose = randint(0,3)
		h = randint(0,2)
		if h == 0:
			height = 5.0 #short
		elif h == 1:
			height = 5.5 #medium
		else:
			height = 6.0 #tall
		skin = randint(0,3)
		age = randint(20,45)
		if gend == 1:
			one = Person(maleNames[nameInt],"male",hair,hairtype,eyes,age,height,skin,nose)
			#del maleNames[nameInt] #add these back eventually
		else:
			one = Person(femaleNames[nameInt],"female",hair,hairtype,eyes,age,height,skin,nose)
			#del femaleNames[nameInt]
		
		#the founder is the first person created!
		if i == 0:
			home.addFounder(one)
			one.isFounder()
			
		people.append(one)
	
	for i in range(8):
		people[i].displayPerson()
	
	one.displayCount()
	print("......\n......")
	#----------------------------------------------------------------------)))))
	
	
	count = 0 #temporary count, just so I can limit the time...
	max = input("\nNow, how many years would you like to pass? >>>")
	while len(people) > 0: #while there's still people alive!----------------------------------------#
		if count == max: #was 100
			break
		times_together = len(people)/4
		#print("---------------------------------------")
		for i in range(times_together):
			#choose two random people to get together :D ---------#
			mate1 = randint(0,len(people)-1)
			mate2 = randint(0,len(people)-1)
			#to prevent duplicates...
			if mate1 == mate2 and mate2 != len(people)-1:
				mate2 += 1
			elif mate1 == mate2 and mate2 != 0:
				mate2 -= 1
			
			people = getTogether(people[mate1],people[mate2],people)
		#----------------------------------------------------------#
	
		#time.sleep(2)
		#print("A year has passed!")
		#increase the date
		year += 1
		if agePeople(people) == -1: #someone(s) died!
			people,records = removeDead(people,records,year) #remove them from the people list and add them to the records
	
		count += 1
	#------------------------------------------------------------------------------------------------#	
	
	print("......\nThe End!")
	print("----Contents of Records------")
	for i in range(len(records)):
		records[i].displayPerson_simple()
	print("-----------------------------")
	print("----People still alive--------")
	descCount = 0
	for i in range(len(people)):
		people[i].displayPerson_simple()
		if people[i].founder_descendant:
			descCount += 1
		
	print("-----------------------------")
	print("Houses built: %d" %(houses))
	home.addLevel(len(people))
	home.displayVillageInfo()
	print("Current population: %d" %(len(people)))
	print("The Founder was: %s / Currently %d of their direct descendants are living." %(home.founder.name,descCount))
	
	print("The year is: %d" %(year))
	if len(people) > 0:
		people[len(people)-1].displayFamily()

	
if __name__ == "__main__":
   main()
	
