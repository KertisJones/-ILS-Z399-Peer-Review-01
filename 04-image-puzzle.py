import sys, pygame, random, os, PIL

assert sys.version_info >= (3,4), 'This script requires at least Python 3.4'


pygame.init()
pygame

size = (width,height) = (800,800)
dimensions = (rows,columns) = (4,4)
font = pygame.font.SysFont("arial",64)
screen = pygame.display.set_mode(size)


class Square(pygame.sprite.Sprite):
	color = ''
	label = ''
	position = (-1,-1),
	dim = (0,0)
	height = 0
	visible = True
	
	def __init__(self, x, y, w, h):
		self.position = (x,y)
		self.dim = (w,h)
		pygame.sprite.Sprite.__init__(self)
		self.image = pygame.image.load(os.path.join("C:\\Users\\mason\\OneDrive\\GitHub\\04-image-puzzle\\cream-disreali-gears.jpg"))
		self.rect = self.image.get_rect()
		self.rect.topleft = (self.position[0] * 200, self.position[1] * 200)

	def update(self):
		self.rect.topleft = (self.position[0] * 200, self.position[1] * 200)

	def check_proximity(self, xy):
		if self.position == (-1,-1): return False
		if self.position == xy: return False
		if (abs(xy[0] - self.position[0]) <= 1 and xy[1] == self.position[1]) or (abs(xy[1] - self.position[1]) <= 1 and xy[0] == self.position[0]):
			return True
		return False
	
	def swap_position(self, xy):
		self.position = xy
		self.rect.topleft = (self.position[0] * 200, self.position[1] * 200)
	
	def in_correct_position(self, pos):
		return False
	
	def draw_square(self, draw, screen):
		if self.visible:
			(x1,y1) = self.position
			(w,h) = self.dim
			(x,y) = (x1 * w,y1 * h)
			self.rect.topleft = (x * 200, y * 200)
			f = font.render(self.label,True,(0,0,0))
			(fwidth,fheight) = font.size(self.label)
			(fx,fy) = (x + (w - fwidth)/2,y + (h - fheight)/2)
			screen.blit(f,(fx,fy))
		return draw


def calculate_xy(pos,puzzle):
	w = width / columns
	h = height / rows
	to_return = (int(pos[0]//w),int(pos[1]//h))
	return to_return


def randomize_puzzle(count,puzzle):
	for e in puzzle:
		if not e.visible:
			for c in range(count):
				xy = (x,y) = (e.position[0] + random.randint(-1,1),e.position + random.randint(-1,1))
				if (x >= 0 and x< columns) and (y >= 0 and y< rows):
					if e.check_proximity(xy):
						for p in puzzle:
							if p.position == xy:
								p.swap_position(e.position)
								e.swap_position(xy)
	return puzzle


def draw_puzzle(puzzle):
	screen.fill((0,0,0))
	for i in range(len(puzzle)):
		puzzle[i].draw_square(pygame.draw,screen)
	pygame.display.flip()


colors = [(0,206,209),(0,255,255),(127,255,212),(0,255,127),(124,252,0),(255,255,0),(255,165,0),(255,0,0),(160,32,240),(218,112,214),(255,105,180),(255,215,0),(240,230,140),(50,205,50),(205,92,92)]
puzzle = []
count = 0

for j in range(columns):
	for i in range(rows):
		temp = Square(i, j, width / columns, height / rows)
		temp.color = colors[count % len(colors)]
		count = count + 1
		temp.label = str(count)

puzzle[len(puzzle) - 1].visible = False
puzzle = randomize_puzzle(500,puzzle)
screen = pygame.display.set_mode(size)

moves = 0
draw_puzzle(puzzle)

winning = False
while not winning:
	for event in pygame.event.get():
		if event.type == pygame.QUIT: sys.exit()
		# handle MOUSEBUTTONUP
		if event.type == pygame.MOUSEBUTTONUP:
			pos = pygame.mouse.get_pos()
			xy = calculate_xy(pos,puzzle)
			print(xy)
			for e in puzzle:
				if not e.visible:
					if e.check_proximity(xy):
						for c in puzzle:
							if c.position == xy:
								c.swap_position(e.position)
								e.swap_position(xy)
								draw_puzzle(puzzle)
								moves = moves + 1
			winning = True
			for i in range(len(puzzle)):
				xy = (x,y) = (i % columns, i // rows)
				if puzzle[i].position != xy:
					winning = False
			if winning:
				for e in puzzle:
					e.visible = True
print('You finished in ' + str(moves) + ' moves.')
