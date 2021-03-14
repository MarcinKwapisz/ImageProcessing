from PIL import Image,ImageQt,ImageEnhance,ImageOps


class Images():
    def __init__(self):
        self.image=[]

    def changeCurrent(self):
        self.current = self.image[-1]

    def saves(self, path):
        extension = str(path[1][0:3]).lower()
        if extension =='pbm'|'pgm'|'ppm':
            ext = 'ppm'
        elif extension == 'jpeg'|'jpg':
            ext = 'jpeg'
        elif extension == 'png':
            ext = 'png'
        self.current.save(path[0]+'.'+extension, ext)

    def imageLoader(self, path):
        self.image.append(Image.open(path).convert('RGBA'))
        self.changeCurrent()

    def toPixmap(self):
        return ImageQt.toqpixmap(self.current)

    def checkIfEmpty(self):
        if len(self.image)>0:
            return True
        else:
            return False
    def undo(self):
        if len(self.image)>1:
            self.image.pop()
            self.changeCurrent()
        else:
            pass

    def saturation(self,ratio):
        converter = ImageEnhance.Color(self.current)
        self.image.append(converter.enhance(ratio))
        self.changeCurrent()

    def light(self,ratio):
        converter = ImageEnhance.Brightness(self.current)
        self.image.append(converter.enhance(ratio))
        self.changeCurrent()

    def invert(self):
        self.image.append(ImageOps.invert(self.current))
        self.changeCurrent()