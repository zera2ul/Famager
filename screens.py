from kivy.uix.screenmanager import Screen
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.label import Label
from kivy.uix.button import Button
from kivy.uix.togglebutton import ToggleButton
from kivy.uix.textinput import TextInput
import webbrowser

from globals import ROLES_EN_RU, ROLES_RU_EN, ROLES_LEVELS, events, current_event, news
from auxiliary import (
    Centred_Text_Input,
    Centred_Button,
    Message_Box,
    Screens_Builder,
    Validator,
    Configuration,
)
from database.queries import (
    User_Queries,
    Family_Queries,
    Invitation_Queries,
    Event_Queries,
    News_Queries,
)


class User_Registration(Screen):
    def __init__(self, **kw):
        super().__init__(**kw)

        registration = Label(text="Регистрация")
        signing_in = Button(text="Вход")
        signing_in.bind(on_press=self.signing_in_on_press)
        upper_layout = BoxLayout(orientation="horizontal", size_hint=(1, 0.25))
        upper_layout.add_widget(registration)
        upper_layout.add_widget(signing_in)

        self.login = Centred_Text_Input(hint_text="Логин")
        self.password = Centred_Text_Input(hint_text="Пароль")

        login_password_layout = BoxLayout(orientation="horizontal")
        login_password_layout.add_widget(self.login)
        login_password_layout.add_widget(self.password)

        self.surname = Centred_Text_Input(hint_text="Фамилия")
        self.Name = Centred_Text_Input(hint_text="Имя")
        self.fathername = Centred_Text_Input(hint_text="Отчество")

        names_layout = BoxLayout(orientation="horizontal")
        names_layout.add_widget(self.surname)
        names_layout.add_widget(self.Name)
        names_layout.add_widget(self.fathername)

        self.birthday = Centred_Text_Input(hint_text="День Рождения")
        register = Button(text="Зарегистрироваться", size_hint=(1, 0.25))
        register.bind(on_press=self.register_on_press)

        layout = BoxLayout(orientation="vertical")
        layout.add_widget(upper_layout)
        layout.add_widget(login_password_layout)
        layout.add_widget(names_layout)
        layout.add_widget(self.birthday)
        layout.add_widget(register)

        self.add_widget(layout)

    def signing_in_on_press(self, instance):
        self.manager.current = "user_signing_in"

    def register_on_press(self, instance):
        login = self.login.text
        if not Validator.validate_login(login):
            self.warning = Message_Box.create_warning(
                self, "Логин может содержать только буквы и цифры"
            )

            self.add_widget(self.warning)

            return

        password = self.password.text

        surname = self.surname.text
        if not Validator.validate_name(surname):
            self.warning = Message_Box.create_warning(
                self, "Фамилия может содержать только буквы"
            )

            self.add_widget(self.warning)

            return

        name = self.Name.text
        if not Validator.validate_name(name):
            self.warning = Message_Box.create_warning(
                self, "Имя может содержать только буквы"
            )

            self.add_widget(self.warning)

            return

        fathername = self.fathername.text
        if not Validator.validate_name(fathername):
            self.warning = Message_Box.create_warning(
                self, "Отчество может содержать только буквы"
            )

            self.add_widget(self.warning)

            return

        birthday = self.birthday.text
        if not Validator.validate_date_format(birthday):
            self.warning = Message_Box.create_warning(
                self, "День Рождения указан неправильно"
            )

            self.add_widget(self.warning)

            return

        user = User_Queries.get(login)
        if not user is None:
            self.warning = Message_Box.create_warning(
                self, "Этот логин уже используется"
            )

            self.add_widget(self.warning)

            return

        User_Queries.add(login, password, surname, name, fathername, birthday)

        self.login.text = ""
        self.password.text = ""
        self.surname.text = ""
        self.Name.text = ""
        self.fathername.text = ""
        self.birthday.text = ""

        self.manager.current = "user_signing_in"

    def close_on_press(self, instance):
        self.remove_widget(self.warning)


class User_Signing_In(Screen):
    def __init__(self, **kw):
        super().__init__(**kw)

        signing_in = Label(text="Вход")
        registration = Button(text="Регистрация")
        registration.bind(on_press=self.registration_on_press)

        upper_layout = BoxLayout(orientation="horizontal", size_hint=(1, 0.2))
        upper_layout.add_widget(signing_in)
        upper_layout.add_widget(registration)

        self.login = Centred_Text_Input(hint_text="Логин")
        self.password = Centred_Text_Input(hint_text="Пароль")
        sign_in = Button(
            text="Войти", size_hint=(1, 0.2), on_press=self.sign_in_on_press
        )

        layout = BoxLayout(orientation="vertical")
        layout.add_widget(upper_layout)
        layout.add_widget(self.login)
        layout.add_widget(self.password)
        layout.add_widget(sign_in)

        self.add_widget(layout)

    def registration_on_press(self, instance):
        self.manager.current = "user_registration"

    def sign_in_on_press(self, instance):
        login = self.login.text
        password = self.password.text

        user = User_Queries.get(login, password)
        if user is None:
            self.warning = Message_Box.create_warning(self, "Неверный логин или пароль")

            self.add_widget(self.warning)

            return

        if Configuration.read_login() == "":
            Configuration.write_login_password(login, password)

        self.login.text = ""
        self.password.text = ""

        main = self.manager.get_screen("main")
        main.user.text = Configuration.read_login()
        self.manager.current = "main"

    def close_on_press(self, instance):
        self.remove_widget(self.warning)


class Main(Screen):
    def __init__(self, **kw):
        super().__init__(**kw)

        self.user = Button(
            text=Configuration.read_login(),
            on_press=self.user_on_press,
            size_hint=(0.3, 1),
        )
        title = Label(text="Главная")
        sign_out = Button(
            text="Выйти", on_press=self.sign_out_on_press, size_hint=(0.3, 1)
        )

        upper_layout = BoxLayout(orientation="horizontal", size_hint=(1, 0.2))
        upper_layout.add_widget(self.user)
        upper_layout.add_widget(title)
        upper_layout.add_widget(sign_out)

        families = Button(text="Семьи", on_press=self.families_on_press)
        events = Button(text="События", on_press=self.events_on_press)
        news = Button(text="Новости", on_press=self.news_on_press)

        layout = BoxLayout(orientation="vertical")
        layout.add_widget(upper_layout)
        layout.add_widget(families)
        layout.add_widget(events)
        layout.add_widget(news)

        self.add_widget(layout)

    def user_on_press(self, instance):
        Screens_Builder.build_changing_personal_data(self)

        self.manager.current = "changing_personal_data"

    def sign_out_on_press(self, instance):
        Configuration.rewrite()

        self.manager.current = "user_signing_in"

    def families_on_press(self, instance):
        self.manager.current = "families"

    def events_on_press(self, instance):
        self.manager.current = "events"

    def news_on_press(self, instance):
        self.manager.current = "news"


class Changing_Personal_Data(Screen):
    def __init__(self, **kw):
        super().__init__(**kw)

        self.clear_widgets()

    def to_main_on_press(self, instance):
        main = self.manager.get_screen("main")
        main.user.text = Configuration.read_login()

        self.manager.current = "main"

    def change_on_press(self, instance):
        login = self.login.text
        password = self.password.text
        surname = self.surname.text
        name = self.Name.text
        fathername = self.fathername.text
        birthday = self.birthday.text
        wishlist = self.wishlist.text

        if not Validator.validate_login(login):
            self.warning = Message_Box.create_warning(
                self, "Логин может содержать только буквы и цифры"
            )

            self.add_widget(self.warning)

            return

        if not Validator.validate_name(surname):
            self.warning = Message_Box.create_warning(
                self, "Фамилия может содержать только буквы"
            )

            self.add_widget(self.warning)

            return

        if not Validator.validate_name(name):
            self.warning = Message_Box.create_warning(
                self, "Имя может содержать только буквы"
            )

            self.add_widget(self.warning)

            return

        if not Validator.validate_name(fathername):
            self.warning = Message_Box.create_warning(
                self, "Отчество может содержать только буквы"
            )

            self.add_widget(self.warning)

            return

        if not Validator.validate_date_format(birthday):
            self.warning = Message_Box.create_warning(
                self, "День Рождения указан неправильно"
            )

            self.add_widget(self.warning)

            return

        if self.old_user_data.login != login:
            user = User_Queries.get(login)

            if not user is None:
                self.warning = Message_Box.create_warning(
                    self, "Этот логин уже используется"
                )

                self.add_widget(self.warning)

                return

            User_Queries.change_data(
                self.old_user_data,
                login,
                password,
                surname,
                name,
                fathername,
                birthday,
                wishlist,
            )

            Family_Queries.change_user_login(self.old_user_data.login, login)
            Invitation_Queries.change_user_login(self.old_user_data.login, login)
            Event_Queries.change_user_login(self.old_user_data.login, login)
            Configuration.rewrite()

            self.manager.current = "user_signing_in"
        elif self.old_user_data.password != password:

            User_Queries.change_data(
                self.old_user_data,
                login,
                password,
                surname,
                name,
                fathername,
                birthday,
                wishlist,
            )

            Configuration.rewrite()

            self.manager.current = "user_signing_in"
        else:
            User_Queries.change_data(
                self.old_user_data,
                login,
                password,
                surname,
                name,
                fathername,
                birthday,
                wishlist,
            )

    def close_on_press(self, instance):
        self.remove_widget(self.warning)


class Families(Screen):
    def __init__(self, **kw):
        super().__init__(**kw)

        invitations = Button(text="Приглашения", on_press=self.invitations_on_press)
        info_about_users = Button(
            text="Информация о пользователях", on_press=self.info_about_users_on_press
        )
        create = Button(text="Создать", on_press=self.create_on_press)
        invite_user = Button(
            text="Пригласить пользователя", on_press=self.invite_user_on_press
        )
        delete = Button(text="Удалить", on_press=self.delete_on_press)
        remove_user = Button(
            text="Удалить пользователя", on_press=self.remove_user_on_press
        )

        layout = BoxLayout(orientation="vertical")
        layout.add_widget(
            Button(
                text="На главную", size_hint=(1, 0.5), on_press=self.to_main_on_press
            )
        )
        layout.add_widget(invitations)
        layout.add_widget(info_about_users)
        layout.add_widget(create)
        layout.add_widget(invite_user)
        layout.add_widget(delete)
        layout.add_widget(remove_user)

        self.add_widget(layout)

    def to_main_on_press(self, instance):
        self.manager.current = "main"

    def invitations_on_press(self, instance):
        Screens_Builder.build_invitations(self)

        self.manager.current = "invitations"

    def info_about_users_on_press(self, instance):
        self.manager.current = "info_about_users"

    def create_on_press(self, instance):
        self.manager.current = "creating_family"

    def invite_user_on_press(self, instance):
        self.manager.current = "inviting_user_into_family"

    def delete_on_press(self, instance):
        self.manager.current = "deleting_family"

    def remove_user_on_press(self, instance):
        self.manager.current = "removing_user_from_family"


class Invitations(Screen):
    def __init__(self, **kw):
        super().__init__(**kw)

        self.clear_widgets()

    def to_main_on_press(self, instance):
        self.manager.current = "main"

    def back_on_press(self, instance):
        self.manager.current = "families"

    def accept_on_press(self, instance):
        inviter = self.Inviter.text
        family = self.Family.text
        role = self.Role.text
        login = Configuration.read_login()

        Family_Queries.add_user(family, inviter, login, ROLES_RU_EN[role])
        Invitation_Queries.delete(login, inviter, family)

        invitation = Invitation_Queries.get_first_by_invited(login)
        if not invitation is None:
            self.Inviter.text = invitation.inviter
            self.Family.text = invitation.family
            self.Role.text = invitation.role
        else:
            self.__init__()
            Screens_Builder.build_invitations(self)

    def decline_on_press(self, instance):
        inviter = self.Inviter.text
        family = self.Family.text
        login = Configuration.read_login()
        Invitation_Queries.delete(login, inviter, family)

        invitation = Invitation_Queries.get_first_by_invited(login)
        if not invitation is None:
            self.Inviter.text = invitation.inviter
            self.Family.text = invitation.family
            self.Role.text = invitation.role
        else:
            self.__init__()
            Screens_Builder.build_invitations(self)


class Info_About_Users(Screen):
    def __init__(self, **kw):
        super().__init__(**kw)

        upper_layout = BoxLayout(orientation="horizontal", size_hint=(1, 0.2))
        upper_layout.add_widget(
            Button(text="На главную", on_press=self.to_main_on_press)
        )
        upper_layout.add_widget(Button(text="Назад", on_press=self.back_on_press))

        self.family = Centred_Text_Input(hint_text="Семья")
        get = Button(text="Получить", on_press=self.get_on_press)

        layout = BoxLayout(orientation="vertical")
        layout.add_widget(upper_layout)
        layout.add_widget(self.family)
        layout.add_widget(get)

        self.add_widget(layout)

    def to_main_on_press(self, instance):
        self.manager.current = "main"

    def back_on_press(self, instance):
        self.manager.current = "families"

    def get_on_press(self, instance):
        family = self.family.text
        user = Configuration.read_login()

        if Family_Queries.is_user_in_family(self.family.text, user) is False:
            self.warning = Message_Box.create_warning(
                self, "Вы не состоите в этой семье"
            )

            self.add_widget(self.warning)

            return

        users_roles = {}
        users = Family_Queries.get_by_member(family, user).users.split("\n")
        for it in users:
            if it == "":
                break

            user_info = it.split(":")
            users_roles[user_info[0]] = ROLES_EN_RU[user_info[1]]

        result = []
        for it in users_roles.items():
            user = User_Queries.get(it[0])
            result.append(
                f"{user.login} - {users_roles[user.login]} - {user.surname} - {user.name} - {user.fathername} - {user.birthday}\n{user.wishlist}\n"
            )

        self.info = Message_Box.create_info(self, "\n".join(result))
        self.add_widget(self.info)

    def close_on_press(self, instance):
        try:
            self.remove_widget(self.warning)
        except:
            pass

        try:
            self.remove_widget(self.info)
        except:
            pass


class Creating_Family(Screen):
    def __init__(self, **kw):
        super().__init__(**kw)

        upper_layout = BoxLayout(orientation="horizontal", size_hint=(1, 0.2))
        upper_layout.add_widget(
            Button(text="На главную", on_press=self.to_main_on_press)
        )
        upper_layout.add_widget(Button(text="Назад", on_press=self.back_on_press))

        self.Name = Centred_Text_Input(hint_text="Название")
        create = Button(text="Создать", on_press=self.create_on_press)

        layout = BoxLayout(orientation="vertical")
        layout.add_widget(upper_layout)
        layout.add_widget(self.Name)
        layout.add_widget(create)

        self.add_widget(layout)

    def to_main_on_press(self, instance):
        self.manager.current = "main"

    def back_on_press(self, instance):
        self.manager.current = "families"

    def create_on_press(self, instance):
        name = self.Name.text
        creator = Configuration.read_login()

        if not Validator.validate_name(name):
            self.warning = Message_Box.create_warning(
                self, "Название семьи может содержать только буквы"
            )

            self.add_widget(self.warning)

            return

        if Family_Queries.is_user_in_family(name, creator) is False:
            Family_Queries.add(name, creator)
        else:
            self.warning = Message_Box.create_warning(
                self, "Вы уже состоите в семье с таким названием"
            )

            self.add_widget(self.warning)

            return

        self.Name.text = ""

    def close_on_press(self, instance):
        self.remove_widget(self.warning)


class Inviting_User_Into_Family(Screen):
    def __init__(self, **kw):
        super().__init__(**kw)

        upper_layout = BoxLayout(orientation="horizontal", size_hint=(1, 0.2))
        upper_layout.add_widget(
            Button(text="На главную", on_press=self.to_main_on_press)
        )
        upper_layout.add_widget(Button(text="Назад", on_press=self.back_on_press))

        self.family_name = Centred_Text_Input(hint_text="Семья")
        self.user = Centred_Text_Input(hint_text="Пользователь")

        self.is_admin = ToggleButton(text="Админ", group="")
        invite = Button(text="Пригласить", on_press=self.invite_on_press)

        layout = BoxLayout(orientation="vertical")
        layout.add_widget(upper_layout)
        layout.add_widget(self.family_name)
        layout.add_widget(self.user)
        layout.add_widget(self.is_admin)
        layout.add_widget(invite)

        self.add_widget(layout)

    def to_main_on_press(self, instance):
        self.manager.current = "main"

    def back_on_press(self, instance):
        self.manager.current = "families"

    def invite_on_press(self, instance):
        family = self.family_name.text
        inviter = Configuration.read_login()
        user = self.user.text

        if Family_Queries.is_user_in_family(family, inviter) is False:
            self.warning = Message_Box.create_warning(
                self, "Вы не состоите в семье с таким названием"
            )

            self.add_widget(self.warning)

            return

        inviter_role = Family_Queries.get_user_role(family, inviter)
        if inviter_role == "Member":
            self.warning = Message_Box.create_warning(
                self, "Вы не можете приглашать пользователей в эту семью"
            )

            self.add_widget(self.warning)

            return

        if User_Queries.get(user) is None:
            self.warning = Message_Box.create_warning(
                self, "Несуществует пользователя с таким логином"
            )

            self.add_widget(self.warning)

            return

        role = "Member"
        if self.is_admin.state == "down":
            role = "Admin"

        if ROLES_LEVELS[inviter_role] == ROLES_LEVELS[role]:
            self.warning = Message_Box.create_warning(
                self, "Вы не можете давать пользователям роль админа"
            )

            self.add_widget(self.warning)

            return

        if Invitation_Queries.is_user_invited_in_family(user, family):
            self.warning = Message_Box.create_warning(
                self, "Этот пользователь уже приглашён в семью с таким названием"
            )

            self.add_widget(self.warning)

            return

        if Family_Queries.is_user_in_family(family, user):
            self.warning = Message_Box.create_warning(
                self, "Этот пользователь уже находится в семье с таким названием"
            )

            self.add_widget(self.warning)

            return

        Invitation_Queries.add(user, inviter, family, role)

        self.family_name.text = ""
        self.user.text = ""
        self.is_admin.state = "normal"

    def close_on_press(self, instance):
        self.remove_widget(self.warning)


class Deleting_Family(Screen):
    def __init__(self, **kw):
        super().__init__(**kw)

        upper_layout = BoxLayout(orientation="horizontal", size_hint=(1, 0.2))
        upper_layout.add_widget(
            Button(text="На главную", on_press=self.to_main_on_press)
        )
        upper_layout.add_widget(Button(text="Назад", on_press=self.back_on_press))

        self.family = Centred_Text_Input(hint_text="Семья")
        delete = Button(text="Удалить", on_press=self.delete_on_press)

        layout = BoxLayout(orientation="vertical")
        layout.add_widget(upper_layout)
        layout.add_widget(self.family)
        layout.add_widget(delete)

        self.add_widget(layout)

    def to_main_on_press(self, instance):
        self.manager.current = "main"

    def back_on_press(self, instance):
        self.manager.current = "families"

    def delete_on_press(self, instance):
        family = self.family.text
        user = Configuration.read_login()

        if Family_Queries.is_user_in_family(family, user) is False:
            self.warning = Message_Box.create_warning(
                self, "Вы не состоите в такой семье"
            )

            self.add_widget(self.warning)

            return

        if Family_Queries.get_user_role(family, user) != "Creator":
            self.warning = Message_Box.create_warning(
                self, "Вы не можете удалить эту семью"
            )

            self.add_widget(self.warning)

            return

        Family_Queries.delete(family, user)
        Event_Queries.delete_by_family(family, user)

        self.family.text = ""

    def close_on_press(self, instance):
        self.remove_widget(self.warning)


class Removing_User_From_Family(Screen):
    def __init__(self, **kw):
        super().__init__(**kw)

        upper_layout = BoxLayout(orientation="horizontal", size_hint=(1, 0.2))
        upper_layout.add_widget(
            Button(text="На главную", on_press=self.to_main_on_press)
        )
        upper_layout.add_widget(Button(text="Назад", on_press=self.back_on_press))

        self.family = Centred_Text_Input(hint_text="Семья")
        self.user = Centred_Text_Input(hint_text="Пользователь")
        remove = Button(text="Удалить", on_press=self.remove_on_press)

        layout = BoxLayout(orientation="vertical")
        layout.add_widget(upper_layout)
        layout.add_widget(self.family)
        layout.add_widget(self.user)
        layout.add_widget(remove)

        self.add_widget(layout)

    def to_main_on_press(self, instance):
        self.manager.curren = "main"

    def back_on_press(self, instance):
        self.manager.current = "families"

    def remove_on_press(self, instance):
        family = self.family.text
        user = self.user.text
        remover = Configuration.read_login()

        if Family_Queries.is_user_in_family(family, remover) is False:
            self.warning = Message_Box.create_warning(
                self, "Вы не состоите в такой семье"
            )

            self.add_widget(self.warning)

            return

        if Family_Queries.is_user_in_family(family, user) is False:
            self.warning = Message_Box.create_warning(
                self, "В этой семье нет такого пользователя"
            )

            self.add_widget(self.warning)

            return

        user_level = ROLES_LEVELS[Family_Queries.get_user_role(family, user)]
        remover_level = ROLES_LEVELS[Family_Queries.get_user_role(family, remover)]

        if user_level >= remover_level:
            self.warning = Message_Box.create_warning(
                self, "Вы не можете удалить этого пользователя из этой семьи"
            )

            self.add_widget(self.warning)

            return

        Family_Queries.remove_user(family, remover, user)

        self.family.text = ""
        self.user.text = ""

    def close_on_press(self, instance):
        self.remove_widget(self.warning)


class Events(Screen):
    def __init__(self, **kw):
        super().__init__(**kw)

        view = Button(text="Просмотреть")
        view.bind(on_press=self.view_on_press)
        create = Button(text="Создать")
        create.bind(on_press=self.create_on_press)
        delete = Button(text="Удалить")
        delete.bind(on_press=self.delete_on_press)

        layout = BoxLayout(orientation="vertical")
        layout.add_widget(
            Button(
                text="На главную", on_press=self.to_main_on_press, size_hint=(1, 0.2)
            )
        )
        layout.add_widget(view)
        layout.add_widget(create)
        layout.add_widget(delete)

        self.add_widget(layout)

    def to_main_on_press(self, instance):
        self.manager.current = "main"

    def view_on_press(self, instance):
        Screens_Builder.build_viewing_events(self)

        self.manager.current = "viewing_events"

    def create_on_press(self, instance):
        self.manager.current = "creating_event"

    def delete_on_press(self, instance):
        self.manager.current = "deleting_event"


class Viewing_Events(Screen):
    def __init__(self, **kw):
        super().__init__(**kw)

        self.clear_widgets()

    def to_main_on_press(self, instance):
        self.manager.current = "main"

    def back_on_press(self, instance):
        self.manager.current = "events"

    def change_status_on_press(self, instance):
        date = self.date.text
        topic = self.topic.text
        family = self.family.text
        user = Configuration.read_login()

        Event_Queries.update_who_doesnt_participate(date, topic, family, user)

        Screens_Builder.build_viewing_events(self)

    def previous_on_press(self, instance):
        global events, current_event

        if current_event == 0:
            return

        current_event -= 1
        self.date.text = str(events[current_event].date)
        self.time.text = str(events[current_event].time)
        self.place.text = str(events[current_event].place)
        self.topic.text = str(events[current_event].topic)

        self.family.text = str(events[current_event].family)
        self.creator.text = str(events[current_event].creator)
        self.who_doesnt_participate.text = str(
            events[current_event].who_doesnt_participate
        )
        self.notes.text = str(events[current_event].notes)

    def next_on_press(self, instance):
        global events, current_event

        if current_event == len(events) - 1:
            return

        current_event += 1
        self.date.text = events[current_event].date
        self.time.text = events[current_event].time
        self.place.text = events[current_event].place
        self.topic.text = events[current_event].topic
        self.family.text = events[current_event].family
        self.creator.text = events[current_event].creator
        self.who_doesnt_participate.text = events[current_event].who_doesnt_participate
        self.notes.text = events[current_event].notes


class Creating_Event(Screen):
    def __init__(self, **kw):
        super().__init__(**kw)

        upper_layout = BoxLayout(orientation="horizontal", size_hint=(1, 0.2))
        upper_layout.add_widget(
            Button(text="На главную", on_press=self.to_main_on_press)
        )
        upper_layout.add_widget(Button(text="Назад", on_press=self.back_on_press))

        self.date = TextInput(hint_text="Дата", multiline=False, halign="center")
        self.time = TextInput(hint_text="Время", multiline=False, halign="center")
        self.place = TextInput(hint_text="Место", multiline=False, halign="center")

        date_time_place_layout = BoxLayout(orientation="horizontal")
        date_time_place_layout.add_widget(self.date)
        date_time_place_layout.add_widget(self.time)
        date_time_place_layout.add_widget(self.place)

        self.topic = TextInput(hint_text="Тема", multiline=False, halign="center")
        self.family = TextInput(hint_text="Семья", multiline=False, halign="center")

        topic_family_layout = BoxLayout(orientation="horizontal")
        topic_family_layout.add_widget(self.topic)
        topic_family_layout.add_widget(self.family)

        self.notes = TextInput(hint_text="Заметки", halign="center")
        create = Button(text="Создать", on_press=self.create_on_press)

        layout = BoxLayout(orientation="vertical")
        layout.add_widget(upper_layout)
        layout.add_widget(date_time_place_layout)
        layout.add_widget(topic_family_layout)
        layout.add_widget(self.notes)
        layout.add_widget(create)

        self.add_widget(layout)

    def to_main_on_press(self, instance):
        self.manager.current = "main"

    def back_on_press(self, instance):
        self.manager.current = "events"

    def create_on_press(self, instance):
        date = self.date.text
        time = self.time.text
        place = self.place.text
        topic = self.topic.text
        notes = self.notes.text
        family = self.family.text
        creator = Configuration.read_login()

        if Validator.validate_date_format(date) is False:
            self.warning = Message_Box.create_warning(self, "Дата указана неправильно")

            self.add_widget(self.warning)

            return

        if Validator.validate_date_value(date) is False:
            self.warning = Message_Box.create_warning(
                self, "Нельзя указывать дату в прошлом"
            )

            self.add_widget(self.warning)

            return

        if Validator.validate_time_format(time) is False:
            self.warning = Message_Box.create_warning(self, "Время указано неправильно")

            self.add_widget(self.warning)

            return

        if Validator.validate_time_value(date, time) is False:
            self.warning = Message_Box.create_warning(
                self, "Нельзя указывать время в прошлом"
            )

            self.add_widget(self.warning)

            return

        if Family_Queries.is_user_in_family(family, creator) is False:
            self.warning = Message_Box.create_warning(
                self, "Вы не состоите в этой семье"
            )

            self.add_widget(self.warning)

            return

        if Family_Queries.get_user_role(family, creator) == "Member":
            self.warning = Message_Box.create_warning(
                self, "Вы не можете создавать события в этой семье"
            )

            self.add_widget(self.warning)

            return

        if not Event_Queries.get_by_participant(date, topic, family, creator) is None:
            self.warning = Message_Box.create_warning(
                self, "Такое событие уже существует"
            )

            self.add_widget(self.warning)

            return

        Event_Queries.add(date, time, place, topic, family, creator, notes)

        self.date.text = ""
        self.time.text = ""
        self.place.text = ""
        self.topic.text = ""
        self.family.text = ""
        self.notes.text = ""

    def close_on_press(self, instance):
        self.remove_widget(self.warning)


class Deleting_Event(Screen):
    def __init__(self, **kw):
        super().__init__(**kw)

        upper_layout = BoxLayout(orientation="horizontal", size_hint=(1, 0.2))
        upper_layout.add_widget(
            Button(text="На главную", on_press=self.to_main_on_press)
        )
        upper_layout.add_widget(Button(text="Назад", on_press=self.back_on_press))

        self.date = Centred_Text_Input(hint_text="Дата")
        self.topic = Centred_Text_Input(hint_text="Тема")
        self.family = Centred_Text_Input(hint_text="Семья")
        delete = Button(text="Удалить", on_press=self.delete_on_press)

        layout = BoxLayout(orientation="vertical")
        layout.add_widget(upper_layout)
        layout.add_widget(self.date)
        layout.add_widget(self.topic)
        layout.add_widget(self.family)
        layout.add_widget(delete)

        self.add_widget(layout)

    def to_main_on_press(self, instance):
        self.manager.current = "main"

    def back_on_press(self, instance):
        self.manager.current = "events"

    def delete_on_press(self, instance):
        date = self.date.text
        topic = self.topic.text
        family = self.family.text
        user = Configuration.read_login()

        if Family_Queries.is_user_in_family(family, user) is False:
            self.warning = Message_Box.create_warning(
                self, "Вы не состоите в этой семье"
            )

            self.add_widget(self.warning)

            return

        if Event_Queries.get_by_participant(date, topic, family, user) is None:
            self.warning = Message_Box.create_warning(
                self, "Такого события не существует"
            )

            self.add_widget(self.warning)

            return

        if Family_Queries.get_user_role(family, user) == "Member":
            self.warning = Message_Box.create_warning(
                self, "Вы не можете удалять события"
            )

            self.add_widget(self.warning)

            return

        Event_Queries.delete_by_participant(date, topic, family, user)

        self.date.text = ""
        self.topic.text = ""
        self.family.text = ""

    def close_on_press(self, instance):
        self.remove_widget(self.warning)


class News(Screen):
    def __init__(self, **kw):
        global news
        super().__init__(**kw)

        layout = BoxLayout(orientation="vertical")
        layout.add_widget(
            Button(
                text="На главную", on_press=self.to_main_on_press, size_hint=(1, 0.5)
            )
        )
        news = News_Queries.get_all()
        for it in news.keys():
            news_button = Centred_Button(text=it, on_press=self.button_on_press)
            layout.add_widget(news_button)

        self.add_widget(layout)

    def to_main_on_press(self, instance):
        self.manager.current = "main"

    def button_on_press(self, instance):
        webbrowser.open(f"https://pravo.by{news[instance.text]}")
