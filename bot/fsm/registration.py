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
    delete_students = State()
    post_new_gr = State()
    set_hour= State()
    set_minute= State()
    select_on_test_type = State()
    send_file_on= State()
    select_enter_channel_link=State()
    detect_on_subject= State()

class StudentMenu(StatesGroup):
    get_code = State()
    select_m_check_online = State()
    scan_omr=State()
    enter_test=State()
    start_own_register=State()
