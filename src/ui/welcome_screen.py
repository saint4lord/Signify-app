from PyQt6.QtCore import QTimer, Qt
from PyQt6.QtGui import QFont, QPalette, QLinearGradient, QColor, QBrush
from PyQt6.QtWidgets import QWidget, QStackedWidget, QVBoxLayout, QLabel


class WelcomeScreen(QWidget):
    def __init__(self, username):
        super().__init__()
        self.username = username
        self.setWindowTitle("Welcome Screen")
        self.setMinimumSize(800, 600)

        # Create QStackedWidget
        self.stacked_widget = QStackedWidget(self)
        self.init_ui()
        
        QTimer.singleShot(2000, self.show_mode_selection_screen)  # go forward delay

    def init_ui(self):
        self.apply_background()
        # Main 
        self.layout = QVBoxLayout(self)

        self.welcome_label = QLabel(f"Welcome back, {self.username}!", self)
        self.welcome_label.setFont(QFont("Arial", 26, QFont.Weight.Bold))
        self.welcome_label.setStyleSheet("color: #cbd5e1;")
        self.welcome_label.setAlignment(Qt.AlignmentFlag.AlignCenter)

        self.layout.addWidget(self.welcome_label)
        self.layout.addWidget(self.stacked_widget)

        # align label
        self.layout.setAlignment(self.welcome_label, Qt.AlignmentFlag.AlignCenter)
        self.setLayout(self.layout)

        # hide after 2000
        self.timer = QTimer(self)
        self.timer.timeout.connect(self.hide_welcome_label)
        self.timer.start(2000)

    def show_mode_selection_screen(self):
        from mode_selection_screen import ModeSelectionScreen

        # mode select screen
        self.mode_selection_screen = ModeSelectionScreen()

        self.stacked_widget.addWidget(self.mode_selection_screen)
        self.stacked_widget.setCurrentWidget(self.mode_selection_screen)

    def hide_welcome_label(self):
        self.welcome_label.setVisible(False)

    def apply_background(self):
        palette = QPalette()
        gradient = QLinearGradient(0, 0, 0, self.height())
        gradient.setColorAt(0.0, QColor("#0f172a"))
        gradient.setColorAt(1.0, QColor("#1e293b")) 
        palette.setBrush(QPalette.ColorRole.Window, QBrush(gradient))
        self.setPalette(palette)

    def resizeEvent(self, event):
        super().resizeEvent(event)
        self.apply_background() 
        self.center_label()

    def center_label(self):
        label_width = self.welcome_label.sizeHint().width()
        label_height = self.welcome_label.sizeHint().height()

        # center
        self.welcome_label.setGeometry(
            (self.width() - label_width) // 2,
            (self.height() - label_height) // 2,
            label_width,
            label_height,
        )