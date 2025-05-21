import requests # a library for making HTTP requests to APIs
import json # a libray for working with JSON data, which is common format for API responses
import os # a library for interacting with the operating system, used to check for file existence

# URL of the Frankfurter API, which provides exchanges rates
API_URL = "https://api.frankfurter.app/latest" 
# The name of the file where conversion history will be saved
HISTORY_FILE = "conversions.json" 

def fetch_exchange_rates(base): # defines a function that represents the currency from which to convert
    try: # begins a try block to handle exceptions that may occur during the API request
        # GET request to the Frankfurter API, appending the base currency to the URL as a query parameter
        response = requests.get(f"{API_URL}?from={base}") 
        # checks if the request was successful (status code 200). If not, it raises an HTTPError, which will be caught by the except block.
        response.raise_for_status() 
        # parses the JSON response from the API into a Python dictionary and stores it in the data variable.
        data = response.json()
        # returns the exchange rates from the parsed data. The rates key contains the currency conversion rates.
        return data['rates']
    # catches any exceptions that occur during the API request, such as connection errors or timeouts.
    except requests.RequestException as e:
        print(f"Error fetching exchange rates: {e}")
        return None

# This line defines a function named 'convert_currency' that takes three parameters: 'amount' (the amount to convert), 'base' (the currency to convert from), and 'target' (the currency to convert to).
def convert_currency(amount, base, target):
    # calls the fetch_exchange_rates function to get the exchange rates for the 'base' currency and stores the result in the 'rates' variable.
    rates = fetch_exchange_rates(base)
    # checks if the 'rates' variable is 'None'
    if rates is None:
        return None
    # checks if the 'target' currency is present in the 'rates' dictionary
    if target not in rates: 
        print(f"Target currency '{target}' not found in rates.")
        return None
    # calculates the converted amount by multiplying the 'amount' by the exchange rate for the 'target' currency.
    converted_amount = amount * rates[target]
    # return the converted value
    return converted_amount

# defines a function named 'save_conversion_history' that takes one parameter, 'record', which is a dictionary containing the conversion details.
def save_conversion_history(record):
    history = [] # initializes ann empty list to store conversion records
    # checks if the 'HISTORY_FILE' exists
    if os.path.exists(HISTORY_FILE):
        # opens 'HISTORY_FILE' in read mode if it exists
        with open(HISTORY_FILE, 'r') as file:
            try: # begins a try block to handle potential exceptions when loading the JSON data
                # loads the existing conversion history from the file into the 'history' list
                history = json.load(file)
                # catches any JSON decoding errors that may occur if the file is empty or contains invalid JSON
            except json.JSONDecodeError:
                # if there is aa JSON decoding error, initializes 'history' as an empty list
                history = []
    # appends the new conversion record to the 'history' list
    history.append(record)
    # open the 'HISTORY_FILE' in write mode to save the updated history
    with open(HISTORY_FILE, 'w') as file:
        # writes the updates 'history' list back to the file in JSON format, with an indentation of 4 spaces for readability
        json.dump(history, file, indent=4)

def main(): # the main function that will execute the main logic of the program which is Currency Converter using Frankfurter API
    print("Currency Converter using Frankfurter API")
    try: # begins a try block to handle a potential exceptions when getting user input
        amount = float(input("Enter amount: ")) # enter amount and converts it to a float
        base = input("From currency (e.g. USD): ").upper() # enter base currency and converts it to uppercase
        target = input("To currency (e.g. EUR): ").upper() # enter target currency and converts it to uppercase
    except ValueError: # catches any ValueError that occurs if the user input for the amount is invalid (e.g., not a number)
        print("Invalid input for amount.")
        return # exits the 'main' function if there was an error in user input

    # calls the 'convert_currency' function to perform the conversion and stores the result in the 'converted' variable
    converted = convert_currency(amount, base, target)
    # checks if the conversion was successful
    if converted is not None:
        print(f"{amount} {base} = {converted:.2f} {target}")

        # Save to history
        # creates a dictionary named 'record' that contains the conversion details (amount, base currency, target currency, and converted amount rounded to two decimal places)
        record = {
            "amount": amount,
            "base": base,
            "target": target,
            "converted": round(converted, 2)
        }
        # calls the 'save_conversion_history' function to save the conversion record to the history file
        save_conversion_history(record)
        print("Conversion saved to history.")

# checks if the script being run directly (not imported as a module). If true, it will execute the following code block
if __name__ == "__main__":
    # calls the 'main' function to start the program
    main()


