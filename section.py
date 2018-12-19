from room import Room

word_part_list1 = ["動詞編", "名詞編", "形容詞編", "副詞・その他", "すべて"]
word_part_list2 = ["動詞編", "名詞編", "形容詞編", "副詞", "すべて"]
word_part_list3 = ["動詞編", "名詞編", "形容詞編", "すべて"]


def generate_rooms():
    game_stages = [Part(1, 9), Part(2, 8), Part(3, 4)]
    return game_stages


class Part:
    def __init__(self, number, section_num):
        self.number = number
        self.sections = [Section(i + 1, str(number) + ",") for i in range(section_num)]


class Section:
    def __init__(self, number, address):
        self.number = number
        if address == "1," and (number <= 2 or number == 4):
            self.word_parts = [SectionPart(word_part_list1[i], address + str(number) + ",") for i in
                               range(len(word_part_list1))]
        elif address == "1," and number == 3:
            self.word_parts = [SectionPart(word_part_list2[i], address + str(number) + ",") for i in
                               range(len(word_part_list2))]
        else:
            self.word_parts = [SectionPart(word_part_list3[i], address + str(number) + ",") for i in
                               range(len(word_part_list3))]


class SectionPart:
    def __init__(self, part_name, address):
        self.part_name = part_name
        self.address = address + part_name + ","
        self.rooms = []

    def create_room(self, name, max_num):
        room = Room(name, self.address, max_num)
        self.rooms.append(room)
        return room
