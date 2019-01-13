from PyQt5 import QtGui
from PyQt5.QtGui import QPixmap, QPalette, QColor
from PyQt5.QtWidgets import QMainWindow, QApplication, QLabel, QWidget


class TransparentWidget(QWidget):
    def __init__(self, parent, size, pos):
        print(size,pos)
        super().__init__(parent)
        self.move(pos)
        self.setFixedSize(200, 200)
        palette = QPalette()
        palette.setColor(QPalette.Background, QColor(255,220,220,200))
        self.setPalette(palette)
        self.setAutoFillBackground(True)
        # self.setBackgroundRole(QPalette.Window)

    # def mousePressEvent(self, a0: QtGui.QMouseEvent):
    #     print("tr", a0.pos())


class GameView(QMainWindow):
    def __init__(self):
        super().__init__()
        back = QPixmap("../res/board.png")
        self.setFixedSize(back.size())
        self.bg = QLabel(self)
        self.bg.setPixmap(back)
        self.bg.setFixedSize(back.size())
        self.setCentralWidget(self.bg)
        # lb = QLabel(self)
        # lb.setText("1234555")
        # lb.setFixedSize(self.bg.size())
        # lb.setPalette(QPalette(QColor(255,5,12,125)))
        # print(back.size())
        # print(lb.size())

        self.transparent = TransparentWidget(self, self.bg.size(),self.pos())

    def mousePressEvent(self, a0: QtGui.QMouseEvent):
        print("main",a0.pos())

class Piece():
    def __init__(self):
        pass

    def getValidMoves(self):
        pass


if __name__ == "__main__":
    app = QApplication([])
    view = GameView()
    view.show()
    app.exit(app.exec_())
