import copy
import random

class Hat:
    def __init__(self, **kwargs):
        self.contents = []
        for color, count in kwargs.items():
            self.contents.extend([color] * count)
        
    def draw(self, num_balls_drawn):
        drawn_balls = []

        if num_balls_drawn >= len(self.contents):
            self.contents = []
            drawn_balls = self.contents
        else:
            for _ in range(num_balls_drawn):
                random_index = random.randint(0, len(self.contents) -1)
                drawn_balls.append(self.contents.pop(random_index))
        return drawn_balls

def experiment(hat, expected_balls, num_balls_drawn, num_experiments):
    count_successful = 0

    for _ in range(num_experiments):

        hat_copy = copy.deepcopy(hat)
        drawn_balls = hat_copy.draw(num_balls_drawn)

        success = True
        
        for color, count in expected_balls.items():
            if drawn_balls.count(color) < count:
                success = False
                break

        if success:
            count_successful += 1
        
    return count_successful/num_experiments


# Examle of use
hat = Hat(black=6, red=4, green=3)
probability = experiment(hat=hat,
                  expected_balls={"red":2,"green":1},
                  num_balls_drawn=5,
                  num_experiments=2000)
print(probability)