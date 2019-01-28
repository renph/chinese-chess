class Piece:

    @staticmethod
    def getValidMoves(pieceName, pos, board):
        pieceMethod = {'j': Piece.Ju, 'm': Piece.Ma, 'p': Piece.Pao, 'z': Piece.Zu, 'b': Piece.Zu,
                       'x': Piece.Xiang, 's': Piece.Shi, 'c': Piece.Jiang}
        method = pieceMethod[pieceName[1]]
        return method(pieceName, pos, board)

    @staticmethod
    def Ju(pieceName, pos, board):
        moves = []
        r, c = pos
        direction = [(1, 0), (-1, 0), (0, -1), (0, 1)]  # up down left right
        dirFlag = [True for _ in range(len(direction))]
        for i in range(1, 10):
            for d in range(len(direction)):
                if not dirFlag[d]:
                    continue
                dr, dc = direction[d]
                row, col = r + dr * i, c + dc * i
                if 0 <= row <= 9 and 0 <= col <= 8:
                    p = board[row][col]
                    if p == 0:
                        moves.append((row, col))
                        continue
                    elif p[0] != pieceName[0]:
                        moves.append((row, col))
                dirFlag[d] = False
        return moves

    @staticmethod
    def Ma(pieceName, pos, board):
        moves = []
        r, c = pos
        direction = [(-1, 0), (1, 0), (0, -1), (0, 1)]  # up down left right
        atkPos = [((-2, -1), (-2, 1)), ((2, -1), (2, 1)),
                  ((-1, -2), (1, -2)), ((-1, 2), (1, 2))]
        for d in range(len(direction)):
            dr, dc = direction[d]
            row, col = r + dr, c + dc
            if 0 <= row <= 9 and 0 <= col <= 8 and board[row][col] == 0:
                for ar, ac in atkPos[d]:
                    aRow, aCol = r + ar, c + ac
                    if 0 <= aRow <= 9 and 0 <= aCol <= 8:
                        p = board[aRow][aCol]
                        if p == 0 or p[0] != pieceName[0]:
                            moves.append((r + ar, c + ac))
        return moves

    @staticmethod
    def Pao(pieceName, pos, board):
        moves = []
        r, c = pos
        direction = [(1, 0), (-1, 0), (0, -1), (0, 1)]  # up down left right
        dirFlag = [True for _ in range(len(direction))]
        atkFlag = [False for _ in range(len(direction))]
        for i in range(1, 10):
            for d in range(len(direction)):
                if not dirFlag[d]:
                    continue
                dr, dc = direction[d]
                row, col = r + dr * i, c + dc * i
                if 0 <= row <= 9 and 0 <= col <= 8:
                    p = board[row][col]
                    if p == 0:
                        if not atkFlag[d]:
                            moves.append((row, col))
                        continue
                    elif not atkFlag[d]:
                        atkFlag[d] = True
                        continue
                    elif p[0] != pieceName[0] and atkFlag[d]:
                        moves.append((row, col))
                dirFlag[d] = False
        return moves

    @staticmethod
    def Zu(pieceName, pos, board):
        moves = []
        r, c = pos
        direction = [(1, 0) if pieceName[1] == 'z' else (-1, 0)]
        if (pieceName[1] == 'z' and r > 4) or (pieceName[1] == 'b' and r <= 4):
            direction.extend([(0, -1), (0, 1)])
        for dr, dc in direction:
            row, col = r + dr, c + dc
            if 0 <= row <= 9 and 0 <= col <= 8:
                p = board[row][col]
                if p == 0 or p[0] != pieceName[0]:
                    moves.append((row, col))
        return moves

    @staticmethod
    def Xiang(pieceName, pos, board):
        moves = []
        r, c = pos
        direction = [(-1, -1), (-1, 1), (1, -1), (1, 1)]
        for d in range(len(direction)):
            dr, dc = direction[d]
            row, col = r + dr, c + dc
            if 0 <= row <= 9 and 0 <= col <= 8:
                p = board[row][col]
                if p == 0:
                    if (pieceName[0] == 'b' and row <= 4) \
                            or (pieceName[0] == 'r' and row > 4):
                        moves.append((row + dr, col + dc))
        return moves

    @staticmethod
    def Shi(pieceName, pos, board):
        r, c = pos
        moves = []
        if c != 4:
            row, col = (1, 4) if r < 4 else (8, 4)
            p = board[row][col]
            if p == 0 or p[0] != pieceName[0]:
                return [(row, col)]
        else:
            direction = [(-1, -1), (-1, 1), (1, -1), (1, 1)]
            for d in range(4):
                dr, dc = direction[d]
                row, col = r + dr, c + dc
                p = board[row][col]
                if p == 0 or p[0] != pieceName[0]:
                    moves.append((row, col))
        return moves

    @staticmethod
    def Jiang(pieceName, pos, board):
        r, c = pos
        moves = []
        direction = [(1, 0), (-1, 0), (0, -1), (0, 1)]  # up down left right
        for d in range(4):
            dr, dc = direction[d]
            row, col = r + dr, c + dc
            if 0 <= row <= 9 and 0 <= col <= 8:
                p = board[row][col]
                if p == 0 or p[0] != pieceName[0]:
                    moves.append((row, col))
        return moves


if __name__ == '__main__':
    board = [['bj0', 'bm0', 'bx0', 'bs0', 'bc', 'bs1', 'bx1', 'bm1', 'bj1'],
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
    m = Piece.getValidMoves('rj0', (8, 4), board)
    print(m)
