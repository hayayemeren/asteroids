import pygame
from constants import SCREEN_WIDTH, SCREEN_HEIGHT
from player import Player
from asteroid import Asteroid
from asteroidfield import AsteroidField
from shot import Shot
import sys

def end_display(player, screen, running):
	game_over_font = pygame.font.Font(None, 72)
	final_score_font = pygame.font.Font(None, 48)
	instruction_font = pygame.font.Font(None, 24)
	game_over_text = game_over_font.render("GAME OVER", True, "red")
	game_over_rect = game_over_text.get_rect(center=(SCREEN_WIDTH / 2, SCREEN_HEIGHT / 2 - 50))
	screen.blit(game_over_text, game_over_rect)
	final_score_text = final_score_font.render(f"Final Score: {player.score}", True, "white")
	final_score_rect = final_score_text.get_rect(center=(SCREEN_WIDTH / 2, SCREEN_HEIGHT / 2 + 20))
	screen.blit(final_score_text, final_score_rect)
	instruction_text = instruction_font.render("Press ENTER to Restart or ESC to Quit", True, "white")
	instruction_rect = instruction_text.get_rect(center=(SCREEN_WIDTH / 2, SCREEN_HEIGHT / 2 + 100))
	screen.blit(instruction_text, instruction_rect)

def score_display(player, screen):
	score_font = pygame.font.Font(None, 36)
	score_text_surface = score_font.render(f"Score: {player.score}", True, "red")
	score_text_rect = score_text_surface.get_rect()
	score_text_rect.topright = (SCREEN_WIDTH - 10, 10)
	screen.blit(score_text_surface, score_text_rect)

def lives_display(player, screen):
	lives_font = pygame.font.Font(None, 36)
	lives_text_surface = lives_font.render(f"Lives: {player.lives}", True, "red")
	lives_text_rect = lives_text_surface.get_rect()
	lives_text_rect.topleft = (10, 10)
	screen.blit(lives_text_surface, lives_text_rect)

def main():
	pygame.init()
	screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
	pygame.display.set_caption("Astroid Game")
	
	clock = pygame.time.Clock()
	dt = 0
	running = True

	updatable = pygame.sprite.Group()
	drawable = pygame.sprite.Group()
	asteroids = pygame.sprite.Group()
	shots = pygame.sprite.Group()

	Player.containers = (updatable, drawable)
	Asteroid.containers = (asteroids, updatable, drawable)
	AsteroidField.containers = updatable
	Shot.containers = (shots, updatable, drawable)

	while True:

		updatable.empty()
		drawable.empty()
		asteroids.empty()
		shots.empty()

		Player.containers = (updatable, drawable)
		Asteroid.containers = (asteroids, updatable, drawable)
		AsteroidField.containers = updatable
		Shot.containers = (shots, updatable, drawable)

		asteroid_field = AsteroidField()
		player = Player(SCREEN_WIDTH / 2, SCREEN_HEIGHT / 2)

		running = True
		while running:
			for event in pygame.event.get():
				if event.type == pygame.QUIT:
					return
			updatable.update(dt)
			screen.fill("black")

			for asteroid in asteroids:
				if asteroid.collides_with(player):
					player.lives -= 1
					if player.lives > 0:
						asteroid.kill()
					else:
						running = False
						break
				for shot in shots:
					if asteroid.collides_with(shot):
						shot.kill()
						asteroid.split()
						player.score += 1

			for obj in drawable:
				obj.draw(screen)
			
			score_display(player, screen)
			lives_display(player, screen)
			
			pygame.display.flip()
			dt = clock.tick(60) / 1000

		game_over = True
		restart = False
		while game_over:
			for event in pygame.event.get():
				if event.type == pygame.QUIT:
					return
				elif event.type == pygame.KEYDOWN:
					if event.key == pygame.K_ESCAPE:
						return
					elif event.key == pygame.K_RETURN:
						game_over = False
						restart = True
			screen.fill("black")
			end_display(player, screen, False)
			pygame.display.flip()
			clock.tick(30)
		if not restart:
			break

if __name__ == "__main__":
	main()
