import random
import math
import copy


class Node:
    def __init__(self, parent=None, chess_board=None, color=0):
        """
        节点类,表示博弈树中的一个节点

        Args:
            parent (Node): 父节点
            chess_board (ChessBoard): 棋盘状态
            color (int): 节点的颜色,1表示黑棋,-1表示白棋
        """
        self.parent = parent
        self.chess_board = chess_board
        self.color = color
        self.visits = 0
        self.value = 0
        self.children = []


def get_win_rate(node):
    """
    计算节点的胜率。

    Args:
        node (Node): 节点

    Returns:
        float: 胜率
    """
    return (node.value / (2*node.visits)) + 0.5


class Agent:
    def __init__(self, chess_board, max_searches):
        """
        博弈代理类，负责搜索最优的棋盘移动。

        Args:
            chess_board (ChessBoard): 初始棋盘状态
            max_searches (int): 搜索的最大次数
        """
        self.root = Node(chess_board=chess_board, color=-chess_board.now_playing)
        self.current_node = self.root
        self.max_searches = max_searches

    def update_root(self, move):
        """
        更新根节点，处理对手的移动。

        Args:
            move (tuple): 对手的移动坐标

        Returns:
            tuple: 当前根节点的访问次数和父节点访问次数的比例
        """
        if self.root.children != []:
            for child in self.root.children:
                if child.chess_board.moves[-1] == move:
                    children_count = len(self.root.children)
                    parent_visits = self.root.visits

                    self.root = child
                    self.root.parent = None

                    return self.root.visits, (parent_visits/children_count)

        chess_board = copy.deepcopy(self.root.chess_board)
        chess_board.play_stone(move)
        self.root = Node(chess_board=chess_board, color=-chess_board.now_playing)
        return 0, 0

    def expand(self):
        """
        展开当前节点，生成子节点。
        """
        vacancies = self.current_node.chess_board.adjacent_vacancies()
        for move in vacancies:
            chess_board = copy.deepcopy(self.current_node.chess_board)
            chess_board.play_stone(move)
            child = Node(
                parent=self.current_node,
                chess_board=chess_board,
                color=-chess_board.now_playing
            )
            self.current_node.children.append(child)

    def roll_out(self):
        """
        随机模拟游戏直到结束,返回游戏结果

        Returns:
            int: 游戏结果,1表示当前节点颜色获胜,-1表示对手颜色获胜,0表示平局
        """
        chess_board = copy.deepcopy(self.current_node.chess_board)
        while not chess_board.is_ended():
            vacancies = chess_board.adjacent_vacancies()
            loc = random.choice(list(vacancies))
            chess_board.play_stone(loc)
        if chess_board.winner == self.current_node.color:
            return 1
        elif chess_board.winner == -self.current_node.color:
            return -1
        else:
            return 0

    def back_propagate(self, value):
        """
        回溯更新节点的访问次数和值。

        Args:
            value (int): 游戏结果,1表示当前节点颜色获胜,-1表示对手颜色获胜,0表示平局
        """
        while self.current_node.parent is not None:
            self.current_node.visits += 1
            self.current_node.value += value
            self.current_node = self.current_node.parent
            value *= -1

        self.root.visits += 1

    def search(self):
        """
        搜索最优移动。

        Returns:
            tuple: 最优移动的坐标，代理的胜率，以及每个子节点的胜率矩阵
        """
        for _ in range(self.max_searches):
            self.current_node = self.root

            # 不是叶节点->选择ucb最大的子节点
            while self.current_node.children != []:
                # 随机选择未访问节点
                zero_visits = []
                for child in self.current_node.children:
                    if child.visits == 0:
                        zero_visits.append(child)
                if zero_visits != []:
                    self.current_node = random.choice(zero_visits)

                # 选择ucb最大的子节点
                else:
                    ucb = lambda node: (node.value / node.visits) + (2 * (math.log(node.parent.visits) / node.visits) ** 0.5)
                    # ucb = lambda node: get_win_rate(node) + (2 * (math.log(node.parent.visits) / node.visits) ** 0.5)
                    ucb_list = [ucb(child) for child in self.current_node.children]
                    idx_max = ucb_list.index(max(ucb_list))
                    self.current_node = self.current_node.children[idx_max]

            if self.current_node.chess_board.is_ended():
                if self.current_node.chess_board.winner == self.current_node.color:
                    value = 1
                elif self.current_node.chess_board.winner == -self.current_node.color:
                    value = -1
                else:
                    value = 0

                self.back_propagate(value)
                continue

            if (self.current_node.visits != 0) or (self.current_node.parent is None):
                self.expand()
                self.current_node = self.current_node.children[0]

            value = self.roll_out()
            self.back_propagate(value)

        best_child = max(self.root.children, key=lambda child: get_win_rate(child))
        # 创建一个胜率矩阵，记录每个子节点的胜率
        l = [[0 for i in range(10)] for j in range(10)]
        for ch in self.root.children:
            x, y = ch.chess_board.moves[-1]
            l[x][y] = get_win_rate(ch)
        # for i in range(10):
        #     print(l[i])
        agent_win_rate = get_win_rate(best_child)
        loc = best_child.chess_board.moves[-1]

        self.root = best_child
        self.root.parent = None
        return loc, agent_win_rate, l
