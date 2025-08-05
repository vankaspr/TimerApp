from PyQt5.QtWidgets import QMainWindow

class TimerWindow(QMainWindow):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Timer-App")
        self.setFixedSize(300, 200)

        # Экземпляр таймера




if __name__ == "__main__":
    import sys
    from PyQt5.QtWidgets import  QApplication
    app = QApplication(sys.argv)
    window = TimerWindow()
    window.show()
    sys.exit(app.exec_())
