from pygame import Rect, Surface, image, Color

class Fontsheet(object):
    def __init__(self, fontsheet, char_w, char_h):
        #load the fontsheet
            self.fontsheet = image.load(fontsheet)
            self.char_w = char_w
            self.char_h = char_h
            self.sheet_w = self.fontsheet.get_width() / char_w
            self.sheet_h = self.fontsheet.get_height() / char_h

    def get_char(self, ascii):
        # crop the fontsheet at the ascii code position
        char = Surface((self.char_w, self.char_h))
        y = ascii / self.sheet_w
        x = ascii - y * self.sheet_w
        try:
            char.blit(self.fontsheet, (0, 0), 
                      (x * self.char_w, y * self.char_h, 
                       self.char_w, self.char_h))
        except:
            print 'Character not found in fontsheet. '
        return char
