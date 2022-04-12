from os import walk
import pygame

def import_folder(path):
    for _, __, img_files in walk(path):
        surfices = [
            pygame.image.load(path + '/' + img_file).convert_alpha()
            for img_file in img_files
            ]
    return surfices
