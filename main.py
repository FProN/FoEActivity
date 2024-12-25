import sys
import csv
import re
import glob
import os
from collections import Counter
import pandas as pd

listOfMembers = []
def main():
    get_members()
    try:
        create_activity_list()
    except FileExistsError:
        pass
    count_words_in_file(listOfMembers, "ListaOsobNaWyscigu.txt", "ActivityList.csv")
    sort_list("ActivityList.csv")
    rename_file("ActivityList.csv", "ActivityList.txt")
    


def create_activity_list():
    n=0
    with open("ActivityList.csv", "x", newline="") as file:
        writer = csv.DictWriter(file, fieldnames=["Player", "Activity"])
        writer.writeheader()
        for i in listOfMembers:
            writer.writerow({"Player":listOfMembers[n], "Activity":"0"})
            n+=1

def get_members():
    filename = glob.glob("Member_*")
    with open(filename[0], newline="") as csvfile:
        rdr = csv.DictReader(csvfile, delimiter=";")
        for row in rdr:
            # Normalize each member name: remove unwanted symbols, lowercase, and strip spaces
            member = re.sub(r'[^\dA-Za-z ]', '', row["member"]).strip().lower()
            listOfMembers.append(member)

def count_words_in_file(word_list, input_file, output_file):
    # Read the content of the .txt file
    with open(input_file, 'r', encoding='utf-8') as file:
        text = file.read().lower()  # Convert to lowercase for case-insensitive matching

    # Normalize whitespace (replace tabs, multiple spaces with a single space)
    text = re.sub(r'\s+', ' ', text)
    text = re.sub(r'[^\dA-Za-z ]', '', text)

    # Prepare the result for the given word list
    results = []
    for phrase in word_list:
        # Handle exact matches, preserving symbols as-is
        escaped_phrase = re.escape(phrase)
        count = len(re.findall(rf'\b{escaped_phrase}\b', text))  # Count exact matches only
        results.append((phrase, count))

    # Write the results to a .csv file
    with open(output_file, 'w', newline='', encoding='utf-8') as csv_file:
        writer = csv.writer(csv_file)
        writer.writerow(['Player', 'Activity'])  # Header row
        writer.writerows(results)

def sort_list(nameOfFile):
    reader = csv.DictReader(open(nameOfFile, 'r'))
    result = sorted(reader, key=lambda d: float(d["Activity"]))
    writer = csv.DictWriter(open("ActivityList.csv", "w", newline=""), reader.fieldnames)
    writer.writeheader()
    writer.writerows(result)

def rename_file(nameOfFile, nameOfNewFile):
    try:
        os.rename(nameOfFile, nameOfNewFile)
    except FileExistsError:
        os.remove(nameOfNewFile)
        os.rename(nameOfFile, nameOfNewFile)

if __name__ == "__main__":
    main()
