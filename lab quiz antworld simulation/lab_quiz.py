import random
import os
import time

# Base Ant class
class Ant:
    def __init__(self, x, y):
        self.x = x
        self.y = y
        self.step_count = 0

    def move(self, grid_width, grid_height, max_distance):
        dx = random.randint(-max_distance, max_distance)
        dy = random.randint(-max_distance, max_distance)
        self.x = max(0, min(grid_width - 1, self.x + dx))
        self.y = max(0, min(grid_height - 1, self.y + dy))
        self.step_count += 1

    def can_eat(self, other_ant):
        return False

    def get_symbol(self):
        return "?"


class AntA(Ant):
    def move(self, grid_width, grid_height):
        super().move(grid_width, grid_height, max_distance=1)

    def can_eat(self, other_ant):
        return isinstance(other_ant, AntB)

    def get_symbol(self):
        return "A"

class AntB(Ant):
    def move(self, grid_width, grid_height):
        super().move(grid_width, grid_height, max_distance=random.randint(1,2))

    def can_eat(self, other_ant):
        return isinstance(other_ant, AntC)

    def get_symbol(self):
        return "B"

class AntC(Ant):
    def move(self, grid_width, grid_height):
        super().move(grid_width, grid_height, max_distance=random.randint(1, 3))

    def can_eat(self, other_ant):
        return isinstance(other_ant, AntA)

    def get_symbol(self):
        return "C"

# Simulation System
class AntWorld:
    def __init__(self, width=60, height=20, num_ants=30):
        self.width = width
        self.height = height
        self.ants = []

        # Initialize 30 ants of each type
        for _ in range(num_ants):
            self.ants.append(AntA(random.randint(0, width - 1), random.randint(0, height - 1)))
            self.ants.append(AntB(random.randint(0, width - 1), random.randint(0, height - 1)))
            self.ants.append(AntC(random.randint(0, width - 1), random.randint(0, height - 1)))

    def update_grid(self):
        """Handles the eating mechanism: removes ants that get eaten."""
        positions = {}
        for ant in self.ants:
            pos = (ant.x, ant.y)
            if pos not in positions:
                positions[pos] = []
            positions[pos].append(ant)

        # Resolve eating interactions
        new_ants = []
        for pos, ants_at_pos in positions.items():
            if len(ants_at_pos) == 1:
                new_ants.append(ants_at_pos[0])
            else:
                # Determine survival based on eating rules
                survivors = ants_at_pos[:]
                for predator in ants_at_pos:
                    for prey in ants_at_pos:
                        if predator.can_eat(prey) and prey in survivors:
                            survivors.remove(prey)
                new_ants.extend(survivors)

        self.ants = new_ants

    def reproduce_ants(self):
        new_ants = []
        for ant in self.ants:
            if ant.step_count % 5 == 0 and random.random() < 0.1:  # 10% chance to reproduce
                new_x = max(0, min(self.width - 1, ant.x + random.choice([-1, 1])))
                new_y = max(0, min(self.height - 1, ant.y + random.choice([-1, 1])))
                new_ants.append(type(ant)(new_x, new_y))  # Creates new ant of same type
        self.ants.extend(new_ants)

    def check_winner(self):
        #Checks if only one ant type remains, stopping the simulation.
        types_present = {type(ant) for ant in self.ants}
        return len(types_present) == 1

    def count_ants(self):
        #Counts the number of each type of ant and prints the result.
        count_a = sum(1 for ant in self.ants if isinstance(ant, AntA))
        print(f"Ant A: {count_a}")

        count_b = sum(1 for ant in self.ants if isinstance(ant, AntB))
        print(f"Ant B: {count_b}")

        count_c = sum(1 for ant in self.ants if isinstance(ant, AntC))
        print(f"Ant C: {count_c}")

    def display(self):
        """Displays the grid with ants and population count."""
        os.system("cls" if os.name == "nt" else "clear")  # Clear console
        grid = [["." for _ in range(self.width)] for _ in range(self.height)]

        # Place ants in the grid
        for ant in self.ants:
            grid[ant.y][ant.x] = ant.get_symbol()

        # Print grid
        for row in grid:
            print("".join(row))

        # Print number of each ant type
        self.count_ants()

    def run(self):
        """Runs the simulation loop for up to 2000 steps."""
        for step in range(1, 2001):
            for ant in self.ants:
                ant.move(self.width, self.height)
            self.update_grid()
            self.reproduce_ants()
            self.display()
            print(f"Step => {step}")

            # Stop if only one type of ant remains
            if self.check_winner():
                print("Simulation ended: Only one type of ant remains.")
                break

            if step == 2000:
                print("Simulation ended: Maximum number of steps reached.")
                break
            time.sleep(0.1)  # Delay for better visualization
        
# Run the simulation
if __name__ == "__main__":
    sim = AntWorld()
    sim.run()