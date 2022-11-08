from PyQt5.QtWidgets import QMainWindow, QApplication, QMenu, QMenuBar, QAction, QFileDialog, QLabel, QColorDialog, QInputDialog, QMessageBox
from PyQt5.QtGui import QIcon, QImage, QPainter, QPen, QBrush, QColor, QPixmap
from PyQt5.QtCore import Qt, QPoint
import sys,ast
# import cv2

class Window(QMainWindow):
    def __init__(self):
        super().__init__()
        global p_path
        print(p_path)
        pixmap = QPixmap(p_path)
        title = "Paint Pointlist details"
        top = 400
        left = 400
        width = 800
        height = 600

        icon = "icons/pain.png"

        self.setWindowTitle(title)
        self.setGeometry(top, left, width, height)
        self.setWindowIcon(QIcon(icon))
        self.image = QImage(self.size(), QImage.Format_RGB32)
        self.image = pixmap #Qt.white
        self.resize(self.image.width(), self.image.height())
      #  self.image.fill(Qt.white)


        self.drawing = False
        self.brushSize = 2
        self.brushColor = Qt.black
        self.lastPoint = QPoint()

        mainMenu = self.menuBar()
        fileMenu = mainMenu.addMenu("File")
        brushSize = mainMenu.addMenu("Brush Size")
        brushColor = mainMenu.addMenu("Brush Color")

        saveAction = QAction(QIcon("icons/save.png"), "Save",self)
        saveAction.setShortcut("Ctrl+S")
        fileMenu.addAction(saveAction)
        saveAction.triggered.connect(self.save)

        clearAction = QAction(QIcon("icons/clear.png"), "Close", self)
        clearAction.setShortcut("Ctrl+C")
        fileMenu.addAction(clearAction)
        clearAction.triggered.connect(self.close_application)

        threepxAction = QAction( QIcon("icons/threepx.png"), "Brush Size", self)
        brushSize.addAction(threepxAction)
        threepxAction.triggered.connect(self.getInteger)
        
        fivepxAction = QAction(QIcon("icons/fivepx.png"), "5px", self)
        brushSize.addAction(fivepxAction)
        fivepxAction.triggered.connect(self.fivePixel)
        
        sevenpxAction = QAction(QIcon("icons/sevenpx.png"),"7px", self)
        brushSize.addAction(sevenpxAction)
        sevenpxAction.triggered.connect(self.sevenPixel)
        
        ninepxAction = QAction(QIcon("icons/ninepx.png"), "9px", self)
        brushSize.addAction(ninepxAction)
        ninepxAction.triggered.connect(self.ninePixel)
        
        choosecolorAction = QAction(QIcon("icons/black.png"), "Choose color", self)
        choosecolorAction.setShortcut("Ctrl+B")
        brushColor.addAction(choosecolorAction)
        choosecolorAction.triggered.connect(self.color_picker)

        


    def mousePressEvent(self, event):
        if event.button() == Qt.LeftButton:
            self.drawing = True
            self.lastPoint = event.pos()
            #print(self.lastPoint)


    def mouseMoveEvent(self, event):
        if(event.buttons() & Qt.LeftButton) & self.drawing:
            painter = QPainter(self.image)
            painter.setPen(QPen(self.brushColor, self.brushSize, Qt.SolidLine, Qt.RoundCap, Qt.RoundJoin))
            painter.drawLine(self.lastPoint, event.pos())
            self.lastPoint = event.pos()
            self.update()



    def mouseReleaseEvent(self, event):

        if event.button() == Qt.LeftButton:
            self.drawing = False


    def paintEvent(self, event):
        canvasPainter  = QPainter(self)
        canvasPainter.drawPixmap(self.rect(),self.image)#, self.image.rect() )




    def save(self):
        filePath, _ = QFileDialog.getSaveFileName(self, "Save Image", "", "PNG(*.png);;JPEG(*.jpg *.jpeg);;All Files(*.*) ")

        if filePath == "":
            return
        self.image.save(filePath)


    def close_application(self):
        choice = QMessageBox.question(self, 'Extract!',
                                            "Do you want to close ?",
                                            QMessageBox.Yes | QMessageBox.No)
        if choice == QMessageBox.Yes:
            print("Yes!!!!")
            sys.exit()
        else:
            pass

    def getInteger(self):
        i, okPressed = QInputDialog.getInt(self, "Get integer","Brush Size:", 2, 0, 30, 1)
        if okPressed:
            self.brushSize = i

    def clear(self):
        self.image.fill(Qt.white)
        self.update()


    def threePixel(self):
        self.brushSize = 3
    
    def fivePixel(self):
        self.brushSize = 5
    
    def sevenPixel(self):
        self.brushSize = 7
    
    def ninePixel(self):
        self.brushSize = 9

    def color_picker(self):
        color = QColorDialog.getColor()
        self.brushColor = color


p_path = sys.argv[1]
# print(ar[1])
app = QApplication(sys.argv)
window = Window()
window.show()
app.exec()
