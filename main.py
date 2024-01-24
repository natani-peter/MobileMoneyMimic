import utils


def main():
    phone = utils.get_user_phone()
    verified_user = utils.check_number(phone)

    if verified_user:
        database_password = verified_user.pin
        print(utils.greet_user(verified_user.f_name, verified_user.l_name))
        utils.main_choice_manager(phone, database_password)
    else:
        print('Register this number with us !')
        utils.register_user()


if __name__ == '__main__':
    utils.create_tables()
    main()
