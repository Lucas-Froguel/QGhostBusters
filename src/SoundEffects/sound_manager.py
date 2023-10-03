
from pygame.mixer import Sound, music, Channel


class BaseSoundManager:
    def __init__(self, channel: Channel = None):
        self.channel = channel

    def play_sound(self, sound: str):
        pass


class ScreenSoundManager(BaseSoundManager):
    def __init__(self, channel: Channel = None):
        super().__init__(channel=channel)
        self.music: str = None

    def play_music(self):
        music.stop()
        music.load(self.music)
        music.play(-1)


class MenuSoundManager(ScreenSoundManager):
    def __init__(self, channel: Channel = None):
        super().__init__(channel=channel)
        self.music = "src/SoundEffects/sound_effects/top-down-fantasy-1.mp3"
        self.select_menu_item = Sound("src/SoundEffects/sound_effects/select_menu_item.wav")

    def play_select_menu_item_sound(self):
        self.channel.play(self.select_menu_item)


class LevelSoundManager(ScreenSoundManager):
    def __init__(
        self,
        channel: Channel = None,
        extra_channel: Channel = None,
        background_track_path: str = None,
        music: str = None
    ):
        super().__init__(channel=channel)
        self.music = music
        self.load_level = Sound("src/SoundEffects/sound_effects/load_level.wav")
        self.game_over = Sound("src/SoundEffects/sound_effects/game_over.wav")
        self.background_sound = Sound(background_track_path) if background_track_path else None
        self.extra_channel = extra_channel
        if self.extra_channel:
            self.play_background_sound()

    def play_background_sound(self):
        self.extra_channel.play(self.background_sound, loops=-1)

    def play_load_level_sound(self):
        self.channel.play(self.load_level)

    def play_game_over_sound(self):
        self.channel.play(self.game_over)


class PlayerSoundManager(BaseSoundManager):
    def __init__(self, channel: Channel = None):
        super().__init__(channel=channel)
        self.attack_sound = Sound("src/SoundEffects/sound_effects/player_shoot.wav")
        self.measure_sound = Sound("src/SoundEffects/sound_effects/measure.wav")

    def play_attack_sound(self):
        self.channel.play(self.attack_sound)

    def play_measure_sound(self):
        self.channel.play(self.measure_sound)


class GhostSoundManager(BaseSoundManager):
    def __init__(self, channel: Channel = None):
        super().__init__(channel=channel)
        self.attack_sound = Sound("src/SoundEffects/sound_effects/ghost_hit.wav")

    def play_attack_sound(self):
        self.channel.play(self.attack_sound)
