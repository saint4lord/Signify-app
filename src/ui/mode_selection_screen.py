from PyQt6.QtGui import QFont, QLinearGradient, QColor, QPalette, QBrush
from PyQt6.QtCore import Qt
from PyQt6.QtWidgets import QWidget, QLabel, QPushButton, QVBoxLayout

class ModeSelectionScreen(QWidget):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Signify - Select Mode")
        self.setMinimumSize(400, 600)
        self.resize(800, 600)
        self.init_ui()

    def init_ui(self):
        # global style
        self.apply_style()

        # background setting up
        palette = QPalette()
        gradient = QLinearGradient(0, 0, 0, self.height())
        gradient.setColorAt(0.0, QColor("#0f172a"))
        gradient.setColorAt(1.0, QColor("#1e293b"))
        palette.setBrush(QPalette.ColorRole.Window, QBrush(gradient))
        self.setPalette(palette)

        # Head of screen
        self.title_label = QLabel("Select Mode", self)
        self.title_label.setFont(QFont("Arial", 26, QFont.Weight.Bold))
        self.title_label.setAlignment(Qt.AlignmentFlag.AlignCenter)

        # mode description
        self.hand_mode_label = QLabel("Hand Mode\nControl your computer using hand gestures", self)
        self.hand_mode_label.setFont(QFont("Arial", 14))
        self.hand_mode_label.setAlignment(Qt.AlignmentFlag.AlignCenter)

        self.face_mode_label = QLabel("Face Mode\nControl your computer using facial gestures", self)
        self.face_mode_label.setFont(QFont("Arial", 14))
        self.face_mode_label.setAlignment(Qt.AlignmentFlag.AlignCenter)

        # mode buttons
        self.hand_button = QPushButton("Hand Mode", self)
        self.hand_button.setStyleSheet(self.button_style())
        self.hand_button.clicked.connect(self.on_hand_mode_clicked)

        self.face_button = QPushButton("Face Mode", self)
        self.face_button.setStyleSheet(self.button_style())
        self.face_button.clicked.connect(self.on_face_mode_clicked)

        self.layout = QVBoxLayout(self)
        self.layout.addWidget(self.title_label)
        self.layout.addWidget(self.hand_mode_label)
        self.layout.addWidget(self.face_mode_label)
        self.layout.addWidget(self.hand_button)
        self.layout.addWidget(self.face_button)

        self.setLayout(self.layout)
        self.reposition_elements()

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
                padding: 10px;
                margin: 10px;
            }
            QPushButton:hover {
                background-color: #1d4ed8; 
            }
            QPushButton:pressed {
                background-color: #1e40af; 
            }
        """

    def on_hand_mode_clicked(self):
        print("Hand Mode Selected")
        # here link to hand_control.py

    def on_face_mode_clicked(self):
        print("Face Mode Selected")
        # here link to face_control.py

    def resizeEvent(self, event):
        super().resizeEvent(event)
        self.reposition_elements()

    def reposition_elements(self):
        window_width = self.width()
        window_height = self.height()

        self.title_label.setGeometry((window_width - 300) // 2, 50, 300, 50)
        self.hand_mode_label.setGeometry((window_width - 300) // 2, 150, 300, 50)
        self.face_mode_label.setGeometry((window_width - 300) // 2, 230, 300, 50)
        self.hand_button.setGeometry((window_width - 300) // 2, 300, 300, 50)
        self.face_button.setGeometry((window_width - 300) // 2, 370, 300, 50)

    def apply_style(self):
        self.setStyleSheet("""
            QWidget {
                background-color: #0f172a;
                color: #cbd5e1;
            }
            QPushButton {
                background-color: #2563eb;
                border: none;
                border-radius: 10px;
                color: #cbd5e1; 
                font-size: 16px;
                font-weight: bold;
                padding: 10px;
                margin: 10px;
            }
            QPushButton:hover {
                background-color: #1d4ed8; 
            }
            QPushButton:pressed {
                background-color: #1e40af; 
            }
        """)

