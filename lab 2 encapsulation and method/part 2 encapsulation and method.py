class Student:
	def __init__(self,student_id, student_name):
		self.__student_id = student_id
		self.__student_name = student_name

	def get_student_id(self):
		return self.__student_id

	def get_student_name(self):
		return self.__student_name

class Subject:
	def __init__(self,subject_id, subject_name, credit):
		self.__subject_id = subject_id
		self.__subject_name = subject_name
		self.__credit = credit
		self.__teacher = None

	def get_subject_id(self):
		return self.__subject_id

	def get_subject_name(self):
		return self.__subject_name

	def get_credit(self):
		return self.__credit

	def get_teacher(self):
		return self.__teacher

	def assign_teacher(self, teacher):
		if isinstance(teacher, Teacher):
			self.__teacher = teacher

class Teacher:
	def __init__(self,teacher_id, teacher_name):
		self.__teacher_id = teacher_id
		self.__teacher_name = teacher_name

	def get_teacher_id(self):
		return self.__teacher_id

	def get_teacher_name(self):
		return self.__teacher_name

class Enrollment:
	def __init__(self, student, subject):
		self.__student = student
		self.__subject = subject
		self.__grade = None

	def get_student(self):
		return self.__student

	def get_subject(self):
		return self.__subject

	def get_grade(self):
		return self.__grade

	def assign_student_grade(self, grade):
		if self.__grade is None:
			self.__grade = grade
		else:
			return "Error"

student_list = []
subject_list = []
teacher_list = []
enrollment_list = []

# TODO 1 : function สำหรับค้นหา instance ของวิชาใน subject_list
def search_subject_by_id(subject_id):
	for subject in subject_list:
		if subject_id == subject.get_subject_id():
			return subject
	return None

# TODO 2 : function สำหรับค้นหา instance ของนักศึกษาใน student_list
def search_student_by_id(student_id):
	for student in student_list:
		if student_id == student.get_student_id():
			return student
	return None

# TODO 3 : function สำหรับสร้างการลงทะเบียน โดยรับ instance ของ student และ subject
def enroll_to_subject(student, subject):
	if isinstance(student, Student) and isinstance(subject, Subject):
		for enrollment in enrollment_list:
			if enrollment.get_student().get_student_id() == student.get_student_id() and enrollment.get_subject().get_subject_id == subject.get_subject_id:
				return "Already Enrolled"

		new_enrollment = Enrollment(student, subject)
		enrollment_list.append(new_enrollment)
		return "Done"
	else:
		return "Error"
# TODO 4 : function สำหรับลบการลงทะเบียน โดยรับ instance ของ student และ subject_s
def drop_from_subject(student, subject):
	if isinstance(student, Student) and isinstance(subject, Subject):
		for enrollment in enrollment_list:
			if enrollment.get_student().get_student_id() == student.get_student_id() and enrollment.get_subject().get_subject_id == subject.get_subject_id:
				enrollment_list.remove(enrollment)
				return "Done"
		return "Not Found"
	else:
		return "Error"

# TODO 5 : function สำหรับค้นหาการลงทะเบียน โดยรับ instance ของ student และ subject
def search_enrollment_subject_student(subject, student):
	if isinstance(student, Student) and isinstance(subject, Subject):
		for enrollment in enrollment_list:
			if enrollment.get_student().get_student_id() == student.get_student_id() and enrollment.get_subject().get_subject_id == subject.get_subject_id:
				return enrollment

# TODO 6 : function สำหรับค้นหาการลงทะเบียนในรายวิชา โดยรับ instance ของ subject
def search_student_enroll_in_subject(subject):
	filter_student_list = []
	if isinstance(subject, Subject):
		for enrollment in enrollment_list:
			if enrollment.get_subject().get_subject_id() == subject.get_subject_id():
				filter_student_list.append(enrollment)
		return filter_student_list
	else:
		return "Error"

# TODO 7 : function สำหรับค้นหาการลงทะเบียนของนักศึกษาว่ามีวิชาอะไรบ้าง โดยรับ instance ของ student
def search_subject_that_student_enrolled(student):
	filter_subject_list = []
	if isinstance(student, Student):
		for enrollment in enrollment_list:
			if enrollment.get_student().get_student_id() == student.get_student_id():
				filter_subject_list.append(enrollment)
		if filter_subject_list == None:
			return "Not Found"
		else:
			return filter_subject_list

# TODO 8 : function สำหรับใส่เกรดลงในการลงทะเบียน โดยรับ instance ของ student และ subject
def assign_grade(student, subject, grade):
	enrollment = search_enrollment_subject_student(subject, student)
	if enrollment is None:
		return "Not Found"
	enrollment.assign_student_grade(grade)
	return "Done"

# TODO 9 : function สำหรับคืน instance ของอาจารย์ที่สอนในวิชา
def get_teacher_teach(subject_search):
    return subject_search.get_teacher()

# TODO 10 : function สำหรับค้นหาจำนวนของนักศึกษาที่ลงทะเบียนในรายวิชา โดยรับ instance ของ subject
def get_no_of_student_enrolled(subject):
	count = 0
	for enrollment in enrollment_list:
		if enrollment.get_subject() == subject:
			count+=1
	return count

# TODO 11 : function สำหรับค้นหาข้อมูลการลงทะเบียนและผลการเรียนโดยรับ instance ของ student
# TODO : และ คืนค่าเป็น dictionary { ‘subject_id’ : [‘subject_name’, ‘grade’ }
def get_student_record(student):
	student_record = {}
	for enrollment in enrollment_list:
		if enrollment.get_student() == student:
			student_record[enrollment.get_subject().get_subject_id()] = [enrollment.get_subject().get_subject_name(), enrollment.get_grade()]
	return student_record

# แปลงจาก เกรด เป็นตัวเลข
def grade_to_count(grade):
	grade_mapping = {'A': 4, 'B': 3, 'C': 2, 'D': 1}
	return grade_mapping.get(grade, 0)

# TODO 12 : function สำหรับคำนวณเกรดเฉลี่ยของนักศึกษา โดยรับ instance ของ student
def get_student_GPS(student):
	total_credits = 0
	total_grade = 0
	for enrollment in enrollment_list:
		if enrollment.get_student() == student and enrollment.get_grade():
			credit = enrollment.get_subject().get_credit()
			total_credits += credit
			total_grade += credit * grade_to_count(enrollment.get_grade())
	return round(total_grade / total_credits, 2) if total_credits > 0 else 0.0

# ค้นหานักศึกษาลงทะเบียน โดยรับเป็น รหัสวิชา และคืนค่าเป็น dictionary {รหัส นศ. : ชื่อ นศ.}
def list_student_enrolled_in_subject(subject_id):
	subject = search_subject_by_id(subject_id)
	if subject is None:
		return "Subject not found"
	filter_student_list = search_student_enroll_in_subject(subject)
	student_dict = {}
	for enrollment in filter_student_list:
		student_dict[enrollment.get_student().get_student_id()] = enrollment.get_student().get_student_name()
	return student_dict

# ค้นหาวิชาที่นักศึกษาลงทะเบียน โดยรับเป็น รหัสนักศึกษา และคืนค่าเป็น dictionary {รหัสวิชา : ชื่อวิชา }
def list_subject_enrolled_by_student(student_id):
	student = search_student_by_id(student_id)
	if student is None:
		return "Student not found"
	filter_subject_list = search_subject_that_student_enrolled(student)
	subject_dict = {}
	for enrollment in filter_subject_list:
		subject_dict[enrollment.subject.subject_id] = enrollment.subject.subject_name
	return subject_dict

#######################################################################################

#สร้าง instance พื้นฐาน
def create_instance():
	student_list.append(Student('66010001', "Keanu Welsh"))
	student_list.append(Student('66010002', "Khadijah Burton"))
	student_list.append(Student('66010003', "Jean Caldwell"))
	student_list.append(Student('66010004', "Jayden Mccall"))
	student_list.append(Student('66010005', "Owain Johnston"))
	student_list.append(Student('66010006', "Isra Cabrera"))
	student_list.append(Student('66010007', "Frances Haynes"))
	student_list.append(Student('66010008', "Steven Moore"))
	student_list.append(Student('66010009', "Zoe Juarez"))
	student_list.append(Student('66010010', "Sebastien Golden"))

	subject_list.append(Subject('CS101', "Computer Programming 1", 3))
	subject_list.append(Subject('CS102', "Computer Programming 2", 3))
	subject_list.append(Subject('CS103', "Data Structure", 3))

	teacher_list.append(Teacher('T001', "Mr. Welsh"))
	teacher_list.append(Teacher('T002', "Mr. Burton"))
	teacher_list.append(Teacher('T003', "Mr. Smith"))

	subject_list[0].assign_teacher(teacher_list[0])
	subject_list[1].assign_teacher(teacher_list[1])
	subject_list[2].assign_teacher(teacher_list[2])

# ลงทะเบียน
def register():
	enroll_to_subject(student_list[0], subject_list[0])  # 001 -> CS101
	enroll_to_subject(student_list[0], subject_list[1])  # 001 -> CS102
	enroll_to_subject(student_list[0], subject_list[2])  # 001 -> CS103
	enroll_to_subject(student_list[1], subject_list[0])  # 002 -> CS101
	enroll_to_subject(student_list[1], subject_list[1])  # 002 -> CS102
	enroll_to_subject(student_list[1], subject_list[2])  # 002 -> CS103
	enroll_to_subject(student_list[2], subject_list[0])  # 003 -> CS101
	enroll_to_subject(student_list[2], subject_list[1])  # 003 -> CS102
	enroll_to_subject(student_list[2], subject_list[2])  # 003 -> CS103
	enroll_to_subject(student_list[3], subject_list[0])  # 004 -> CS101
	enroll_to_subject(student_list[3], subject_list[1])  # 004 -> CS102
	enroll_to_subject(student_list[4], subject_list[0])  # 005 -> CS101
	enroll_to_subject(student_list[4], subject_list[2])  # 005 -> CS103
	enroll_to_subject(student_list[5], subject_list[1])  # 006 -> CS102
	enroll_to_subject(student_list[5], subject_list[2])  # 006 -> CS103
	enroll_to_subject(student_list[6], subject_list[0])  # 007 -> CS101
	enroll_to_subject(student_list[7], subject_list[1])  # 008 -> CS102
	enroll_to_subject(student_list[8], subject_list[2])  # 009 -> CS103

create_instance()
register()

# ### Test Case #1 : test enroll_to_subject complete ###
student_enroll = list_student_enrolled_in_subject('CS101')
print("Test Case #1 : test enroll_to_subject complete")
print("Answer : {'66010001': 'Keanu Welsh', '66010002': 'Khadijah Burton', '66010003': 'Jean Caldwell', '66010004': 'Jayden Mccall', '66010005': 'Owain Johnston', '66010007': 'Frances Haynes'}")
print(student_enroll)
print("")

# ### Test case #2 : test enroll_to_subject in case of invalid argument
print("Test case #2 : test enroll_to_subject in case of invalid argument")
print("Answer : Error")
print(enroll_to_subject('66010001','CS101'))
print("")

# ### Test case #3 : test enroll_to_subject in case of duplicate enrolled
print("Test case #3 : test enroll_to_subject in case of duplicate enrolled")
print("Answer : Already Enrolled")
print(enroll_to_subject(student_list[0], subject_list[0]))
print("")

# ### Test case #4 : test drop_from_subject in case of invalid argument 
print("Test case #4 : test drop_from_subject in case of invalid argument")
print("Answer : Error")
print(drop_from_subject('66010001', 'CS101'))
print("")

# ### Test case #5 : test drop_from_subject in case of not found 
print("Test case #5 : test drop_from_subject in case of not found")
print("Answer : Not Found")
print(drop_from_subject(student_list[8], subject_list[0]))
print("")

# ### Test case #6 : test drop_from_subject in case of drop successful
print("Test case #6 : test drop_from_subject in case of drop successful")
print("Answer : {'66010002': 'Khadijah Burton', '66010003': 'Jean Caldwell', '66010004': 'Jayden Mccall', '66010005': 'Owain Johnston', '66010007': 'Frances Haynes'}")
drop_from_subject(student_list[0], subject_list[0])
print(list_student_enrolled_in_subject(subject_list[0].get_subject_id()))
print("")

# ### Test case #7 : test search_student_enrolled_in_subject
print("Test case #7 : test search_student_enrolled_in_subject")
print("Answer : ['66010002','66010003','66010004','66010005','66010007']")
lst = search_student_enroll_in_subject(subject_list[0])  # Students enrolled in CS101
print([enrollment.get_student().get_student_id() for enrollment in lst])  # Extract student IDs
print("")

# ### Test case #8 : get_no_of_student_enrolled
print("Test case #8 : get_no_of_student_enrolled")
print("Answer : 5")
print(get_no_of_student_enrolled(subject_list[0]))  # Count of students in CS101
print("")

# ### Test case #9 : search_subject_that_student_enrolled
print("Test case #9 : search_subject_that_student_enrolled")
print("Answer : ['CS102','CS103']")
lst = search_subject_that_student_enrolled(student_list[0])  # Subjects for student 66010001
print([enrollment.get_subject().get_subject_id() for enrollment in lst])  # Extract subject IDs
print("")

# ### Test case #10 : get_teacher_teach
print("Test case #10 : get_teacher_teach")
print("Answer : Mr. Welsh")
teacher = get_teacher_teach(subject_list[0])  # Teacher for CS101
print(teacher.get_teacher_name())  # Teacher's name
print("")

# ### Test case #11 : search_enrollment_subject_student
print("Test case #11 : search_enrollment_subject_student")
print("Answer : CS101 66010002")
enroll = search_enrollment_subject_student(subject_list[0], student_list[1])  # Enrollment for CS101, student 66010002
print(enroll.get_subject().get_subject_id(), enroll.get_student().get_student_id())  # Subject and student IDs
print("")

# ### Test case #12 : assign_grade
print("Test case #12 : assign_grade")
print("Answer : Done")
assign_grade(student_list[1], subject_list[0], 'A')  # Grade A for CS101
assign_grade(student_list[1], subject_list[1], 'B')  # Grade B for CS102
print(assign_grade(student_list[1], subject_list[2], 'C'))  # Grade C for CS103
print("")

# ### Test case #13 : get_student_record
print("Test case #13 : get_student_record")
print("Answer : {'CS101': ['Computer Programming 1', 'A'], 'CS102': ['Computer Programming 2', 'B'], 'CS103': ['Data Structure', 'C']}")
print(get_student_record(student_list[1]))  # Record of student 66010002
print("")

# ### Test case #14 : get_student_GPS
print("Test case #14 : get_student_GPS")
print("Answer : 3.0")
print(get_student_GPS(student_list[1]))  # GPA of student 66010002
print("")