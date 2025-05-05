import modules

def later_date(input_date, days):
    # Convert input_date string to a datetime object
    input_date = modules.datetime.strptime(input_date, "%B %d")
    # Add the specified number of days to the input_date
    later_date = input_date + modules.timedelta(days=days)
    # Return the later date as a string
    return later_date.strftime("%B %d")

# Outputs the information stored in the database
def view():
    headers = ["Female", "Breed Date", "Buck", "Palpate", "Nest Box", 
    "Kindling Date", "Comments"]

    # Define a fixed width for each column (adjust these as needed)
    col_widths = [10, 15, 10, 15, 15, 15, 30]

    # Print headers
    header_row = "".join(header.ljust(width) for header, width in zip(headers, col_widths))
    print(header_row)
    print("-" * sum(col_widths))  # separator line

    rows = modules.db.view_data()
    for row in rows:
        formatted_row = "".join(str(cell).ljust(width) for cell, width in 
            zip(row, col_widths))
        print(formatted_row)

    print("\n")

def gather_data():
    modules.Utils.clear()
    print("Please enter the following information.")

    # Define questions and corresponding keys
    questions = {
        "name": "What is the name of the doe? ",
        "bred": """What date was she bred? (Type 'today' for today's date, 
        or enter Month and day, ex. May 5): """,
        "buck": "Which buck was bred? ",
        "comments": "What other comments do you have? "
    }

    # Gather data
    data = {}
    for key, question in questions.items():
        if key == "bred":
            response = input(question).strip().lower()
            if response == "today":
                # Get today's date in "Month Day" format, e.g., "April 6"
                data[key] = modules.datetime.now().strftime("%B %d")
            else:
                data[key] = response
        else:
            data[key] = input(question)       

    # Calculate dates
    palpatating, nest, due = later_date(data["bred"], 15), later_date(data["bred"], 27), later_date(data["bred"], 31)

    # Display dates
    print("\nPalpatate, Nest box, Due")
    print(palpatating, nest, due)

    # Insert data
    modules.db.insert_data(data["name"], data["bred"], data["buck"], palpatating, nest, due, data["comments"])
    
    # Return to the main options after a button press
    print("\n Press any key to continue ... \n")
    input()
    modules.Utils.clear()

def delete_data():
    modules.Utils.clear()
    print("Please enter the name of the doe you want to delete: ")
    name = input().strip()
    date = input("Please enter the date of the breeding (Month Day): ").strip()
    modules.db.delete_data(name, date)
    print(f"Data for {name} on {date} has been deleted.")
    
    # Return to the main options after a button press
    print("\n Press any key to continue ... \n")
    input()
    modules.Utils.clear()
    
def input_and_handle_entry():
    while True:
        print("\nWhat data would you like to enter?")
        print("""(\033[4mA\033[0mnimals, \033[4mM\033[0mating, \033[4mG\033
        [0mrowth, \033[4mH\033[0mealth, \033[4mB\033[0mehavioral, \033[4mE\033
        [0mconomics, \033[4mE\033[0mxit to main menu)""")

        sub_input = input("Enter your choice: ").lower()

        if sub_input == 'x':
            print("\nReturning to main menu...\n")
            break  # Exit back to the main input loop

        sub_actions = {
            'a': lambda: (modules.Utils.clear(), animals()),
            'm': lambda: (modules.Utils.clear(), mating()),
            'g': lambda: (modules.Utils.clear(), growth()),
            'h': lambda: (modules.Utils.clear(), health()),
            'b': lambda: (modules.Utils.clear(), behavioral()),
            'e': lambda: (modules.Utils.clear(), economics()),
        }

        sub_action = sub_actions.get(sub_input)
        if sub_action:
            sub_action()
        else:
            print("""Invalid input. Please try again or press 'X' to return 
            to the main menu.""")
