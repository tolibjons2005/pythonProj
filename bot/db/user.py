import datetime
from enum import unique

import sqlalchemy
from asyncpg import UniqueViolationError
from sqlalchemy import Column, Integer, VARCHAR, DATE, null
from .base import BaseModel
from sqlalchemy.exc import ProgrammingError, IntegrityError, SQLAlchemyError

from sqlalchemy import Column, Integer, VARCHAR, select, BigInteger, Enum  # type: ignore

from sqlalchemy.orm import sessionmaker, relationship, selectinload, load_only  # type: ignore
from sqlalchemy import update


class User(BaseModel):
    __tablename__ = 'students'


    student_id = Column(Integer, unique=True, nullable=False, primary_key=True)

    teacher_id = Column(Integer, nullable=False)

    st_fullname = Column(VARCHAR(30),  nullable=False)

    t_fullname = Column(VARCHAR(30), nullable=False)

    teacher_subject = Column(VARCHAR(30), nullable=False)

    school_name = Column(VARCHAR(60), nullable=False)

    subject_1 = Column(VARCHAR(28), nullable=False)

    subject_2 = Column(VARCHAR(28), nullable=False)

    district = Column(VARCHAR(30),  nullable=False)

    region = Column(VARCHAR(30),  nullable=False)
    group_name = Column(VARCHAR(30), nullable=False)
    st_answers = Column(VARCHAR(90), nullable=True)

    # upd_date = Column(DATE, onupdate=datetime.date.today())

    def __str__(self) -> str:
        return f"Users:{self.student_id}>"


async def get_st_ids(user_id: int, session_maker: sessionmaker) -> User.student_id:
    """
    Получить пользователя по его id
    :param user_id:
    :param session_maker:
    :return:
    """
    async with session_maker() as session:
        async with session.begin():
            result = await session.execute(
                select(User).options(load_only(User.student_id, User.st_fullname))
                    .filter(User.teacher_id == user_id)  # type: ignore
            )
            return result.scalars().all()

async def get_st_datas(user_id: int, session_maker: sessionmaker) -> User.student_id:
    """
    Получить пользователя по его id
    :param user_id:
    :param session_maker:
    :return:
    """

    async with session_maker() as session:
        async with session.begin():
            result = await session.execute(
                select(User).options(load_only(User.school_name, User.subject_1, User.subject_2, User.group_name))
                    .filter(User.teacher_id == user_id)  # type: ignore
            )
            return result.scalars().first()


async def create_user(student_id: int,teacher_id: int, st_fullname:str, t_fullname:str, teacher_subject:str, school_name:str, subject_1:str, subject_2:str, district:str, region:str,group_name:str, session_maker: sessionmaker) -> None:
    async with session_maker() as session:

       try:
           async with session.begin():

               user = User(
                   student_id=student_id,
                   teacher_id=teacher_id,
                   st_fullname=st_fullname,
                   t_fullname=t_fullname,
                   teacher_subject=teacher_subject,
                   school_name=school_name,
                   subject_1=subject_1,
                   subject_2=subject_2,
                   district=district,
                   region=region,
                   group_name=group_name

               )
               try:
                   session.add(user)
               except SQLAlchemyError:
                   print("Could not add student")
                   # assert isinstance(e.orig, UniqueViolationError)
       except:
           async with session.begin():
               await session.execute(update(User).values({'teacher_id': teacher_id,
                                                          'st_fullname': st_fullname,
                                                          't_fullname': t_fullname,
                                                          'teacher_subject': teacher_subject,
                                                          'school_name': school_name,
                                                          'subject_1': subject_1,
                                                          'subject_2': subject_2,
                                                          'district': district,
                                                          'region': region,
                                                          'group_name': group_name}).where(
                   User.student_id == student_id))

async def add_answers(st_id:int,answers:str, session_maker: sessionmaker):
    async with session_maker() as session:


       async with session.begin():
           await session.execute(update(User).values({'st_answers':answers}).where(User.student_id == st_id))

async def get_st_answ(user_id: int, session_maker: sessionmaker) -> User.student_id:
    """
    Получить пользователя по его id
    :param user_id:
    :param session_maker:
    :return:
    """

    async with session_maker() as session:
        async with session.begin():
            result = await session.execute(
                select(User.st_answers)
                    .filter(User.student_id == user_id)  # type: ignore
            )
            return result.scalars().one()