class Settings():
	def __init__(self):
		self.bg_color=(200,200,218);  #background colour
		self.screen_width=1200;
		self.screen_height=650;
		
		#self.bullet_speed=0.5;  #bullet
		self.bullet_width=2;  #bullet
		self.bullet_height=15;
		self.bullet_color=30,30,30;
		
		#self.alien_speed=2.5;  #alien
		#self.fleet_drop_speed=10;
		#self.fleet_direction=1;  #1==right,-1==left
		
		self.speedup_scale=0.15;
		self.score_scale=2;
		
		self.initialize_dynamic_settings();
		
	def initialize_dynamic_settings(self):
		self.bullet_speed=1;  #bullet
		self.bullets_allowed=4;
		
		self.ship_speed=5;  #ship
		self.ships_limit=3;
		
		self.alien_speed=2;  #alien
		self.fleet_drop_speed=15;
		self.fleet_direction=1;
		self.alien_point=70;
	
	def increase_speed(self):
		self.ship_speed+=self.speedup_scale;
		self.bullet_speed+=self.speedup_scale;
		self.alien_speed+=self.speedup_scale;
		self.fleet_drop_speed+=self.speedup_scale;
		self.bullets_allowed+=2;
		self.alien_point*=self.score_scale;