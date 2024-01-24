# menu management
def main_menu():
    """ Displays the main menu of the system"""
    print(f"1.\tSend Money\n"
          f"2.\tDeposit Money\n"
          f"3.\tWithdraw Money\n"
          f"4.\tMy Account")


def sub_menu():
    """Displays the sub menu of the function"""
    print(f"1.\tCheck Balance\n"
          f"2.\tRecent Transactions\n"
          f"3.\tChange Pin\n"
          f"4.\tReset Pin")


def main_choice_manager(phone: str, database_password):
    """used to manage choices made on the main menu"""
    main_menu()
    choice = get_user_choice(1, 5, 'Choose a service:\t')
    if choice == 1:
        final_stage(lambda: transfer(phone), database_password)
    elif choice == 2:
        deposit(phone)
    elif choice == 3:
        final_stage(lambda: withdraw(phone), database_password)

    elif choice == 4:
        sub_service_manager(phone, database_password)


def sub_service_manager(phone: str, database_password):
    """used as interface for the sub menu choices"""
    sub_menu()
    choice = get_user_choice(1, 5, 'Choose a service:\t')
    sub_choice_manager(phone, choice, database_password)


def sub_choice_manager(phone: str, choice: int, database_password):
    """used to manage sub menu choices"""
    if choice == 1:
        final_stage(lambda: print(f"Your Account balance is {get_user_current_balance(phone)}."), database_password)
    elif choice == 2:
        final_stage(lambda: recent_transactions(phone), database_password)
    elif choice == 3:
        final_stage(lambda: change_pin(phone), database_password)
    elif choice == 4:
        reset_pin(phone)


# interacting with a user

def acquire_user_details():
    """used to get details of a user during registration"""
    f_name = get_user_string('What is you first name? ')
    l_name = get_user_string('What is your last name? ')
    phone = get_user_phone()

    while True:
        if len(phone) == 12:
            break
        else:
            phone = get_user_phone()

    pin = pin_registration()

    birth_month = str(get_user_choice(1, 13, 'What is your birth month\nUse a number. '))
    birth_year = get_user_string('What is your birth year? ')

    return {"f_name": f_name, "l_name": l_name, "phone": phone, "pin": pin, "birth_month": birth_month,
            "birth_year": birth_year}


def get_user_choice(from_: int, to: int, prompt: str):
    """Used When we need user numerical choice in a range of values"""
    while True:
        try:
            number = int(input(prompt))

            if from_ <= number < to:
                return number
            else:
                print('Invalid Choice made')
        except ValueError:
            print('Use Numbers Only')


def get_user_string(prompt: str):
    """ Used When we need an answer to a given question"""
    while True:
        answer = input(prompt)

        if len(answer) >= 3:
            return answer
        else:
            print('Too Short Answer')


def get_user_phone(prompt: str = 'Enter your phone number in the form 256772111333\n:\t'):
    """ Used to get the user phone number"""
    phone = input(prompt)
    while True:
        if len(phone) == 12:
            return phone
        else:
            phone = input(prompt)


def pin_registration():
    """used to obtain a user's pin"""
    new_pin1 = get_user_string('Enter a five digit Pin: ')
    while True:
        if len(new_pin1) == 5 and new_pin1.isdigit():
            break
        else:
            print('The Pin must be five digits')
            new_pin1 = get_user_string('Enter a five digit Pin: ')

    new_pin2 = get_user_string('Confirm Your Pin: ')

    while True:
        if new_pin1 == new_pin2:
            new_pin = secure_pin(new_pin1)
            break
        else:
            new_pin2 = get_user_string('Please Confirm Your Pin')
    return new_pin


def get_user_current_balance(phone: str):
    """used to obtain the current active user balance"""
    import models
    from database import session

    user = session.query(models.User).filter_by(phone=phone).first()
    return int(user.balance)


def get_user_id(phone: str):
    """used to obtain current user id"""
    user = check_number(phone)
    return user.id


# utility functions
def check_number(phone: str):
    """used to check the phone number in the database"""
    import models
    from database import session

    return session.query(models.User).filter_by(phone=phone).first()


def greet_user(f_name: str, l_name: str):
    """Used to greet our Users"""
    from datetime import datetime
    current_time = datetime.now().time()
    if current_time < datetime.strptime('12:00:00', '%H:%M:%S').time():
        return f"GOOD MORNING {f_name.title()} {l_name.title()}\n"
    elif current_time < datetime.strptime('18:00:00', '%H:%M:%S').time():
        return f"GOOD AFTERNOON {f_name.title()} {l_name.title()}\n"
    else:
        return f"GOOD EVENING {f_name.title()} {l_name.title()}\n"


def create_tables():
    """Used to create database tables and the first user (company)"""
    from database import engine
    import models
    models.Base.metadata.create_all(engine)

    company = check_number('256772123123')
    if company:
        pass
    else:
        create_new_user(
            f_name='BISHOP MOBILE MONEY',
            l_name='NOELINE MOBILE MONEY',
            phone='256772123123',
            pin="b'$2b$12$wJky8Jo27VJFSvBiQSvN6.RJn4BTZRio3x4Xka/DKKD/K7j1ZvlFq'",
            birth_month='1',
            birth_year='2024'
        )


def secure_pin(pin: str):
    """used to generate a hash of a pin"""
    import bcrypt
    salt = bcrypt.gensalt()
    hashed = str(bcrypt.hashpw(pin.encode('utf-8'), salt))
    return hashed


def verify_pin(pin: str, hashed: str):
    """used to verify a pin"""
    import bcrypt
    database_hashed = hashed[2:-1].encode()
    if bcrypt.checkpw(pin.encode(), database_hashed):
        return True
    return False


def confirm_identity(phone: str):
    """used to approve the identity of a user before resetting the pin"""
    from database import session
    import models
    birth_month = str(get_user_choice(1, 13, 'What is your birth month\nUse a number. '))
    birth_year = get_user_string('What is your birth year? ')

    user = session.query(models.User).filter_by(phone=phone).first()

    if user.birth_month == birth_month and user.birth_year == birth_year:
        return True
    else:
        return False


def create_new_user(f_name: str, l_name: str,
                    phone: str, pin: str,
                    birth_month: str, birth_year: str):
    """Used to add users to our database"""
    from database import session
    import models
    new_user = models.User(f_name=f_name,
                           l_name=l_name,
                           phone=phone,
                           pin=pin,
                           birth_month=birth_month,
                           birth_year=birth_year)
    session.add(new_user)
    session.commit()


def register_user():
    """used to register users"""
    user_details = acquire_user_details()
    create_new_user(
        user_details.get("f_name"), user_details.get("l_name"), user_details.get("phone"),
        user_details.get("pin"), user_details.get("birth_month"), user_details.get("birth_year")
    )
    print('Account created successfully,\nYou have Free 500/=')


def final_stage(func, database_password):
    """used to handle final service delivery"""
    pin = get_user_string('Enter Your Pin:\t')
    if verify_pin(pin, database_password):
        func()
    else:
        print('Wrong Pin!')


# withdrawing and depositing


def deposit_withdraw(phone: str, top_up: int, action: str = 'deposit'):
    """used to deposit or withdraw money"""
    from database import session
    balance = get_user_current_balance(phone)
    user = check_number(phone)

    if action == 'deposit':
        if top_up >= 500:
            balance += top_up
        else:
            return "You can't deposit amount less than 500", "fail"
    else:
        if top_up <= balance:
            if top_up > 499:
                balance -= top_up
            else:
                return "You can't withdraw amount less than 500", "fail"
        else:
            return 'Not Enough Balance', 'fail'

    user.balance = balance

    session.commit()

    if action == 'deposit':
        return f"Cash Deposit of {top_up} has been made.\nYour new balance is {balance}", balance
    else:
        return f"Cash Withdraw of {top_up} has been made.\nYour new balance is {balance}", balance


def deposit(phone: str):
    """used to deposit money"""
    top_up = int(input('Enter how much to deposit:\t'))
    transactions = deposit_withdraw(phone, top_up)
    if transactions[1] != 'fail':
        company_transactions('deposit', top_up, transactions[1], phone)
        print(transactions[0])
    else:
        print(transactions[0])


def withdraw(phone: str):
    """used to withdraw money"""
    top_up = int(input('Enter how much to withdraw:\t'))
    transactions = deposit_withdraw(phone, top_up, 'withdraw')
    if transactions[1] != 'fail':
        company_transactions('withdraw', top_up, transactions[1], phone)
        print(transactions[0])
    else:
        print(transactions[0])


# money transfer
def transfer(phone: str):
    """used to send money from one user to another"""
    receiver = get_user_phone('Enter the reciever number:\t')
    verification = check_number(receiver)
    if verification:
        amount = int(get_user_string('Enter the amount to send:\t'))
        money_transfer = transfer_money(phone, receiver, amount)
        if money_transfer[1] == 'fail':
            print(money_transfer[0])
        else:
            sender, receive, sender_b, receive_b, amount_ = money_transfer
            user_transactions(amount_, sender_b, receive_b, sender, receive)
            print(f"\nYou have Sent Shs. {amount_} to {receive}\n"
                  f"Your new account balance is {sender_b}")
    else:
        print('User does not exist')


def transfer_money(sender_phone: str, reciever_phone: str, amount: int):
    """used to send money between two users"""
    from database import session
    if amount >= 500:
        sender_balance = get_user_current_balance(sender_phone)
        reciever_balance = get_user_current_balance(reciever_phone)
        sender = check_number(sender_phone)
        receiver = check_number(reciever_phone)

        if sender_balance >= amount:
            sender_balance -= amount
            reciever_balance += amount
            sender.balance = sender_balance
            receiver.balance = reciever_balance
            session.commit()

            return sender_phone, reciever_phone, sender_balance, reciever_balance, amount
        else:
            return 'Not enough Balance', 'fail'
    else:
        return 'You can\'t transfer amount less than 500', 'fail'


# transactions


def company_transactions(action: str, amount: int, new_balance, phone: str):
    """used to record transactions involving the company"""
    import models
    from database import session
    user_id = get_user_id(phone)
    company_id = get_user_id('256772123123')

    if action == 'deposit':
        new_transaction = models.Transaction(
            phone=phone,
            action=action,
            amount=amount,
            balance=int(new_balance),
            sender_id=user_id,
            receiver_id=company_id

        )

        session.add(new_transaction)
        session.commit()

    elif action == 'withdraw':
        new_transaction = models.Transaction(
            phone=phone,
            action=action,
            amount=amount,
            balance=int(new_balance),
            sender_id=company_id,
            receiver_id=user_id

        )

        session.add(new_transaction)
        session.commit()


def user_transactions(amount: int, sender_new_balance, receiver_new_balance, sender_phone: str, receiver_phone):
    """used to record transactions involving two users"""
    import models
    from database import session
    action: str = 'money transfer'
    sender_id = get_user_id(sender_phone)
    receiver_id = get_user_id(receiver_phone)

    sender_transaction = models.Transaction(
        phone=sender_phone,
        action=action,
        amount=amount,
        balance=int(sender_new_balance),
        sender_id=sender_id,
        receiver_id=receiver_id

    )
    receiver_transaction = models.Transaction(
        phone=receiver_phone,
        action=action,
        amount=amount,
        balance=int(receiver_new_balance),
        sender_id=sender_id,
        receiver_id=receiver_id

    )

    transactions = [sender_transaction, receiver_transaction]
    for transaction in transactions:
        session.add(transaction)
        session.commit()


def recent_transactions(phone: str):
    """used to get a users last ten transactions"""
    import models
    from database import session
    count = 1
    user_recent_transactions = session.query(models.Transaction).filter_by(phone=phone).all()[:11]
    if user_recent_transactions:
        for transaction in user_recent_transactions:
            if transaction.action == 'deposit':
                sender = session.query(models.User).filter_by(id=transaction.sender_id).first().phone
                receiver_name = session.query(models.User).filter_by(id=transaction.receiver_id).first().f_name
            elif transaction.action == 'withdraw':
                receiver_name = session.query(models.User).filter_by(id=transaction.receiver_id).first().phone
                sender = session.query(models.User).filter_by(id=transaction.sender_id).first().f_name
            else:
                receiver_name = session.query(models.User).filter_by(id=transaction.receiver_id).first().phone
                sender = session.query(models.User).filter_by(id=transaction.sender_id).first().phone

            print(f'{count}.\tDate:\t\t{transaction.transaction_date.date()}\n'
                  f'\tAction:\t\t{transaction.action.title()}\n'
                  f'\tAmount:\t\t{transaction.amount}\n'
                  f'\tBalance:\t{transaction.balance}\n'
                  f'\tSender:\t\t{sender}\n'
                  f'\tReciever:\t{receiver_name}\n')
            count += 1
    else:
        print('You have no transactions !')


# modifying user pin

def change_pin(phone: str):
    """used to handle changing the state of the pin"""
    from database import session
    import models
    verification = True

    if verification:
        new_pin = pin_registration()

        user = session.query(models.User).filter_by(phone=phone).first()

        user.pin = new_pin
        session.commit()
        print('Change of Pin successful')
    else:
        print('Invalid Pin')


def reset_pin(phone: str):
    """ used to reset the user's pin"""
    from database import session
    import models
    verification = confirm_identity(phone)

    if verification:
        user = session.query(models.User).filter_by(phone=phone).first()
        new_pin = pin_registration()
        user.pin = new_pin
        session.commit()
        print('Pin Reset Successful')
    else:
        print('Invalid Replies about birth month and birth year')
