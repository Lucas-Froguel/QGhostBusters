
from pygame.mixer import Sound
from pygame.mixer import music


class BaseSoundManager:
    def __init__(self):
        pass

    def play_sound(self, sound: str):
        pass


class ScreenSoundManager(BaseSoundManager):
    def __init__(self):
        self.music: str = None

    def play_music(self):
        music.stop()
        music.load(self.music)
        music.play(-1)


class MenuSoundManager(ScreenSoundManager):
    def __init__(self):
        self.music = "src/SoundEffects/sound_effects/top-down-fantasy-1.mp3.wav"
        self.select_menu_item = Sound("src/SoundEffects/sound_effects/select_menu_item.wav")

    def play_select_menu_item_sound(self):
        self.select_menu_item.play()


class LevelSoundManager(ScreenSoundManager):
    def __init__(self, music: str = None):
        self.music = music
        self.load_level = Sound("src/SoundEffects/sound_effects/load_level.wav")
        self.game_over = Sound("src/SoundEffects/sound_effects/game_over.wav")

    def play_load_level_sound(self):
        self.load_level.play()

    def play_game_over_sound(self):
        self.game_over.play()


class PlayerSoundManager(BaseSoundManager):
    def __init__(self):
        self.attack_sound = Sound("src/SoundEffects/sound_effects/player_shoot.wav")
        self.measure_sound = Sound("src/SoundEffects/sound_effects/measure.wav")

    def play_attack_sound(self):
        self.attack_sound.play()

    def play_measure_sound(self):
        self.measure_sound.play()
