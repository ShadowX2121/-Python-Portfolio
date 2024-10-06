"""
Name: Aaron Adams
"""

# Import the python datetime module.
import datetime

# Import the python csv module.
import csv


class FileReader:

    """
    Initialize an object that will hold the file name of each input file with a constructor.
    """
    def __init__(self, file_name):
        self.file_name = file_name

    """
    Method that takes file name as input, asks data class for columns, then reads file and populates a dictionary that
    contains other dictionaries by creating an outer dictionary that uses the student ids as keys, and assigns an inner
    dictionary to them as the values. The inner dictionaries are created by referencing the list of column names, and the
    list of data types for those columns provided by the data class that called this method. The keys for each of the inner
    dictionaries become each of the column names from the list of column names, and their associated values are extracted 
    from the csv input file and stored as the data type (the method uses the list of data types provided by the data class 
    that called it to determine which data type to store the associated value for each column as) associated with each column name.
    Then, each of the inner dictionaries are assigned to each student id that serves as a key in the outer dictionary. The 
    method then returns the completed outer dictionary back to the data class that called it.
    """
    def data_extractor(self, column_names, column_types):
        file_contents = {}
        file = open(self.file_name)
        csv_file = csv.reader(file, delimiter=",")
        for line in csv_file:
            line_dictionary = {}
            for index, column in enumerate(line):
                if column_types[index] == "integer":
                    line_dictionary[column_names[index]] = int(column)
                elif column_types[index] == "string":
                    line_dictionary[column_names[index]] = column
                elif column_types[index] == "float":
                    line_dictionary[column_names[index]] = float(column)
                elif column_types[index] == "boolean":
                    if column == "Y":
                        column = "Y"
                    else:
                        column = ""
                    line_dictionary[column_names[index]] = column
                elif column_types[index] == "datetime":
                    line_dictionary[column_names[index]] = datetime.datetime.strptime(column, "%m/%d/%Y")
                else:
                    continue
            student_id = line_dictionary["student_id"]
            file_contents[student_id] = line_dictionary
        return file_contents


class StudentsMajorsList:

    """
    Initialize an empty list that will be filled with the data that the data_extractor() method in the FileReader class
    extracted from a csv input file, a list filled with the names of each column that will be used as keys in the inner
    dictionaries created with the data_extractor() method, and a list of the data types that the data in those columns will
    be with a constructor.
    """
    def __init__(self):
        self.majors_list = []
        self.column_names = ["student_id", "Last Name", "First Name", "Major", "Disciplined"]
        self.column_types = ["integer", "string", "string", "string", "boolean"]

    """
    Method that creates a instance of the FileReader class with the name of a csv input file and then, calls the data_extractor() 
    method in the FileReader class and provides the name list of column names, and the list of data types for those columns as 
    arguments. Then, it returns the filled list to the main part of the program that called it.
    """
    def load_data(self):
        file_reader = FileReader("StudentsMajorsList.csv")
        self.majors_list = file_reader.data_extractor(self.column_names, self.column_types)
        return self.majors_list


class GPAList:

    """
    Initialize an empty list that will be filled with the data that the data_extractor() method in the FileReader class
    extracted from a csv input file, a list filled with the names of each column that will be used as keys in the inner
    dictionaries created with the data_extractor() method, and a list of the data types that the data in those columns will
    be with a constructor.
    """
    def __init__(self):
        self.GPA_list = []
        self.column_names = ["student_id", "GPA"]
        self.column_types = ["integer", "float"]

    """
    Method that creates a instance of the FileReader class with the name of a csv input file and then, calls the data_extractor() 
    method in the FileReader class and provides the name list of column names, and the list of data types for those columns as 
    arguments. Then, it returns the filled list to the main part of the program that called it.
    """
    def load_data(self):
        file_reader = FileReader("GPAList.csv")
        self.GPA_list = file_reader.data_extractor(self.column_names, self.column_types)
        return self.GPA_list


class GraduationDatesList:

    """
    Initialize an empty list that will be filled with the data that the data_extractor() method in the FileReader class
    extracted from a csv input file, a list filled with the names of each column that will be used as keys in the inner
    dictionaries created with the data_extractor() method, and a list of the data types that the data in those columns will
    be with a constructor.
    """
    def __init__(self):
        self.graduation_dates_list = []
        self.column_names = ["student_id", "Graduation Date"]
        self.column_types = ["integer", "datetime"]

    """
    Method that creates a instance of the FileReader class with the name of a csv input file and then, calls the data_extractor() 
    method in the FileReader class and provides the name list of column names, and the list of data types for those columns as 
    arguments. Then, it returns the filled list to the main part of the program that called it.
    """
    def load_data(self):
        file_reader = FileReader("GraduationDatesList.csv")
        self.graduation_dates_list = file_reader.data_extractor(self.column_names, self.column_types)
        return self.graduation_dates_list


def main():

    """
    Create an instance of the GraduationDatesList class and fill it with the data from the GraduationDatesList csv input
    file, and then store it in a variable.
    """
    graduation_dates = GraduationDatesList()
    filled_graduation_dates = graduation_dates.load_data()

    """
    Create an instance of the GPAList class and fill it with the data from the GPAList csv input
    file, and then store it in a variable.
    """
    gpa_dict = GPAList()
    filled_gpa_dict = gpa_dict.load_data()

    """
    Create an instance of the StudentsMajorsList class and fill it with the data from the StudentsMajorsList csv input
    file, and then store it in a variable.
    """
    student_majors_dict = StudentsMajorsList()
    filled_student_majors_dict = student_majors_dict.load_data()

    """
    Create the FullRoster csv output file by, creating a dictionary that uses the last names of the different students 
    as keys, and assigning the associated student id of each of those last names as the value. Then, the keys of new dictionary
    are sorted in alphabetical order. The FullRoster csv file is then created and filled with rows that are in the order of
    the student id, major, first name, last name, GPA, graduation date, and a disciplinary action indicator (if the student was disciplined).
    """
    last_name_dictionary = {}
    for student_id, student_dict in filled_student_majors_dict.items():
        student_last_name = student_dict["Last Name"]
        last_name_dictionary[student_last_name] = student_id
    sorted_last_name_list = sorted(last_name_dictionary.items())
    with open("FullRoster.csv", "w", newline="") as roster_file:
        writer = csv.writer(roster_file)
        for student_last_name, student_id in sorted_last_name_list:
            writer.writerow([student_id, filled_student_majors_dict[student_id]["Major"],
                             filled_student_majors_dict[student_id]["First Name"], student_last_name,
                             filled_gpa_dict[student_id]["GPA"],
                             filled_graduation_dates[student_id]["Graduation Date"].strftime("%m/%d/%Y"),
                             filled_student_majors_dict[student_id]["Disciplined"]])

    """
    Create the ScholarshipCandidates csv output file by, creating an instance of the datetime.datetime.today() method in 
    the datetime python module that stores the current date, and then creating a dictionary that uses the GPA's of the different students 
    as keys, and assigning the associated student id of each of those GPA's as the value. Then, the keys of new dictionary are sorted 
    from highest to lowest. The ScholarshipCandidates csv file is then created and filled with rows that are in the order 
    of the student id, last name, first name, major, and GPA of students that have a GPA higher than 3.8, have a graduation 
    date that is after the current date stored from creating an instance of datetime.datetime.today(), and do not have a 
    disciplinary action indicator.
    """
    current_date = datetime.datetime.today()
    gpa_dictionary = {}
    for student_id, student_dict in filled_gpa_dict.items():
        student_gpa = student_dict["GPA"]
        gpa_dictionary[student_gpa] = student_id
    sorted_gpa_list = sorted(gpa_dictionary.items(), reverse=True)
    with open("ScholarshipCandidates.csv", "w", newline="") as scholarship_file:
        scholarship_writer = csv.writer(scholarship_file)
        for student_gpa, student_id in sorted_gpa_list:
            if filled_student_majors_dict[student_id]["Disciplined"] != "Y" and student_gpa > 3.8:
                if filled_graduation_dates[student_id]["Graduation Date"] > current_date:
                    scholarship_writer.writerow([student_id, filled_student_majors_dict[student_id]["Last Name"],
                                                 filled_student_majors_dict[student_id]["First Name"],
                                                 filled_student_majors_dict[student_id]["Major"], student_gpa])

    """
    Create the DisciplinedStudents csv output file by creating a dictionary that uses the graduation dates of the different students 
    as keys, and assigning the associated student id of each of those graduation dates as the value (if there are multiple 
    students that share the same graduation date then, each separate student id is appended to the newly created graduation
    dates dictionary). Then, the keys of new dictionary are sorted from the oldest graduation date to the most recent graduation
    date. The DisciplinedStudents csv file is then created and filled with rows that are sorted by graduation date and are 
    in the order of the student id, last name, first name, and graduation date of students that have a disciplinary action indicator.
    """
    graduation_dates_dictionary = {}
    for student_id, student_dict in filled_graduation_dates.items():
        student_graduation_date = student_dict["Graduation Date"]
        if filled_student_majors_dict[student_id]["Disciplined"] == "Y":
            if student_graduation_date in graduation_dates_dictionary:
                graduation_dates_dictionary[student_graduation_date].append(student_id)
            else:
                graduation_dates_dictionary[student_graduation_date] = [student_id]
    sorted_graduation_dates_list = sorted(graduation_dates_dictionary.items())
    with open("DisciplinedStudents.csv", "w", newline="") as discipline_file:
        discipline_writer = csv.writer(discipline_file)
        for student_graduation_date, student_id_list in sorted_graduation_dates_list:
            for student_id in student_id_list:
                discipline_writer.writerow([student_id, filled_student_majors_dict[student_id]["Last Name"],
                                            filled_student_majors_dict[student_id]["First Name"],
                                            student_graduation_date.strftime("%m/%d/%Y")])

    """
    Create a csv output file for each major by sorting the student ids that are stored in the filled_student_majors_dict
    variable from lowest to highest. Each csv file for each major is then created and filled with rows of students with a 
    particular major that are sorted by student id and are in the order of student id, last name, first name, graduation date, 
    and a disciplinary action indicator (if the student was disciplined).
    """
    sorted_majors_list = sorted(filled_student_majors_dict.items())
    majors_list = []
    for student_id, student_dict in filled_student_majors_dict.items():
        if not student_dict["Major"] in majors_list:
            majors_list.append(student_dict["Major"])
    for major in majors_list:
        file_major = major.replace(" ", "")
        with open(f"{file_major}Students.csv", "w", newline="") as majors_file:
            majors_writer = csv.writer(majors_file)
            for student_id in sorted_majors_list:
                student_id = student_id[0]
                if major == filled_student_majors_dict[student_id]["Major"]:
                    majors_writer.writerow([student_id, filled_student_majors_dict[student_id]["Last Name"],
                                            filled_student_majors_dict[student_id]["First Name"],
                                            filled_graduation_dates[student_id]["Graduation Date"].strftime("%m/%d/%Y"),
                                            filled_student_majors_dict[student_id]["Disciplined"]])


# Call the main() function.
main()