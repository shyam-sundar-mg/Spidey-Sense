import pygame
import sys
from pygame.locals import *
from math import *

WHITE = (255, 255, 255)
BLACK = (0, 0, 0, 0)
RED = (255, 0, 0)
BLUE = (0, 0, 255)
GREEN = (0, 255, 0)
GRAY = (60, 120, 120)
PINK = (250, 0, 0)
YELLOW = (255, 255, 0)
desX = 325
desY = 325
pygame.init()
WIN = pygame.display.set_mode((650, 650))
WIN.fill(BLACK)
bot = pygame.Rect(30, 30, 50, 30)
clk = pygame.time.Clock()
VR = 0
VL = 0


class diffDrive:
    def __init__(self):
        ##-------------------initializing required variables ------------------------------##

        # --initial position of centre----------#
        self.pose = [325, 325]
        self.theta = pi / 2

        ##---------- self.vel[0] = left wheel :: self.vel[1] = right wheel ----------------##
        self.vel = [0, 0]

        ##---------------time gap and length of of axle of bot-------------------------#
        self.dt = 0.1
        self.l = 30

        # -------variables for calculating params-----#
        self.integral = 0
        self.der = 0
        self.distdummy = 0

        # --------Naming the bot-------#
        self.font = pygame.font.Font('freesansbold.ttf', 10)
        self.text = self.font.render('default', True, PINK, GRAY)
        self.textRect = self.text.get_rect()
        self.trail_set = []

    def move(self):
        ##---------------differential drive kinematics --------------------##
        ##---------------using velocity changing the position --------------##
        self.controller()

        v = (self.vel[0] + self.vel[1]) / 2
        w = (-self.vel[1] + self.vel[0]) / self.l

        self.theta += w * self.dt

        self.pose[0] = self.pose[0] + v * cos(self.theta) * self.dt
        self.pose[1] = self.pose[1] + v * sin(self.theta) * self.dt

        self.textRect.center = (self.pose[0] + 3, self.pose[1])

    def controller(self):

        # ----Tuned Parameters of PID COntroller----#
        Kp = 1 / 5
        Ki = 0.001
        Kd = 0.01
        # ------Distance from centre------#
        self.dist = sqrt(pow((self.pose[0] - desX), 2) + pow((self.pose[1] - desY), 2))

        # ------Derivative term------#
        self.der = (self.dist - self.distdummy) / self.dt
        self.distdummy = self.dist

        # ------------POSITIONS------------#

        # ------Position of right and left wheel------#
        self.Rpose = [self.pose[0] + self.l * sin(self.theta) / 2, self.pose[1] - self.l * cos(self.theta) / 2]
        self.Lpose = [self.pose[0] - self.l * sin(self.theta) / 2, self.pose[1] + self.l * cos(self.theta) / 2]

        # -----Distance of target from right and left wheel----#
        self.Rdist = sqrt(pow((self.pose[0] - self.Rpose[0]), 2) + pow((self.pose[1] - self.Rpose[1]), 2))
        self.Ldist = sqrt(pow((self.pose[0] - self.Lpose[0]), 2) + pow((self.pose[1] - self.Lpose[1]), 2))

        # -------Radius of drive-------#
        # -----den::denominator-----#
        den = 1
        if self.Ldist < self.dist:
            den = 2 * ((desX - self.pose[0]) * (-sin(self.theta)) + (desY - self.pose[1]) * (cos(self.theta)))
        if self.Rdist < self.dist:
            den = 2 * ((desX - self.pose[0]) * (sin(self.theta)) + (desY - self.pose[1]) * (-cos(self.theta)))
        # -----Radius of curvature-----#
        R = self.dist * self.dist / den

        # -----Integral term-----#
        self.integral += self.dist * self.dt
        w = self.dist * Kp + self.integral * Ki + self.der * Kd

        # -----ICC(only for reference)------#
        self.Iccx = self.pose[0] + R * sin(self.theta)
        self.Iccy = self.pose[1] - R * cos(self.theta)

        # -----Descision to stop------#
        if self.dist < 5:
            self.vel[0] = 0
            self.vel[1] = 0
        # ------Fixing velocity of wheels--------#
        else:
            self.vel[0] = -w * (1 - self.l / (2 * R))
            self.vel[1] = -w * (1 + self.l / (2 * R))

    # ----function to name the bot----#
    def write_info(self):
        text = "Spidy"
        self.text = self.font.render(text, True, PINK, GRAY)
        WIN.blit(self.text, self.textRect)

    def trail(self, pose):
        for i in range(0, len(self.trail_set) - 1):
            pygame.draw.line(WIN, YELLOW, (self.trail_set[i][0], self.trail_set[i][1]),
                             (self.trail_set[i + 1][0], self.trail_set[i + 1][1]))
        if (self.trail_set.__sizeof__() > 700):
            self.trail_set.pop(0)
        self.trail_set.append(pose)


# -----Object declaration of Class diffDrive------#
ddr = diffDrive()

if __name__ == '__main__':
    while True:
        clk.tick(100)

        # ----------this is called when we need to quit the window------------------#
        for event in pygame.event.get():
            if event.type == QUIT:
                pygame.quit()
                sys.exit()

            # ------------------setting destination to be where cursor is placed--------##
            if pygame.mouse.get_pressed():
                if event.type == MOUSEBUTTONDOWN:
                    desX, desY = pygame.mouse.get_pos()
                    print(desX, desY)
        ddr.move()

        # ---------------------- portion below is design of bot and display screen --------------#
        X = floor(ddr.pose[0] - (6 * cos(ddr.theta)))
        Y = floor(ddr.pose[1] - (6 * sin(ddr.theta)))
        X1 = floor(ddr.pose[0] + (6 * cos(ddr.theta)))
        Y1 = floor(ddr.pose[1] + (6 * sin(ddr.theta)))
        front_X = floor(X - (15 * sin(ddr.theta)))
        front_Y = floor(Y + (15 * cos(ddr.theta)))
        front_X1 = floor(X + (15 * sin(ddr.theta)))
        front_Y1 = floor(Y - (15 * cos(ddr.theta)))
        back_X = floor(X1 - (15 * sin(ddr.theta)))
        back_Y = floor(Y1 + (15 * cos(ddr.theta)))
        back_X1 = floor(X1 + (15 * sin(ddr.theta)))
        back_Y1 = floor(Y1 - (15 * cos(ddr.theta)))
        WIN.fill(BLACK)
        pygame.draw.line(WIN, RED, (0, 5), (floor(ddr.vel[0] * 8 + 350), 5), 10)
        pygame.draw.line(WIN, GREEN, (0, 15), (floor(ddr.vel[1] * 8 + 350), 15), 10)
        pygame.draw.circle(WIN, GRAY, (floor(ddr.pose[0]), floor(ddr.pose[1])), 14)
        pygame.draw.line(WIN, WHITE, (front_X, front_Y), (back_X, back_Y), 3)
        pygame.draw.line(WIN, WHITE, (front_X1, front_Y1), (back_X1, back_Y1), 3)
        ddr.write_info()
        ddr.trail((ddr.pose[0], ddr.pose[1]))
        pygame.display.flip()
