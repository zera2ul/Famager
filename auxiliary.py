from datetime import datetime
from kivy.uix.popup import Popup
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.label import Label
from kivy.uix.button import Button
from kivy.uix.textinput import TextInput

from consts import ROLES_EN_RU
from database.queries import User_Queries, Invitation_Queries, Event_Queries


events = []
current_event = 0
news = {}


class Message_Box:
    def message_width(self, instance):
        self.setter("text_size")(self, (self.width, None))

    @classmethod
    def create_warning(cls, parent, text):
        warning = Popup(
            title="Предупреждение",
            title_align="center",
            size_hint=(0.75, 0.75),
            pos_hint={"center_x": 0.5, "center_y": 0.5},
        )
        message = Label(text=text, halign="center", valign="middle")
        message.bind(width=cls.message_width)
        close = Button(text="Закрыть")
        close.bind(on_press=parent.close_on_press)

        content = BoxLayout(orientation="vertical")
        content.add_widget(message)
        content.add_widget(close)
        warning.content = content

        return warning

    @classmethod
    def create_info(cls, parent, text):
        info = Popup(
            title="Информация",
            title_align="center",
        )
        message = Label(text=text, halign="center", valign="middle")
        message.bind(width=cls.message_width)
        close = Button(
            text="Закрыть", on_press=parent.close_on_press, size_hint=(1, 0.2)
        )

        content = BoxLayout(orientation="vertical")
        content.add_widget(message)
        content.add_widget(close)
        info.content = content

        return info


class Screens_Builder:
    @staticmethod
    def build_changing_personal_data(screen):
        changing_personal_data = screen.manager.get_screen("changing_personal_data")
        changing_personal_data.__init__()

        to_main = Button(text="На главную", size_hint=(1, 0.2))
        to_main.bind(on_press=changing_personal_data.to_main_on_press)

        changing_personal_data.old_user_data = User_Queries.get(
            Configuration.read_login()
        )
        changing_personal_data.login = TextInput(
            text=changing_personal_data.old_user_data.login, halign="center"
        )
        changing_personal_data.password = TextInput(
            text=changing_personal_data.old_user_data.password, halign="center"
        )
        changing_personal_data.surname = TextInput(
            text=changing_personal_data.old_user_data.surname, halign="center"
        )
        changing_personal_data.Name = TextInput(
            text=changing_personal_data.old_user_data.name, halign="center"
        )
        changing_personal_data.fathername = TextInput(
            text=changing_personal_data.old_user_data.fathername, halign="center"
        )
        changing_personal_data.birthday = TextInput(
            text=changing_personal_data.old_user_data.birthday, halign="center"
        )

        left_layout = BoxLayout(orientation="vertical")
        left_layout.add_widget(changing_personal_data.login)
        left_layout.add_widget(changing_personal_data.password)
        left_layout.add_widget(changing_personal_data.surname)
        left_layout.add_widget(changing_personal_data.Name)
        left_layout.add_widget(changing_personal_data.fathername)
        left_layout.add_widget(changing_personal_data.birthday)

        changing_personal_data.wishlist = TextInput(
            hint_text="Вишлист",
            text=changing_personal_data.old_user_data.wishlist,
            halign="center",
        )

        center_layout = BoxLayout(orientation="horizontal")
        center_layout.add_widget(left_layout)
        center_layout.add_widget(changing_personal_data.wishlist)

        change = Button(
            text="Изменить",
            on_press=changing_personal_data.change_on_press,
            size_hint=(1, 0.2),
        )

        layout = BoxLayout(orientation="vertical")
        layout.add_widget(to_main)
        layout.add_widget(center_layout)
        layout.add_widget(change)

        changing_personal_data.add_widget(layout)

    @staticmethod
    def build_invitations(screen):
        invitations = screen.manager.get_screen("invitations")
        invitations.__init__()

        to_main = Button(text="На главную")
        to_main.bind(on_press=invitations.to_main_on_press)
        back = Button(text="Назад")
        back.bind(on_press=invitations.back_on_press)

        upper_layout = BoxLayout(orientation="horizontal", size_hint=(1, 0.2))
        upper_layout.add_widget(to_main)
        upper_layout.add_widget(back)

        layout = BoxLayout(orientation="vertical")
        layout.add_widget(upper_layout)

        login = Configuration.read_login()
        invitation = Invitation_Queries.get_first_by_invited(login)
        if not invitation is None:
            Inviter_Label = Label(text="Вас пригласил")
            Family_Label = Label(text="В семью")
            Role_Label = Label(text="Ваша роль")
            labels_layout_1 = BoxLayout(orientation="horizontal", size_hint=(1, 0.2))
            labels_layout_1.add_widget(Inviter_Label)
            labels_layout_1.add_widget(Family_Label)
            labels_layout_1.add_widget(Role_Label)

            inviter = invitation.inviter
            family = invitation.family
            role = invitation.role
            Inviter = Label(text=inviter)
            Family = Label(text=family)
            Role = Label(text=ROLES_EN_RU[role])
            labels_layout_2 = BoxLayout(orientation="horizontal")
            labels_layout_2.Inviter = Inviter
            labels_layout_2.add_widget(labels_layout_2.Inviter)
            labels_layout_2.Family = Family
            labels_layout_2.add_widget(labels_layout_2.Family)
            labels_layout_2.Role = Role
            labels_layout_2.add_widget(labels_layout_2.Role)

            accept = Button(text="Принять")
            accept.bind(on_press=invitations.accept_on_press)
            decline = Button(text="Отклонить")
            decline.bind(on_press=invitations.decline_on_press)
            buttons_layout = BoxLayout(orientation="horizontal")
            buttons_layout.add_widget(accept)
            buttons_layout.add_widget(decline)

            layout.labels_layout_1 = labels_layout_1
            layout.add_widget(layout.labels_layout_1)
            layout.labels_layout_2 = labels_layout_2
            layout.add_widget(layout.labels_layout_2)
            layout.buttons_layout = buttons_layout
            layout.add_widget(layout.buttons_layout)

        invitations.layout = layout
        invitations.add_widget(invitations.layout)

    @staticmethod
    def build_viewing_events(screen):
        global events, current_event

        viewing_events = screen.manager.get_screen("viewing_events")
        viewing_events.__init__()

        to_main = Button(text="На главную")
        to_main.bind(on_press=viewing_events.to_main_on_press)
        back = Button(text="Назад")
        back.bind(on_press=viewing_events.back_on_press)

        upper_layout = BoxLayout(orientation="horizontal", size_hint=(1, 0.2))
        upper_layout.add_widget(to_main)
        upper_layout.add_widget(back)

        layout = BoxLayout(orientation="vertical")
        layout.add_widget(upper_layout)

        user = Configuration.read_login()
        events = Event_Queries.get_all_by_user(user)
        if events != []:
            date_label = Label(text="Дата")
            time_label = Label(text="Время")
            place_label = Label(text="Место")
            topic_label = Label(text="Тема")

            family_label = Label(text="Семья")
            creator_label = Label(text="Создатель")
            who_doesnt_participate_label = Label(text="Кто не участвует")
            notes_label = Label(text="Заметки")

            labels_layout_1 = BoxLayout(orientation="horizontal", size_hint=(1, 0.2))
            labels_layout_1.add_widget(date_label)
            labels_layout_1.add_widget(time_label)
            labels_layout_1.add_widget(place_label)
            labels_layout_1.add_widget(topic_label)
            labels_layout_1.add_widget(family_label)
            labels_layout_1.add_widget(creator_label)
            labels_layout_1.add_widget(who_doesnt_participate_label)
            labels_layout_1.add_widget(notes_label)

            viewing_events.date = Label(text=events[current_event].date)
            viewing_events.time = Label(text=events[current_event].time)
            viewing_events.place = Label(text=events[current_event].place)
            viewing_events.topic = Label(text=events[current_event].topic)

            viewing_events.family = Label(text=events[current_event].family)
            viewing_events.creator = Label(text=events[current_event].creator)
            viewing_events.who_doesnt_participate = Label(
                text=events[current_event].who_doesnt_participate
            )
            viewing_events.notes = Label(text=events[current_event].notes)

            labels_layout_2 = BoxLayout(orientation="horizontal")
            labels_layout_2.add_widget(viewing_events.date)
            labels_layout_2.add_widget(viewing_events.time)
            labels_layout_2.add_widget(viewing_events.place)
            labels_layout_2.add_widget(viewing_events.topic)
            labels_layout_2.add_widget(viewing_events.family)
            labels_layout_2.add_widget(viewing_events.creator)
            labels_layout_2.add_widget(viewing_events.who_doesnt_participate)
            labels_layout_2.add_widget(viewing_events.notes)

            previous = Button(
                text="Предыдущее", on_press=viewing_events.previous_on_press
            )
            change_status = Button(
                text="Сменить статус", on_press=viewing_events.change_status_on_press
            )
            next = Button(text="Следующее", on_press=viewing_events.next_on_press)

            buttons_layout = BoxLayout(orientation="horizontal")
            buttons_layout.add_widget(previous)
            buttons_layout.add_widget(change_status)
            buttons_layout.add_widget(next)

            layout.add_widget(labels_layout_1)
            layout.add_widget(labels_layout_2)
            layout.add_widget(buttons_layout)

        viewing_events.add_widget(layout)


class Validator:
    def validate_login(login):
        login = login.capitalize()

        if not login.isalnum():
            return False

        return True

    def validate_name(name):
        if name.isalpha():
            return True

        return False

    def validate_date_format(date):
        try:
            date = datetime.strptime(date, "%d.%m.%Y").date()

            return True
        except:
            return False

    def validate_date_value(date):
        date = datetime.strptime(date, "%d.%m.%Y").date()
        now = datetime.now().date()

        if date < now:
            return False

        return True

    def validate_time_format(time):
        try:
            time = datetime.strptime(time, "%H:%M").time()

            return True
        except:
            return False

    def validate_time_value(date, time):
        now = datetime.now()

        if date == now.date() and time <= now.time():
            return False

        return True


class Configuration:
    @classmethod
    def update(cls):
        try:
            login = cls.read_login()

            if login != "":
                password = cls.read_password()

                if not User_Queries.get(login, password) is None:
                    return True
                else:
                    cls.rewrite()
                    return False
        except:
            return False

    def rewrite():
        with open("configuration.txt", "w") as file:
            file.write("")

    def write_login_password(login, password):
        with open("configuration.txt", "w") as file:
            file.write(f"{login}\n{password}")

    def read_login():
        try:
            with open("configuration.txt", "r") as file:
                return file.read().split("\n")[0]
        except:
            return ""

    def read_password():
        try:
            with open("configuration.txt", "r") as file:
                return file.read().split("\n")[1]
        except:
            pass
