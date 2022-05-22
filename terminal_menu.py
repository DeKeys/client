from functions import check_keys, sign_data, init_user, add_password, remove_password, get_passwords, generate_keys

def menu_terminal():
    picture_terminal()
    private_key, public_key, pub_key_string = (keys_terminal())
    signature, data = (sign_data(private_key))
    init_flag = init_user(pub_key_string, signature, data)
    if init_flag != True:
        print("Your keys are invalid")
        return
    while True:
        print(''.join(40 * ["[]"]))
        print(f""" DeKeys Menu:\n1 - Show all paswords\n2 - Add Password\n3 - Remove Password\n4 - Leave""")
        choice = input("Enter an option: ")
        if choice in ["1", "2", "3", "4"]:
            print(''.join(40 * ["[]"]))
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
                break

def picture_terminal():
    print(""""╔═══╗╔═══╗╔╗╔═╗╔═══╗╔╗──╔╗╔═══╗
╚╗╔╗║║╔══╝║║║╔╝║╔══╝║╚╗╔╝║║╔═╗║
─║║║║║╚══╗║╚╝╝─║╚══╗╚╗╚╝╔╝║╚══╗
─║║║║║╔══╝║╔╗║─║╔══╝─╚╗╔╝─╚══╗║
╔╝╚╝║║╚══╗║║║╚╗║╚══╗──║║──║╚═╝║
╚═══╝╚═══╝╚╝╚═╝╚═══╝──╚╝──╚═══╝""")

def keys_terminal():
    print(''.join(40 * ["[]"]))
    key_flag = (input("Do you have a private and public key?\nY/N\n")).upper()
    if key_flag == "N":
        generate_keys()
    private_key, public_key, pub_key_string = (check_keys())
    return private_key, public_key, pub_key_string

def add_password_terminal(public_key, pub_key_string, signature, data):
    service = input("Enter service:\n")
    login = input("\nEnter login:\n")
    password = input("\nEnter password:\n")
    check_flag = (input("\nDo you approve the addition?\nY/N\n")).upper()
    if check_flag == "N":
        return
    add_password(public_key, pub_key_string, signature, data, service, login, password)
    print("Your password has been successfully added")

def get_password_terminal(pub_key_string, private_key, signature, data):
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
    choice = input("Please, enter password id, which you want remove:\n")
    res = get_passwords(pub_key_string, private_key, signature, data)
    try:
        choice = int(choice)
        address = res[choice-1]["address"]
    except:
        print("Something went wrong")
        return
    remove_password(pub_key_string, signature, data, address)
    print("Your password has been removed")


