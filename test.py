from turtle import distance
import pygame
import math
pygame.init()

WIDTH, HEIGHT = 800, 800
WIN = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Planet Simulation")

WHITE = (255,255,255)
GREY = (50, 50, 50)
YELLOW = (255, 255, 0)
BLUE = (100, 100, 255)
RED = (255, 50, 50)
PINK = (255, 150, 150)
ORANGE = (255, 100, 0)
FONT = pygame.font.SysFont("helvetica",16)

class Planet:
    AU = 149.6e9
    G = 6.67428e-11
    SCALE = 200/AU # 1AU = 100px
    TIMESTEP = 86400

    def __init__(self, x, y, radius, color, mass):
        self.x = x
        self.y = y
        self.radius = radius
        self.color = color
        self.mass = mass

        self.orbit = []
        self.sun = False
        self.distance_to_sun = 0


        self.x_vel = 0
        self.y_vel = 0
        
    def draw(self, win):
        x = self.x * self.SCALE + WIDTH/2
        y = self.y * self.SCALE + HEIGHT/2


        if len(self.orbit) > 2:
            updated_points = []
            for point in self.orbit:
                x,y = point
                x = x * self.SCALE + WIDTH/2
                y = y * self.SCALE + HEIGHT/2
                updated_points.append((x,y))

            pygame.draw.lines(win, self.color, False, updated_points, 2)
        pygame.draw.circle(win, self.color, (x,y), self.radius)

        if not self.sun:
            distance_text = FONT.render(f"{round(self.distance_to_sun/149.6e9, 3)}AU",1, WHITE)
            win.blit(distance_text, (x-distance_text.get_width()/2, y-distance_text.get_height()/2))   

    def attraction(self, other):
        other_x, other_y = other.x, other.y
        distance_x = other_x - self.x
        distance_y = other_y - self.y
        distance = math.sqrt(distance_x ** 2 + distance_y ** 2)

        if other.sun:
            self.distance_to_sun = distance

        force = self.G * self.mass * other.mass / distance ** 2
        theta = math.atan2(distance_y, distance_x)
        force_x = math.cos(theta)*force
        force_y = math.sin(theta)*force
        return force_x, force_y

    def update_position(self, planets):
        total_fx = total_fy = 0
        for planet in planets:
            if self == planet:
                continue

            fx, fy = self.attraction(planet)
            total_fx += fx
            total_fy += fy
        self.x_vel += total_fx / self.mass * self.TIMESTEP
        self.y_vel += total_fy / self.mass * self.TIMESTEP

        self.x += self.x_vel * self.TIMESTEP
        self.y += self.y_vel * self.TIMESTEP
        self.orbit.append((self.x, self.y))





def main():
    run = True
    clock = pygame.time.Clock() #framerate of simulation 

    sun = Planet(0,0,30,YELLOW, 1.98892e30)
    sun.sun = True

    earth = Planet(-1*Planet.AU,0,16,BLUE, 5.9742e24)
    earth.y_vel = 29783

    mars = Planet(-1.524*Planet.AU,0,12,RED, 6.39e23)
    mars.y_vel = 24077

    venus = Planet(-0.723*Planet.AU,0,14,ORANGE, 4.8685e24)
    venus.y_vel = 35020

    mercury = Planet(-0.387*Planet.AU,0,8,GREY, 3.3e23)
    mercury.y_vel = 47400

    jupiter = Planet(-1.8*Planet.AU,0,20,PINK, 3.3e27)
    jupiter.y_vel = 10000

    planets = [sun, earth, mars, venus, mercury, jupiter]

    while run:
        clock.tick(500) #sim speed
        WIN.fill((0,0,0))
        

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                run = False

        for planet in planets:
            planet.update_position(planets)
            planet.draw(WIN)

        pygame.display.update()

    pygame.quit()

main()