

def normalize(v):
    lengthSquared = v[0] * v[0] + v[1] * v[1];
    if (lengthSquared is not 0):
        length = sqrt(lengthSquared)
        v[0] /= length
        v[1] /= length
    return v
