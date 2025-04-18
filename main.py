from kivy.core.window import Window
from kivy.app import App
from kivy.uix.screenmanager import ScreenManager

from auxiliary import Configuration
from screens import (
    User_Registration,
    User_Signing_In,
    Main,
    Changing_Personal_Data,
    Families,
    Invitations,
    Info_About_Users,
    Creating_Family,
    Inviting_User_Into_Family,
    Deleting_Family,
    Removing_User_From_Family,
    Events,
    Viewing_Events,
    Creating_Event,
    Deleting_Event,
    News,
)


class Application(App):
    def build(self):
        # Window.fullscreen = "auto"

        scr_manager = ScreenManager()
        scr_manager.add_widget(User_Registration(name="user_registration"))
        scr_manager.add_widget(User_Signing_In(name="user_signing_in"))
        scr_manager.add_widget(Main(name="main"))
        scr_manager.add_widget(Changing_Personal_Data(name="changing_personal_data"))
        scr_manager.add_widget(Families(name="families"))
        scr_manager.add_widget(Invitations(name="invitations"))
        scr_manager.add_widget(Info_About_Users(name="info_about_users"))
        scr_manager.add_widget(Creating_Family(name="creating_family"))
        scr_manager.add_widget(
            Inviting_User_Into_Family(name="inviting_user_into_family")
        )
        scr_manager.add_widget(Deleting_Family(name="deleting_family"))
        scr_manager.add_widget(
            Removing_User_From_Family(name="removing_user_from_family")
        )
        scr_manager.add_widget(Events(name="events"))
        scr_manager.add_widget(Viewing_Events(name="viewing_events"))
        scr_manager.add_widget(Creating_Event(name="creating_event"))
        scr_manager.add_widget(Deleting_Event(name="deleting_event"))
        scr_manager.add_widget(News(name="news"))

        if Configuration.update():
            scr_manager.current = "main"

        return scr_manager


if __name__ == "__main__":
    Application().run()
