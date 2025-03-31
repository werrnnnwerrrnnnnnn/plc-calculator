import sys
from PyQt6 import uic
from PyQt6.QtWidgets import QApplication
from PyQt6.QtWidgets import QMainWindow, QLineEdit, QPushButton, QLCDNumber

from components.lexica import MyLexer
from components.parsers import PrefixParser
from components.memory import Memory

class MainWindow(QMainWindow):

    # Do this for intellisense
    button_1: QPushButton        # 1
    button_2: QPushButton        # 2
    button_3: QPushButton        # 3
    button_4: QPushButton        # 4
    button_5: QPushButton        # 5
    button_6: QPushButton        # 6
    button_7: QPushButton        # 7
    button_8: QPushButton        # 8
    button_9: QPushButton        # 9
    button_plus: QPushButton     # +
    button_star: QPushButton     # *
    button_equal: QPushButton    # =
    button_clear: QPushButton    # Clear

    input_prefix: QLineEdit      # Prefix input
    output_infix: QLineEdit      # Infix output
    # output_postfix: QLineEdit  # Postfix output
    output_answer: QLCDNumber    # Answer output

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        uic.loadUi("./components/main.ui", self)

        #### Binding button to function ####
        self.button_0.clicked.connect(lambda: self.push("0"))   
        self.button_1.clicked.connect(lambda: self.push("1"))
        self.button_2.clicked.connect(lambda: self.push("2"))
        self.button_3.clicked.connect(lambda: self.push("3"))
        self.button_4.clicked.connect(lambda: self.push("4"))
        self.button_5.clicked.connect(lambda: self.push("5"))
        self.button_6.clicked.connect(lambda: self.push("6"))
        self.button_7.clicked.connect(lambda: self.push("7"))
        self.button_8.clicked.connect(lambda: self.push("8"))
        self.button_9.clicked.connect(lambda: self.push("9"))

        self.button_plus.clicked.connect(lambda: self.push("+"))
        self.button_star.clicked.connect(lambda: self.push("*"))
        self.button_equal.clicked.connect(self.push_equal)
        self.button_clear.clicked.connect(self.clear)

    def push_1(self):
        current_text:str = self.input_prefix.text()
        self.input_prefix.setText(f"{current_text}1")
    
    def push(self, text:str):
        current_text:str = self.input_prefix.text()
        self.input_prefix.setText(f"{current_text} {text}")
    
    def push_equal(self):
        print("\n========================================================================")
        print("📍 Calculating from Prefix Input...")

        lexer = MyLexer()
        # parser = MyParser()
        prefix_parser = PrefixParser()
        memory = Memory()

        input_prefix = self.input_prefix.text()
        # result = parser.parse(lexer.tokenize(input_prefix))
        result = prefix_parser.parse(lexer.tokenize(input_prefix))
        print(f"✅ Answer type : {type(result)}")
        print(f"✅ Answer : {result}\n")
        self.output_answer.display(result)
        self.output_infix.setText(prefix_parser.get_infix())
        
        # for debug
        print(memory)
    
    def clear(self):
        current_text:str = ''
        self.input_prefix.setText(current_text)
        self.input_prefix.setText("")       # Clear prefix input
        self.output_answer.display(0)       # Reset answer display
        self.output_infix.setText("")       # Clear infix output

if __name__ == "__main__":
    app = QApplication(sys.argv)
    window = MainWindow()
    window.show()
    app.exec()