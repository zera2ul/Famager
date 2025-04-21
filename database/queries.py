from datetime import datetime
from sqlalchemy import select, update
import requests
from bs4 import BeautifulSoup

try:
    from database.models import (
        session_maker,
        User,
        Family,
        Invitation,
        Event,
        News,
    )
except:
    from models import session_maker, Event, News


class User_Queries:
    def add(login, password, surname, name, fathername, birthday):
        login = login.capitalize()
        surname = surname.capitalize()
        name = name.capitalize()
        fathername = fathername.capitalize()

        with session_maker() as session:
            session.add(
                User(
                    login=login,
                    password=password,
                    surname=surname,
                    name=name,
                    fathername=fathername,
                    birthday=birthday,
                    wishlist="",
                )
            )

            session.commit()

    def change_data(
        old_user_data, login, password, surname, name, fathername, birthday, wishlist
    ):
        login = login.capitalize()
        surname = surname.capitalize()
        name = name.capitalize()
        fathername = fathername.capitalize()
        wishlist = wishlist.split("\n")
        for ind, el in enumerate(wishlist):
            wishlist[ind] = el.title()
        wishlist = "\n".join(wishlist)

        with session_maker() as session:
            session.execute(
                update(User)
                .where(User.id == old_user_data.id)
                .values(login=login)
                .values(password=password)
                .values(surname=surname)
                .values(name=name)
                .values(fathername=fathername)
                .values(birthday=birthday)
                .values(wishlist=wishlist)
            )

            session.commit()

    def get(*args):
        login = args[0].capitalize()

        if len(args) == 1:
            with session_maker() as session:
                user = session.scalar(select(User).where(User.login == login))

            return user
        else:
            with session_maker() as session:
                user = session.scalar(
                    select(User)
                    .where(User.login == login)
                    .where(User.password == args[1])
                )

            return user


class Family_Queries:
    def add(name, creator):
        name = name.capitalize()
        creator = creator.capitalize()

        with session_maker() as session:
            session.add(Family(name=name, users=f"{creator}:Creator\n"))

            session.commit()

    @classmethod
    def add_user(cls, name, creator, user, role):
        name = name.capitalize()
        creator = creator.capitalize()
        user = user.capitalize()

        with session_maker() as session:
            family = cls.get(name, creator)
            family.users += f"{user}:{role}\n"

            session.execute(
                update(Family).where(Family.id == family.id).values(users=family.users)
            )

            session.commit()

    def change_user_login(old_login, new_login):
        old_login = old_login.capitalize()
        new_login = new_login.capitalize()

        with session_maker() as session:
            families = session.scalars(select(Family))

            for it_1 in families:
                old_users = str(it_1.users).split("\n")
                new_users = []

                for it_2 in old_users:
                    user_info = it_2.split(":")

                    if user_info[0] == old_login:
                        new_users.append(f"{new_login}:{user_info[1]}")
                    else:
                        new_users.append(":".join(user_info))
                new_users = "\n".join(new_users)
                session.execute(
                    update(Family).where(Family.id == it_1.id).values(users=new_users)
                )

            session.commit()

    @classmethod
    def delete(cls, name, creator):
        name = name.capitalize()
        creator = creator.capitalize()

        with session_maker() as session:
            session.delete(cls.get(name, creator))

            session.commit()

    @classmethod
    def remove_user(cls, name, remover, user):
        name = name.capitalize()
        remover = remover.capitalize()
        user = user.capitalize()

        with session_maker() as session:
            family = cls.get_by_member(name, remover)
            old_users = family.users.split("\n")

            new_users = []
            for it in old_users:
                user_info = it.split(":")

                if user_info[0] != user:
                    new_users.append(it)
            new_users = "\n".join(new_users)
            session.execute(
                update(Family).where(Family.id == family.id).values(users=new_users)
            )

            session.commit()

    def get(name, creator):
        name = name.capitalize()
        creator = creator.capitalize()

        with session_maker() as session:
            families = session.scalars(select(Family))

            for family in families:
                if family.name == name:
                    users = str(family.users).split("\n")

                    for user in users:
                        if user.split(":")[0] == creator:
                            return family

            return None

    def get_all_by_user(user):
        user = user.capitalize()

        with session_maker() as session:
            families = session.scalars(select(Family))
            result = []

            for it_1 in families:
                users = str(it_1.users).split("\n")

                for it_2 in users:
                    if it_2.split(":")[0] == user:
                        result.append(it_1)

            return result

    def get_by_member(family, member):
        family = family.capitalize()
        member = member.capitalize()

        with session_maker() as session:
            families = session.scalars(select(Family).where(Family.name == family))

            for it_1 in families:
                members = str(it_1.users).split("\n")

                for it_2 in members:
                    member_info = it_2.split(":")

                    if member_info[0] == member:
                        return it_1

    def get_user_role(family, user):
        family = family.capitalize()
        user = user.capitalize()

        with session_maker() as session:
            families = session.scalars(select(Family).where(Family.name == family))

            for it_1 in families:
                users = (it_1.users).split("\n")

                for it_2 in users:
                    user_info = it_2.split(":")

                    if user_info[0] == user:
                        return user_info[1]

    def is_user_in_family(family, user):
        family = family.capitalize()
        user = user.capitalize()

        with session_maker() as session:
            families = session.scalars(select(Family).where(Family.name == family))

            for it_1 in families:
                users = (it_1.users).split("\n")

                for it_2 in users:
                    if it_2.split(":")[0] == user:
                        return True

            return False


class Invitation_Queries:
    def add(invited, inviter, family, role):
        invited = invited.capitalize()
        inviter = inviter.capitalize()
        family = family.capitalize()

        with session_maker() as session:
            session.add(
                Invitation(invited=invited, inviter=inviter, family=family, role=role)
            )

            session.commit()

    def change_user_login(old_login, new_login):
        old_login = old_login.capitalize()
        new_login = new_login.capitalize()

        with session_maker() as session:
            session.execute(
                update(Invitation)
                .where(Invitation.invited == old_login)
                .values(invited=new_login)
            )

            session.execute(
                update(Invitation)
                .where(Invitation.inviter == old_login)
                .values(inviter=new_login)
            )

            session.commit()

    @classmethod
    def delete(cls, invited, inviter, family):
        invited = invited.capitalize()
        inviter = inviter.capitalize()
        family = family.capitalize()

        with session_maker() as session:
            session.delete(cls.get(invited, inviter, family))

            session.commit()

    def get(invited, inviter, family):
        invited = invited.capitalize()
        inviter = inviter.capitalize()
        family = family.capitalize()

        with session_maker() as session:
            return session.scalar(
                select(Invitation)
                .where(Invitation.invited == invited)
                .where(Invitation.inviter == inviter)
                .where(Invitation.family == family)
            )

    def get_first_by_invited(invited):
        invited = invited.capitalize()

        with session_maker() as session:
            return session.scalar(
                select(Invitation).where(Invitation.invited == invited).limit(1)
            )

    def is_user_invited_in_family(user, family):
        user = user.capitalize()
        family = family.capitalize()

        with session_maker() as session:
            invitations = session.scalars(
                select(Invitation)
                .where(Invitation.invited == user)
                .where(Invitation.family == family)
            )

            if len(list(invitations)) == 1:
                return True

            return False


class Event_Queries:
    def update():
        now = datetime.now().date()

        with session_maker() as session:
            events = session.scalars(select(Event))

            for it in events:
                date = datetime.strptime(it.date, "%d.%m.%Y").date()

                if date < now:
                    session.delete(it)

            session.commit()

    def add(date, time, place, topic, family, creator, notes):
        place = place.capitalize()
        topic = topic.capitalize()
        family = family.capitalize()
        creator = creator.capitalize()
        notes = notes.capitalize()

        with session_maker() as session:
            session.add(
                Event(
                    date=date,
                    time=time,
                    place=place,
                    topic=topic,
                    who_doesnt_participate="",
                    family=family,
                    creator=creator,
                    notes=notes,
                )
            )

            session.commit()

    def change_user_login(old_login, new_login):
        old_login = old_login.capitalize()
        new_login = new_login.capitalize()

        with session_maker() as session:
            session.execute(
                update(Event)
                .where(Event.creator == old_login)
                .values(creator=new_login)
            )

            session.commit()

    @classmethod
    def update_who_doesnt_participate(cls, date, topic, family, user):
        topic = topic.capitalize()
        family = family.capitalize()
        user = user.capitalize()

        with session_maker() as session:
            event = cls.get_by_participant(date, topic, family, user)
            who_doesnt_participate = str(event.who_doesnt_participate).split("\n")

            user_doesnt_participate = False
            for ind, el in enumerate(who_doesnt_participate):
                if el == user:
                    user_doesnt_participate = True
                    del who_doesnt_participate[ind]
                    break

        if user_doesnt_participate is False:
            who_doesnt_participate.append(user)

        who_doesnt_participate = "\n".join(who_doesnt_participate)
        session.execute(
            update(Event)
            .where(Event.id == event.id)
            .values(who_doesnt_participate=who_doesnt_participate)
        )

        session.commit()

    @classmethod
    def delete(cls, date, topic, family, creator):
        date = date.capitalize()
        topic = topic.capitalize()
        family = family.capitalize()
        creator = creator.capitalize()

        with session_maker() as session:
            session.delete(cls.get(date, topic, family, creator))

            session.commit()

    @classmethod
    def delete_by_family(cls, family, creator):
        family = family.capitalize()
        creator = creator.capitalize()

        with session_maker() as session:
            events = cls.get_all_by_family(family, creator)

            for it in events:
                session.delete(it)

            session.commit()

    @classmethod
    def delete_by_participant(cls, date, topic, family, participant):
        date = date.capitalize()
        topic = topic.capitalize()
        family = family.capitalize()
        participant = participant.capitalize()

        with session_maker() as session:
            session.delete(cls.get_by_participant(date, topic, family, participant))

            session.commit()

    def get(date, topic, family, creator):
        date = date.capitalize()
        topic = topic.capitalize()
        family = family.capitalize()
        creator = creator.capitalize()

        with session_maker() as session:
            events = session.scalars(select(Event))

            for it in events:
                if (
                    it.date == date
                    and it.topic == topic
                    and it.family == family
                    and it.creator == creator
                ):
                    return it

            return None

    def get_all_by_family(family, creator):
        family = family.capitalize()
        creator = creator.capitalize()

        with session_maker() as session:
            events = session.scalars(
                select(Event)
                .where(Event.family == family)
                .where(Event.creator == creator)
            )

            return events

    def compare(event):
        return (
            datetime.strptime(event.date, "%d.%m.%Y").date(),
            datetime.strptime(event.time, "%H:%M").time(),
        )

    @classmethod
    def get_all_by_user(cls, user):
        user = user.capitalize()

        with session_maker() as session:
            events = session.scalars(select(Event))
            families = Family_Queries.get_all_by_user(user)
            result = []

            for it_1 in events:
                for it_2 in families:
                    if (
                        Family_Queries.get_by_member(it_1.family, it_1.creator).id
                        == it_2.id
                    ):
                        result.append(it_1)

            result.sort(key=cls.compare)

            return result

    def get_by_participant(date, topic, family, participant):
        date = date.capitalize()
        topic = topic.capitalize()
        family = family.capitalize()
        participant = participant.capitalize()

        with session_maker() as session:
            events = session.scalars(select(Event))
            family_id = Family_Queries.get_by_member(family, participant).id

            for it in events:
                if (
                    it.date == date
                    and it.topic == topic
                    and it.family == family
                    and Family_Queries.get_by_member(family, it.creator).id == family_id
                ):
                    return it

            return None


class News_Queries:
    @classmethod
    def update(cls):
        soup = BeautifulSoup(
            requests.get(
                "https://pravo.by/novosti/novosti-po-tegu/?tag=%D0%B1%D1%80%D0%B0%D1%87%D0%BD%D0%BE-%D1%81%D0%B5%D0%BC%D0%B5%D0%B9%D0%BD%D1%8B%D0%B5%20%D0%BE%D1%82%D0%BD%D0%BE%D1%88%D0%B5%D0%BD%D0%B8%D1%8F",
                headers={
                    "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36"
                },
            ).text,
            "html.parser",
        )

        items = soup.find_all("a", class_="news__item", limit=5)
        for it in items:
            topic = str(it.text).strip()
            topic = topic[: len(topic) - 10]
            link = it["href"]

            cls.add(topic, link)

    def add(topic, link):
        with session_maker() as session:
            session.add(News(topic=topic, link=link))

            session.commit()

    def get_all():
        with session_maker() as session:
            news = session.scalars(select(News))

            news_dict = {}
            for it in news:
                news_dict[it.topic] = it.link

            return news_dict
