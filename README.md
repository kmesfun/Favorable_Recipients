Files:
-----------
challenge.py: main file
test.py: test file
Clean_Favorable_Recipients.csv: csv file with no duplicates information from Favorable_Recipients.csv
Favorable_Recipients.csv: The Information of Recipients and Pickup

How to run:
-----------
for main file: python3 challenge.py
for test file: python3 test.py



~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

Initial Thoughts: Find all the people who fit the description as possible recipients. These people are that are the closest by distance are favorable recipients. Another interpretation of favorable can be the earliest possible pickup time.

Plans: Store the excel data into a dictionary to access information easier. Have a method to convert the numbers to bits then finding the "1" in the bitstring to see what category it belongs to. Simplify the main function with methods including a csv maker method and a sort csv method. Create a boolean function to check if the distance is within 5 miles and create functions to find the 1 hour difference of availability.

Approach: Write methods to simplify the information to make it easier to get information and to check the names of all favorable recipients. Since all timezones are America/Los_Angeles the +/- time shouldn't matter, so that part will be ignored. Store information in an array and convert the array to a csv file then sort it.

Unit test results: Using several libraries I checked if the results would work for edge cases and if they accurate measured the distances. Another test was to check if the categories with restriction if accurate and return a list of food categories. These test were to verify that everything works.

Overall results: All information needed is stored in a csv file with the recipient information and the pickup information in the appropriate columns and rows.

Results analysis: The csv file is sorted from least to most for distance since I have decided that distance if what determines a favorable recipient.

Conclusion: Everything worked without any fails on the unit tests or for the main function. The abstraction was correct and so was the implementation of the algorithm. The csv file has headers to make reading the file easier and more organized.



