import sys
from PyQt6.QtWidgets import QApplication, QMainWindow, QPushButton, QVBoxLayout, QWidget
import subprocess
import os

class MainWindow(QMainWindow):
    def __init__(self):
        super().__init__()

        self.setWindowTitle("Signify")
        self.setGeometry(100, 100, 600, 400)  # Window size

        self.center()

        # Create buttons for choosing control mode
        self.button_hand = QPushButton("Hand Control")
        self.button_face = QPushButton("Face Control")

        # Button style
        self.button_hand.setStyleSheet("""
            QPushButton {
                background-color: #00FF00;
                color: black;
                font-size: 20px;
                border-radius: 12px;
                border: 2px solid #00FF00;
            }
            QPushButton:hover {
                background-color: #00CC00;
            }
        """)

        self.button_face.setStyleSheet("""
            QPushButton {
                background-color: #FF00FF;
                color: black;
                font-size: 20px;
                border-radius: 12px;
                border: 2px solid #FF00FF;
            }
            QPushButton:hover {
                background-color: #CC00CC;
            }
        """)

        # Signals for buttons
        self.button_hand.clicked.connect(self.run_hand_control)
        self.button_face.clicked.connect(self.run_face_control)

        # Main layout
        layout = QVBoxLayout()
        layout.addWidget(self.button_hand)
        layout.addWidget(self.button_face)

        # Middle widget and layout settings
        central_widget = QWidget()
        central_widget.setLayout(layout)
        self.setCentralWidget(central_widget)

        self.selected_mode = None  # Initialize selected_mode to None

    def run_hand_control(self):
        """Run hand control mode"""
        self.selected_mode = "hands"
        self.close()  # Close the window when a mode is selected

    def run_face_control(self):
        """Run face control mode"""
        self.selected_mode = "face"
        self.close()  # Close the window when a mode is selected

    def center(self):
        """Center window on screen"""
        screen_geometry = QApplication.primaryScreen().availableGeometry()
        frame_geometry = self.frameGeometry()
        center_point = screen_geometry.center()
        frame_geometry.moveCenter(center_point)
        self.move(frame_geometry.topLeft())

def run_gui():
    """Start GUI interface and return selected mode"""
    app = QApplication(sys.argv)
    window = MainWindow()
    window.show()
    app.exec()
    return window.selected_mode  # Return the selected mode after the GUI is closed
