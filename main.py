#pass
from ants import Anthill

if __name__ == "__main__":
    anthill = Anthill(file_number=3)
    anthill.init_movement()
    anthill.simulate_ants_movement_with_multiple_paths("Sv", "Sd")
