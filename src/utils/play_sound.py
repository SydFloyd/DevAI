import pygame

def play_sound(sound_file):
    pygame.init()
    pygame.mixer.init()
    sound = pygame.mixer.Sound(sound_file)
    sound.play()
    while pygame.mixer.get_busy():  # Wait for the sound to finish playing
        pygame.time.Clock().tick(10)