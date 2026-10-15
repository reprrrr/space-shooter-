import json 
import random
import utils

class Wave():
	enemy_type = 0
	number_of_enemies = 0
	time_between_enemies = 0
	startx = 0
	starty = 0
	speedx = 0
	speedy = 0

class WaveManager():
	def __init__(self):
		self.waves = []
		self.current_wave = 0
		self.enemies_types = utils.get_files_names("json/Enemies", ".json")
	def load_wave(self, wave_number, screen_width, screen_height):
		try:
			with open(f"json/waves/wave_{wave_number}.json", "r") as f:
				wave_data = json.load(f)
				wave = Wave()
				wave.enemy_type = wave_data["enemy_type"]
				wave.number_of_enemies = wave_data["number_of_enemies"]
				wave.time_between_enemies = wave_data["time_between_enemies"]
				wave.startx = wave_data["startx"]
				wave.starty = wave_data["starty"]
				wave.speedx = wave_data["speedx"]
				wave.speedy = wave_data["speedy"]
				return wave  
		except FileNotFoundError:
			print(f"Wave {wave_number} not found.")
			
			default_wave = Wave()

			valid_enemy = False
			while not valid_enemy:
				e_type = random.choice(self.enemies_types)
				with open(f"json/Enemies/{e_type}.json", "r") as f:
					enemy_data = json.load(f)
					if enemy_data["type"] == "basic":
						valid_enemy = True
					else:
						e_type = random.choice(self.enemies_types)
			default_wave.enemy_type = e_type
			default_wave.number_of_enemies = random.randint(5, 12)
			default_wave.time_between_enemies = random.random()*3
			default_wave.startx = random.randint(0, screen_width)
			default_wave.starty = random.randint(0, screen_height//2)
			default_wave.speedx = random.randint(1, 3)
			default_wave.speedy = random.randint(1, 3)
			return default_wave





# wave_3 = Wave()
# wave_3.enemy_type = 1
# wave_3.number_of_enemies = 4000
# wave_3.time_between_enemies = 0
# wave_3.startx = 7
# wave_3.starty = 3
# wave_3.speedx = 20
# wave_3.speedy = 1
# waves.append(wave_3)
