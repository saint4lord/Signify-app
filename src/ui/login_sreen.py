import sys
from PyQt6.QtWidgets import QApplication, QWidget, QLabel, QLineEdit, QPushButton, QGraphicsDropShadowEffect, QMessageBox
from PyQt6.QtGui import QFont, QPalette, QLinearGradient, QColor, QBrush, QPixmap
from PyQt6.QtCore import Qt
from welcome_screen import WelcomeScreen


class LoginScreen(QWidget):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Signify - Login")
        self.setMinimumSize(400, 600)
        self.resize(400, 600)
        self.init_ui()

    def init_ui(self):
        # Настройка фона
        palette = QPalette()
        gradient = QLinearGradient(0, 0, 0, self.height())
        gradient.setColorAt(0.0, QColor("#0f172a"))
        gradient.setColorAt(1.0, QColor("#1e293b"))
        palette.setBrush(QPalette.ColorRole.Window, QBrush(gradient))
        self.setPalette(palette)

        # Логотип (PNG вместо текста)
        self.logo_label = QLabel(self)
        pixmap = QPixmap("src/assets/logo.png")
        self.logo_label.setPixmap(pixmap)
        self.logo_label.setAlignment(Qt.AlignmentFlag.AlignCenter)

        # Поле для логина
        self.login_field = QLineEdit(self)
        self.login_field.setPlaceholderText("Email")
        self.login_field.setStyleSheet(self.field_style())
        apply_shadow(self.login_field)

        # Поле для пароля
        self.password_field = QLineEdit(self)
        self.password_field.setPlaceholderText("Password")
        self.password_field.setEchoMode(QLineEdit.EchoMode.Password)
        self.password_field.setStyleSheet(self.field_style())
        apply_shadow(self.password_field)

        # Кнопка "Sign In"
        self.sign_in_button = QPushButton("Sign In", self)
        self.sign_in_button.setStyleSheet(self.button_style())
        apply_shadow(self.sign_in_button)
        self.sign_in_button.clicked.connect(self.on_sign_in_clicked)

        # Надпись "Forgot Password"
        self.forgot_label = QLabel("Forgot Password?", self)
        self.forgot_label.setFont(QFont("Arial", 10))
        self.forgot_label.setStyleSheet("color: #94a3b8;")
        self.forgot_label.setAlignment(Qt.AlignmentFlag.AlignLeft)

        # Надпись "Register"
        self.register_label = QLabel("Register", self)
        self.register_label.setFont(QFont("Arial", 10, QFont.Weight.Bold))
        self.register_label.setStyleSheet("color: #38bdf8; text-decoration: underline;")
        self.register_label.setAlignment(Qt.AlignmentFlag.AlignCenter)

        self.reposition_elements()

    def on_sign_in_clicked(self):
        email = self.login_field.text()
        password = self.password_field.text()

        # Проверка заполнения полей
        if not email or not password:
            QMessageBox.warning(self, "Error", "Please fill in all fields!")
            return

        # Проверка логина через validate_login
        if validate_login(email, password):
            QMessageBox.information(self, "Success", "Login successful!")
            self.hide()
            self.welcome_screen = WelcomeScreen(email)  # Передача логина в экран приветствия
            self.welcome_screen.show()
        else:
            QMessageBox.warning(self, "Error", "Invalid email or password!")

    def field_style(self):
        return """
            QLineEdit {
                background: #1e293b; 
                border: 1px solid #334155;
                border-radius: 10px;
                color: #cbd5e1;
                padding: 5px 10px;
                font-size: 14px;
                outline: none;
            }
            QLineEdit:focus {
                border-color: #38bdf8;
            }
        """

    def button_style(self):
        return """
            QPushButton {
                background-color: #2563eb;
                border: none;
                border-radius: 10px;
                color: #cbd5e1; 
                font-size: 16px;
                font-weight: bold;
                outline: none;
            }
            QPushButton:hover {
                background-color: #1d4ed8;
            }
            QPushButton:pressed {
                background-color: #1e40af;
            }
        """

    def resizeEvent(self, event):
        super().resizeEvent(event)
        self.reposition_elements()

    def reposition_elements(self):
        # Центрируем элементы
        window_width = self.width()
        window_height = self.height()

        self.logo_label.setGeometry((window_width - 200) // 2, 50, 200, 50)
        self.login_field.setGeometry((window_width - 300) // 2, 150, 300, 40)
        self.password_field.setGeometry((window_width - 300) // 2, 210, 300, 40)
        self.sign_in_button.setGeometry((window_width - 300) // 2, 290, 300, 50)
        self.forgot_label.setGeometry((window_width - 300) // 2, 260, 300, 20)
        self.register_label.setGeometry((window_width - 300) // 2, 350, 300, 20)

def apply_shadow(widget):
    shadow_effect = QGraphicsDropShadowEffect()
    shadow_effect.setBlurRadius(30)
    shadow_effect.setXOffset(0)
    shadow_effect.setYOffset(0)
    shadow_effect.setColor(QColor(30, 40, 50, 160))
    widget.setGraphicsEffect(shadow_effect)

if __name__ == "__main__":
    app = QApplication(sys.argv)
    login_screen = LoginScreen()
    login_screen.show()
    app.exec()

