import datetime
from enum import unique

import numpy as np
import sqlalchemy
from asyncpg import UniqueViolationError
from sqlalchemy import literal_column, Float, func
from sqlalchemy.ext.mutable import MutableList

from .base import BaseModel
from sqlalchemy.exc import ProgrammingError, IntegrityError, SQLAlchemyError

from sqlalchemy import Column, String, Integer, VARCHAR, select,  ARRAY  # type: ignore

from sqlalchemy.orm import sessionmaker, relationship, selectinload, load_only  # type: ignore
from sqlalchemy import update
from aiogram import html


class User(BaseModel):
    __tablename__ = 'students'

    numer = Column(Integer, primary_key=True, autoincrement=True)


    student_id = Column(Integer,  nullable=False)

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
    st_answers90 = Column(VARCHAR(90), nullable=True)
    st_answers30 = Column(VARCHAR(30), nullable=True)

    ans_message = Column(String, nullable=True)
    st_score90 = Column(MutableList.as_mutable(ARRAY(Float)), nullable=True)
    st_score30 = Column(MutableList.as_mutable(ARRAY(Float)), nullable=True)
    n_test= Column(VARCHAR(2), nullable=False)


    # upd_date = Column(DATE, onupdate=datetime.date.today())

    def __str__(self) -> str:
        return f"Users:{self.student_id}>"


async def get_st_ids(user_id: int,group_name:str, session_maker: sessionmaker) -> User.student_id:
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
                    .filter(User.teacher_id == user_id, User.group_name==group_name)  # type: ignore
            )
            return result.scalars().all()

async def get_group_names(user_id: int, session_maker: sessionmaker) -> User.student_id:
    """
    Получить пользователя по его id
    :param user_id:
    :param session_maker:
    :return:
    """
    async with session_maker() as session:
        async with session.begin():
            result = await session.execute(
                select(User.group_name).distinct()
                    .filter(User.teacher_id == user_id)  # type: ignore
            )
            return result.scalars().all()
async def get_sub_names(user_id: int, session_maker: sessionmaker) -> User.student_id:
    """
    Получить пользователя по его id
    :param user_id:
    :param session_maker:
    :return:
    """
    async with session_maker() as session:
        async with session.begin():
            result = await session.execute(
                select(User.t_fullname)
                    .filter(User.student_id == user_id)  # type: ignore
            )
            return result.scalars().all()
async def get_stat(user_id: int, session_maker: sessionmaker):
    async with session_maker() as session:
        async with session.begin():
            result = await session.execute(func.avg(func.unnest(User.st_score90)).filter(User.teacher_id == user_id))

            return result.scalars().one()
async def get_st_datas(user_id: int,group_name:str, session_maker: sessionmaker) -> User.student_id:
    """
    Получить пользователя по его id
    :param user_id:
    :param session_maker:
    :return:
    """

    async with session_maker() as session:
        async with session.begin():
            result = await session.execute(
                select(User).options(load_only(User.teacher_subject,User.school_name, User.subject_1, User.subject_2))
                    .filter(User.teacher_id == user_id, User.group_name==group_name)  # type: ignore
            )
            return result.scalars().first()
async def get_st_dats(user_id: int, session_maker: sessionmaker,group_name:str):
    """
    Получить пользователя по его id
    :param user_id:
    :param session_maker:
    :return:
    """

    async with session_maker() as session:
        async with session.begin():
            if group_name:
                result = await session.execute(
                    select(User).options(
                        load_only(User.school_name, User.teacher_subject, User.region, User.t_fullname, User.district,
                                  User.subject_1, User.subject_2))
                    .filter(User.teacher_id == user_id, User.group_name == group_name)  # type: ignore
                )

            else:
                result = await session.execute(
                    select(User).options(
                        load_only(User.school_name, User.teacher_subject, User.region, User.t_fullname, User.district,
                                  User.subject_1, User.subject_2))
                    .filter(User.teacher_id == user_id))

            return result.scalars().first()




async def create_user(student_id: int,teacher_id: int, st_fullname:str, t_fullname:str, teacher_subject:str, school_name:str, subject_1:str, subject_2:str, district:str, region:str,group_name:str, session_maker: sessionmaker) -> None:
    async with session_maker() as session:
        async with session.begin():
            rest = await session.execute(
                select(User).where(User.student_id == student_id, User.teacher_subject == teacher_subject))
            bl = rest.one_or_none()

            if bl == None:
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
                    group_name=group_name,
                    n_test='00'

                )
                try:
                    session.add(user)
                except SQLAlchemyError:
                    print("Could not add student")
                    # assert isinstance(e.orig, UniqueViolationError)
            else:

                    await session.execute(update(User).values({'teacher_id': teacher_id,
                                                                'st_fullname': st_fullname,
                                                               't_fullname': t_fullname,

                                                               'school_name': school_name,
                                                               'subject_1': subject_1,
                                                               'subject_2': subject_2,
                                                               'district': district,
                                                               'region': region,
                                                               'group_name': group_name, }).where(
                        User.student_id == student_id, User.teacher_subject == teacher_subject))


async def add_answers(st_id:int,teacher_id:int,answers:str,test_type:str, session_maker: sessionmaker):
    if test_type == '30':
        varans = "st_answers30"
    else:
        varans = "st_answers90"

    async with session_maker() as session:


       async with session.begin():
           await session.execute(update(User).values({varans:answers}).where(User.student_id == st_id, User.teacher_id == teacher_id))

async def add_score(st_id:int,teacher_id:int,score:float, n:int,test_type:str, session_maker: sessionmaker):
    async with session_maker() as session:


       async with session.begin():
           result = await session.execute(
               select(User.n_test)
               .filter(User.student_id == st_id, User.teacher_id == teacher_id)  # type: ignore
           )
           n1 = result.scalars().one()
           if test_type == '90':
               try:
                   await session.execute(update(User).values({User.st_score90[n]: score}).where(User.student_id == st_id, User.teacher_id == teacher_id))

               except:
                   await session.execute(
                       update(User).values({'st_score90': literal_column(f"array_append(st_score90, {score})")}).where(
                           User.student_id == st_id, User.teacher_id == teacher_id))

               if n == 9:
                   n1= '0'+n1[1]
                   await session.execute(update(User).values({'n_test': n1}).where(User.student_id == st_id, User.teacher_id == teacher_id))
               else:
                   n=n+1
                   n1 =str(n)+n1[1]
                   await session.execute(update(User).values({'n_test': n1}).where(User.student_id == st_id, User.teacher_id == teacher_id))

               await session.execute(update(User).values({'st_answers90': '8'}).where(User.student_id == st_id, User.teacher_id == teacher_id))
           elif test_type == '30':
               try:
                   await session.execute(update(User).values({User.st_score30[n]: score}).where(User.student_id == st_id, User.teacher_id == teacher_id))

               except:
                   await session.execute(
                       update(User).values({'st_score30': literal_column(f"array_append(st_score30, {score})")}).where(
                           User.student_id == st_id, User.teacher_id == teacher_id))

               if n == 9:
                   n1 = n1[0]+'0'
                   await session.execute(update(User).values({'n_test': n1}).where(User.student_id == st_id, User.teacher_id == teacher_id))
               else:
                   n=n+1
                   n1 = n1[0]+str(n)
                   await session.execute(update(User).values({'n_test': n1}).where(User.student_id == st_id, User.teacher_id == teacher_id))

               await session.execute(update(User).values({'st_answers30': '8'}).where(User.student_id == st_id, User.teacher_id == teacher_id))






           # await session.execute(update(User).values({'st_score': literal_column("array_append(st_score, score)")}).where(User.student_id == st_id))

async def get_st_scores(user_id: int,group_name:str, test_type:str, session_maker: sessionmaker) -> User.student_id:
    """
    Получить пользователя по его id
    :param user_id:
    :param session_maker:
    :return:
    """

    async with session_maker() as session:
        async with session.begin():
            resut = await session.execute(
                select(User.st_fullname)
                .filter(User.teacher_id == user_id, User.group_name==group_name)  # type: ignore
            )


            if test_type == '90':
                result = await session.execute(
                    select(User.st_score90)
                    .filter(User.teacher_id == user_id, User.group_name == group_name)  # type: ignore
                )
                ball = '189.0 ball'
            else:
                result = await session.execute(
                    select(User.st_score30)
                    .filter(User.teacher_id == user_id, User.group_name == group_name)  # type: ignore
                )
                ball = '30 ta'
            try:
                names = resut.scalars().all()
                names = np.array(names)
                score = []

                for j in result.scalars().all():
                    if j == None:
                        score.append(0)
                    else:
                        score.append(np.average(j))

                score = np.array(score)
                idx = np.argsort(-score)
                score = np.array(score)[idx]
                names = np.array(names)[idx]
                text = ''
                emoji = '🥇🥈🥉'
                for i in range(len(score)):
                    if i in [0, 1, 2]:
                        text += f"\n{emoji[i]} {html.bold(html.quote(names[i]))} - {round(score[i], 1)}/{ball}"
                    else:
                        text += f"\n {i + 1}.  {html.bold(html.quote(names[i]))} - {round(score[i], 1)}/{ball} "



            except:
                name = resut.scalars().one()
                score=np.average(result.scalars().one())
                text = f"\n🥇 {html.bold(html.quote(name))} - {round(score, 1)}/{ball}"










            return text

async def get_st_answ(user_id: int,teacher_id:int,test_type:str, session_maker: sessionmaker):
    """
    Получить пользователя по его id
    :param user_id:
    :param session_maker:
    :return:
    """

    async with session_maker() as session:
        async with session.begin():
            if test_type == '90':
                result = await session.execute(
                    select(User).options(load_only(User.st_answers90, User.st_fullname, User.subject_1, User.subject_2))
                    .filter(User.student_id == user_id, User.teacher_id == teacher_id)  # type: ignore
                )
            elif test_type == '30':
                result = await session.execute(
                    select(User).options(load_only(User.st_answers30, User.st_fullname, User.subject_1, User.subject_2))
                    .filter(User.student_id == user_id, User.teacher_id == teacher_id)  # type: ignore
                )

            return result.scalars().one()
async def add_ans_message(user_id: int, teacher_id:int, message:str, session_maker: sessionmaker):
    async with session_maker() as session:


       async with session.begin():
           await session.execute(update(User).values({'ans_message':message}).where(User.student_id == user_id, User.teacher_id == teacher_id))
async def get_ans_message(user_id: int,subject:str, session_maker: sessionmaker):
    async with session_maker() as session:
        async with session.begin():
            try:
                result = await session.execute(
                    select(User.ans_message)
                    .filter(User.student_id == user_id, User.t_fullname==subject)  # type: ignore
                )
                return result.scalars().one()
            except:
                return "Test tekshirilgan"

# async def increase_n_test(user_id: int, session_maker: sessionmaker):
#     async with session_maker() as session:
#         async with session.begin():
#             result = await session.execute(
#                 select(User.n_test)
#                 .filter(User.student_id == user_id)  # type: ignore
#             )
#             result=result.scalars().one()
#             if result==9:
#                 await session.execute(update(User).values({'n_test': 0}).where(User.student_id == user_id))
#             else:
#                 await session.execute(update(User).values({'n_test': result+1}).where(User.student_id == user_id))
async def get_n_test(user_id: int,teacher_id:int, session_maker: sessionmaker):
    async with session_maker() as session:
        async with session.begin():
            result = await session.execute(
                select(User.n_test)
                    .filter(User.student_id == user_id, User.teacher_id == teacher_id)  # type: ignore
            )
            return result.scalars().one()

async def get_t_sub(user_id:int, session_maker: sessionmaker):
    async with session_maker() as session:
        async with session.begin():
            result = await session.execute(
                select(User.teacher_subject)
                    .filter(User.teacher_id == user_id)  # type: ignore
            )
            return result.scalars().first()