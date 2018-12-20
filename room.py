import hashlib


class Room:

    def __init__(self, name, address, max_num):
        hashcode = hashlib.md5()
        hashcode.update(name.encode("ascii"))
        self.hashcode = hashcode.hexdigest()
        self.name = name
        self.address = address + name
        self.max_num = max_num
        self.players = []
        self.score_list = dict()
        self.reception = True
        self.index = 0

    # 部屋の状況を確認する
    def check_vacancy(self):
        if len(self.players) >= int(self.max_num):
            self.reception = False

        if len(self.players) < int(self.max_num):
            self.reception = True

        return self.reception

    # プレイヤーを部屋に追加する
    def add_player(self, player):
        self.players.append(player)

    # プレイヤーを部屋から出す
    def remove_player(self, player):
        self.players.remove(player)
