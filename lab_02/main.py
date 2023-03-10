# Асадуллин Тагир ИУ7-24Б. Конвертор в 2 СС из 10. И наоборот
import sys

from PyQt5.QtWidgets import QApplication, QMainWindow, QWidget
from PyQt5 import QtCore, QtGui

from lab_01.ui.main_window_ui import Ui_MainWindow
from lab_01.ui.info_window_ui import Ui_InfoWindow


class MainWindow(QMainWindow, Ui_MainWindow):
    def __init__(self):
        super().__init__()
        self.setWindowIcon(QtGui.QIcon('ui/source/icon.png'))
        self.setupUi(self)
        self.connect_buttons()
        self.action_bars()
        self.set_validator()

    def connect_buttons(self):
        """Привязка кнопок к действию"""
        for i in self.nums.buttons():  # кнопки '1234567890.'
            i.clicked.connect(self.entering)
        self.neg.clicked.connect(self.entering)
        self.execute.clicked.connect(self.run)  # кнопка '='

        self.to10.clicked.connect(self.disable)  # переключатель 2->10
        self.to10.clicked.connect(self.switch)
        self.to2.clicked.connect(self.disable)  # переключатель 0->2
        self.to2.clicked.connect(self.switch)

        self.delete_2.clicked.connect(self.cls)  # кнопка 'C'
        self.switch_2.clicked.connect(self.switch)  # кнопка '<->'
        self.enter_bar.textChanged.connect(self.run)  # выполняется при новом символе

    def entering(self):
        """Ввод символа с меню на позицию курсора"""
        cursor_position = self.enter_bar.cursorPosition()
        button_type = self.sender().text()
        enter_bar_text = self.enter_bar.text()
        if cursor_position == 0 and enter_bar_text.count('-') == 1:
            return
        if button_type == '-' and (cursor_position != 0 or enter_bar_text.count('-') == 1):
            return
        if button_type == '.' and \
                ((cursor_position == 0 or enter_bar_text.count('.') == 1)
                 or (cursor_position == 1 and enter_bar_text.count('-') == 1)):
            return
        self.enter_bar.setText(
            enter_bar_text[:cursor_position] + button_type + enter_bar_text[cursor_position:])

    def set_validator(self):
        """Разрешает вводить только подходящие вещественные числа"""
        if self.to2.isChecked():
            validator = QtGui.QRegExpValidator(QtCore.QRegExp(r"-?\d+(\.\d+)?"))  # вещественные десятеричные
        if self.to10.isChecked():
            validator = QtGui.QRegExpValidator(QtCore.QRegExp(r"-?[01]+(\.[01]+)?"))  # вещественные двоичные
        self.enter_bar.setValidator(validator)

    def disable(self):
        """Отключить кнопки, цифры которых недоступны в 2-ой СС"""
        if self.to10.isChecked():
            for i in self.nums.buttons()[1:-2]:  # выключить кнопки 2-9
                i.setDisabled(True)
            for i in self.menuPlace.actions()[3:-3]:  # выключить 2-9 в меню
                i.setDisabled(True)
        if self.to2.isChecked():
            for i in self.nums.buttons():  # включить кнопки 2-9
                i.setEnabled(True)
            for i in self.menuPlace.actions()[3:-3]:  # включить 2-9 в меню
                i.setEnabled(True)

    def run(self):
        """Конвертирует число enter_bar"""
        import convert
        enter_bar_text = self.enter_bar.text()
        if not self.enter_bar.text() or enter_bar_text == '-':
            self.res_bar.clear()
            return

        addition_text = '='
        if enter_bar_text[0] == '-':
            enter_bar_text = enter_bar_text[1:]
            addition_text = '=-'
        # конвертирует
        if self.to2.isChecked():
            self.res_bar.setText(addition_text + convert.float_to2(enter_bar_text))
            self.to2.setEnabled(False)
            self.to10.setEnabled(True)
        elif self.to10.isChecked():
            self.to10.setEnabled(False)
            self.to2.setEnabled(True)
            self.res_bar.setText(addition_text + convert.float_to10(enter_bar_text))
        self.res_bar.setCursorPosition(1)

    def cls(self):
        """Очистка одного элемента перед курсором"""
        cursor_position = self.enter_bar.cursorPosition()
        if cursor_position <= 0:
            return
        self.enter_bar.setText(self.enter_bar.text()[:cursor_position - 1] + self.enter_bar.text()[cursor_position:])

    def switch(self):
        """Если меняется порядок перевода, меняется res_bar с enter_bar"""
        # если с помощью кнопки <->, поменять radiobutton'ы
        if self.sender() is self.switch_2 or self.sender() is self.actionSwitch:
            if self.to2.isChecked():
                self.to10.setChecked(True)
            else:
                self.to2.setChecked(True)
        self.set_validator()
        self.disable()
        self.enter_bar.setText(self.res_bar.text()[1:])
        self.run()

    def action_bars(self):
        """Настройка выпадающего меню"""

        def op():
            """Открыть второе окно"""
            self.second_form = InfoWindow()
            self.second_form.show()

        self.actionHelp.triggered.connect(op)
        for i in self.menuPlace.actions():
            i.triggered.connect(self.entering)
        self.actionAll.triggered.connect(lambda _: self.enter_bar.clear())
        self.actionChar.triggered.connect(self.cls)
        self.actionSwitch.triggered.connect(self.switch)
        self.actionExecute.triggered.connect(self.run)


class InfoWindow(QWidget, Ui_InfoWindow):
    def __init__(self):
        super().__init__()
        self.setupUi(self)
        self.pushButton.clicked.connect(self.close_window)
        # задает окну первостепенность
        self.setWindowModality(QtCore.Qt.WindowModality(2))
        self.setWindowFlags(QtCore.Qt.WindowCloseButtonHint)

    def close_window(self):
        """Закрыть окно"""
        self.close()


if __name__ == '__main__':
    app = QApplication(sys.argv)
    ex = MainWindow()
    ex.show()
    sys.exit(app.exec_())
