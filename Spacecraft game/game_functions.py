import sys;
import pygame;
from time import sleep;

from bullet import Bullet;
from alien import Alien;

def check_keydown_events(event,ai_settings,screen,ship,bullets):
	if event.key==pygame.K_RIGHT:
		ship.rect.centerx+=ship.ship_speed;
		ship.moving_right=True;
	if event.key==pygame.K_LEFT:
		ship.rect.centerx-=ship.ship_speed;
		ship.moving_left=True;
	if event.key==pygame.K_UP:
		ship.rect.bottom-=ship.ship_speed;
		ship.moving_up=True;
	if event.key==pygame.K_DOWN:
		ship.rect.bottom+=ship.ship_speed;
		ship.moving_down=True;
	if event.key==pygame.K_SPACE:
		fire_bullet(ai_settings,screen,ship,bullets);
	
	if event.key==pygame.K_d:
		ship.rect.centerx+=ship.ship_speed;
		ship.moving_right=True;
	if event.key==pygame.K_a:
		ship.rect.centerx-=ship.ship_speed;
		ship.moving_left=True;
	if event.key==pygame.K_w:
		ship.rect.bottom-=ship.ship_speed;
		ship.moving_up=True;
	if event.key==pygame.K_s:
		ship.rect.bottom+=ship.ship_speed;
		ship.moving_down=True;
	if event.key==pygame.K_q:
		sys.exit();

def check_keyup_events(event,ship):
	if event.key==pygame.K_RIGHT:
		ship.moving_right=False;
	if event.key==pygame.K_LEFT:
		ship.moving_left=False;
	if event.key==pygame.K_UP:
		ship.moving_up=False;
	if event.key==pygame.K_DOWN:
		ship.moving_down=False;
		
	if event.key==pygame.K_d:
		ship.moving_right=False;
	if event.key==pygame.K_a:
		ship.moving_left=False;
	if event.key==pygame.K_w:
		ship.moving_up=False;
	if event.key==pygame.K_s:
		ship.moving_down=False;
		
def check_events(ai_settings,screen,stats,scoreboard,play_button,ship,aliens,bullets):
	for event in pygame.event.get():
			if event.type ==pygame.QUIT:
				sys.exit();
				
			elif event.type==pygame.KEYDOWN:
				check_keydown_events(event,ai_settings,screen,ship,bullets);
					
			elif event.type==pygame.KEYUP:
				check_keyup_events(event,ship);
				
			elif event.type==pygame.MOUSEBUTTONDOWN:
				mouse_x,mouse_y=pygame.mouse.get_pos();
				check_play_buttons(ai_settings,screen,stats,scoreboard,play_button,ship,
					aliens,bullets,mouse_x,mouse_y);

def update_screen(ai_settings,screen,stats,scoreboard,ship,aliens,bullets,play_button):
	screen.fill(ai_settings.bg_color);
	
	for bullet in bullets.sprites():
		bullet.draw_bullet();
	
	ship.blitme();		
	#alien.blitme();
	aliens.draw(screen);
	scoreboard.show_score();
	
	if not stats.game_active:
		play_button.draw_button();
	
	pygame.display.flip();
	
def update_bullets(ai_settings,screen,stats,scoreboard,ship,aliens,bullets):
	bullets.update();
	for bullet in bullets.copy():
		if bullet.rect.bottom<=0:
			bullets.remove(bullet);
				
	check_bullet_alien_collisions(ai_settings,screen,stats,scoreboard,ship,aliens,bullets);
	
def check_bullet_alien_collisions(ai_settings,screen,stats,scoreboard,ship,aliens,bullets):
	#collisions=pygame.sprite.groupcollide(bullets,aliens,True,True);
	#penetrative bullets
	collisions=pygame.sprite.groupcollide(bullets,aliens,False,True); 

	if collisions:
		for aliens in collisions.values():
			stats.score+=ai_settings.alien_point*len(aliens);
			scoreboard.prep_score();
		check_high_score(stats,scoreboard);
	
	if len(aliens)==0:
		bullets.empty();
		ai_settings.increase_speed();
		stats.level+=1;
		scoreboard.prep_level();
		create_fleet(ai_settings,screen,ship,aliens);
	
def fire_bullet(ai_settings,screen,ship,bullets):
	if len(bullets)<=ai_settings.bullets_allowed:
		new_bullet=Bullet(ai_settings,screen,ship);
		bullets.add(new_bullet);	
	
def get_number_aliens_x(ai_settings,alien_width):
	available_space_x=ai_settings.screen_width-2*alien_width;
	number_aliens_x=int(available_space_x/(2*alien_width));
	return number_aliens_x;
	
def get_number_rows(ai_settings,ship_height,alien_height):
	available_space_y=ai_settings.screen_height-(3*alien_height)-ship_height;
	number_rows=int(available_space_y)/(2*alien_height);  #modify alien row_number
	return number_rows;
	
def create_alien(ai_settings,screen,aliens,alien_number,row_number):
	alien=Alien(ai_settings,screen);
	alien_width=alien.rect.width;
	alien.x=alien_width+2*alien_width*alien_number;
	alien.rect.x=alien.x;
	alien.rect.y=alien.rect.height+1.5*alien.rect.height*row_number; #modify row distance
	aliens.add(alien);
	

def create_fleet(ai_settings,screen,ship,aliens):
	alien=Alien(ai_settings,screen);
	number_aliens_x=get_number_aliens_x(ai_settings,alien.rect.width);
	number_rows=int(get_number_rows(ai_settings,ship.rect.height,alien.rect.height));
	
	for row_number in range(number_rows):
		for alien_number in range(number_aliens_x):
			create_alien(ai_settings,screen,aliens,alien_number,row_number);
			
def update_aliens(ai_settings,stats,scoreboard,screen,ship,aliens,bullets):
	check_fleet_edges(ai_settings,aliens);
	aliens.update();
	
	if pygame.sprite.spritecollideany(ship,aliens):
		ship_hit(ai_settings,stats,scoreboard,screen,ship,aliens,bullets);
		
	check_aliens_bottom(ai_settings,stats,screen,scoreboard,ship,aliens,bullets);
	
def check_fleet_edges(ai_settings,aliens):
	for alien in aliens.sprites():
		if alien.check_edges():
			change_fleet_direction(ai_settings,aliens);
			break;
			
def change_fleet_direction(ai_settings,aliens):
	for alien in aliens.sprites():
		alien.rect.y+=ai_settings.fleet_drop_speed;
	ai_settings.fleet_direction*=-1;
	
def ship_hit(ai_settings,stats,scoreboard,screen,ship,aliens,bullets):
	if stats.ships_left>0:
		stats.ships_left-=1;
		scoreboard.prep_ships();
	
		aliens.empty();
		bullets.empty();
	
		create_fleet(ai_settings,screen,ship,aliens);
		ship.center_ship();
	
		sleep(3);
	
	else:
		pygame.mouse.set_visible(True);
		stats.game_active=False;
	
def check_aliens_bottom(ai_settings,stats,screen,scoreboard,ship,aliens,bullets):
	screen_rect=screen.get_rect();
	for alien in aliens.sprites():
		if alien.rect.bottom>=screen_rect.bottom:
			ship_hit(ai_settings,stats,scoreboard,screen,ship,aliens,bullets);
			break;
			
def check_play_buttons(ai_settings,screen,stats,scoreboard,play_button,ship,
		aliens,bullets,mouse_x,mouse_y):
	
	button_clicked=play_button.rect.collidepoint(mouse_x,mouse_y);
	if button_clicked and not stats.game_active:
		pygame.mouse.set_visible(False);
		stats.reset_stats();
		stats.game_active=True;
		
		scoreboard.prep_score();
		scoreboard.prep_high_score();
		scoreboard.prep_level();
		scoreboard.prep_ships();
		
		aliens.empty();
		bullets.empty();
		
		create_fleet(ai_settings,screen,ship,aliens);
		ship.center_ship();
		
def check_high_score(stats,scoreboard):
	if stats.score>stats.high_score:
		stats.high_score=stats.score;
		scoreboard.prep_high_score();
