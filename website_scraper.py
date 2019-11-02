"""
Code Written By Srijith Shashidhar
-The starting and ending usn can be specfied in the below mentioned variables along with year and department
-Uses beautifulsoup python library to parse the HTML code
-The file name can be modified according to the user wish

"""
# The url of the result page of the RVCE
URL = "http://results.rvce.edu.in/viewresult2.php"
# Output file name (in CSV format)
FILENAME = "results.csv"
# Starting USN from where the result to be fetched
USN_START = 0
# Ending USN to fetch the results
USN_END = 21
# Year of joining (16 for 2016, 17 for 2017,18 for 2018 etc.)
YEAR_OF_JOINING = "17"
# Department id (2 letter code: AS, CS, CV, IS, ME etc.)
DEPARTMENT = "CS"
# Print result to console (True or False)
PRINT_TO_CONSOLE = True



import requests
# For parsing the html
from bs4 import BeautifulSoup
# For exporting/saving to a CSV file
import csv

###############################################################################
# this is to get the values of numbers mentioned in "what is 6+5" in result webpage
def getCaptcha(session):
    result = session.post(URL)
    soup = BeautifulSoup(result.content, "lxml")
    samples = soup.find_all("label")
    captcha = str(samples[1].string)
    num1 = captcha[8]
    num2 = captcha[12]
    ans = int(num1) + int(num2)
    return ans

###############################################################################

def getResult(session):

    rows = []
    ans = getCaptcha(session)

    for i in range(USN_START, USN_END + 1):

        params = {
            "usn": "1RV" + YEAR_OF_JOINING + DEPARTMENT + '{:03}'.format(i),
            "captcha": ans
        }
        result = session.post(URL, params)
        # we are sending the format of "1RV17CS202" and along with the calculated sum
        soup = BeautifulSoup(result.content, "lxml")
        checkVal = soup.find(attrs={"data-title" : "PROGRAMME"})

        # Skip if no result is found
        if checkVal:
            # Extract the required fields
            name = soup.find(attrs={"data-title" : "NAME"}).string
            usn = soup.find(attrs={"data-title" : "USN"}).string
            grades = soup.find_all(attrs={"data-title" : "GRADE"})
            sgpa = soup.find(attrs={"data-title" : "SGPA"}).string

            # Create a row with the details and results of 1 person
            row = []
            row.append(name)
            row.append(usn)
            for grade in grades:
                row.append(grade.string)
            row.append(sgpa)

            # Append to the list containing details of each student
            rows.append(row)
            if (PRINT_TO_CONSOLE):
                print(row)

    return rows

###############################################################################

def writeResult(rows):
    with open(FILENAME, 'w', newline='') as csvfile:
        wr = csv.writer(csvfile)
        wr.writerows(rows)

###############################################################################

# Create a new session
session = requests.session()
# Time for action
writeResult(getResult(session))
