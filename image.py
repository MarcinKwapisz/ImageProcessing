from PIL import Image, ImageQt, ImageEnhance, ImageOps
import math
import copy
import numpy as np
import matplotlib.pyplot as plt


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
        else:
            ext = extension
        self.current.save(path[0] + '.' + extension, ext)

    def imageLoader(self, path):
        self.image.append(Image.open(path).convert('RGB'))
        self.changeCurrent()

    def toPixmap(self):
        return ImageQt.toqpixmap(self.current)

    def rgb_to_hsv(self, r, g, b):
        r = float(r)
        g = float(g)
        b = float(b)
        high = max(r, g, b)
        low = min(r, g, b)
        h, s, v = high, high, high

        d = high - low
        s = 0 if high == 0 else d / high

        if high == low:
            h = 0.0
        else:
            h = {
                r: (g - b) / d + (6 if g < b else 0),
                g: (b - r) / d + 2,
                b: (r - g) / d + 4,
            }[high]
            h /= 6

        return h, s, v

    def hsv_to_rgb(self, h, s, v):
        # h, s = h / 253.3, s / 253.3
        i = math.floor(h * 6)
        f = h * 6 - i
        p = v * (1 - s)
        q = v * (1 - f * s)
        t = v * (1 - (1 - f) * s)

        r, g, b = [
            (v, t, p),
            (q, v, p),
            (p, v, t),
            (p, q, v),
            (t, p, v),
            (v, p, q),
        ][int(i % 6)]

        return int(r), int(g), int(b)

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
        self.image.append(ImageOps.invert(self.current.convert('RGB')))
        self.changeCurrent()

    def monochromatic(self):
        self.image.append(self.current.convert('L').convert('RGB'))
        self.changeCurrent()

    def monochromatic2(self):
        self.image.append(self.current.convert('1').convert('RGB'))
        self.changeCurrent()

    def saturationOwn(self, ratio):
        tmpHSV = copy.deepcopy(self.current)
        width, height = tmpHSV.size
        for w in range(width):
            for h in range(height):
                hue, sat, val = tmpHSV.getpixel((w, h))
                p = self.rgb_to_hsv(hue, sat, val)
                saturation = p[1] * ratio
                if saturation > 1:
                    saturation = 1
                elif saturation < 0:
                    saturation = 0
                tmpHSV.putpixel((w, h), self.hsv_to_rgb(p[0], saturation, p[2]))
        self.image.append(tmpHSV)
        self.changeCurrent()

    def lightOwn(self, ratio):
        tmpHSV = copy.deepcopy(self.current)
        width, height = tmpHSV.size
        for w in range(width):
            for h in range(height):
                hue, sat, val = tmpHSV.getpixel((w, h))
                p = self.rgb_to_hsv(hue, sat, val)
                light = p[2] * ratio
                if light > 255:
                    light = 255
                elif light < 0:
                    light = 0
                tmpHSV.putpixel((w, h), self.hsv_to_rgb(p[0], p[1], light))
        self.image.append(tmpHSV)
        self.changeCurrent()

    def invertOwn(self):
        tmpRGB = copy.deepcopy(self.current)
        width, height = tmpRGB.size
        for w in range(width):
            for h in range(height):
                p = tmpRGB.getpixel((w, h))
                tmpRGB.putpixel((w, h), (255 - p[0], 255 - p[1], 255 - p[2]))
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
                tmpRGB.putpixel((w, h), (avg, avg, avg))
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
                tmpRGB.putpixel((w, h), (newRed, newGreen, newBlue))
        self.image.append(tmpRGB)
        self.changeCurrent()

    def logcontrastOwn(self, ratio):
        tmpRGB = copy.deepcopy(self.current)
        width, height = tmpRGB.size
        c = ratio / math.log(256)
        for w in range(width):
            for h in range(height):
                p = tmpRGB.getpixel((w, h))
                # print(str(math.log(p[0]+1)) + "  " + str(p[0]) + " "+ str(ratio))
                newRed = math.floor(c * math.log(p[0] + 1))
                newGreen = math.floor(c * math.log(p[1] + 1))
                newBlue = math.floor(c * math.log(p[2] + 1))
                tmpRGB.putpixel((w, h), (newRed, newGreen, newBlue))
        self.image.append(tmpRGB)
        self.changeCurrent()

    def powercontrastOwn(self, ratio):
        tmpRGB = copy.deepcopy(self.current)
        width, height = tmpRGB.size
        c = ratio / math.log(256)
        for w in range(width):
            for h in range(height):
                p = tmpRGB.getpixel((w, h))
                # print(str(math.log(p[0]+1)) + "  " + str(p[0]) + " "+ str(ratio))
                newRed = math.floor(c * math.log(p[0] + 1))
                newGreen = math.floor(c * math.log(p[1] + 1))
                newBlue = math.floor(c * math.log(p[2] + 1))
                tmpRGB.putpixel((w, h), (newRed, newGreen, newBlue, p[3]))
        self.image.append(tmpRGB)
        self.changeCurrent()

    def incOwn(self, ratio):
        tmpRGB = copy.deepcopy(self.current)
        width, height = tmpRGB.size
        for w in range(width):
            for h in range(height):
                p = tmpRGB.getpixel((w, h))
                colors = [math.floor(p[0] + ratio), math.floor(p[1] + ratio), math.floor(p[2] + ratio), p[3]]
                for i in range(3):
                    if colors[i] > 255:
                        colors[i] = 255
                tmpRGB.putpixel((w, h), tuple(colors))
        self.image.append(tmpRGB)
        self.changeCurrent()

    def decOwn(self, ratio):
        tmpRGB = copy.deepcopy(self.current)
        width, height = tmpRGB.size
        for w in range(width):
            for h in range(height):
                p = tmpRGB.getpixel((w, h))
                colors = [math.floor(p[0] - ratio), math.floor(p[1] - ratio), math.floor(p[2] - ratio), p[3]]
                for i in range(3):
                    if colors[i] < 0:
                        colors[i] = 0
                tmpRGB.putpixel((w, h), tuple(colors))
        self.image.append(tmpRGB)
        self.changeCurrent()

    def mulOwn(self, ratio):
        tmpRGB = copy.deepcopy(self.current)
        width, height = tmpRGB.size
        for w in range(width):
            for h in range(height):
                p = tmpRGB.getpixel((w, h))
                colors = [math.floor(p[0] * ratio), math.floor(p[1] * ratio), math.floor(p[2] * ratio), p[3]]
                for i in range(3):
                    if colors[i] > 255:
                        colors[i] = 255
                tmpRGB.putpixel((w, h), tuple(colors))
        self.image.append(tmpRGB)
        self.changeCurrent()

    def showHistogram(self, color):
        if color == 0:
            histogram = [0] * 256
            tmp = self.current.histogram()
            for i in range(3):
                for j in range(256):
                    histogram[j] += tmp[0]
                    tmp.pop(0)
        else:
            r, g, b = self.current.split()
            if color == 1:
                histogram = r.histogram()
            elif color == 2:
                histogram = b.histogram()
            else:
                histogram = g.histogram()

        plt.style.use('ggplot')
        plt.xlim(0, 255)
        plt.bar(range(256), histogram)
        plt.show()

    def normalizeRed(self, intensity):
        iI = intensity
        minI = 86
        maxI = 230
        minO = 0
        maxO = 255
        iO = (iI - minI) * (((maxO - minO) / (maxI - minI)) + minO)
        return iO

    def normalizeGreen(self, intensity):
        iI = intensity
        minI = 90
        maxI = 225
        minO = 0
        maxO = 255
        iO = (iI - minI) * (((maxO - minO) / (maxI - minI)) + minO)
        return iO

    def normalizeBlue(self, intensity):
        iI = intensity
        minI = 100
        maxI = 210
        minO = 0
        maxO = 255
        iO = (iI - minI) * (((maxO - minO) / (maxI - minI)) + minO)
        return iO

    def stretchHistogram(self):
        tmpRGB = copy.deepcopy(self.current)
        # constant = (255-0)/(tmpRGB.max())
        multiBands = tmpRGB.split()
        normalizedRedBand = multiBands[0].point(self.normalizeRed)
        normalizedGreenBand = multiBands[1].point(self.normalizeGreen)
        normalizedBlueBand = multiBands[2].point(self.normalizeBlue)
        normalizedImage = Image.merge("RGB", (normalizedRedBand, normalizedGreenBand, normalizedBlueBand))
        self.image.append(normalizedImage)
        self.changeCurrent()

    def otsuHist(self, img):
        row, col = img.shape
        y = np.zeros(256)
        for i in range(0, row):
            for j in range(0, col):
                y[img[i, j]] += 1
        return y

    def countPixel(self, h):
        cnt = 0
        for i in range(0, len(h)):
            if self.h[i] > 0:
                cnt += self.h[i]
        return cnt

    def weight(self, s, e):
        w = 0
        for i in range(s, e):
            w += self.h[i]
        return w

    def mean(self, s, e):
        m = 0
        w = self.weight(s, e)
        for i in range(s, e):
            m += self.h[i] * i
        val = m / float(w)
        return val

    def variance(self, s, e):
        v = 0
        m = self.mean(s, e)
        w = self.weight(s, e)
        for i in range(s, e):
            v += ((i - m) ** 2) * self.h[i]
        v /= w
        return v

    def threshold(self, h):
        cnt = self.countPixel(h)
        for i in range(1, len(self.h)):
            vb = self.variance(0, i)
            wb = self.weight(0, i) / float(cnt)
            mb = self.mean(0, i)

            vf = self.variance(i, len(self.h))
            wf = self.weight(i, len(self.h)) / float(cnt)
            mf = self.mean(i, len(self.h))

            V2w = wb * (vb) + wf * (vf)
            V2b = wb * wf * (mb - mf) ** 2

            if not math.isnan(V2w):
                self.threshold_values[i] = V2w

    def get_optimal_threshold(self):
        min_V2w = min(self.threshold_values.values())
        optimal_threshold = [k for k, v in self.threshold_values.items() if v == min_V2w]
        return optimal_threshold[0]

    def otsu(self):
        self.threshold_values = {}
        self.h = [1]
        tmpRGB = copy.deepcopy(self.current.convert('L'))
        width, height = tmpRGB.size
        img = np.asarray(copy.deepcopy(tmpRGB))
        self.h = self.otsuHist(img)
        self.threshold(self.h)
        op_thres = self.get_optimal_threshold()
        for w in range(width):
            for h in range(height):
                p = tmpRGB.getpixel((w, h))
                if p > op_thres:
                    tmpRGB.putpixel((w, h), 255)
                else:
                    tmpRGB.putpixel((w, h), 0)

        self.image.append(tmpRGB)
        self.changeCurrent()
