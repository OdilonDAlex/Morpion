
from tinydb import TinyDB
from tinydb.storages import MemoryStorage

ICONS = {
    "circle" : "data/circle.png",
    "cross"  : "data/cross.png"
}

class Pion:

    database = TinyDB(storage=MemoryStorage)

    def __init__(self, type_, position_):

        self.type = type_

        self.icon = ICONS.get(self.type)

        self.position = position_

    def __str__(self):
        return f"Pion(type : {self.type})"

    def __repr__(self):
        return f"Pion(Pos({self.position}))"

    def change_pos(self, new_pos):
        for pion in get_all_pion():
            if new_pos == pion.position:
                print("Error")
                return False

        self.position = new_pos
        return True

    def save_pion(self):
        return Pion.database.insert(self.__dict__)

    def verif_game(self):
        same_type_in_same_row = 0
        same_type_in_same_col = 0
        same_type_in_diag = 0

        for pion in [pions for pions in get_all_pion() if ( pions.type == self.type and pions.position != self.position )]:
            if any([tuple(pos+1 for pos in list(pion.position)) == self.position,
                    tuple(pos-1 for pos in list(pion.position)) == self.position,
                    tuple(pos+2 for pos in list(pion.position)) == self.position,
                    tuple(pos-2 for pos in list(pion.position)) == self.position,
                    (pion.position[0] + 1, pion.position[1] - 1) == self.position,
                    (pion.position[0] - 1, pion.position[1] + 1) == self.position,
                    (pion.position[0] - 2, pion.position[1] + 2) == self.position,
                    (pion.position[0] + 2, pion.position[1] - 2) == self.position]):
                same_type_in_diag += 1

            if pion.position[1] == self.position[1]:
                same_type_in_same_col += 1

            if pion.position[0] == self.position[0]:
                same_type_in_same_row += 1

        if any([same_type_in_same_row == 2, same_type_in_diag == 2, same_type_in_same_col == 2]):
            return True

        return False


def get_all_pion():
    all_pion = []
    for pion in Pion.database.all():
        all_pion.append(Pion(pion.get("type"), pion.get("position")))

    return all_pion


if __name__ == "__main__":
    pion = Pion(type_="Circle red", position_=(0, 0))
    pion_1 = Pion(type_="Circle red", position_=(0, 1))

    pion.save_pion()
    pion_1.save_pion()

    print(pion_1.change_pos((0, 1)))

    print(get_all_pion())
