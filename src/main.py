import sys, os
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), 'ui')))
from PyQt6.QtWidgets import QApplication
from ui.login_screen import LoginScreen

def main():
    app = QApplication(sys.argv)

    login_screen = LoginScreen()
    login_screen.show()

    sys.exit(app.exec())

if __name__ == "__main__":
    main()
