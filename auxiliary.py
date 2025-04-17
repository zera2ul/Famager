from datetime import datetime
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.label import Label
from kivy.uix.button import Button
from kivy.uix.textinput import TextInput
from kivy.uix.popup import Popup

from globals import ROLES_EN_RU, events, current_event
from database.queries import User_Queries, Invitation_Queries, Event_Queries


class Centered_Text_Input(TextInput):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)

        self.multiline = False
        self.halign = "center"
        self.bind(height=self.center_text)

    def center_text(screen, self, height):
        self.padding = [0, (height - self.line_height) / 2]


class Centered_Label(Label):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)

        self.halign = "center"
        self.valign = "middle"
        self.bind(width=self.center_text)

    def center_text(self, instance, width):
        self.setter("text_size")(self, (self.width, None))


class Centered_Button(Button):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)

        self.halign = "center"
        self.valign = "middle"
        self.bind(width=self.center_text, text=self.center_text)

    def center_text(self, *args):
        args[0].text_size = (args[0].width, None)
        args[0].height = args[0].texture_size[0] + 20


class Message_Box:
    @classmethod
    def create_warning(cls, screen, text):
        message = Centered_Label(text=text)
        message.bind(width=cls.message_width)
        close = Button(
            text="Закрыть", on_press=screen.close_on_press, size_hint=(1, 0.2)
        )

        content = BoxLayout(orientation="vertical")
        content.add_widget(message)
        content.add_widget(close)

        warning = Popup(
            title="Предупреждение",
            content=content,
            title_align="center",
            size_hint=(0.75, 0.75),
            pos_hint={"center_x": 0.5, "center_y": 0.5},
        )

        return warning

    @classmethod
    def create_info(cls, screen, text):
        message = Centered_Label(text=text)
        message.bind(width=cls.message_width)
        close = Button(
            text="Закрыть", on_press=screen.close_on_press, size_hint=(1, 0.2)
        )

        content = BoxLayout(orientation="vertical")
        content.add_widget(message)
        content.add_widget(close)

        info = Popup(
            title="Информация",
            title_align="center",
        )
        info.content = content

        return info

    def message_width(self, instance):
        self.setter("text_size")(self, (self.width, None))


class Screens_Builder:
    @staticmethod
    def build_changing_personal_data(screen):
        changing_personal_data = screen.manager.get_screen("changing_personal_data")
        changing_personal_data.__init__()

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
        layout.add_widget(
            Button(
                text="На главную",
                on_press=changing_personal_data.to_main_on_press,
                size_hint=(1, 0.2),
            )
        )
        layout.add_widget(center_layout)
        layout.add_widget(change)

        changing_personal_data.add_widget(layout)

    @staticmethod
    def build_invitations(screen):
        invitations = screen.manager.get_screen("invitations")
        invitations.__init__()

        upper_layout = BoxLayout(orientation="horizontal", size_hint=(1, 0.2))
        upper_layout.add_widget(
            Button(text="На главную", on_press=invitations.to_main_on_press)
        )
        upper_layout.add_widget(
            Button(text="Назад", on_press=invitations.back_on_press)
        )

        layout = BoxLayout(orientation="vertical")
        layout.add_widget(upper_layout)

        login = Configuration.read_login()
        invitation = Invitation_Queries.get_first_by_invited(login)
        if not invitation is None:
            labels_layout_1 = BoxLayout(orientation="horizontal", size_hint=(1, 0.2))
            labels_layout_1.add_widget(Label(text="Вас пригласил"))
            labels_layout_1.add_widget(Label(text="В семью"))
            labels_layout_1.add_widget(Label(text="Ваша роль"))

            inviter = invitation.inviter
            family = invitation.family
            role = invitation.role
            invitations.Inviter = Label(text=inviter)
            invitations.Family = Label(text=family)
            invitations.Role = Label(text=ROLES_EN_RU[role])

            labels_layout_2 = BoxLayout(orientation="horizontal")
            labels_layout_2.add_widget(invitations.Inviter)
            labels_layout_2.add_widget(invitations.Family)
            labels_layout_2.add_widget(invitations.Role)

            accept = Button(text="Принять", on_press=invitations.accept_on_press)
            decline = Button(text="Отклонить", on_press=invitations.decline_on_press)

            buttons_layout = BoxLayout(orientation="horizontal")
            buttons_layout.add_widget(accept)
            buttons_layout.add_widget(decline)

            layout.add_widget(labels_layout_1)
            layout.add_widget(labels_layout_2)
            layout.add_widget(buttons_layout)

        invitations.add_widget(layout)

    @classmethod
    def build_viewing_events(cls, screen):
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
            date_label = Label(
                text="Дата",
                halign="center",
                valign="middle",
                font_size="10sp",
            )
            date_label.bind(width=cls.message_width)
            time_label = Label(
                text="Время",
                halign="center",
                valign="middle",
                font_size="10sp",
            )
            time_label.bind(width=cls.message_width)
            place_label = Label(
                text="Место",
                halign="center",
                valign="middle",
                font_size="10sp",
            )
            place_label.bind(width=cls.message_width)
            topic_label = Label(
                text="Тема",
                halign="center",
                valign="middle",
                font_size="10sp",
            )
            topic_label.bind(width=cls.message_width)
            family_label = Label(
                text="Семья",
                halign="center",
                font_size="10sp",
            )
            family_label.bind(width=cls.message_width)
            creator_label = Label(
                text="Создатель",
                halign="center",
                valign="middle",
                font_size="10sp",
            )
            creator_label.bind(width=cls.message_width)
            who_doesnt_participate_label = Label(
                text="Кто\nне участвует",
                halign="center",
                valign="middle",
                font_size="10sp",
            )
            who_doesnt_participate_label.bind(width=cls.message_width)
            notes_label = Label(
                text="Заметки",
                halign="center",
                valign="middle",
                font_size="10sp",
            )
            notes_label.bind(width=cls.message_width)

            labels_layout_1 = BoxLayout(orientation="horizontal", size_hint=(1, 0.2))
            labels_layout_1.add_widget(date_label)
            labels_layout_1.add_widget(time_label)
            labels_layout_1.add_widget(place_label)
            labels_layout_1.add_widget(topic_label)
            labels_layout_1.add_widget(family_label)
            labels_layout_1.add_widget(creator_label)
            labels_layout_1.add_widget(who_doesnt_participate_label)
            labels_layout_1.add_widget(notes_label)

            viewing_events.date = Label(
                text=events[current_event].date,
                halign="center",
                valign="middle",
                font_size="10sp",
            )
            viewing_events.date.bind(width=cls.message_width)
            viewing_events.time = Label(
                text=events[current_event].time,
                halign="center",
                valign="middle",
                font_size="10sp",
            )
            viewing_events.time.bind(width=cls.message_width)
            viewing_events.place = Label(
                text=events[current_event].place,
                halign="center",
                valign="middle",
                font_size="10sp",
            )
            viewing_events.place.bind(width=cls.message_width)
            viewing_events.topic = Label(
                text=events[current_event].topic,
                halign="center",
                valign="middle",
                font_size="10sp",
            )
            viewing_events.topic.bind(width=cls.message_width)
            viewing_events.family = Label(
                text=events[current_event].family,
                halign="center",
                valign="middle",
                font_size="10sp",
            )
            viewing_events.family.bind(width=cls.message_width)
            viewing_events.creator = Label(
                text=events[current_event].creator,
                halign="center",
                valign="middle",
                font_size="10sp",
            )
            viewing_events.creator.bind(width=cls.message_width)
            viewing_events.who_doesnt_participate = Label(
                text=events[current_event].who_doesnt_participate,
                halign="center",
                valign="middle",
                font_size="10sp",
            )
            viewing_events.who_doesnt_participate.bind(width=cls.message_width)
            viewing_events.notes = Label(
                text=events[current_event].notes,
                halign="center",
                valign="middle",
                font_size="10sp",
            )
            viewing_events.notes.bind(width=cls.message_width)

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
