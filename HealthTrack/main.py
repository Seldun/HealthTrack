"""
#################################################
#                                               #
#       ОСТАВЬ НАДЕЖДУ ВСЯК СЮДА ВХОДЯЩИЙ       #
#                                               #
#################################################
"""



import json
import sys
import threading
import platform
from PyQt5 import QtWidgets, QtCore
import os


if platform.system() == 'Windows':
    from MainLoadWin_windows import Ui_MainDownload
    from Window1_windows import Ui_Window1
    from Window2_windows import Ui_Window2
    from Window3_windows import Ui_Window3
    from end_windows import Ui_AnswerWindow
else:  # для Linux и MacOS
    from MainLoadWin import Ui_MainDownload
    from Window1 import Ui_Window1
    from Window2 import Ui_Window2
    from Window3 import Ui_Window3
    from answerWind import Ui_AnswerWindow

from Secret import Ui_Password_wind
from Cat import Ui_Cat_wind
from Warning import Ui_Dialog
from curcle import CircularProgress
from preparations_for_the_answer import HealthAdvisorAI


class LoadingWindow(QtWidgets.QDialog):
    def __init__(self):
        super().__init__()
        self.ui = Ui_MainDownload()
        self.ui.setupUi(self)
        
        # Устанавливаем фиксированный размер окна
        self.setFixedSize(1280, 720)
        self.setMinimumSize(1280, 720)
        self.setMaximumSize(1280, 720)

        self.ui.pushButton.clicked.connect(self.transition_to_window1)

    def transition_to_window1(self):

        self.controller = MainController()
        self.controller.show_window1()
        self.close()


class MainController:
    def __init__(self):
        # Добавляем определение пути к data.json
        self.base_dir = os.path.dirname(os.path.abspath(__file__))
        self.data_path = os.path.join(self.base_dir, "data.json")
        
        # Инициализация переменных для хранения данных
        self.data = {
            "window1": {"name": "", "gender": "", "birthday": "2008-01-01"},
            "window2": {"height": 160, "weight": 60, "nationality": "", "residence": ""},
            "window3": {"symptoms": "", "throat": "", "stomach": ""}
        }

        self.password = "jy_kj["

        # Создание окон
        self.window1 = QtWidgets.QMainWindow()
        self.ui1 = Ui_Window1()
        self.ui1.setupUi(self.window1)
        self.window1.setFixedSize(1280, 720)
        self.window1.setMinimumSize(1280, 720)
        self.window1.setMaximumSize(1280, 720)

        self.window2 = QtWidgets.QDialog()
        self.ui2 = Ui_Window2()
        self.ui2.setupUi(self.window2)
        self.window2.setFixedSize(1280, 720)
        self.window2.setMinimumSize(1280, 720)
        self.window2.setMaximumSize(1280, 720)

        self.window3 = QtWidgets.QDialog()
        self.ui3 = Ui_Window3()
        self.ui3.setupUi(self.window3)
        self.window3.setFixedSize(1280, 720)
        self.window3.setMinimumSize(1280, 720)
        self.window3.setMaximumSize(1280, 720)
        
        self.war_win = QtWidgets.QDialog()
        self.war = Ui_Dialog()
        self.war.setupUi(self.war_win)
        self.war_win.setFixedSize(1280, 720)
        self.war_win.setMinimumSize(1280, 720)
        self.war_win.setMaximumSize(1280, 720)

        self.sec_win = QtWidgets.QDialog()
        self.secr = Ui_Password_wind()
        self.secr.setupUi(self.sec_win)
        self.sec_win.setFixedSize(1100, 720)
        self.sec_win.setMinimumSize(1100, 720)
        self.sec_win.setMaximumSize(1100, 720)

        self.joke = QtWidgets.QDialog()
        self.cat = Ui_Cat_wind()
        self.cat.setupUi(self.joke)
        self.joke.setFixedSize(1280, 960)
        self.joke.setMinimumSize(1280, 960)
        self.joke.setMaximumSize(1280, 960)


        # Связываем кнопки с функциями
        self.ui1.page1to2_btm.clicked.connect(self.save_and_go_to_window2)
        self.ui2.page2to1_btm.clicked.connect(self.save_and_go_to_window1)
        self.ui2.page2to3_btm.clicked.connect(self.save_and_go_to_window3)
        self.ui3.page3to2_btm.clicked.connect(self.save_and_go_to_window2)
        self.ui3.answer_btm.clicked.connect(self.save_and_go_to_curcle)
        self.war.agree_btm.clicked.connect(self.show_answer)
        self.secr.dream.clicked.connect(self.password_check)


        # Связываем сигналы с обновлением данных
        self.ui1.name.textChanged.connect(lambda: self.update_data("window1", "name", self.ui1.name.text()))
        self.ui1.male_btm.clicked.connect(lambda: self.update_data("window1", "gender", "male"))
        self.ui1.female_btm.clicked.connect(lambda: self.update_data("window1", "gender", "female"))
        self.ui1.birthday.dateChanged.connect(
            lambda: self.update_data("window1", "birthday", self.ui1.birthday.date().toString("yyyy-MM-dd")))

        self.ui2.height.valueChanged.connect(lambda: self.update_data("window2", "height", self.ui2.height.value()))
        self.ui2.weight.valueChanged.connect(lambda: self.update_data("window2", "weight", self.ui2.weight.value()))
        self.ui2.nationality.textChanged.connect(
            lambda: self.update_data("window2", "nationality", self.ui2.nationality.text()))
        self.ui2.residence.textChanged.connect(
            lambda: self.update_data("window2", "residence", self.ui2.residence.text()))

        self.ui3.symptoms.textChanged.connect(
            lambda: self.update_data("window3", "symptoms", self.ui3.symptoms.toPlainText()))
        self.ui3.throat.clicked.connect(lambda: self.update_data("window3", "throat", "throat_issue"))
        self.ui3.stomach.clicked.connect(lambda: self.update_data("window3", "stomach", "stomach_issue"))

    def password_check(self):
        a = self.secr.password_line.text()
        if a == self.password:
            self.paradise()

    def update_data(self, window, key, value):
        self.data[window][key] = value

    def save_data(self):
        with open(self.data_path, "w", encoding="utf-8") as file:
            json.dump(self.data, file, indent=4, ensure_ascii=False)

    def load_data(self):
        try:
            with open(self.data_path, "r", encoding="utf-8") as file:
                self.data = json.load(file)
        except FileNotFoundError:
            print("Файл не найден, будет создан новый")
            self.save_data()

    def show_window1(self):
        self.load_data()
        self.window1.show()
        self.window2.hide()
        self.window3.hide()

    def show_window2(self):
        self.load_data()
        self.window2.show()
        self.window1.hide()
        self.window3.hide()

    def show_window3(self):
        self.load_data()
        self.window3.show()
        self.window1.hide()
        self.window2.hide()

    def paradise(self):
        self.sec_win.hide()
        self.joke.show()

    def save_and_go_to_window2(self):
        self.save_data()
        self.show_window2()

    def save_and_go_to_window1(self):
        self.save_data()
        self.show_window1()

    def save_and_go_to_window3(self):
        self.save_data()
        self.show_window3()

    def generate_report_in_thread(self):
        # Чтение данных из data.json
        with open(self.data_path, "r", encoding="utf-8") as file:
            user_data = json.load(file)

        # Генерация отчета
        self.advisor = HealthAdvisorAI(user_data)
        self.advisor.generate_full_report()

    def save_and_go_to_curcle(self):
        self.save_data()
        self.window3.hide()
        self.ninth_circle_of_hell = CircularProgress()
        self.ninth_circle_of_hell.show()

        report_thread = threading.Thread(target=self.generate_report_in_thread)
        report_thread.start()

        self.ninth_circle_of_hell.anim_fin.connect(self.show_answer)
    
    def show_waring(self):
        self.ninth_circle_of_hell.hide()
        '''self.war_win = QtWidgets.QDialog()
        self.war = Ui_Dialog()
        self.war.setupUi(self.war_win)'''
        self.war_win.show()


        self.war.agree_btm.clicked.connect(self.show_answer)

    def go_to_password(self):
        self.ans_wind.hide()
        self.sec_win.show()

    def show_answer(self):
        self.ninth_circle_of_hell.close()
        self.ans_wind = QtWidgets.QDialog()
        self.ans_cl = Ui_AnswerWindow()
        self.ans_cl.setupUi(self.ans_wind)
        self.ans_wind.setFixedSize(1280, 720)
        self.ans_wind.setMinimumSize(1280, 720)
        self.ans_wind.setMaximumSize(1280, 720)
        self.ans_wind.show()

        self.ans_cl.mishka.clicked.connect(self.go_to_password)
        # 6. Сброс данных ПОСЛЕ показа окна
        self.data = {
            "window1": {"name": "", "gender": "", "birthday": "2008-01-01"},
            "window2": {"height": 160, "weight": 60, "nationality": "", "residence": ""},
            "window3": {"symptoms": "", "throat": "", "stomach": ""}
        }
        with open(self.data_path, "w", encoding="utf-8") as file:
            json.dump(self.data, file, indent=4, ensure_ascii=False)


if __name__ == '__main__':
    app = QtWidgets.QApplication(sys.argv)
    window = LoadingWindow()
    window.show()
    sys.exit(app.exec_())


"""
Спасибо, что дочитали до конца! 
Знаю, код местами похож на лапшу, которую уронил кот,
но он работает, и это главное (｡•́‿•̀｡)

С уважением,
Разработчик, который слишком много пил кофе во время написания этого кода и ругался на других котов

P.S.
    Огромное спасибо дизайнеру АФ (⌒▽⌒)♡
"""
