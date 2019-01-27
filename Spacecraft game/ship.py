import pygame;
from pygame.sprite import Sprite;

class Ship(Sprite):
	def __init__(self,ai_settings,screen):
		super(Ship,self).__init__();
		
		self.screen=screen;

		self.image=pygame.image.load("images/meng.jpg");
		self.rect=self.image.get_rect();
		self.screen_rect=screen.get_rect();
		self.ship_speed=ai_settings.ship_speed;
		
		self.rect.centerx=float(self.screen_rect.centerx);
		self.rect.bottom=self.screen_rect.bottom;
		
		self.moving_right=False;
		self.moving_left=False;
		self.moving_up=False;
		self.moving_down=False;
	
	def update(self):
		if self.moving_right and (self.rect.right<self.screen_rect.right):
			self.rect.centerx+=self.ship_speed;
		if self.moving_left and (self.rect.left>0):
			self.rect.centerx-=self.ship_speed;
		if self.moving_up and (self.rect.top>0):
			self.rect.centery-=self.ship_speed; #moving up
		if self.moving_down and (self.rect.bottom<self.screen_rect.bottom):
			self.rect.centery+=self.ship_speed; #moving down
	
	def center_ship(self):
		self.rect.centerx=self.screen_rect.centerx;
		self.rect.bottom=self.screen_rect.bottom;
		
	def blitme(self):
		self.screen.blit(self.image,self.rect);