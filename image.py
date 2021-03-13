from PIL import Image,ImageQt,ImageEnhance,ImageOps


class Images():
    def __init__(self):
        self.image = [Image.open('/home/marcin/Projekty/PycharmProjects/SkeletonAppPO/123')]
        self.changeCurrent()

    def changeCurrent(self):
        self.current = self.image[-1]

    def save(self, path):
        pass

    def imageLoader(self, path):
        self.image.append(Image.open(path))
        self.changeCurrent()

    def toPixmap(self):
        return ImageQt.toqpixmap(self.current)

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

    def invert(self):
        ImageOps.invert()
        self.image.append(converter.enhance(ratio))
