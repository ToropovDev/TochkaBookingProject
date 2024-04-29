def position_handler(position: id) -> str:
    match position:
        case 0:
            return "opposite"
        case 1:
            return "outside_1"
        case 2:
            return "outside_2"
        case 3:
            return "setter"
        case 4:
            return "middle_1"
        case 5:
            return "middle_2"
        case 6:
            return "libero"
        case _:
            raise Exception("Invalid position")
