import urllib.request
import logging
from datetime import datetime
import argparse

# Part II - Download the Data
def downloadData(url):
    with urllib.request.urlopen(url) as response:
        return response.read().decode('utf-8')

# Part III - Process Data
def processData(file_content):
    data = {}
    lines = file_content.strip().split('\n')
    for i, line in enumerate(lines[1:], start=2):  # Start at 2 for proper line number
        try:
            person_id, name, birthday = line.split(',')
            birthday_date = datetime.strptime(birthday, '%d/%m/%Y')
            data[int(person_id)] = (name, birthday_date)
        except Exception as e:
            logging.getLogger('assignment2').error(f"Error processing line #{i} for ID #{person_id}")
    return data

# Part IV - Display / User Input
def displayPerson(person_id, personData):
    if person_id in personData:
        name, birthday = personData[person_id]
        print(f"Person #{person_id} is {name} with a birthday of {birthday.strftime('%Y-%m-%d')}")
    else:
        print("No user found with that id")

# Main Function
def main():
    parser = argparse.ArgumentParser()
    parser.add_argument('--url', help='URL to the CSV file')
    args = parser.parse_args()

    logging.basicConfig(filename='errors.log', level=logging.ERROR)

    if args.url:
        url = args.url
    else:
        url = input("Enter the URL to the CSV file: ")
    try:
        csv_data = downloadData(url)
    except Exception as e:
        print(f"Failed to download data: {e}")
        return

    person_data = processData(csv_data)

    while True:
        try:
            person_id = int(input("Enter an ID to lookup (negative number to exit): "))
            if person_id <= 0:
                break
            displayPerson(person_id, person_data)
        except ValueError:
            print("Invalid input, please enter a valid ID.")

if __name__ == '__main__':
    main()


