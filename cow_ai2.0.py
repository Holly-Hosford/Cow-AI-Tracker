import datetime
from datetime import timedelta
import sys

cow_dict = {}
add = open("practice.txt", "a")
read = open("practice.txt", "r")
if len(read.readlines()) > 0:
    with open("practice.txt", "r") as read:
        cow_dict = eval(read.read())


def get_number():
    try:
        number = int(input("Enter the cow number you want to enter/add to/look at: "))
        get_function(number)
    except ValueError:
        print("You did not enter a number, please try again.")
        get_number()


def get_function(number):
    num = str(number)
    start = input("To enter information to the cow " + num + ", type enter. \n"
                  "To get the information on cow " + num + ", type get. \n"
                  "To find the expected calving date of cow " + num + ", type date. \n"
                  "To edit the information on cow " + num + ", enter edit. \n"
                  "To choose a different cow number, enter change. \n"
                  "To add additional information to the cow " + num + ", type add. \n"
                  "To end the program type exit. \n"
                  "To remove some information from the cow, " + num + ", type remove. \n"
                  "To find all the cows with a common bull, type common: ")
    decide_function(start.lower(), number)


def repeat(number):
    start = input("Type exit to end the program, else type enter, get, date, edit, add, remove, common or "
                  "change to continue: ")
    decide_function(start.lower(), number)



def decide_function(start, number):
    if start == "exit":
        new = open("practice.txt", "w")
        new2 = open("cow_ai_info2.0.txt", "w")
        new.write(str(cow_dict))
        for key, val in cow_dict.items():
            cow_list = key, val
            new2.write(str(cow_list))
            new2.write("\n")
        read.close()
        add.close()
        new.close()
        new2.close()
        print("All information has been added")
        sys.exit()
    elif start == "add":
        additional(number)
    elif start == "enter":
        check_num(number)
    elif start == "change":
        get_number()
    elif start == "get":
        get(number)
    elif start == "date":
        estimate_date(number)
    elif start == "edit":
        one_two(number)
    elif start == "remove":
        remove(number)
    elif start == "common":
        common(number)
    else:
        repeat(number)


def check_num(number):
    if number in cow_dict:
        add_info(number)
    elif number not in cow_dict:
        add_num(number)


def add_num(number):
    first_ai = input("Please enter first date dd-mm-yyyy: ")
    try:
        check_date(first_ai)
    except ValueError:
        print("Please enter the date again. It was entered incorrectly")
        add_num(number)
    else:
        bull = input("Please enter the bull number: ")
        cow_dict[number] = [[first_ai, bull]]
        repeat(number)


def add_info(number):
    add_ai = input("Please enter the date dd-mm-yyyy: ")
    try:
        check_date(add_ai)
    except ValueError:
        print("An error occurred when the date was entered. Please try again. ")
        add_info(number)
    else:
        bull_num = input("Please enter the bull number: ")
        cow_dict[number] += [[add_ai, bull_num]]
        repeat(number)


def check_date(date):
    datetime.datetime.strptime(date, "%d-%m-%Y").date()



def get(number):
    if number in cow_dict:
        print(cow_dict.get(number))
        repeat(number)
    else:
        print("That cow has not previously been entered")
        repeat(number)


def estimate_date(number):
    try:
        info = cow_dict.get(number)
        num = len([len(i) for i in info])
        if num == 1:
            initial_date = info[0][0]
        else:
            initial_date = info[len(info) - 1][0]
        initial_date = datetime.datetime.strptime(initial_date, "%d-%m-%Y")
        initial_date = initial_date.date()
        first_date = (initial_date + timedelta(days=279)).isoformat()
        last_date = (initial_date + timedelta(days=287)).isoformat()
        print(first_date, "-", last_date)
        repeat(number)
    except TypeError:
        print("An error has occurred. Please type get to see the information regarding cow number " + str(number) +
              " and try again later.")
        repeat(number)
    except ValueError:
        print("There is no date to estimate for this cow. Please type get to see the information regarding "
              "cow number " + str(number) + " and try again later.")
        repeat(number)


def one_two(number):
    try:
        choice = int(input("Type 1 to edit records or 2 to edit additional information for this cow: "))
        if choice == 1 or choice == 2:
            edit(number, choice)
        else:
            print("That is not one of the options. Try again.")
            one_two(number)
    except ValueError:
        print("That choice was not an option. Please try again")
        one_two(number)


def edit(number, choice):
    if number in cow_dict:
        info = cow_dict.get(number)
        len1 = len([len(i) for i in info])
        len2 = [len(i) for i in info]
        num = len1
        for i in range(len1):
            if len(info[i]) == 2:
                try:
                    datetime.datetime.strptime(info[i][0], "%d-%m-%Y")
                    if choice == 1:
                        if len1 == 1:
                            if len2[0] == 2:
                                new_date = input(
                                    "There is only one record for this cow. Please enter the correct date dd-mm-yyyy: ")
                                try:
                                    check_date(new_date)
                                except ValueError:
                                    print("An error occurred when the date was entered. Please try again.")
                                    edit(number, choice)
                                else:
                                    new_bull = input("Please enter the correct bull number: ")
                                    cow_dict[number] = [[new_date, new_bull]]
                                    repeat(number)
                        else:
                            print("There are " + str(
                                num) + " records for this cow. Please repeat the records for this cow individually. ")
                            additional_info = cow_dict.get(number)[0:len1-num]
                            cow_dict[number] = additional_info
                            for j in range(0, num):
                                new_date = input("Please enter the correct date dd-mm-yyyy: ")
                                try:
                                    check_date(new_date)
                                except ValueError:
                                    print("An error occurred when the date was entered. Please try again.")
                                    edit(number, choice)
                                else:
                                    new_bull = input("Please enter the correct bull number: ")
                                    cow_dict[number] += [[new_date, new_bull]]
                            break
                    elif choice == 2:
                        cow_records = info[(len1 - num):len1]
                        cow_dict[number] = []
                        for j in range(0, len1-num):
                            new_additional_info = input("Please enter the correct additional information: ")
                            cow_dict[number] += [new_additional_info]
                        else:
                            print("There is no additional information to be edited")
                        cow_dict[number] += cow_records
                        break
                except ValueError:
                    num -= 1
            else:
                num -= 1
    else:
        print("That cow has not previously been entered")
    repeat(number)


def additional(number):
    prev_add = []
    if number in cow_dict:
        old_info = cow_dict[number]
        info = cow_dict.get(number)
        len1 = len([len(i) for i in info])
        for i in range(0, len1):
            if len(info[i]) == 2:
                try:
                    datetime.datetime.strptime(info[i][0], "%d-%m-%Y")
                    prev_add = info[0:i]
                    break
                except ValueError:
                    continue
            prev_add = info[0:i]
        new_info = input("Enter the additional information here: ")
        cow_dict[number] = prev_add
        cow_dict[number] += [new_info]
        cow_dict[number] += old_info[len(cow_dict[number])-1:len1]
        repeat(number)
    else:
        new_info = input("Enter the additional information here: ")
        cow_dict[number] = [new_info]
        repeat(number)


def remove(number):
    if cow_dict.get(number) != None:
        print(cow_dict.get(number))
    choice = input("Would you like to remove all information on the cow " + str(number) + " or would you like to "
                   "remove 1 piece of information. Please type all to remove all information on this cow or 1 to "
                   "remove 1 piece of information. ")
    if choice.lower() == "all":
        try:
            cow_dict.pop(number)
        except KeyError:
            print("There are no records on this cow to remove.")
    elif choice.lower() == "1":
        try:
            info = cow_dict.get(number)
            num_list = list(range(1, len(info)+1))
            for i, j in zip(num_list, info):
                print(i, j)
            try:
                to_remove = int(input("Please type in the number which corresponds with the piece of information you "
                                      "want to remove from the list above: "))
                del cow_dict[number][to_remove - 1]
            except TypeError:
                print("That is not a number. Please try again.")
                remove(number)
            except IndexError:
                print("That was not one of the options. Please Try again.")
            if cow_dict[number] == []:
                cow_dict.pop(number)
        except KeyError:
            print("There are no records on this cow to remove.")
        except TypeError:
            print("There are no records on this cow to remove.")
    else:
        repeat(number)
    repeat(number)


def common(number):
    bull = input("Type in which bull you are looking: ")
    bull_list = [key for key, val in cow_dict.items() for i in val for j in i if bull in j]
    if len(bull_list) > 0:
        print(bull_list)
    else:
        print("There is no record with that bull number in it.")
    repeat(number)


get_number()
