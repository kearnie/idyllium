# perlin noise generator
# based on http://freespace.virgin.net/hugo.elias/models/m_perlin.htm

def linInterpolate(x, y, w):
    return (1 - w) * x + y * w


def noise1d(x, y):
    n = x + y * 57
    n = (n << 13) ^ n
    return (1 - ((n * (n * n * 15731 + 789221) + 1376312589) & 0x7ffffff)) / 1073741824.0


def smooth1(x, y):
    corners = (noise1d(x - 1, y - 1) + noise1d(x + 1, y - 1) + noise1d(x - 1, y + 1) + noise1d(x + 1, y + 1)) / 16
    sides = (noise1d(x - 1, y) + noise1d(x + 1, y) + noise1d(x, y - 1) + noise1d(x, y + 1)) / 8
    center = noise1d(x, y) / 4
    return corners + sides + center


def interpolatedNoise1(x, y):
    xint = int(x)
    fracX = x - xint
    yint = int(y)
    fracY = y - yint
    v1 = smooth1(xint, yint)
    v2 = smooth1(xint + 1, yint)
    v3 = smooth1(xint, yint + 1)
    v4 = smooth1(xint + 1, yint + 1)

    i1 = linInterpolate(v1, v2, fracX)
    i2 = linInterpolate(v3, v4, fracX)
    return linInterpolate(i1, i2, fracY)


def perlin2d(x, y):
    total = 0
    persistence = .5
    octaves = 4
    for i in range(octaves):
        freq = 2 ** i
        amp = persistence ** i
        total += interpolatedNoise1(x * freq, y * freq) * amp
    return total
