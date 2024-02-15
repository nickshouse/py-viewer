import os
from natsort import natsorted, ns
from PyQt5.QtWidgets import QApplication, QMainWindow, QAction, QLabel, QFileDialog
from PyQt5.QtGui import QPixmap
from PyQt5.QtCore import Qt
import sys

class ImageViewer(QMainWindow):
    def __init__(self):
        super().__init__()
        self.setWindowTitle('One Dark Image Viewer')
        self.setGeometry(100, 100, 800, 600)
        self.currentImagePath = None
        self.currentImageIndex = 0
        self.imageFiles = []
        self.initUI()

    def initUI(self):
        self.statusBar = self.statusBar()
        
        openAction = QAction('&Open Image', self)
        openAction.setShortcut('Ctrl+O')
        openAction.setStatusTip('Open image')
        openAction.triggered.connect(self.openImage)
        
        menubar = self.menuBar()
        fileMenu = menubar.addMenu('&File')
        fileMenu.addAction(openAction)
        
        self.imageLabel = QLabel(self)
        self.imageLabel.setAlignment(Qt.AlignCenter)
        self.setCentralWidget(self.imageLabel)
        
        self.applyOneDarkTheme()
    
    def openImage(self, filePath=None):
        if not filePath:
            filePath, _ = QFileDialog.getOpenFileName(self, "Open Image", "", "Image Files (*.png *.jpg *.jpeg *.bmp *.gif)")
            if not filePath:  # User cancelled the selection
                return  # Exit the method if no file was selected

        filePath = os.path.abspath(filePath)  # Convert to absolute path for consistency
        self.currentImagePath = filePath
        directory = os.path.dirname(filePath)
        # Construct absolute paths for comparison
        self.imageFiles = natsorted([os.path.abspath(os.path.join(directory, f)) for f in os.listdir(directory) if f.endswith(('png', 'jpg', 'jpeg', 'bmp', 'gif'))], alg=ns.IGNORECASE)

        if filePath in self.imageFiles:
            self.currentImageIndex = self.imageFiles.index(filePath)
            pixmap = QPixmap(filePath)
            self.imageLabel.setPixmap(pixmap.scaled(self.imageLabel.size(), Qt.KeepAspectRatio, Qt.SmoothTransformation))
            self.updateStatusBar()
        else:
            print(f"Debug: filePath not in imageFiles. FilePath: {filePath}")  # Debugging output
            for f in self.imageFiles:  # Debugging output
                print(f"Available: {f}")  # Debugging output
            self.statusBar.showMessage("Selected file is not in the current directory's list.")

    def wheelEvent(self, event):
        delta = event.angleDelta().y()
        if delta > 0 and self.imageFiles:  # Scroll up
            self.loadPreviousImage()

    def loadPreviousImage(self):
        if self.currentImageIndex > 0:
            self.currentImageIndex -= 1
        else:
            self.currentImageIndex = len(self.imageFiles) - 1

        nextImagePath = self.imageFiles[self.currentImageIndex]
        self.openImage(nextImagePath)

    def updateStatusBar(self):
        if self.currentImagePath:
            fileIndex = self.imageFiles.index(self.currentImagePath) + 1
            self.statusBar.showMessage(f"Image {fileIndex} of {len(self.imageFiles)} in directory (Sorted naturally)")

    def applyOneDarkTheme(self):
        self.setStyleSheet("""
            QMainWindow {
                background-color: #282c34;
            }
            QLabel {
                color: #abb2bf;
            }
            QMenuBar {
                background-color: #282c34;
                color: #abb2bf;
            }
            QMenuBar::item:selected {
                background-color: #3e4451;
            }
            QMenu {
                background-color: #282c34;
                color: #abb2bf;
            }
            QMenu::item:selected {
                background-color: #3e4451;
            }
        """)

def main():
    app = QApplication(sys.argv)
    viewer = ImageViewer()
    viewer.show()
    sys.exit(app.exec_())

if __name__ == "__main__":
    main()
