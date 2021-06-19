from PIL import Image, ImageQt, ImageEnhance, ImageOps, ImageDraw, ImageFile
import math
import copy
import numpy as np
from scipy.ndimage.filters import convolve
import scipy.stats as st
import matplotlib.pyplot as plt


class Images():
    def __init__(self):
        ImageFile.LOAD_TRUNCATED_IMAGES = True
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
        return m / float(w)  # warning about divide by 0, left in case of other warnings

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

    def gaussian_kernel(self, size, sigma=1.8):
        size = int(size) // 2
        x, y = np.mgrid[-size:size + 1, -size:size + 1]
        normal = 1 / (2.0 * np.pi * sigma ** 2)
        g = np.exp(-((x ** 2 + y ** 2) / (2.0 * sigma ** 2))) * normal
        return g

    def sobel_filters(self, A):
        Kx = np.array([[-1, 0, 1], [-2, 0, 2], [-1, 0, 1]])
        Ky = np.array([[1, 2, 1], [0, 0, 0], [-1, -2, -1]])
        Kz = np.array([[0, 1, 2], [-1, 0, 1], [-2, -1, 0]])
        Kv = np.array([[2, 1, 0], [1, 0, -1], [0, -1, -2]])

        Gx = self.convolve(A, Kx)
        Gy = self.convolve(A, Ky)
        Gz = self.convolve(A, Kz)
        Gv = self.convolve(A, Kv)
        P = np.hypot(Gx, Gy)
        Gg = np.hypot(Gz, Gv)
        P = np.hypot(P, Gg)
        P = P / P.max() * 255
        theta = np.arctan2(Gy, Gx)

        return (P, theta)

    def non_max_suppression(self, img, D):
        M, N = img.shape
        Z = np.zeros((M, N), dtype=np.int32)
        angle = D * 180. / np.pi
        angle[angle < 0] += 180

        for i in range(1, M - 1):
            for j in range(1, N - 1):
                try:
                    q = 255
                    r = 255

                    # angle 0
                    if (0 <= angle[i, j] < 22.5) or (157.5 <= angle[i, j] <= 180):
                        q = img[i, j + 1]
                        r = img[i, j - 1]
                    # angle 45
                    elif (22.5 <= angle[i, j] < 67.5):
                        q = img[i + 1, j - 1]
                        r = img[i - 1, j + 1]
                    # angle 90
                    elif (67.5 <= angle[i, j] < 112.5):
                        q = img[i + 1, j]
                        r = img[i - 1, j]
                    # angle 135
                    elif (112.5 <= angle[i, j] < 157.5):
                        q = img[i - 1, j - 1]
                        r = img[i + 1, j + 1]

                    if (img[i, j] >= q) and (img[i, j] >= r):
                        Z[i, j] = img[i, j]
                    else:
                        Z[i, j] = 0

                except IndexError as e:
                    pass

        return Z

    def threshold(self, img, lowRatio, highRatio):

        highThreshold = img.max() * highRatio
        lowThreshold = highThreshold * lowRatio

        M, N = img.shape
        thresh = np.zeros((M, N), dtype=np.int8)

        weak = np.int8(25)
        strong = np.int8(255)

        strong_i, strong_j = np.where(img >= highThreshold)
        zeros_i, zeros_j = np.where(img < lowThreshold)

        weak_i, weak_j = np.where((img <= highThreshold) & (img >= lowThreshold))

        thresh[strong_i, strong_j] = strong
        thresh[weak_i, weak_j] = weak

        return (thresh, weak, strong)

    def edgeTrack(self, img, weak, strong=255):

        M, N = img.shape

        for i in range(1, M - 1):
            for j in range(1, N - 1):
                if (img[i, j] == weak):
                    try:
                        if ((img[i + 1, j - 1] == strong) or (img[i + 1, j] == strong) or (img[i + 1, j + 1] == strong)
                                or (img[i, j - 1] == strong) or (img[i, j + 1] == strong)
                                or (img[i - 1, j - 1] == strong) or (img[i - 1, j] == strong) or (
                                        img[i - 1, j + 1] == strong)):
                            img[i, j] = strong
                        else:
                            img[i, j] = 0
                    except IndexError as e:
                        pass

        return img

    def convolve(self, array, convolver):
        return convolve(array, convolver)

    def canny(self,low=0.05,high=0.20):
        tmpRGB = np.asarray(copy.deepcopy(self.current.convert('I')))
        gauss = self.gaussian_kernel(5, sigma=1.5)
        tmp = self.convolve(tmpRGB, gauss)
        im, imTheta = self.sobel_filters(tmp)
        nMax = self.non_max_suppression(im, imTheta)
        thresh, weak, strong = self.threshold(nMax, lowRatio=low, highRatio=high)
        img = self.edgeTrack(thresh, weak, strong=strong)

        tmpRGB = Image.fromarray(img.astype(np.uint8))
        self.image.append(tmpRGB)
        self.changeCurrent()

    def gaussian_blur(self,ratio):
        kernel_lenght= int(ratio)
        nsig=2.5
        x = np.linspace(-nsig, nsig, kernel_lenght + 1)
        kern1d = np.diff(st.norm.cdf(x))
        kern2d = np.outer(kern1d, kern1d)
        gauss_kernel = kern2d/kern2d.sum()
        self.convultion_with_kernel(gauss_kernel)

    def mean_blur(self,ratio):
        mean_kernel = [[1/10-ratio, 1/10-ratio, 1/10-ratio],
                  [1/10-ratio, 1/10-ratio, 1/10-ratio],
                  [1/10-ratio, 1/10-ratio, 1/10-ratio]]
        self.convultion_with_kernel(mean_kernel)

    def sharp(self,ratio):
        kernel = np.array([[0, -.5, 0],
                  [-.5, 3, -.5],
                  [0, -.5, 0]]) * (1+ratio)
        self.convultion_with_kernel(kernel)

    def sobel(self):
        tmpRGB = np.asarray(copy.deepcopy(self.current.convert('I')))
        im, imTheta = self.sobel_filters(tmpRGB)
        tmpRGB = Image.fromarray(im.astype(np.uint8))
        self.image.append(tmpRGB)
        self.changeCurrent()

    def prewitt(self):
        A = np.asarray(copy.deepcopy(self.current.convert('I')))
        Kx = np.array([[1,1,1],[0,0,0],[-1,-1,-1]])
        Ky = np.array([[-1,0,1],[-1,0,1],[-1,0,1]])
        Gx = self.convolve(A, Kx)
        Gy = self.convolve(A, Ky)
        P = np.hypot(Gx, Gy)
        P = P / P.max() * 255
        tmpRGB = Image.fromarray(P.astype(np.uint8))
        self.image.append(tmpRGB)
        self.changeCurrent()

    def roberts(self):
        A = np.asarray(copy.deepcopy(self.current.convert('I')))
        Kx = np.array([[ 0, 0, 0 ],
                       [ 0, 1, 0 ],
                       [ 0, 0,-1 ]])
        Ky = np.array([[ 0, 0, 0 ],
                       [ 0, 0, 1 ],
                       [ 0,-1, 0 ]])
        Gx = self.convolve(A, Kx)
        Gy = self.convolve(A, Ky)
        P = np.hypot(Gx, Gy)
        P = P / P.max() * 255
        tmpRGB = Image.fromarray(P.astype(np.uint8))
        self.image.append(tmpRGB)
        self.changeCurrent()

    def kirsch(self):
        A = np.asarray(copy.deepcopy(self.current.convert('I')))
        Kx = np.array([[5, -3, -3], [5, 0, -3], [5, -3, -3]])
        Ky = np.array([[-3, -3, 5], [-3, 0, 5], [-3, -3, 5]])
        Kz = np.array([[-3, -3, -3], [5, 0, -3], [5, 5, -3]])
        Kv = np.array([[-3, 5, 5], [-3, 0, 5], [-3, -3, -3]])
        Kb = np.array([[-3, -3, -3], [-3, 0, -3], [5, 5, 5]])
        Kn = np.array([[5, 5, 5], [-3, 0, -3], [-3, -3, -3]])
        Km = np.array([[-3, -3, -3], [-3, 0, 5], [-3, 5, 5]])
        Kl = np.array([[5, 5, -3], [5, 0, -3], [-3, -3, -3]])

        Gx = self.convolve(A, Kx)
        Gy = self.convolve(A, Ky)
        Gz = self.convolve(A, Kz)
        Gv = self.convolve(A, Kv)
        Gb = self.convolve(A, Kb)
        Gn = self.convolve(A, Kn)
        Gm = self.convolve(A, Km)
        Gl = self.convolve(A, Kl)

        P = np.hypot(Gx, Gy)
        Gg = np.hypot(Gz, Gv)
        Pg = np.hypot(Gb, Gn)
        Pb = np.hypot(Gm, Gl)
        P = np.hypot(P, Gg)
        P = np.hypot(P, Pg)
        P = np.hypot(P, Pb)
        P = P / P.max() * 255
        tmpRGB = Image.fromarray(P.astype(np.uint8))
        self.image.append(tmpRGB)
        self.changeCurrent()

    def convultion_with_kernel(self,kernel):
        tmpRGB = copy.deepcopy(self.current)
        old_pixels = tmpRGB.load()
        # prepare new image to draw
        new_image = Image.new("RGB", tmpRGB.size)
        draw = ImageDraw.Draw(new_image)
        # get middle of our kernel
        offset = len(kernel) // 2
        for x in range(offset, tmpRGB.width - offset):
            for y in range(offset, tmpRGB.height - offset):
                acc = [0, 0, 0]
                for a in range(len(kernel)):
                    for b in range(len(kernel)):
                        xn = x + a - offset
                        yn = y + b - offset
                        pixel = old_pixels[xn, yn]
                        acc[0] += pixel[0] * kernel[a][b]
                        acc[1] += pixel[1] * kernel[a][b]
                        acc[2] += pixel[2] * kernel[a][b]

                draw.point((x, y), (int(acc[0]), int(acc[1]), int(acc[2])))
        self.image.append(new_image)
        self.changeCurrent()