#Abijah Buttendorf, 
# A file to travers a directory recursivley, and searches the logs it contains for entries based on a specifies option
import os, argparse, re, sys
import yaml

try:
    with open('searchTerms.yaml', 'r') as yf:
        keywords = yaml.safe_load(yf)
except EnvironmentError as e:
    print(e.strerror)

#parser
parser = argparse.ArgumentParser(

    description="Traverses directories and builds a forensic body file",
    epilog="Developed by Abijah 9/21/22"
)


# Add an arguments to the fs.py program
parser.add_argument("-d", "--directory", required="True", help="Directory that you want to traverse.")
parser.add_argument("-s", "--search", required="True", help="Specify Search Terms: 'SHELL', 'SQL', 'TRV', 'CMS'")

# parse the arguments
args = parser.parse_args()
rootDir = args.directory
searchTerms = keywords[args.search]

# Getting information from CMD
# Checking if passed argument is directory
if not os.path.isdir(rootDir):
    print("Invalid Directory => {} ".format(rootDir))
    exit()

# Define flist for outputs
flist = []

# Crawling the specified Directory
for root, subfolders, filenames in os.walk(rootDir):
    for f in filenames:
        #print(root + "\\" + f)
        fileList = root + "\\" + f
        #print(fileList)
        flist.append(fileList)

def _syslog(filename,service):

    #Query the Ymal for the terms specified inside
    #Service is main, term is sub
    terms = service

    #Split the etries by the commas
    listOfKeywords = terms.split(", ")

    # Open a file 
    with open(filename) as f:
        #read in the file and save the output into a variable
        contents = f.readlines()

    # List of Results
    results = []

    # loop through the list and return the entries in each line
    for line in contents:

        # Loops through keywords
        for eachKeyword in listOfKeywords:

            #if the line contains the keyword it is printed out
            #if eachKeyword in line:
            x = re.findall(r''+eachKeyword+'', line)

            for found in x:
                #Appending returned values to the results list
                results.append(found)

    #Check to see if results are present

    #Sort the results
    results = sorted(results)
    cleanResults = []

    #Print the results to the cli
    for line in results:
        print(line)
    
    return cleanResults
#call for _syslog
for f in flist:
    _syslog(f, searchTerms)