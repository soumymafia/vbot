import sqlite3, sys, re  # noqa E401
import pyperclip

try:
    from telethon.sync import TelegramClient, events
    from telethon.sessions import StringSession
    from telethon import functions
    from telethon.tl.types import Channel
    import telethon.errors
except (ImportError, ModuleNotFoundError):
    print("\n―― ⚠️ Telethon library is not installed. Please install it using `pip install telethon`")
    sys.exit()

try:
    from pyrogram import Client, filters
except (ImportError, ModuleNotFoundError):
    print("\n―― ⚠️ Pyrogram library is not installed. Please install it using `pip install pyrogram`")
    sys.exit()


class SessionManager:
    """
    Create a Telegram session using Telethon or Pyrogram.

    `[YouTube] How to Create Telegram Sessions <https://www.youtube.com/watch?v=-2vWERIXXZU>`_
    """
    @staticmethod
    def telethon(api_id: int = None, api_hash: str = None, phone: str = None, password=None,
                 session_file=False, session_string=False) -> None:
        """
        Create Telethon Sessions.

        `API ID & API HASH <https://my.telegram.org/auth>`_ |
        `What are Sessions? <https://docs.telethon.dev/en/stable/concepts/sessions.html#what-are-sessions>`_
        :param api_id: Telegram API ID.
        :param api_hash: Telegram API hash.
        :param phone: Phone number in international format (e.g. +1234567890).
        :param password: 2-Step Verification password.
        :param session_file: If True, create a Telethon session file.
        :param session_string: If True, generate a Telethon string session.
        """

        if session_file and session_string or not session_file and not session_string:
            print("\n―― ⚠️ Please specify a valid session type."
                  "\n―― To create a Telethon session file, set 'session_file' to True."
                  "\n―― To generate a Telethon string session, set 'session_string' to True.")
            return

        try:
            api_id_ = api_id or int(input("Enter your API ID: "))
            api_hash_ = api_hash or input("Enter your API HASH: ")
            phone_ = phone or input("Enter your phone number (e.g. +1234567890): ")
            pwd_ = password or input("Enter 2-Step Verification (press 'Enter' if you don't have it): ")

            if session_file:
                client = TelegramClient(f'{phone_}.session', api_id_, api_hash_)
                client.start(phone_, pwd_)
                print("\n―― 🟢 Session file created successfully!")

            if session_string:
                print("\n―― [1]. Create string session by logging in"
                      "\n―― [2]. Generate string session from existing session file")
                _method = input("\n―― Choose how you want to create the session string: ")

                if _method == "1":
                    with TelegramClient(StringSession(), api_id_, api_hash_).start(phone=phone_, password=pwd_) as client:
                        string = client.session.save()
                        print(f"\n{string}")
                        print("\n―― 🟢 String session created successfully!")
                        try:
                            pyperclip.copy(string)  # Auto copy the string to Clipboard
                            print("―― 🟢 String copied to clipboard!")
                        except (ImportError, ModuleNotFoundError):
                            pass

                elif _method == "2":
                    name = input("Enter your Telethon session file name: ")
                    try:
                        client = TelegramClient(name, api_id_, api_hash_)
                        string = StringSession.save(client.session)
                        print(f"\n{string}")
                        print("\n―― 🟢 String session created successfully!")
                        try:
                            pyperclip.copy(string)
                            print("―― 🟢 String copied to clipboard!")
                        except (ImportError, ModuleNotFoundError):
                            pass
                    except sqlite3.OperationalError:
                        print("\n―― ⚠️ Unable to generate the session string. Please ensure you are using a Telethon session file.")
                else:
                    print("\n―― ⚠️ Invalid input. Please type `1` to create a new string session or `2` to generate a string session from an existing session file.")
        except Exception as e:
            print(f"\n―― ❌ An error has occurred: {e}")

    @staticmethod
    def pyrogram(api_id: int = None, api_hash: str = None, phone: str = None,
                 session_file=False, session_string=False) -> None:
        """
        Create Pyrogram Sessions.

        `API ID & API HASH <https://my.telegram.org/auth>`_ |
        `More about Pyrogram <https://docs.pyrogram.org/api/client/>`_
        :param api_id: Telegram API ID.
        :param api_hash: Telegram API hash.
        :param phone: Phone number in international format (e.g. +1234567890).
        :param session_file: If True, create a Pyrogram session file.
        :param session_string: If True, generate a Pyrogram string session.
        """

        if session_file and session_string or not session_file and not session_string:
            print("\n―― ⚠️ Please specify a valid session type."
                  "\n―― To create a Pyrogram session file, set 'session_file' to True."
                  "\n―― To generate a Pyrogram string session, set 'session_string' to True.")
            return

        try:
            api_id_ = api_id or int(input("Enter your API ID: "))
            api_hash_ = api_hash or input("Enter your API HASH: ")
            phone_ = phone or input("Enter your phone number (e.g. +1234567890): ")

            if session_file:
                with Client(phone_, api_id_, api_hash_, phone_number=phone_) as client:
                    client.send_message('me', 'Hi!')
                    print("\n―― 🟢 Session file created successfully!")
            elif session_string:
                print("\n―― [1]. Create string session by logging in"
                      "\n―― [2]. Generate string session from existing session file")
                _method = input("\n―― Choose how you want to create the session string: ")

                if _method == "1":
                    with Client(phone_, api_id_, api_hash_, phone_number=phone_) as client:
                        string = client.export_session_string()
                        print(f"\n{string}")
                        print("\n―― 🟢 String session created successfully!")
                        try:
                            pyperclip.copy(string)
                            print("―― 🟢 String copied to clipboard!")
                        except (ImportError, ModuleNotFoundError):
                            pass
                elif _method == "2":
                    try:
                        name = input("Enter your Pyrogram session file name: ")
                        with Client(name, api_id_, api_hash_) as client:
                            string = client.export_session_string()
                            print(f"\n{string}")
                            print("\n―― 🟢 String session created successfully!")
                            try:
                                pyperclip.copy(string)
                                print("―― 🟢 String copied to clipboard!")
                            except (ImportError, ModuleNotFoundError):
                                pass
                    except sqlite3.OperationalError:
                        print("\n―― ⚠️ Unable to generate the session string. Please ensure you are using a Pyrogram session file.")
                else:
                    print("\n―― ⚠️ Invalid input. Please type `1` to create a new string session or `2` to generate a string session from an existing session file.")
        except Exception as e:
            print(f"\n―― ❌ An error has occurred: {e}")


class Telegram:
    """
    Interact with Telegram.

    `[YouTube] Login to Telegram Using a Session File or String Session <https://www.youtube.com/watch?v=T2qQfX7kjgI>`_
    """
    @staticmethod
    def login(api_id: int = None, api_hash: str = None, session_name: str = None) -> None:
        """
        Login to Telegram using Telethon session file.
        :param api_id: Telegram API ID.
        :param api_hash: Telegram API hash.
        :param session_name: Your Telethon session file name
        """
        try:
            api_id_ = api_id or int(input("Enter your API ID: "))
            api_hash_ = api_hash or input("Enter your API HASH: ")
            name_ = session_name or input("Enter your Telethon session file name: ")

            client = TelegramClient(name_, api_id_, api_hash_)
            client.connect()
            if client.is_user_authorized():
                print("\n―― 🟢 User Authorized!")

                @client.on(events.NewMessage(from_users=777000))  # '777000' is the ID of Telegram Notification Service.
                async def catch_msg(event):
                    otp = re.search(r'\b(\d{5})\b', event.raw_text)
                    if otp:
                        print("\n―― OTP received ✅\n―― Your login code:", otp.group(0))
                        client.disconnect()
                print("\n―― Please request an OTP code in your Telegram app.\n―― 📲 𝙻𝚒𝚜𝚝𝚎𝚗𝚒𝚗𝚐 𝚏𝚘𝚛 𝚒𝚗𝚌𝚘𝚖𝚒𝚗𝚐 𝙾𝚃𝙿 . . .")
                with client:
                    client.run_until_disconnected()
            else:
                print("\n―― 🔴 Authorization Failed!"
                      "\n―― Invalid Telethon session file or the session has expired.")
        except sqlite3.OperationalError:
            print("\n―― ⚠️ Unable to generate the session string. Please ensure you are using a Pyrogram session file.")
        except Exception as e:
            print(f"\n—— ❌ An error has occurred: {e}")

    @staticmethod
    async def set_2fa(session_name: str, api_id: int, api_hash: str, new_password: str):
        """
        Sets a new Two-Step Verification (2FA) password.

        >>> # Call this function from within an asynchronous context
        >>> tg = Telegram()
        >>> asyncio.run(tg.set_2fa('telethon.session', api_id, api_hash, 'my_password'))  # noqa
        :param session_name: The name of your Telethon session file (e.g., 'my_session.session').
        :param api_id: Telegram API ID.
        :param api_hash: Telegram API hash.
        :param new_password: The new 2FA password to set for the account.
        """
        
        _name = session_name or input("Enter your Telethon session file name: ")
        _api_id = api_id or int(input("Enter your API ID: "))
        _api_hash = api_hash or input("Enter your API HASH: ")
        _new_pwd = new_password or input("Enter your new 2FA password: ")
        
        async with TelegramClient(_name, _api_id, _api_hash) as client:
            try:
                await client.edit_2fa(new_password=_new_pwd)
                print(f"—— 🟢 2FA password '{_new_pwd}' has been set successfully!")
            except telethon.errors.PasswordHashInvalidError:
                print("—— ❌ 2FA is already enabled. You need to provide the current 2FA password.")
                
    @staticmethod
    def userinfo(api_id: int = None, api_hash: str = None, session_name: str = None) -> None:
        """
        Retrieves information about the current user.
        :param api_id: Telegram API ID.
        :param api_hash: Telegram API hash.
        :param session_name: Your Telethon session file name
        """
        try:
            api_id_ = api_id or int(input("Enter your API ID: "))
            api_hash_ = api_hash or input("Enter your API HASH: ")
            name_ = session_name or input("Enter your Telethon session file name: ")

            with TelegramClient(name_, api_id_, api_hash_) as client:
                me = client.get_me()

                name = me.first_name if me.first_name else "-"
                username = f'@{me.username}' if me.username else "-"
                uid = me.id
                phone = me.phone
                print(
                    f"\n  [ACCOUNT's INFO]\n\n"
                    f"  Name: {name}\n"
                    f"  Username: {username}\n"
                    f"  ID: {uid}\n"
                    f"  Phone Number: +{phone}\n\n"
                    f"1. View all connected devices.\n2. See a list of groups and channels.\n3. Exit.\n"
                )
                user_input = input("Choose an option by typing its number: ")
                if user_input == "1":
                    result = client(functions.account.GetAuthorizationsRequest())
                    print(result.stringify())

                elif user_input == "2":
                    pub_gr = 0
                    priv_gr = 0
                    pub_ch = 0
                    priv_ch = 0

                    dialogs = client.get_dialogs()
                    created_groups = [dialog for dialog in dialogs if
                                      isinstance(dialog.entity, Channel) and dialog.entity.creator]

                    for group in created_groups:
                        print('\nGroup Name:', group.entity.title)
                        print('Group ID:', group.entity.id)
                        print('Username:', group.entity.username) if group.entity.username else print("Username: [Private]")
                        print('Creation Date:', group.entity.date.strftime('%Y-%m-%d'))
                        print(f'Link: https://www.t.me/{group.entity.username}\n' if group.entity.username else 'Link: [Private]')

                        if group.entity.megagroup:
                            if group.entity.username:
                                pub_ch += 1
                            else:
                                priv_ch += 1
                        else:
                            if group.entity.username:
                                pub_gr += 1
                            else:
                                priv_gr += 1

                    print(
                        f"Public Groups: {pub_gr}\n"
                        f"Private Groups: {priv_gr}\n"
                        f"Public Channels: {pub_ch}\n"
                        f"Private Channels: {priv_ch}\n\n"
                    )

                else:
                    sys.exit()
        except sqlite3.OperationalError:
            print("\n―― ⚠️ Unable to connect. Please ensure you are using a Telethon session file.")
