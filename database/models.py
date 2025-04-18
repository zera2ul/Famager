from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker, DeclarativeBase, Mapped, mapped_column

try:
    from database.configuration import DATABASE_URL
except:
    from configuration import DATABASE_URL

engine = create_engine(url=DATABASE_URL)
session_maker = sessionmaker(engine)


class Base(DeclarativeBase):
    @classmethod
    def delete_models(cls):
        cls.metadata.drop_all(engine)

    @classmethod
    def create_models(cls):
        cls.metadata.create_all(engine)


class User(Base):
    __tablename__ = "users"

    id: Mapped[int] = mapped_column(primary_key=True)
    login: Mapped[str] = mapped_column()
    password: Mapped[str] = mapped_column()
    surname: Mapped[str] = mapped_column()
    name: Mapped[str] = mapped_column()
    fathername: Mapped[str] = mapped_column()
    birthday: Mapped[str] = mapped_column()
    wishlist: Mapped[str] = mapped_column()


class Family(Base):
    __tablename__ = "families"

    id: Mapped[int] = mapped_column(primary_key=True)
    name: Mapped[str] = mapped_column()
    users: Mapped[str] = mapped_column()


class Invitation(Base):
    __tablename__ = "invitations"

    id: Mapped[int] = mapped_column(primary_key=True)
    invited: Mapped[str] = mapped_column()
    inviter: Mapped[str] = mapped_column()
    family: Mapped[str] = mapped_column()
    role: Mapped[str] = mapped_column()


class Event(Base):
    __tablename__ = "events"

    id: Mapped[int] = mapped_column(primary_key=True)
    date: Mapped[str] = mapped_column()
    time: Mapped[str] = mapped_column()
    place: Mapped[str] = mapped_column()
    topic: Mapped[str] = mapped_column()
    who_doesnt_participate: Mapped[str] = mapped_column()
    family: Mapped[str] = mapped_column()
    creator: Mapped[str] = mapped_column()
    notes: Mapped[str] = mapped_column()


class News(Base):
    __tablename__ = "news"

    id: Mapped[int] = mapped_column(primary_key=True)
    topic: Mapped[str] = mapped_column()
    link: Mapped[str] = mapped_column()
