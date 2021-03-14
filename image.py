from PIL import Image, ImageQt, ImageEnhance, ImageOps
import math
import copy


class Images():
    def __init__(self):
        self.image = []
        self.imagePoped = []

    def changeCurrent(self):
        self.current = self.image[-1]

    def saves(self, path):
        extension = str(path[1][0:3]).lower()
        if extension in ['pbm', 'pgm', 'ppm']:
            ext = 'ppm'
        elif extension in ['jpeg', 'jpg']:
            ext = 'jpeg'
        elif extension in ['png']:
            ext = 'png'
        self.current.save(path[0] + '.' + extension, ext)

    def imageLoader(self, path):
        self.image.append(Image.open(path).convert('RGBA'))
        self.changeCurrent()

    def toPixmap(self):
        return ImageQt.toqpixmap(self.current)

    def checkIfEmpty(self):
        if len(self.image) > 0:
            return True
        else:
            return False

    def undo(self):
        if len(self.image) > 1:
            self.imagePoped.append(self.image.pop())
            self.changeCurrent()
        else:
            pass

    def forward(self):
        if len(self.imagePoped) > 0:
            self.image.append(self.imagePoped.pop())
            self.changeCurrent()
        else:
            pass

    def saturation(self, ratio):
        converter = ImageEnhance.Color(self.current)
        self.image.append(converter.enhance(ratio))
        self.changeCurrent()

    def light(self, ratio):
        converter = ImageEnhance.Brightness(self.current)
        self.image.append(converter.enhance(ratio))
        self.changeCurrent()

    def invert(self):
        self.image.append(ImageOps.invert(self.current.convert('RGB')).convert('RGBA'))
        self.changeCurrent()

    def monochromatic(self):
        self.image.append(self.current.convert('L').convert('RGBA'))
        self.changeCurrent()

    def monochromatic2(self):
        self.image.append(self.current.convert('1').convert('RGBA'))
        self.changeCurrent()

    def saturationOwn(self, ratio):
        tmpHSV = copy.deepcopy(self.current.convert('HSV'))
        width, height = tmpHSV.size
        for w in range(width):
            for h in range(height):
                p = tmpHSV.getpixel((w, h))
                saturation = int(p[1] * ratio)
                if saturation > 255:
                    saturation = 255
                tmpHSV.putpixel((w, h), (p[0], saturation, p[2]))
        self.image.append(tmpHSV.convert('RGBA'))
        self.changeCurrent()

    def lightOwn(self, ratio):
        tmpHSV = copy.deepcopy(self.current.convert('HSV'))
        width, height = tmpHSV.size
        for w in range(width):
            for h in range(height):
                p = tmpHSV.getpixel((w, h))
                value = int(p[2] * ratio)
                if value > 255:
                    value = 255
                tmpHSV.putpixel((w, h), (p[0], p[1], value))
        self.image.append(tmpHSV.convert('RGBA'))
        self.changeCurrent()

    def invertOwn(self):
        tmpRGB = copy.deepcopy(self.current)
        width, height = tmpRGB.size
        for w in range(width):
            for h in range(height):
                p = tmpRGB.getpixel((w, h))
                tmpRGB.putpixel((w, h), (255 - p[0], 255 - p[1], 255 - p[2], p[3]))
        self.image.append(tmpRGB)
        self.changeCurrent()

    def monochromaticOwn(self):
        tmpRGB = copy.deepcopy(self.current)
        width, height = tmpRGB.size
        for w in range(width):
            for h in range(height):
                p = tmpRGB.getpixel((w, h))
                avg = int(math.floor(((p[0] * 1.3) + (p[1] * 1.6) + (p[2] * 1.1)) / 3))
                if avg > 255:
                    avg = 255
                tmpRGB.putpixel((w, h), (avg, avg, avg, p[3]))
        self.image.append(tmpRGB)
        self.changeCurrent()

    def monochromatic2Own(self):
        tmpRGB = self.current
        print(tmpRGB.getpixel((0, 0)))

    def linearcontrastOwn(self, ratio):
        tmpRGB = copy.deepcopy(self.current)
        factor = (259 * (ratio + 255)) / (255 * (259 - ratio))
        width, height = tmpRGB.size
        for w in range(width):
            for h in range(height):
                p = tmpRGB.getpixel((w, h))
                newRed = math.floor(factor * (p[0] - 128) + 128)
                newGreen = math.floor(factor * (p[1] - 128) + 128)
                newBlue = math.floor(factor * (p[2] - 128) + 128)
                tmpRGB.putpixel((w, h), (newRed, newGreen, newBlue, p[3]))
        self.image.append(tmpRGB)
        self.changeCurrent()

    def logcontrastOwn(self, ratio):
        tmpRGB = copy.deepcopy(self.current)
        width, height = tmpRGB.size
        for w in range(width):
            for h in range(height):
                p = tmpRGB.getpixel((w, h))
                # print(str(math.log(p[0]+1)) + "  " + str(p[0]) + " "+ str(ratio))
                newRed = math.floor(ratio * math.log(p[0]+1))
                newGreen = math.floor(ratio * math.log(p[1]+1))
                newBlue = math.floor(ratio * math.log(p[2]+1))
                tmpRGB.putpixel((w, h), (newRed, newGreen, newBlue, p[3]))
        self.image.append(tmpRGB)
        self.changeCurrent()