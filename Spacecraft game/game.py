import sys;
import pygame;
from time import sleep;
from pygame.sprite import Group;

from setting import Settings;
from ship import Ship;
from alien import Alien;
from game_stats import GameStats;
from button import Button;
from scoreboard import Scoreboard;
import game_functions as gf;

def run_game():
	pygame.init();
	ai_settings=Settings();
	screen=pygame.display.set_mode((ai_settings.screen_width,ai_settings.screen_height));
	pygame.display.set_caption("Alien Invasion");
	stats=GameStats(ai_settings);
	scoreboard=Scoreboard(ai_settings,screen,stats);
	play_button=Button(ai_settings,screen,"play");
	
	ship=Ship(ai_settings,screen);
	alien=Alien(ai_settings,screen);
	bullets=Group();
	aliens=Group();
	
	gf.create_fleet(ai_settings,screen,ship,aliens);
	
	while True:  #main loop
		gf.check_events(ai_settings,screen,stats,scoreboard,play_button,ship,
			aliens,bullets);
		
		if stats.game_active:
			ship.update();
			bullets.update();
			gf.update_bullets(ai_settings,screen,stats,scoreboard,ship,aliens,bullets);
			gf.update_aliens(ai_settings,stats,scoreboard,screen,ship,aliens,bullets);
		
		gf.update_screen(ai_settings,screen,stats,scoreboard,ship,aliens,bullets,play_button);
		
def greeting():
	print("\n\nWelcome to Alien Invasion!\n");
	print("=============================================");
	sleep(1);
	print("Instructions:");
	print("'a' or LEFT_KEY for 'LEFT',");
	print("'s' or DOWN_KEY for 'DOWN',");
	print("'d' or RIGHT_KEY for 'RIGHT',");
	print("'w' or UP_KEY for 'UP'\n");
	print("SPACE for SHOOT");
	print("'q' to quit.");
	print("=============================================");
	sleep(1);
	while True:
		answer=input("Do you understand? '1' for 'yes','0' for 'no':");
		if answer=="1":
			run_game();
		else:
			answer=input("Are you sure?'1' for 'yes','0' for 'no':");
			if answer=="1":
				print("OHHHH,I'm so sorry...Bye!");
				break;
			else:
				print("Please input again!");
			
greeting();