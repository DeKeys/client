from functions import check_keys, sign_data, init_user, add_password, delete_password, get_passwords, generate_keys, edit_password


def menu_terminal():
    """Func which print menu and start another functions to work with server"""
    picture_terminal()
    private_key, public_key, pub_key_string = (keys_terminal())
    signature, data = (sign_data(private_key))
    init_flag = init_user(pub_key_string, signature, data)
    if init_flag != True:
        print("Your keys are invalid")
        return
    while True:
        print(''.join(40 * ["[]"]))
        print(f""" DeKeys Menu:\n1 - Show all paswords\n2 - Add Password\n3 - Remove Password\n4 - Edit Password\n5 - Leave""")
        choice = input("Enter an option: ")
        if choice in ["1", "2", "3", "4", "5"]:
            print_delimiter()
        else:
            print("Invalid character")
        match choice:
            case "1":
                get_password_terminal(pub_key_string, private_key, signature, data)
            case "2":
                add_password_terminal(public_key, pub_key_string, signature, data)
            case "3":
                remove_password_terminal(pub_key_string, signature, data, private_key)
            case "4":
                change_password_terminal(public_key, pub_key_string, signature, data, private_key)
            case "5":
                break

def picture_terminal():
    """Func which print logo"""
    print(""""╔═══╗╔═══╗╔╗╔═╗╔═══╗╔╗──╔╗╔═══╗
╚╗╔╗║║╔══╝║║║╔╝║╔══╝║╚╗╔╝║║╔═╗║
─║║║║║╚══╗║╚╝╝─║╚══╗╚╗╚╝╔╝║╚══╗
─║║║║║╔══╝║╔╗║─║╔══╝─╚╗╔╝─╚══╗║
╔╝╚╝║║╚══╗║║║╚╗║╚══╗──║║──║╚═╝║
╚═══╝╚═══╝╚╝╚═╝╚═══╝──╚╝──╚═══╝""")


def print_delimiter():
    """Func which print delimiter"""
    print("=" * 80)


def keys_terminal():
    """Func which check/create private and public key"""
    print_delimiter()
    key_flag = (input("Do you have a private and public key?\nY/N\n")).upper()
    if key_flag == "N":
        generate_keys()
    private_key, public_key, pub_key_string = (check_keys())
    return private_key, public_key, pub_key_string


def add_password_terminal(public_key, pub_key_string, signature, data):
    """Func which input data from user and start add_password func from functions.py"""
    service = input("Enter service:\n")
    login = input("\nEnter login:\n")
    password = input("\nEnter password:\n")
    check_flag = (input("\nDo you approve the addition?\nY/N\n")).upper()
    if check_flag == "N":
        return
    add_password(public_key, pub_key_string, signature, data, service, login, password)
    print("Your password has been successfully added")


def get_password_terminal(pub_key_string, private_key, signature, data):
    """Func which start get_passwords func from functions and print all keys to screen"""
    res = get_passwords(pub_key_string, private_key, signature, data)
    count = 0
    print("")
    for i in res:
        count += 1
        print(f"id: {count}")
        print(f"Service: {i['service']}")
        print(f"Login: {i['login']}")
        print(f"Password: {i['password']}\n")
        print(f"Address: {i['address']}\n")


def remove_password_terminal(pub_key_string, signature, data, private_key):
    """Func which find key which user want delete and start delete_password from functions.py"""
    choice = input("Please, enter password id, which you want remove:\n")
    res = get_passwords(pub_key_string, private_key, signature, data)
    try:
        choice = int(choice)
        address = res[choice-1]["address"]
    except:
        print("Something went wrong")
        return
    delete_password(pub_key_string, signature, data, address)
    print("Your password has been removed")

def change_password_terminal(public_key, pub_key_string, signature, data, private_key):
    """Func which input data from user and start edit_password from functions"""
    choice = input("Please, enter password id, which you want change\n")
    res = get_passwords(pub_key_string, private_key, signature, data)
    try:
        choice = int(choice)
        block = res[choice - 1]
    except:
        print("Something went wrong")
        return
    login = input("\nEnter login:\n")
    password = input("\nEnter password:\n")
    check_flag = (input("\nDo you approve the addition?\nY/N\n")).upper()
    if check_flag == "N":
        return
    edit_password(public_key, pub_key_string, signature, block["address"], block["service"], login, password, data)
