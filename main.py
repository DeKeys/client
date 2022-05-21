from functions import check_keys, sign_data, init_user, menu, add_password, remove_password, get_passwords

private_key, public_key, pub_key_string = (check_keys())
signature, data = (sign_data(private_key))
init_flag = init_user(pub_key_string, signature, data)
if init_flag == True:
    while True:
        choice = menu()
        match choice:
            case "1":
                get_passwords(pub_key_string, private_key, signature, data)
            case "2":
                add_password(public_key, pub_key_string, signature, data)
            case "3":
                remove_password(pub_key_string,signature, data)
            case "4":
                break
