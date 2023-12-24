from functools import partial

from PySide6 import QtWidgets, QtCore, QtGui

from morpion import Pion, get_all_pion

CSS_DIR = "style.css"


class MainWidget(QtWidgets.QWidget):

    def __init__(self):
        super().__init__()
        self.setup_ui()
        with open(CSS_DIR, "r") as style_:
            self.setStyleSheet(style_.read())

        self.list_pion = []

        self.current_player = 'circle'
        self.pion_numbers = 0

    def setup_ui(self):
        self.create_layout()
        self.create_widget()
        self.add_widget_to_layout()
        self.modify_widget()
        self.setup_connection()

    def create_layout(self):
        self.main_layout = QtWidgets.QHBoxLayout(self)
        self.frame = QtWidgets.QFrame()
        self.morpion_layout = QtWidgets.QGridLayout()
        self.frame.setLayout(self.morpion_layout)

        self.lbl_MORPION = QtWidgets.QLabel("MORPION")

        self.morpion_layout.addWidget(self.lbl_MORPION, 0, 0, 1, 3)
        self.main_layout.addWidget(self.frame)

    def create_widget(self):
        self.btn_ = [QtWidgets.QPushButton('') for i in range(9)]

    def add_widget_to_layout(self):
        k = 0
        for x in range(1, 4):
            for y in range(3):
                self.morpion_layout.addWidget(self.btn_[k], x, y, 1, 1)
                k += 1

    def modify_widget(self):
        self.lbl_MORPION.setAlignment(QtCore.Qt.AlignCenter)

        self.lbl_MORPION.setStyleSheet(f"""
                QLabel {{
                    color : rgb(180, 180, 220);
                    font-size : 40px ;
                    font-family : consolas ;
                    font-weight : 400 ;
                    margin-bottom : 20px ;
                }}
            """)

        self.frame.setFixedSize(3*150, 3*150 + 60)

        self.morpion_layout.setSpacing(0)

        for btn in self.btn_:
            btn.setMinimumSize(150, 150)
            btn.setSizePolicy(QtWidgets.QSizePolicy.Policy.Fixed, QtWidgets.QSizePolicy.Policy.Fixed)

        for btn in self.btn_:
            btn.setStyleSheet(f"""
                QPushButton {{
                    font-size : 60px ;
                    font-weight : 600 ;
                    border : 1px solid rgb(80, 80, 80) ; 
                }}
                QPushButton::pressed {{
                    background-color : rgb(150, 150, 150) ;
                    border : 0.5px solid rgb(70, 70, 70);
                    color : grey ;
                }}
            """)

    def next_player(self):
        if self.current_player == 'circle':
            self.current_player = 'cross'
        else:
            self.current_player = 'circle'

    def setup_connection(self):
        for btn in self.btn_:
            btn.pressed.connect(partial(self.compute, btn))

    def compute(self, btn):
        position_ = self.morpion_layout.getItemPosition(self.morpion_layout.indexOf(btn))[:2]

        if get_all_pion():
            for pion in get_all_pion():
                if pion.position == position_:
                    print("Deja Prise")
                    return False

            self.create_pion(btn, position_)

        else:
            self.create_pion(btn, position_)

    def create_pion(self, btn, position_):
        if self.pion_numbers < 8:
            new_pion = Pion(self.current_player, position_)
            btn.setIcon(QtGui.QIcon(new_pion.icon))
            btn.setIconSize(QtCore.QSize(100, 100))
            new_pion.save_pion()
            self.pion_numbers += 1
            if new_pion.verif_game():          # If the end state end game is true
                message = QtWidgets.QMessageBox(QtWidgets.QMessageBox.Icon.Information,
                                                "END",
                                                f"""{'Player 1' if self.current_player == 'circle' else 'Player 2'} Win""")
                message.setStyleSheet('width : 300px ; font-size : 18px ; font-weight : 400 ;')
                message.show()
                message.exec()

                Pion.database.truncate()

                for btn in self.btn_:
                    btn.setIcon(QtGui.QIcon(""))
                    self.pion_numbers = 0

            self.next_player()
        else:
            message = QtWidgets.QMessageBox(QtWidgets.QMessageBox.Icon.Information,
                                            "END",
                                            "END")

            message.setStyleSheet(f'''
                        * {{
                            background-color : rgb(40, 40, 40) ;
                            color : rgb(200, 200, 200)  ;
                            font-size : 18px ;
                            width : 300px ;
                            font-weight : 400 ;
                        }}
                        
                        QPushButton {{
                            border : 0.5 solid rgb(60, 60, 60) ;
                        }}
                        
                        QPushButton::pressed{{
                            background-color : rgb(80, 80, 80) ;     
                            }} 
                ''')
            message.show()
            message.exec()

            Pion.database.truncate()

            for btn in self.btn_:
                btn.setIcon(QtGui.QIcon(""))
                self.pion_numbers = 0


app = QtWidgets.QApplication()
win = MainWidget()
win.show()
app.exec()