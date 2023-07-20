import datetime
from enum import unique

import numpy as np
import sqlalchemy
from asyncpg import UniqueViolationError
from sqlalchemy import literal_column, Float, func, bindparam
from sqlalchemy.ext.mutable import MutableList

from .base import BaseModel
from sqlalchemy.exc import ProgrammingError, IntegrityError, SQLAlchemyError

from sqlalchemy import Boolean,DateTime,Column, String, Integer, VARCHAR, select,  ARRAY, BigInteger,delete, JSON,insert  # type: ignore

from sqlalchemy.orm import sessionmaker, relationship, selectinload, load_only  # type: ignore
from sqlalchemy import update
from aiogram import html
from sqlalchemy.sql.expression import text


class User(BaseModel):
    __tablename__ = 'students'

    numer = Column(Integer, primary_key=True, autoincrement=True)


    student_id = Column(BigInteger,  nullable=True)

    teacher_id = Column(BigInteger, nullable=True)

    st_fullname = Column(VARCHAR(25),  nullable=True)

    t_fullname = Column(VARCHAR(30), nullable=True)

    teacher_subject = Column(VARCHAR(30), nullable=True)

    school_name = Column(VARCHAR(60), nullable=True)

    subject_1 = Column(VARCHAR(28), nullable=True)

    subject_2 = Column(VARCHAR(28), nullable=True)

    district = Column(VARCHAR(30),  nullable=True)

    region = Column(VARCHAR(30),  nullable=True)
    group_name = Column(VARCHAR(25), nullable=True)
    st_answers90 = Column(VARCHAR(90), nullable=True)
    st_answers30 = Column(VARCHAR(30), nullable=True)


    ans_message = Column(String, nullable=True)
    st_score90 = Column(MutableList.as_mutable(ARRAY(Float)), nullable=True)
    st_score30 = Column(MutableList.as_mutable(ARRAY(Float)), nullable=True)
    n_test= Column(VARCHAR(2), nullable=True)
    is_active = Column(Boolean, default=True)


    # upd_date = Column(DATE, onupdate=datetime.date.today())

    def __str__(self) -> str:
        return f"Users:{self.student_id}>"

class IsPremium(BaseModel):
    __tablename__ = 'ispremium'

    numer = Column(Integer, primary_key=True, autoincrement=True)


    teacher_id = Column(BigInteger,  nullable=False)
    is_premium = Column(Boolean, default=False)
    expire_date = Column(DateTime, server_default=func.now(), index=True, nullable=True)




    # upd_date = Column(DATE, onupdate=datetime.date.today())

    def __str__(self) -> str:
        return f"Users:{self.user_id}>"

class StarterDB(BaseModel):
    __tablename__ = 'starterdb'

    numer = Column(Integer, primary_key=True, autoincrement=True)


    user_id = Column(BigInteger,  nullable=False)
    user_fullname = Column(VARCHAR(30), nullable=True)
    user_uname = Column(VARCHAR(30), nullable=True)






    # upd_date = Column(DATE, onupdate=datetime.date.today())

    def __str__(self) -> str:
        return f"Users:{self.user_id}>"

class DbForOnlineTest(BaseModel):
    __tablename__ = 'onlinetestdb'

    numer = Column(Integer, primary_key=True, autoincrement=True)


    teacher_id = Column(BigInteger,  nullable=True)
    st_answers90 = Column(VARCHAR(90), nullable=True)
    st_answers30 = Column(VARCHAR(30), nullable=True)
    subject_1 = Column(VARCHAR(28), nullable=True)

    subject_2 = Column(VARCHAR(28), nullable=True)
    expire_date = Column(DateTime, server_default=func.now(), index=True, nullable=True)
    data = Column(JSON, nullable=True)
    def __str__(self) -> str:
        return f"Users:{self.teacher_id}>"


class IsUsedDB(BaseModel):
    __tablename__ = 'isuseddb'
    numer = Column(Integer, primary_key=True, autoincrement=True)


    teacher_id = Column(BigInteger,  nullable=True)
    is_used_online = Column(Boolean, default=False)



    # upd_date = Column(DATE, onupdate=datetime.date.today())

    def __str__(self) -> str:
        return f"Users:{self.teacher_id}>"

async def change_is_used(teacher_id:int,session_maker:sessionmaker):
    async with session_maker() as session:
        async with session.begin():
            await session.execute(update(IsUsedDB).values(
                {'is_used_online': True}).where(
                (IsUsedDB.teacher_id==teacher_id)))
async def is_used_checker(teacher_id:int,session_maker:sessionmaker):
    async with session_maker() as session:
        async with session.begin():
            users = await session.execute(
                select(IsUsedDB.is_used_online).where(IsUsedDB.teacher_id == teacher_id))
            teacher = users.scalars().first()
            if teacher==None:
                user = IsUsedDB(
                    teacher_id=teacher_id,
                    is_used_online=False

                )
                session.add(user)
                return False
            else:
                return teacher











async def get_online_stats(teacher_id:int,session_maker:sessionmaker):
    async with session_maker() as session:
        async with session.begin():


            users=await session.execute(
                    select(DbForOnlineTest.data).where(DbForOnlineTest.teacher_id==teacher_id))
            students=users.scalars().first()
            rest = await session.execute(
                select(IsPremium).where(IsPremium.teacher_id == teacher_id, IsPremium.is_premium == True))
            bl = rest.one_or_none()
            if students ==None or students=={}:
                return 2
            elif bl == None:
                return 1
            else:
                user_list = [(key, *value.split("%")) for key, value in students.items()]

                sorted_users = sorted(user_list, key=lambda x: (-float(x[1]), x[3]))

                return sorted_users



async def register_student_fof(student_id:int,st_fullname:str, session_maker:sessionmaker):
    async with session_maker() as session:
        async with session.begin():
            user = User(
                teacher_id=5,
                student_id=student_id,
                st_fullname=st_fullname


            )
            session.add(user)

async def can_i_use(teacher_id:int,test_type:str,session_maker:sessionmaker):
    async with session_maker() as session:
        async with session.begin():
            if test_type == '90':
                rest = await session.execute(
                    select(DbForOnlineTest.st_answers90, DbForOnlineTest.data).where(DbForOnlineTest.teacher_id==teacher_id))
                bl=rest.one_or_none()

                if bl.st_answers90 == None:
                    return False, bl.data
                else:
                    return True, bl.data
            else:
                rest = await session.execute(
                    select(DbForOnlineTest.st_answers30, DbForOnlineTest.data).where(DbForOnlineTest.teacher_id == teacher_id))

                bl = rest.one_or_none()
                print(bl.data)

                if bl.st_answers30 == None:

                    return False, bl.data
                else:
                    return True, bl.data


async def is_registered(student_id:int,session_maker:sessionmaker):
    async with session_maker() as session:
        async with session.begin():
            rest = await session.execute(
                select(User.teacher_id).where(User.student_id == student_id).order_by(User.numer.desc()))

            bl=rest.scalars().first()

            if bl!=None and bl >0:
                print(bl)
                return 2
            elif bl!=None and bl==0:
                return 1
            else:
                return 0


async def get_schname_tsub(teacher_id:int, session_maker: sessionmaker):
    async with session_maker() as session:
        async with session.begin():
            result = await session.execute(
                select(User).options(load_only(User.school_name, User.teacher_subject))
                    .filter(User.teacher_id == teacher_id)  # type: ignore
            )
            return result.scalars().first()
async def get_answers_oo(teacher_id:int,test_type:str, session_maker:sessionmaker, student_id:int):
    datNow = datetime.datetime.now()
    async with session_maker() as session:
        async with session.begin():
            ti_res=await session.execute(
                select(User).where(User.student_id == student_id).order_by(User.numer.desc()))
            tid_res = ti_res.scalars().first()
            if tid_res.teacher_id <6:
                n=tid_res.teacher_id-1
                await session.execute(update(User).values(
                    {'teacher_id': n}).where(
                    User.student_id== student_id))


            if test_type == '90':
                result = await session.execute(
                    select(DbForOnlineTest).options(load_only(DbForOnlineTest.st_answers90,  DbForOnlineTest.subject_1, DbForOnlineTest.subject_2, DbForOnlineTest.data, ))
                    .filter(DbForOnlineTest.teacher_id == teacher_id,DbForOnlineTest.expire_date>datNow)  # type: ignore
                )
            elif test_type == '30':
                result = await session.execute(
                    select(DbForOnlineTest).options(load_only(DbForOnlineTest.st_answers30,DbForOnlineTest.data))
                    .filter(DbForOnlineTest.teacher_id == teacher_id,DbForOnlineTest.expire_date>datNow)  # type: ignore
                )

            return result.scalars().one(), tid_res.st_fullname
async def add_to_ONLINE(teacher_id:int,answer:str, expire_date:list,session_maker:sessionmaker,subject_1=None,subject_2=None):
    async with session_maker() as session:
        async with session.begin():
            if expire_date[0]==0 and expire_date[1]==0:
                expd = datetime.datetime.now() + datetime.timedelta(days=365)

                epd=None
            else:
                expd=datetime.datetime.now()+datetime.timedelta(hours=expire_date[0], minutes=expire_date[1])
                epd=expd.strftime("%c")

            rest = await session.execute(
                select(DbForOnlineTest).where(DbForOnlineTest.teacher_id == teacher_id))
            bl = rest.one_or_none()

            if bl == None:
                if len(answer)==90:
                    user = DbForOnlineTest(
                        teacher_id=teacher_id,
                        st_answers90= answer,
                        expire_date=expd,
                        subject_1=subject_1,
                        subject_2=subject_2


                    )
                    session.add(user)
                else:
                    user = DbForOnlineTest(
                        teacher_id=teacher_id,
                        st_answers30=answer,
                        expire_date=expd

                    )
                    session.add(user)
            else:
                if len(answer)==90:
                    await session.execute(update(DbForOnlineTest).values({'st_answers90': answer, 'st_answers30': None,"expire_date":expd, "subject_1": subject_1, "subject_2":subject_2, "data":{}}).where(DbForOnlineTest.teacher_id == teacher_id))
                else:
                    await session.execute(update(DbForOnlineTest).values({'st_answers30': answer, 'st_answers90': None,"expire_date":expd, "data":{}}).where(
                        DbForOnlineTest.teacher_id == teacher_id))
            return epd





async def add_to_dict(teacher_id:int,st_id:int,score:str,session_maker:sessionmaker):
    async with session_maker() as session:
        async with session.begin():

            row = await session.execute(select(DbForOnlineTest).where(DbForOnlineTest.teacher_id == teacher_id))
            my_table = row.scalar_one()

            # Modify the JSONB data
            data = my_table.data or {}
            print(len(data))
            data[f'{st_id}'] = score

            # Update the row with the modified JSONB data
            await session.execute(update(DbForOnlineTest).where(DbForOnlineTest.teacher_id == teacher_id).values(data=data))



async def wr_starter_db(user_id:int, session_maker:sessionmaker,user_fullname=None, user_uname=None ):
    async with session_maker() as session:
        async with session.begin():

            rest = await session.execute(
                select(StarterDB).where(StarterDB.user_id == user_id))
            bl = rest.scalars().first()

            if bl == None:
                user = StarterDB(

                    user_id=user_id,
                    user_fullname=user_fullname,
                    user_uname=user_uname

                )

                session.add(user)
            else:

                await session.execute(update(StarterDB).values({'user_fullname':user_fullname,
                                                           'user_uname':user_uname}).where(
                   StarterDB.user_id ==user_id))


async def is_group_active(user_id:int, group_name:str, session_maker:sessionmaker):
    async with session_maker() as session:
        async with session.begin():
            rest = await session.execute(select(User.student_id).where(User.teacher_id == user_id, User.group_name==group_name,  User.is_active == False))
            rest2 = await session.execute(select(User.student_id).where(User.teacher_id == user_id, User.group_name == group_name))
            if len(rest.scalars().all()) == len(rest2.scalars().all()):
                return False
            else:
                return True


async def premium_checker(user_id:int, session_maker: sessionmaker):
    async with session_maker() as session:
        async with session.begin():

            rest = await session.execute(
                select(IsPremium).where(IsPremium.teacher_id == user_id, IsPremium.is_premium == True))
            bl = rest.one_or_none()
            if bl != None:
                return True
            return False
async def expire_date(teacher_id:int, premium_type:int,session_maker:sessionmaker):
    async with session_maker() as session:
        async with session.begin():

            expire_dat = datetime.datetime.now()+datetime.timedelta(days=premium_type)
            rest = await session.execute(
                select(IsPremium).where(IsPremium.teacher_id == teacher_id))
            bl = rest.scalars().first()


            if bl == None:
                user = IsPremium(

                    teacher_id=teacher_id,
                    is_premium=True,
                    expire_date=expire_dat,
                    

                )

                session.add(user)
            else:

                if bl.is_premium:
                    expire_dat=bl.expire_date + datetime.timedelta(days=premium_type)
                    await session.execute(update(IsPremium).values({'expire_date': expire_dat,
                                                                    'is_premium': True}).where(
                        IsPremium.teacher_id == teacher_id))
                elif not bl.is_premium:
                    await session.execute(
                        update(IsPremium).values({'expire_date': expire_dat,
                                                  'is_premium': True}).where(
                            IsPremium.teacher_id == teacher_id))




                await session.execute(update(User).values({"is_active": True}).where(User.teacher_id == teacher_id))
            return expire_dat



async def get_expired_users(session_maker: sessionmaker):
    datNow=datetime.datetime.now()
    """
    Получить пользователя по его id
    :param user_id:
    :param session_maker:
    :return:
    """
    async with session_maker() as session:

        async with session.begin():

            teachers_id = await session.execute(
                select(IsPremium.teacher_id)
                    .filter(IsPremium.expire_date<datNow)  # type: ignore
            )
            await session.execute(update(IsPremium).values({'expire_date': (datetime.datetime.now()+datetime.timedelta(days=365)),'is_premium': False}).where(IsPremium.expire_date<datNow))
            teachers_id=teachers_id.scalars().all()
            for tid in teachers_id:


                result = await session.execute(
                    select(User.group_name).distinct()
                    .where(User.teacher_id == tid)  # type: ignore
                )

                result = result.scalars().all()
                for r in range(len(result)):
                    if r <= 1:
                        print(r)
                        res = await session.execute(select(User.student_id).where(User.teacher_id == tid,
                                                                                  User.group_name == result[
                                                                                      r]).order_by(
                            User.numer.asc()).offset(15))
                        res = res.scalars().all()
                        await session.execute(
                            update(User).values({"is_active": False}).where(User.student_id.in_(res),
                                                                            User.group_name == result[
                                                                                r]))
                    else:
                        print(r)
                        await session.execute(
                            update(User).values({"is_active": False}).where(User.teacher_id == tid,
                                                                            User.group_name == result[r]))



            return teachers_id
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
async def count_students(user_id: int,group_name:str, session_maker: sessionmaker) -> User.student_id:
    """
    Получить пользователя по его id
    :param user_id:
    :param session_maker:
    :return:
    """
    async with session_maker() as session:
        async with session.begin():
            result = await session.execute(
                select(User.student_id).distinct()
                    .filter(User.teacher_id == user_id, User.group_name == group_name)  # type: ignore
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
                select(User)
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

async def delete_student_r(user_id: int, teacher_id:int, session_maker: sessionmaker):
    async with session_maker() as session:


       async with session.begin():
           await session.execute(delete(User).where(User.student_id == user_id, User.teacher_id == teacher_id))
async def get_ans_message(user_id: int,subject:str, session_maker: sessionmaker):
    async with session_maker() as session:
        async with session.begin():
            result = await session.execute(
                select(User.ans_message)
                .filter(User.student_id == user_id, User.teacher_id == int(subject))  # type: ignore
            )
            bl=result.scalars().first()

                
            if bl != None:
                return bl
            else:
                return "Hali bironta ham siz tomoningizdan ishlangan test tekshirilmagan"

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
