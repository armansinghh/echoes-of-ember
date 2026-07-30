import pygame

def load_frames(path, frame_count):
    """
    loads a horizontal sprite sheet and slices it into a list of surfaces.
    assumes all frames are equal width, single row.
    """
    sheet = pygame.image.load(path).convert_alpha()
    sheet_width, sheet_height = sheet.get_size()
    frame_width = sheet_width // frame_count
    frame_height = sheet_height

    frames = []
    for i in range(frame_count):
        frame = sheet.subsurface((i * frame_width, 0, frame_width, frame_height))
        frames.append(frame)
    return frames