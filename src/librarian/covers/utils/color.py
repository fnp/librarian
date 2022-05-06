def luminance(rgb):
    rgb = [
        c / 255 
        for c in rgb
    ]
    rgb = [
        c / 12.92 if c < .03928 else ((c + .055) / 1.055) ** 2.4
        for c in rgb
    ]
    return .2126 * rgb[0] + .7152 * rgb[1] + .0722 * rgb[2]


def cdist(a, b):
    d = abs(a-b)
    if d > 128:
        d = 256 - d
    return d


def algo_contrast_or_hue(img, colors):
    rgb = img.convert('RGB').resize((1, 1)).getpixel((0, 0))
    lumi = luminance(rgb)

    if lumi > .9:
        return colors[3]
    elif lumi < .1:
        return colors[2]

    hue = img.convert('HSV').resize((1, 1)).getpixel((0, 0))[0]
    return max(
        colors[:3],
        key=lambda c: cdist(hue, c['hsv'][0]) ** 2 + (lumi - c['luminance']) ** 2
    )


def is_very_bright(img):
    rgb = img.convert('RGB').getpixel((0, 0))
    lumi = luminance(rgb)
    return lumi > .95
