import sys


# простите за *
from PyQt5.QtCore import *
from PyQt5.QtGui import *
from PyQt5.QtWidgets import *


class CircularProgress(QWidget):
    anim_fin = pyqtSignal()

    def __init__(self):
        super().__init__()
        # Убираем фон окна
        self.setWindowFlags(Qt.FramelessWindowHint)
        self.setAttribute(Qt.WA_TranslucentBackground)

        # Нач знач
        self.value = 0
        self.width = 300
        self.height = 300
        self.progress_width = 30  # толщина внешней линии
        self.inner_progress_width = 2
        self.progress_rounded_cap = True
        self.gap = 35  #отступ между линиями

        # градиент
        self.progress_color_start = QColor(76, 162, 87) 
        self.progress_color_end = QColor(178, 214, 183) 
        self.inner_progress_color = QColor(247, 186, 11) 
        self.font_size = 40
        self.suffix = "%"
        self.text_color = QColor(76, 162, 87)

        # Углы для дуг
        self.outer_arc_length = 0
        self.inner_arc_length = 0

        self.animation_duration = 25  # с
        self.update_interval = 40     # млс
        self.total_steps = int(self.animation_duration * 1000 / self.update_interval)
        self.step_value = 100.0 / self.total_steps  # float для плавности

        # Таймер для анимации
        self.timer = QTimer()
        self.timer.timeout.connect(self.update_progress)
        self.timer.start(self.update_interval)

        # Размеры окна
        self.resize(self.width, self.height)

        self.center()

    def center(self):
        # Получаем геому осн экрана
        screen = QDesktopWidget().screenGeometry()
        # Получаем геому окна
        window = self.geometry()
        # Где центр
        x = (screen.width() - window.width()) // 2
        y = (screen.height() - window.height()) // 2
        # Перемещаем окно
        self.move(x, y)

    def update_progress(self):
        if self.value < 100:
            self.value += self.step_value
            # Плавная обнова дуг с float значением
            progress = self.value / 100.0
            self.outer_arc_length = int(-360 * progress * 16)
            self.inner_arc_length = int(360 * progress * 16)
            self.update()
        else:
            self.timer.stop()
            self.anim_fin.emit()  # флажок

    def paintEvent(self, event):
        painter = QPainter()
        painter.begin(self)
        painter.setRenderHint(QPainter.Antialiasing)

        # Расчет размеров
        rect = QRect(0, 0, self.width, self.height)
        margin = self.progress_width / 2

        # Создание градиента для внеш круга
        gradient = QLinearGradient(rect.center().x(), 0, rect.center().x(), rect.height())
        gradient.setColorAt(0, self.progress_color_start)
        gradient.setColorAt(1, self.progress_color_end)

        # Настройка пера для внеш круга
        pen = QPen()
        pen.setWidth(self.progress_width)
        pen.setCapStyle(Qt.RoundCap if self.progress_rounded_cap else Qt.FlatCap)
        pen.setStyle(Qt.SolidLine)
        pen.setBrush(gradient)

        # Рисование внеш круга (фон)
        painter.setPen(QPen(QColor(244, 248, 244, 100), self.progress_width)) # 40 40 40
        painter.drawArc(int(margin), int(margin),
                        int(self.width - self.progress_width),
                        int(self.height - self.progress_width),
                        0, 360 * 16)

        # Рисование внеш круга (прогресс)
        painter.setPen(pen)
        painter.drawArc(int(margin), int(margin),
                        int(self.width - self.progress_width),
                        int(self.height - self.progress_width),
                        90 * 16, self.outer_arc_length)

        # Рисование внутр круга (фон)
        inner_margin = margin + self.gap  # Увеличенный отступ для внутр круга
        painter.setPen(QPen(QColor(40, 40, 40), self.inner_progress_width))
        painter.drawArc(int(inner_margin),
                        int(inner_margin),
                        int(self.width - inner_margin * 2),
                        int(self.height - inner_margin * 2),
                        0, 360 * 16)

        # Рисование внутр круга (прогресс)
        painter.setPen(QPen(self.inner_progress_color, self.inner_progress_width))
        painter.drawArc(int(inner_margin),
                        int(inner_margin),
                        int(self.width - inner_margin * 2),
                        int(self.height - inner_margin * 2),
                        90 * 16, self.inner_arc_length)

        # Рисование текста с жирным шрифтом
        font = QFont('Segoe UI', self.font_size)
        font.setBold(True)  
        font.setWeight(75)  #  0 - 99

        painter.setPen(self.text_color)
        painter.setFont(font)
        painter.drawText(rect, Qt.AlignCenter, f"{int(self.value)}{self.suffix}")

        painter.end()

#       писать это было сложно
# так что и читать должно быть не проще
#              (^◕ᴥ◕^)

if __name__ == '__main__':
    app = QApplication(sys.argv)
    window = CircularProgress()
    window.show()
    sys.exit(app.exec_())