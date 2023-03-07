import sys
import os
from PyQt5.QtWidgets import QApplication, QWidget, QPushButton, QVBoxLayout, QMessageBox

class AnonsurfOSX(QWidget):
    def __init__(self):
        super().__init__()
        self.initUI()

    def initUI(self):
        # Create start button
        self.startButton = QPushButton('Start Tor Routing', self)
        self.startButton.setToolTip('Start routing traffic through Tor')
        self.startButton.clicked.connect(self.startTorRouting)

        # Create stop button
        self.stopButton = QPushButton('Stop Tor Routing', self)
        self.stopButton.setToolTip('Stop routing traffic through Tor')
        self.stopButton.clicked.connect(self.stopTorRouting)

        # Create restart button
        self.restartButton = QPushButton('Restart Tor Routing', self)
        self.restartButton.setToolTip('Restart Tor routing with a new entry node')
        self.restartButton.clicked.connect(self.restartTorRouting)

        # Create layout for buttons
        vbox = QVBoxLayout()
        vbox.addWidget(self.startButton)
        vbox.addWidget(self.stopButton)
        vbox.addWidget(self.restartButton)

        # Set window layout
        self.setLayout(vbox)
        self.setGeometry(100, 100, 300, 150)
        self.setWindowTitle('Tor Router')
        self.show()

    def startTorRouting(self):
        # Install Tor using Homebrew
        # os.system("brew install tor")

        # Configure network settings to use Tor as a proxy
        os.system("networksetup -setsocksfirewallproxy Wi-Fi 127.0.0.1 9050 on")

        # Start Tor as a background process
        os.system("tor &")

        # Test Tor connection
        output = os.popen("curl --socks5 127.0.0.1:9050 https://check.torproject.org/").read()

        # Check if Tor connection is successful
        if "Congratulations" in output:
            QMessageBox.information(self, "Tor Router", "Tor routing started successfully.")
        else:
            QMessageBox.critical(self, "Tor Router", "Failed to start Tor routing.")

    def stopTorRouting(self):
        # Stop Tor process
        os.system("killall tor")

        # Reset network settings to not use a proxy
        os.system("networksetup -setsocksfirewallproxystate Wi-Fi off")

        QMessageBox.information(self, "Tor Router", "Tor routing stopped.")

    def restartTorRouting(self):
        self.stopTorRouting()
        self.startTorRouting()

if __name__ == '__main__':
    app = QApplication(sys.argv)
    anonsurf_macos = AnonsurfOSX()
    sys.exit(app.exec_())
