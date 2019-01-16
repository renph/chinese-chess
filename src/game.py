from PyQt5 import QtGui
from PyQt5.QtCore import Qt
from PyQt5.QtGui import QPixmap, QPalette, QColor, QPainter
from PyQt5.QtWidgets import QMainWindow, QApplication, QLabel, QWidget


class TransparentWidget(QWidget):
    def __init__(self, parent, size, pos):
        super().__init__(parent)
        # print(size, pos)
        self.move(pos)
        self.setFixedSize(size)
        palette = QPalette()
        palette.setColor(QPalette.Background, QColor(255, 220, 220, 0))
        self.setPalette(palette)
        self.setAutoFillBackground(True)
        self.setMouseTracking(True)
        self.position = None
        self.cellSize = 67
        self.riverSize = self.cellSize + 14
        self.boardSize = (85, 45, 622 - 84, 662 - 45)

        self.mousePos = (-1, -1)
        # self.setBackgroundRole(QPalette.Window)

    def updateMousePos(self, pos):
        board_x, board_y, board_w, board_h = self.boardSize
        x = pos.x() - board_x
        y = pos.y() - board_y
        if y > 346:
            y -= 15
        mx = x // self.cellSize + (1 if x % self.cellSize > 33 else 0)
        my = y // self.cellSize + (1 if y % self.cellSize > 33 else 0)
        self.mousePos = (mx, my)

    def updateShadow(self, pos):
        self.position = pos
        self.update()
        # print(self.position)

    def mouseMoveEvent(self, a0: QtGui.QMouseEvent):
        # print("mouse move")
        self.position = a0.pos()
        self.updateMousePos(self.position)

        self.update()

    def paintEvent(self, a0: QtGui.QPaintEvent):
        painter = QPainter(self)
        pen = painter.pen()
        pen.setColor(QColor(Qt.red))
        pen.setWidth(20)
        pen.setStyle(Qt.SolidLine)
        painter.setPen(pen)
        # if self.position is not None:
        #     painter.drawEllipse(self.position, 3, 3)

        board_x, board_y, board_w, board_h = self.boardSize

        pen.setWidth(3)
        # pen.setColor(Qt.red)
        painter.setPen(pen)

        mx, my = self.mousePos
        cursor_width, cursor_len = 30, 10
        if 0 <= mx <= 8 and 0 <= my <= 9:
            cx, cy = mx * self.cellSize + board_x, my * self.cellSize + board_y
            if my > 4:
                cy += 14
            x1, y1 = cx - cursor_width, cy - cursor_width  # upper left
            x2, y2 = cx + cursor_width, cy - cursor_width  # upper right
            x3, y3 = cx - cursor_width, cy + cursor_width  # bottom left
            x4, y4 = cx + cursor_width, cy + cursor_width  # bottom right
            painter.drawLine(x1, y1, x1, y1 + cursor_len)
            painter.drawLine(x1, y1, x1 + cursor_len, y1)
            painter.drawLine(x2, y2, x2 - cursor_len, y2)
            painter.drawLine(x2, y2, x2, y2 + cursor_len)

            painter.drawLine(x3, y3, x3, y3 - cursor_len)
            painter.drawLine(x3, y3, x3 + cursor_len, y3)
            painter.drawLine(x4, y4, x4 - cursor_len, y4)
            painter.drawLine(x4, y4, x4, y4 - cursor_len)

    def mousePressEvent(self, a0: QtGui.QMouseEvent):
        print("tr", a0.pos())


class GameView(QMainWindow):
    def __init__(self):
        super().__init__()
        back = QPixmap("../res/board.png")
        self.setFixedSize(back.size())
        self.bg = QLabel(self)
        self.bg.setPixmap(back)
        self.bg.setFixedSize(back.size())
        self.setCentralWidget(self.bg)
        self.transparent = TransparentWidget(self, self.bg.size(), self.pos())

    def mousePressEvent(self, a0: QtGui.QMouseEvent):
        print("main",a0.pos())
        self.transparent.updateShadow(a0.pos())

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
