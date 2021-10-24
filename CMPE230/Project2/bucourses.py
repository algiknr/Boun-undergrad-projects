import bs4 as bs
import urllib.request
import sys

#input first semester
x=sys.argv[1]
#input last semester 
y=sys.argv[2]

#earliest semester
s=1998

#will include semester names in input format
sem1=[]	
#will include semester names in url format
sem2=[]

#used to add all possible semester names and codes to lists sem1 and sem2
for c in range(0,63):
	if c%3==0:
		sem1.append(str(s)+'-Fall')
		sem2.append(str(s)+'/'+str((s+1))+"-1")
		s=s+1
		
	if c%3==1:
		sem1.append(str(s)+'-Spring')
		sem2.append(str((s-1))+'/'+str(s)+"-2")
		
	if c%3==2:
		sem1.append(str(s)+'-Summer')
		sem2.append(str((s-1))+'/'+str(s)+"-3")

#dept names added manually
deptnames = ['ASIAN STUDIES',
'ASIAN STUDIES WITH THESIS',
'ATATURK INSTITUTE FOR MODERN TURKISH HISTORY',
'AUTOMOTIVE ENGINEERING',
'BIOMEDICAL ENGINEERING',
'BUSINESS INFORMATION+SYSTEMS',
'CHEMICAL ENGINEERING',
'CHEMISTRY',
'CIVIL ENGINEERING',
'COGNITIVE SCIENCE',
'COMPUTATIONAL SCIENCE & ENGINEERING',
'COMPUTER EDUCATION & EDUCATIONAL TECHNOLOGY',
'COMPUTER ENGINEERING',
'CONFERENCE INTERPRETING',
'CONSTRUCTION ENGINEERING AND MANAGEMENT',
'CRITICAL AND CULTURAL STUDIES',
'EARTHQUAKE ENGINEERING',
'ECONOMICS',
'ECONOMICS AND FINANCE',
'EDUCATIONAL SCIENCES',
'EDUCATIONAL TECHNOLOGY',
'ELECTRICAL & ELECTRONICS ENGINEERING',
'ENGINEERING AND TECHNOLOGY MANAGEMENT',
'ENVIRONMENTAL SCIENCES',
'ENVIRONMENTAL TECHNOLOGY',
'EXECUTIVE MBA',
'FINANCIAL ENGINEERING',
'FINE ARTS',
'FOREIGN LANGUAGE EDUCATION',
'GEODESY',
'GEOPHYSICS',
'GUIDANCE & PSYCHOLOGICAL COUNSELING',
'HISTORY',
'HUMANITIES COURSES COORDINATOR',
'INDUSTRIAL ENGINEERING',
'INTERNATIONAL COMPETITION AND TRADE',
'INTERNATIONAL RELATIONS:TURKEY,EUROPE AND THE MIDDLE EAST',
'INTERNATIONAL RELATIONS:TURKEY,EUROPE AND THE MIDDLE EAST WITH THESIS',
'INTERNATIONAL TRADE',
'INTERNATIONAL TRADE MANAGEMENT',
'LEARNING SCIENCES',
'LINGUISTICS',
'MANAGEMENT',
'MANAGEMENT INFORMATION SYSTEMS',
'MATHEMATICS',
'MATHEMATICS AND SCIENCE EDUCATION',
'MECHANICAL ENGINEERING',
'MECHATRONICS ENGINEERING',
'MOLECULAR BIOLOGY & GENETICS',
'PHILOSOPHY',
'PHYSICAL EDUCATION',
'PHYSICS',
'POLITICAL SCIENCE & INTERNATIONAL RELATIONS',
'PRIMARY EDUCATION',
'PSYCHOLOGY',
'SCHOOL OF FOREIGN LANGUAGES',
'SECONDARY SCHOOL SCIENCE AND MATHEMATICS EDUCATION',
'SOCIAL POLICY WITH THESIS',
'SOCIOLOGY',
'SOFTWARE ENGINEERING',
'SOFTWARE ENGINEERING WITH THESIS',
'SUSTAINABLE TOURISM MANAGEMENT',
'SYSTEMS & CONTROL ENGINEERING',
'TOURISM ADMINISTRATION',
'TRANSLATION',
'TRANSLATION AND INTERPRETING STUDIES',
'TURKISH COURSES COORDINATOR',
'TURKISH LANGUAGE & LITERATURE',
'WESTERN LANGUAGES & LITERATURE']

#dept names added manually to use later for url reading purposes
prog=[]
prog.append("ASIA&bolum=ASIAN+STUDIES")
prog.append("ASIA&bolum=ASIAN+STUDIES+WITH+THESIS")
prog.append("ATA&bolum=ATATURK+INSTITUTE+FOR+MODERN+TURKISH+HISTORY")
prog.append("AUTO&bolum=AUTOMOTIVE+ENGINEERING")
prog.append("BM&bolum=BIOMEDICAL+ENGINEERING")
prog.append("BIS&bolum=BUSINESS+INFORMATION+SYSTEMS")
prog.append("CHE&bolum=CHEMICAL+ENGINEERING")
prog.append("CHEM&bolum=CHEMISTRY")
prog.append("CE&bolum=CIVIL+ENGINEERING")
prog.append("COGS&bolum=COGNITIVE+SCIENCE")
prog.append("CSE&bolum=COMPUTATIONAL+SCIENCE+%26+ENGINEERING")
prog.append("CET&bolum=COMPUTER+EDUCATION+%26+EDUCATIONAL+TECHNOLOGY")
prog.append("CMPE&bolum=COMPUTER+ENGINEERING")
prog.append("INT&bolum=CONFERENCE+INTERPRETING")
prog.append("CEM&bolum=CONSTRUCTION+ENGINEERING+AND+MANAGEMENT")
prog.append("CCS&bolum=CRITICAL+AND+CULTURAL+STUDIES")
prog.append("EQE&bolum=EARTHQUAKE+ENGINEERING")
prog.append("EC&bolum=ECONOMICS")
prog.append("EF&bolum=ECONOMICS+AND+FINANCE")
prog.append("ED&bolum=EDUCATIONAL+SCIENCES")
prog.append("CET&bolum=EDUCATIONAL+TECHNOLOGY")
prog.append("EE&bolum=ELECTRICAL+%26+ELECTRONICS+ENGINEERING")
prog.append("ETM&bolum=ENGINEERING+AND+TECHNOLOGY+MANAGEMENT")
prog.append("ENV&bolum=ENVIRONMENTAL+SCIENCES")
prog.append("ENVT&bolum=ENVIRONMENTAL+TECHNOLOGY")
prog.append("XMBA&bolum=EXECUTIVE+MBA")
prog.append("FE&bolum=FINANCIAL+ENGINEERING")
prog.append("PA&bolum=FINE+ARTS")
prog.append("FLED&bolum=FOREIGN+LANGUAGE+EDUCATION")
prog.append("GED&bolum=GEODESY")
prog.append("GPH&bolum=GEOPHYSICS")
prog.append("GUID&bolum=GUIDANCE+%26+PSYCHOLOGICAL+COUNSELING")
prog.append("HIST&bolum=HISTORY")
prog.append("HUM&bolum=HUMANITIES+COURSES+COORDINATOR")
prog.append("IE&bolum=INDUSTRIAL+ENGINEERING")
prog.append("INCT&bolum=INTERNATIONAL+COMPETITION+AND+TRADE")
prog.append("MIR&bolum=INTERNATIONAL+RELATIONS%3aTURKEY,EUROPE+AND+THE+MIDDLE+EAST")
prog.append("MIR&bolum=INTERNATIONAL+RELATIONS%3aTURKEY,EUROPE+AND+THE+MIDDLE+EAST+WITH+THESIS")
prog.append("INTT&bolum=INTERNATIONAL+TRADE")
prog.append("INTT&bolum=INTERNATIONAL+TRADE+MANAGEMENT")
prog.append("LS&bolum=LEARNING+SCIENCES")
prog.append("LING&bolum=LINGUISTICS")
prog.append("AD&bolum=MANAGEMENT")
prog.append("MIS&bolum=MANAGEMENT+INFORMATION+SYSTEMS")
prog.append("MATH&bolum=MATHEMATICS")
prog.append("SCED&bolum=MATHEMATICS+AND+SCIENCE+EDUCATION")
prog.append("ME&bolum=MECHANICAL+ENGINEERING")
prog.append("MECA&bolum=MECHATRONICS+ENGINEERING")
prog.append("BIO&bolum=MOLECULAR+BIOLOGY+%26+GENETICS")
prog.append("PHIL&bolum=PHILOSOPHY")
prog.append("PE&bolum=PHYSICAL+EDUCATION")
prog.append("PHYS&bolum=PHYSICS")
prog.append("POLS&bolum=POLITICAL+SCIENCE%26INTERNATIONAL+RELATIONS")
prog.append("PRED&bolum=PRIMARY+EDUCATION")
prog.append("PSY&bolum=PSYCHOLOGY")
prog.append("YADYOK&bolum=SCHOOL+OF+FOREIGN+LANGUAGES")
prog.append("SCED&bolum=SECONDARY+SCHOOL+SCIENCE+AND+MATHEMATICS+EDUCATION")
prog.append("SPL&bolum=SOCIAL+POLICY+WITH+THESIS")
prog.append("SOC&bolum=SOCIOLOGY")
prog.append("SWE&bolum=SOFTWARE+ENGINEERING")
prog.append("SWE&bolum=SOFTWARE+ENGINEERING+WITH+THESIS")
prog.append("TRM&bolum=SUSTAINABLE+TOURISM+MANAGEMENT")
prog.append("SCO&bolum=SYSTEMS+%26+CONTROL+ENGINEERING")
prog.append("TRM&bolum=TOURISM+ADMINISTRATION")
prog.append("WTR&bolum=TRANSLATION")
prog.append("TR&bolum=TRANSLATION+AND+INTERPRETING+STUDIES")
prog.append("TK&bolum=TURKISH+COURSES+COORDINATOR")
prog.append("TKL&bolum=TURKISH+LANGUAGE+%26+LITERATURE")
prog.append("LL&bolum=WESTERN+LANGUAGES+%26+LITERATURES")


count1=0
count2=0
start=0
finish=0

#determines the first and last semester
for i in sem1:
	if i== x:
		start = count1
	count1+=1

for j in sem1: 
	if j== y:
		finish = count2
	count2+=1
	
#data structures
mydict_dept={}		#{deptcode:mydict_deptname}
mydict_deptname={}	#{deptname:mydict_lesson}
mydict_lesson={}	#{coursecode:set_name_inst}
set_name_inst={}	#{coursename:sem_inst_dict}
sem_inst_dict={}	#{semester:set_inst}
set_inst=set()		#set of instructors of a specific course
set_inst_all=set()	#set of instructors of a specific department
set_courses=set()	#set of courses of a department
deptcount={} 		#{semester: [undergraduate, graduate]}
countlisttemp={}	#{deptname: deptcount}
countlist={}  		#{deptcode: countlisttemp}(semester based undergraduate&graduate counts)
totaldicttemp={}	#matches deptname to strings containing the info of undergraduate&graduate counts
totaldict={}		#{deptcode:totaldicttemp}
tttemp={}			#keeps info of total undergraduate&graduate column
tt={}				#{deptcode:tttemp}
coursenames={}		#this dict will be used to understand if a course has same code but different names

#some flags to help us examine correctly
atstart=1
initial=0
doit=1
look1=0
look2=0
initial_course_code=0
stop=False

#loops through all departments
for index2 in prog: 
	deptcode = index2.split('&')[0]
	deptname = deptnames[prog.index(index2)]
	dept_undergraduate=0
	dept_graduate=0
	#we also need to clear prev_course_code and current_course_code when going through another department since the last code of the previos department can coincide with the latter department's first course
	prev_course_code=0
	current_course_code=0
	
	set_courses.clear()
	coursenames.clear()

	#loops through all semesters according to the input semester range
	for index1 in range(start,finish+1):
		semester_graduate=0
		semester_undergraduate=0
		semester=sem1[index1]
		set_name_inst.clear()
		set_inst.clear()
		sem_inst_dict.clear()
	
		sauce2 = urllib.request.urlopen('https://registration.boun.edu.tr/scripts/sch.asp?donem='+sem2[index1]+'&kisaadi='+index2).read()
		soup2 = bs.BeautifulSoup(sauce2, 'lxml')

		for t1 in soup2.find_all("tr", {"class":["schtd", "schtd2"]}):
			#first reading handled separately
			if atstart ==1:
				t2 = t1.find_all("td")
				itr = iter(t2)
				course = (next(itr).text)			
				coursecode=course.split('.')[0]
				intcode = coursecode[-3:]
				#checks the course code and updates graduate/undergraduate counts for each semester
				#course codes that begin with 5 or more are graduate courses
				#everything else is counted as undergraduate course
				if not intcode.isdigit():
					if intcode[0].isdigit():
						look1=int(intcode[0],10)
						if look1>=5:
							semester_graduate +=1
							doit=0
						else:
							semester_undergraduate +=1
							doit=0
					else:
						semester_undergraduate +=1
						doit=0
				if doit==1:
					initial=int(intcode[0],10)
				#keeping the previous and current course codes to handle different sections of the course
				prev_course_code=intcode
				current_course_code = prev_course_code
				set_courses.add(coursecode)
				
				if doit==1:
					if initial>=5:
						semester_graduate +=1
					else:
						semester_undergraduate +=1

				next(itr)

				coursename=(next(itr).text)
				coursenames.update({coursecode:coursename})

				next(itr)
				next(itr)	

				#STAFF STAFF is not counted as a distinct instructor
				instructor=(next(itr).text)
				instructor=instructor[:-1]
				if(instructor != 'STAFF STAFF'):
					set_inst.add(instructor)
				set_inst.add(instructor)

				#updating the data structures 
				sem_inst_dict.update({semester:set_inst.copy()})
				set_name_inst.update({coursename:sem_inst_dict.copy()})
				mydict_lesson.update({coursecode:set_name_inst.copy()})
				mydict_deptname.update({deptname:mydict_lesson.copy()})
				doit=1

			if atstart==0:
				t2 = t1.find_all("td")
				itr = iter(t2)
				course = (next(itr).text)
				if len(course)>2: #eliminating the empty boxes
					coursecode=course.split('.')[0]
					current_course_code=coursecode[-3:]
					#checks the course code and updates graduate/undergraduate counts for each semester
					#course codes that begin with 5 or more are graduate courses
					#everything else is counted as an undergraduate course
					if not current_course_code.isdigit():
						if(prev_course_code != current_course_code):
							if current_course_code[0].isdigit():
								look2=int(current_course_code[0],10)
								if look2>=5:
									semester_graduate +=1
									doit=0
								else:
									semester_undergraduate +=1
									doit=0
							else:
								semester_undergraduate +=1
								doit=0
						doit=0
					if doit==1:
						initial_course_code=int(current_course_code[0],10)
					#the stop value will indicate whether the course have been added previously
					if coursecode in set_courses:
						stop=True
					set_courses.add(coursecode)
						
					#if prev_course_code and current_course_code are the same, that means we have different sections of the same course
					#thus, we'll keep our sets of instructors as they are
					#if prev_course_code and current_course_code are different, we empty the sets of instructors
					if(prev_course_code != current_course_code):
						set_inst.clear()
						set_name_inst.clear()
						sem_inst_dict.clear()
						if doit==1:
							if initial_course_code>=5:
								semester_graduate +=1
							else:
								semester_undergraduate +=1

					next(itr)

					coursename=(next(itr).text)
					
					#there exists courses with same coursecode but different names(changed throughout the semesters)
					#if that's the case, we keep the latest name of that course
					if stop:
						if not coursename in coursenames:
							coursename=coursenames.get(coursecode)
					else:
						coursenames.update({coursecode:coursename})

					if mydict_lesson.get(coursecode)==None :
						set_name_inst.clear()
						set_inst.clear()
						sem_inst_dict.clear()
					else:
					#prevents loosing the semester's info
						temp1 = mydict_lesson.get(coursecode)
						if(temp1!=None):
							temp2 = temp1.get(coursename)
							if(temp2!=None):
								for sem in temp2:
									sem_inst_dict.update({sem:temp2.get(sem)})
					
					next(itr)
					next(itr)

					#STAFF STAFF is not counted as a distinct instructor
					instructor=(next(itr).text)
					instructor=instructor[:-1]
					if(instructor != 'STAFF STAFF'):
						set_inst.add(instructor)

					#updating the data structures
					sem_inst_dict.update({semester:set_inst.copy()})
					set_name_inst.update({coursename:sem_inst_dict.copy()})
					mydict_lesson.update({coursecode:set_name_inst.copy()})
					mydict_deptname.update({deptname:mydict_lesson.copy()})
					doit=1

			atstart=0
			prev_course_code = current_course_code
			stop=False
		
		#keeping the graduate and undergraduate counts of the semester as a string
		tempstring='U' + str(semester_undergraduate) + ' G' + str(semester_graduate)
		dept_graduate=dept_graduate+semester_graduate
		dept_undergraduate=dept_undergraduate+semester_undergraduate
		#will work to access graduate and undergraduate numbers in semester basis
		deptcount.update({semester : tempstring})
	
	#loop through all semesters for a single department has ended
	#updating our data

	mydict_deptname.update({deptname:mydict_lesson.copy()})
	#this if statement handles the different departments that have the same deparment code
	#if such departments exist, we keep their data separately under the same department code with different department names
	if deptcode in mydict_dept:
		mydict_dept[deptcode].update({deptname:mydict_lesson.copy()})
	else:
		mydict_dept.update({deptcode:mydict_deptname.copy()})

	#keeping the graduate and undergraduate counts of the department as a string
	tempstring2 = 'U' + str(dept_undergraduate) + ' G' + str(dept_graduate)

	dept_undergraduate=0
	dept_graduate=0
	
	for course in set_courses:
		temp = course[-3:][0]
		if temp.isdigit():
			if int(course[-3:][0],10)>=5:
				dept_graduate +=1
			else:
				dept_undergraduate +=1
		else:
			dept_undergraduate +=1
	tempstring3 = 'U' + str(dept_undergraduate) + ' G' + str(dept_graduate)

	#updating data structures
	totaldicttemp.update({deptname:tempstring2})
	totaldict.update({deptcode:totaldicttemp.copy()})
	countlisttemp.update({deptname:deptcount.copy()})
	countlist.update({deptcode:countlisttemp.copy()})
	tttemp.update({deptname:tempstring3})
	tt.update({deptcode:tttemp.copy()})

	#getting ready for the next department loop
	mydict_lesson.clear()
	mydict_deptname.clear()

#forms the first line of the table and prints it
firstline='Dept./Prog.(name),Course Code,Course Name,'	
for index1 in range(start,finish+1):
	semester=sem1[index1]
	firstline=firstline+semester+','
firstline=firstline+'Total Offerings'
print(firstline)


stotal=set() #holds all instructors for one department
separator={} #this links the departments with semester and with just that semester'instructors
s=set()	#s will take the department's instructor info including all semesters
sa=set()#sa will take the department's just that semester'instructors
setsemester={}#via this dict separator does its task
y=""#line which is responsible from showing the existence of courses
res=''#all individual courses result lines
existcoursecount=0;#how many times the course exist info
tos={}#whole total of instructors
resarray=[]#the array which contains the result lines

#these will be used for writing out the results
all=''
b=''
d=''
#in order to keep the initial start value
allstart=start
#while writing the courses existence this helps to display spaces when the course doesn't occur in that semester
prevsemester=0


#traverses all depts according to their deptcode
for key1,value1 in sorted(mydict_dept.items()):
	#traverses all depts according to their name
	for key2, value2 in value1.items():
		#traverses a dept's courses according to their codes
		for key3, value3 in value2.items():
			#traverses a dept's courses according to their names
			for key4, value4 in value3.items():
				#traverses a dept's courses according to the semester and that semester's instructors
				for semester, instructor in value4.items():
					#this part is to put the x sign whether in that year the course exists
					if existcoursecount==0:
						for dizi in range(start,sem1.index(semester)):
							y=y+' ,'
						y=y+'x,'
					else:
						for dizi in range(prevsemester,sem1.index(semester)-1):
							y=y+' ,'
						y=y+'x,'	

					existcoursecount=existcoursecount+1
					#this for will work to determine the instructors via the sets and dictionaries which had been explain above in terms of tasks
					for inst in instructor:
						stotal.add(inst)
						tos.update({key2:stotal.copy()})
						s.add(inst)
						sa.add(inst)
						for m, n in setsemester.items():
							if m==semester:
								for j in n:
									sa.add(j)
					#prevents the information loss when all instructors are Staff
					if len(instructor)==0:
						#gets the previous courses in the same semester's instructor info 
						for m, n in setsemester.items():
							if m==semester:
								for j in n:
									sa.add(j)
					setsemester.update({semester:sa.copy()})
					separator.update({key2:setsemester.copy()})
					sa.clear()
					prevsemester=sem1.index(semester)
			#puts all of the courses result lines into the array
			for son in range(sem1.index(semester),finish):
				y=y+" ,"
			key4=key4[:-1]
			res="   ,"+key3+',"'+key4+'",'+y+str(existcoursecount)+" / "+str(len(s))			
			
			resarray.append(res)
			s.clear()
			existcoursecount=0  
			y=''
			start=allstart
			
		#puts all departments each semesters' results and adds them up as a string 
		for index in range(start,finish+1):	
			if separator.get(key2,{}).get(sem1[index])==None :
				all=all+"U0 G0 I0,"
			else:
				all=all+str(countlist.get(key1,{}).get(key2,{}).get(sem1[index]))+" I"+str(len(separator.get(key2,{}).get(sem1[index])))+","
		if(tos.get(key2) and totaldict.get(key1,{}).get(key2)):
			b=str(totaldict.get(key1,{}).get(key2))+" I"+str(len(tos.get(key2)))
			d=str(tt.get(key1,{}).get(key2))
			#prints the line which contains all the info of instructors,undergraduate courses and graduate courses 
			print(key1+"("+key2+"),"+d+", ,"+all+b)
			for finale in sorted(resarray):
				print(finale)
		stotal.clear()
		tos.clear()
		setsemester.clear()
		separator.clear()
		all=""
		resarray.clear()
		existcoursecount=0
