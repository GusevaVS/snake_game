import cv2
import numpy as np
import cvzone
import math
import random

class SnakeGame:
    def __init__(self, path_food):
        self.points = [] # all points of the snake
        self.lengths = [] #distance between each point
        self.current_length = 0 # the total length of the snake
        self.allowed_length = 150 #total allowed length
        self.previous_head = 0, 0 # previous head point

        self.img_food = cv2.imread(path_food, cv2.IMREAD_UNCHANGED)
        self.height_food, self.width_food, _ = self.img_food.shape
        self.food_point = 0, 0
        self.random_food_location()

        self.score = 0
        self.game_over = False


    def random_food_location(self):
        """Generate random x, y coordinates of new portion of snake's food"""
        self.food_point = random.randint(100, 1000), random.randint(100, 600)


    def check_eat(self, curr_x, curr_y):
        """Checks if the snake ate food. If it happened the length and score
        of the snake would increase"""
        rx, ry = self.food_point
        if rx - self.width_food // 2 < curr_x < rx + self.width_food // 2\
               and ry - self.height_food // 2 < curr_y < ry + \
               self.height_food // 2:
            self.random_food_location()
            self.allowed_length += 50
            self.score += 1


    def draw_snake(self, img):
        """Takes the image of the screen and draws the snake on it"""
        if self.points:
            for i, point in enumerate(self.points):
                if i != 0:
                    cv2.line(img, self.points[i - 1], self.points[i],
                             (0,51,0), 20)
                    cv2.circle(img, self.points[-1], 20,(248, 23, 62),
                               cv2.FILLED)


    def draw_food(self, img):
        """Takes the image of the screen and returns it with the
        food visualization on it"""
        random_x, random_y = self.food_point
        img = cvzone.overlayPNG(img, self.img_food,
                        pos=[random_x - self.width_food // 2,
                           random_y - self.height_food // 2])
        return img


    def check_for_collision(self, curr_x, curr_y, img):
        """Takes current x, y coordinates of the snake and the object of
        the image of screen"""
        pts = np.array(self.points[:-2], np.int32)
        pts = pts.reshape((-1, 1, 2))
        cv2.polylines(img, [pts], False, (0, 200, 0), 3)
        min_distance = cv2.pointPolygonTest(pts, (curr_x, curr_y), True)
        if  -0.5 <= min_distance <= 0.5 and self.current_length * 1.1 > \
           self.allowed_length:
            self.game_over = True

       
    def update(self, img_main, head_current):
        """This function updates the image of the screen"""
        if self.game_over:
            cvzone.putTextRect(img_main, 'Game Over', [300, 250],
                               scale = 6, thickness=4, offset=10,
                               colorR=(255, 143, 162))
            cvzone.putTextRect(img_main, f'Your score: {self.score}', [300, 320],
                               scale = 6, thickness=4, offset=10,
                               colorR=(255, 143, 162))
            cvzone.putTextRect(img_main, f'Press "r" to restart', [220, 391],
                               scale = 5, thickness=4, offset=10,
                               colorR=(255, 143, 162))
            self.points = [] 
            self.lengths = [] 
            self.current_length = 0 
            self.allowed_length = 150 
            self.previous_head = 0, 0 
            self.random_food_location()
        else:    
            prev_x, prev_y = self.previous_head
            curr_x, curr_y = head_current

            self.points.append([curr_x, curr_y])
            distance = math.hypot(curr_x - prev_x, curr_y - prev_y)
            self.lengths.append(distance)
            self.current_length += distance
            self.previous_head = curr_x, curr_y

            if self.current_length > self.allowed_length:
                for i, length in enumerate(self.lengths):
                    self.current_length -= length
                    self.lengths.pop(i)
                    self.points.pop(i)
                    if self.current_length < self.allowed_length:
                        break

            self.check_eat(curr_x, curr_y)
            self.draw_snake(img_main)
            img_main = self.draw_food(img_main)
            cvzone.putTextRect(img_main, f'Score: {self.score}', [50, 80],
                               scale=3, thickness=3, offset=10,
                               colorR=(255, 143, 140))
            self.check_for_collision(curr_x, curr_y, img_main)        
        return img_main
