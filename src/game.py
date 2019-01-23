import traceback

from PyQt5 import QtGui
from PyQt5.QtCore import Qt, QPoint
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
        self._selected = None
        # self.setBackgroundRole(QPalette.Window)

    @property
    def cursorPosition(self):
        return self.mousePos

    @cursorPosition.setter
    def cursorPosition(self, pos):
        if self.mousePos != pos:
            my, mx = pos
            if 0 <= mx <= 8 and 0 <= my <= 9:
                self.mousePos = (my, mx)
            else:
                self.mousePos = (-1, -1)
            self.update()

    @property
    def selectedPiece(self):
        return self._selected

    @selectedPiece.setter
    def selectedPiece(self, sel):
        self._selected = sel
        if sel is not None:
            row, col = sel
            px = 85 + 67 * col
            py = 45 + 67 * row
            if row > 4:
                py += 15
            self._selected = (px, py)
        self.update()


    def mouseMoveEvent(self, a0: QtGui.QMouseEvent):
        # event redirect
        self.parent().mouseMoveEvent(a0)

    def updateShadow(self, pos):
        self.position = pos
        self.update()
        # print(self.position)

    def updateCursor(self, pos):
        if self.mousePos != pos:
            self.mousePos = pos
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

        my, mx = self.mousePos
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

        if self.selectedPiece is not None:
            mx, my = self.selectedPiece
            # print("draw ell {}".format(self.selectedPiece))
            painter.drawEllipse(QPoint(mx, my), 20, 20)

    # def mousePressEvent(self, a0: QtGui.QMouseEvent):
    #     print("tr", a0.pos())


class ChessGameModel:
    def __init__(self, rev=False):
        self.board = [['bj0', 'bm0', 'bx0', 'bs0', 'bc', 'bs1', 'bx1', 'bm1', 'bj1'],
                      [0, 0, 0, 0, 0, 0, 0, 0, 0],
                      [0, 'bp0', 0, 0, 0, 0, 0, 'bp1', 0],
                      ['bz0', 0, 'bz1', 0, 'bz2', 0, 'bz3', 0, 'bz4'],
                      [0, 0, 0, 0, 0, 0, 0, 0, 0],
                      [0, 0, 0, 0, 0, 0, 0, 0, 0],
                      ['rb0', 0, 'rb1', 0, 'rb2', 0, 'rb3', 0, 'rb4'],
                      [0, 'rp0', 0, 0, 0, 0, 0, 'rp1', 0],
                      [0, 0, 0, 0, 0, 0, 0, 0, 0],
                      ['rj0', 'rm0', 'rx0', 'rs0', 'rc', 'rs1', 'rx1', 'rm1', 'rj1'],
                      ]
        # print(self.board)

    def getValidMoves(self, pieceName, pos):
        if pieceName[1] in 'zb':
            pass
        elif pieceName[1] == 'j':
            pass

    def getAllValidMoves(self):
        pass
    def get(self, pos):
        row, col = pos
        if 0 <= row <= 9 and 0 <= col <= 8:
            return self.board[row][col]

    def __getitem__(self, item):
        """[] operator overload"""
        return self.board[item]

    def isValidMove(self, sr, sc, dr, dc):
        if self.board[sr][sc] == 0 or not (0 <= dr <= 9) or not (0 <= dc <= 8):
            return False

        return True

    def moveTo(self, sr, sc, dr, dc):
        print('game model move to')
        if self.isValidMove(sr, sc, dr, dc):
            self.board[dr][dc] = self.board[sr][sc]
            self.board[sr][sc] = 0
            return True


class GameController:
    def __init__(self):
        self.gameMdl = ChessGameModel()
        self.isNewGame = True
        # print(self.gameMdl[0][0])
        self.view = GameView(self)
        self.view.show()

    def newGame(self):
        self.isNewGame = True

    def moveTo(self, src, des):
        if not self.isNewGame:
            return
        sr, sc = src
        dr, dc = des
        srcName = self.gameMdl[sr][sc]
        desName = self.gameMdl[dr][dc]
        print("move {} from {} to {}".format(srcName, src, des))
        if self.gameMdl.moveTo(sr, sc, dr, dc) is not None:
            print("move {} from {} to {}".format(srcName, src, des))
            self.view.afterMove(srcName, desName)


class GameView(QMainWindow):
    def __init__(self, controller):
        super().__init__()
        self.controller = controller

        self.setMouseTracking(True)
        self.mousePos = (-1, -1)
        self._src = None
        self.des = None

        back = QPixmap("../res/board.png")
        self.setFixedSize(back.size())
        self.bg = QLabel(self)
        self.bg.setPixmap(back)
        self.bg.setFixedSize(back.size())
        self.setCentralWidget(self.bg)
        self.boardSize = (85, 45, 622 - 84, 662 - 45)
        self.cellSize = 67
        self.pieces = dict()
        self.initPieces()
        self.transparent = TransparentWidget(self, self.bg.size(), self.pos())

    @property
    def src(self):
        return self._src

    @src.setter
    def src(self, pos):
        self._src = pos
        if self._src == (-1, -1):
            self._src = None
        self.transparent.selectedPiece = self._src

    def afterMove(self, srcName, desName):
        if desName != 0:
            desPiece = self.pieces[desName]
            desPiece.setVisible(False)
        srcPiece = self.pieces[srcName]
        srcPiece.move(*self.getPiecePos(*self.des))

    def resetFlags(self):
        self.src = None
        self.des = None

    def updateMousePos(self, pos):
        board_x, board_y, board_w, board_h = self.boardSize
        x = pos.x() - board_x
        y = pos.y() - board_y
        if y > 346:
            y -= 15
        mx = x // self.cellSize + (1 if x % self.cellSize > 33 else 0)
        my = y // self.cellSize + (1 if y % self.cellSize > 33 else 0)
        if 0 <= my <= 9 and 0 <= mx <= 8:
            self.mousePos = (my, mx)
        else:
            self.mousePos = (-1, -1)

    def mouseReleaseEvent(self, a0: QtGui.QMouseEvent):
        print("main release")
        if a0.button() == Qt.LeftButton:
            print("click on pos {}".format(self.mousePos))
            row, col = self.mousePos
            if 0 <= row <= 9 and 0 <= col <= 8:
                # if click again, cancel selecting
                if self.mousePos == self.src:
                    self.src = None
                elif self.src is None:
                    if self.controller.gameMdl.get(self.mousePos):
                        self.src = self.mousePos
                elif self.des is None:
                    self.des = self.mousePos
                    print("move pieces")
                    self.controller.moveTo(self.src, self.des)
                    self.resetFlags()
            else:
                self.resetFlags()

    def mouseMoveEvent(self, a0: QtGui.QMouseEvent):
        # print("mouse move")
        self.updateMousePos(a0.pos())
        self.transparent.cursorPosition = self.mousePos

    def getPiecePos(self, row, col):
        # px,py,_,_ = self.boardSize
        px = 85 + 67 * col - 34
        py = 45 + 67 * row - 34
        if row > 4:
            py += 15
        return px, py

    def initPieces(self):
        for row in range(10):
            for col in range(9):
                # print(self.controller.gameMdl[row][col])
                pieceName = self.controller.gameMdl[row][col]
                if pieceName != 0:
                    path = '../res/{}.png'.format(pieceName[:2])
                    # print(path)
                    piece = QLabel(self)
                    piece.setPixmap(QPixmap(path))
                    piece.setFixedSize(piece.pixmap().size())
                    px, py = self.getPiecePos(row, col)
                    piece.move(px, py)
                    self.pieces[pieceName] = piece

    # def mousePressEvent(self, a0: QtGui.QMouseEvent):
    #     print("main", a0.pos())
    #     self.transparent.updateShadow(a0.pos())


class Piece():
    def __init__(self):
        pass

    def getValidMoves(self):
        pass


if __name__ == "__main__":
    app = QApplication([])
    game = GameController()
    app.exit(app.exec_())
