from aiogram.fsm.state import StatesGroup, State


class Registration(StatesGroup):
    tutorial = State()
    register_t_name = State()
    register_school_name = State()
    register_subject = State()
    register_students = State()
    register_group_name = State()
    end = State()
    slkt_role = State()
    show_res = State()

class PostRegistration(StatesGroup):
    scan_test = State()
    send_file = State()
    menu = State()
    add_students = State()
    edit_datas = State()
    stats = State()
    new_gr = State()
    register_students_new = State()


