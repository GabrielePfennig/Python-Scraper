
"""
WFI Ingolstadt School of Management
Webscraping & Textual Analysis in Python
Winter 2023/24
David Streich

01_Python_basics.py

-----------------------------------------------
1. Printing and lists
2. If/else statements
3. Loops
4. Exception handling
5. Saving to files
-----------------------------------------------

"""
##############################################################################
### 1. Printing and lists
##############################################################################
# Use the print command to display the contents of variables and lists
print("Hello World!!!")

test_str = "This is a test"
test_int = 4-3
test_list = [1, 2, 3, 4, 5]

print(test_str)
print(test_int)
print(test_list)
print(test_list[0]) # -> Python starts indexing at 0 (pick first element of the list to show with 0)


##############################################################################
### 2. If/else & statements
##############################################################################
numbers = [0, 1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11, 12, 13]
for number in numbers:
    if number % 2 == 0:
        print(str(number)+" is an even number.")
    else:
        print(str(number)+" is an odd number.")


# You can also specify more than 1 if condition:
for number in numbers:
    if number >= 10:
        print(str(number)+" is at least 10.")
    elif number >= 5: 
        print(str(number)+" is at least 5, but less than 10.")
    else:
        print(str(number)+" is less than 5.")


##############################################################################
### 3. Loops
##############################################################################
### 3.1 For loops
##############################################################################
# Use the for [...] in command to loop through list elements
# When looping through subpages, it may be useful to pause after each iteration ...
# ... to allow the website to load. Use the time.sleep function.
import time

words = ["The", "cat", "sat", "on", "the", "carpet"]
for word in words:
    print(word)
    time.sleep(2)     #pause for two seconds after every loop time.sleep defined in seconds
    #Tipp: Use number generator easier to scrape websites since it is less predictable

##############################################################################
### 3.2 While loops
##############################################################################
# The while command allows you to repeat a command until a condition is met.
# You may want to attempt reaching a subpage multiple times before moving on ...
# ... to the next one.
count = 1
while count <= 10:
    print(count)
    count += 1    
print("Done!")

##############################################################################
### 4. Exception handling
##############################################################################
# Errors cause Python to stop running. You can stop this by including exception ...
# ... handling in your code. 

# Python exits the following loop at the third list element.
numbers = [1, 2, 0, 3, 4, 5]
results = []
for number in numbers:
    result = 10 / number
    results.append(result)
    print(result)

# Exception handling allows you to skip the third element and move on to the fourth
results = []
for number in numbers:
    try:
        result = 10 / number
        print(result)
        results.append(result)
    except: # when no error type is specified, all errors are handled
        print("Computation not possible.")
print(result)
#try to do this if you find error keep doing. (try except: keep running even if it catches an error)
#we did not specify error here

# You can also restrict exception handling to specific error types:
results = []
for number in numbers:
    try:
        result = 10 / number
        print(result)
        results.append(result)
    except ZeroDivisionError: #specify error
        print("Computation not possible.")
print(result)

##############################################################################
### 5. Saving to file
##############################################################################
### 5.1 Saving lists to csv
##############################################################################
import csv
words = ["The", "cat", "sat", "on", "the", "carpet"]

with open('/Users/gabriele/Desktop/Master KU/Webscraping & Textual Analysis/Python code snippets/words.csv', 'w', newline = "") as f:    
    write = csv.writer(f)
    for word in words:
        write.writerow([word])

##############################################################################
### 5.2 Saving pandas dataframe to csv
##############################################################################
import pandas as pd
dftable = pd.DataFrame()
dftable["Words"] = words
dftable["Numbers"] = [1, 2, 3, 4, 5, 6]
dftable.to_csv('./dftable.csv', index = False)

##############################################################################