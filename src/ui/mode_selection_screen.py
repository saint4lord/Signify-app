import os
from PyQt6.QtGui import QFont, QLinearGradient, QColor, QPalette, QBrush, QPixmap, QIcon
from PyQt6.QtCore import Qt
from PyQt6.QtWidgets import QWidget, QLabel, QVBoxLayout, QHBoxLayout, QPushButton, QFrame, QSizePolicy


class ModeSelectionScreen(QWidget):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Signify - Select Mode")
        self.setMinimumSize(400, 600)
        self.resize(800, 600)
        self.init_ui()

    def init_ui(self):
        # Apply global style
        self.apply_style()

        # Background gradient
        palette = QPalette()
        gradient = QLinearGradient(0, 0, 0, self.height())
        gradient.setColorAt(0.0, QColor("#0f172a"))
        gradient.setColorAt(1.0, QColor("#1e293b"))
        palette.setBrush(QPalette.ColorRole.Window, QBrush(gradient))
        self.setPalette(palette)

        # Create cards
        base_path = r"X:\WindowsFolders\Music\Projects\Signify-app\src"
        hand_icon_path = os.path.join(base_path, "assets/icons/hand_mode_3d64.png")
        face_icon_path = os.path.join(base_path, "assets/icons/face_mode_3d64.png")

        self.hand_card = self.create_card(
            hand_icon_path,
            "Hand Mode",
            "Control your PC by hands.",
            self.on_hand_mode_clicked
        )

        self.face_card = self.create_card(
            face_icon_path,
            "Face Mode",
            "Control your PC by face.",
            self.on_face_mode_clicked
        )

        # Update button text
        self.hand_card.findChild(QPushButton).setText("Use Hands")
        self.face_card.findChild(QPushButton).setText("Use Face")

        # Layout setup
        self.main_layout = QVBoxLayout(self)

        # Horizontal layout for cards
        self.card_layout = QHBoxLayout()
        self.card_layout.addWidget(self.hand_card)
        self.card_layout.addWidget(self.face_card)
        self.card_layout.setSpacing(20)
        self.card_layout.setAlignment(Qt.AlignmentFlag.AlignCenter)

        self.main_layout.addLayout(self.card_layout)
        self.setLayout(self.main_layout)

    def create_card(self, icon_path, title, description, on_click):
    # Create a card container
        card = QFrame(self)
        card.setStyleSheet("""
            QFrame {
                background-color: #1e293b;
                border-radius: 15px;
                border: 2px solid #334155;
                padding: 15px;
            }
        """)
        card.setFixedSize(320, 320)
        card_layout = QVBoxLayout(card)
        card_layout.setContentsMargins(10, 10, 10, 10)
        card_layout.setSpacing(10)

        # Icon for the card
        if os.path.exists(icon_path):
            icon_label = QLabel(card)
            pixmap = QPixmap(icon_path)

            pixmap = pixmap.scaled(40, 40, Qt.AspectRatioMode.KeepAspectRatio, Qt.TransformationMode.SmoothTransformation)

            # set image to Qlabel
            icon_label.setPixmap(pixmap)
            icon_label.setAlignment(Qt.AlignmentFlag.AlignCenter)
            icon_label.setStyleSheet("border: none;")
            card_layout.addWidget(icon_label)
        else:
            print(f"Icon not found: {icon_path}")

        # Title of the card
        title_label = QLabel(title, card)
        title_label.setFont(QFont("SF Pro Display Bold", 18, QFont.Weight.Bold))
        title_label.setAlignment(Qt.AlignmentFlag.AlignCenter)
        title_label.setSizePolicy(QSizePolicy.Policy.Expanding, QSizePolicy.Policy.Fixed)

        # Description of the card
        desc_label = QLabel(description, card)
        desc_label.setFont(QFont("SF Pro Display", 12))
        desc_label.setAlignment(Qt.AlignmentFlag.AlignCenter)
        desc_label.setWordWrap(True)
        desc_label.setSizePolicy(QSizePolicy.Policy.Expanding, QSizePolicy.Policy.Fixed)

        # Button for the card
        button = QPushButton(title, card)
        button.setStyleSheet(self.button_style())
        button.clicked.connect(on_click)

        # Add widgets to the card layout
        card_layout.addWidget(title_label)
        card_layout.addWidget(desc_label)
        card_layout.addWidget(button)

        return card




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
                padding: 16px;
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

    def apply_style(self):
        self.setStyleSheet("""
            QWidget {
                background-color: #0f172a;
                color: #cbd5e1;
            }
        """)
