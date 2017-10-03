import math


def mMultiply(A: list, B: list, C: list, m: int):
    for i in range(0, m):
        for j in range(0, m):
            s = 0.
            for k in range(0, m):
                s += A[i * m + k] * B[k * m + j]
            C[i * m + j] = s


def mPower(A: list, eA: int, V: list, eV: list, m: int, n: int):
    if n == 1:
        for i in range(0, m * m):
            V[i] = A[i]
        eV[0] = eA
        return None
    mPower(A, eA, V, eV, m, int(n / 2))
    B = []
    for i in range(0, m * m):
        B.append(0.0)
    mMultiply(V, V, B, m)
    eB = 2 * (eV[0])
    if n % 2 == 0:
        for i in range(0, m * m):
            V[i] = B[i]
        eV[0] = eB
    else:
        mMultiply(A, B, V, m)
        eV[0] = eA + eB
    if V[int(m / 2) * m + int(m / 2)] > 1e140:
        for i in range(0, m * m):
            V[i] = V[i] * 1e-140
        eV[0] += 140


def K(n: int, d: float) -> float:
    if d < 0:
        return 0

    # OMIT NEXT LINE IF YOU REQUIRE >7 DIGIT ACCURACY IN THE RIGHT TAIL
    s = d * d * n
    if s > 7.24 or (s > 3.76 and n > 99):
        return 1 - 2 * math.exp(-(2.000071 + .331 / math.sqrt(n) + 1.409 / n) * s)
    k = int((n * d) + 1)
    m = 2 * k - 1
    h = k - n * d
    H = []
    Q = []
    for i in range(0, m * m):
        H.append(0.0)
        Q.append(0.0)
    for i in range(0, m):
        for j in range(0, m):
            if i - j + 1 < 0:
                H[i * m + j] = 0
            else:
                H[i * m + j] = 1

    for i in range(0, m):
        H[i * m] -= math.pow(h, i + 1)
        H[(m - 1) * m + i] -= math.pow(h, (m - i))

    H[(m - 1) * m] += math.pow(2 * h - 1, m) if (2 * h - 1 > 0) else 0
    for i in range(0, m):
        for j in range(0, m):
            if i - j + 1 > 0:
                for g in range(1, i - j + 2):
                    H[i * m + j] /= g
    eH = 0
    eQ = [0]
    mPower(H, eH, Q, eQ, m, int(n))
    s = Q[(k - 1) * m + k - 1]
    for i in range(1, n + 1):
        s = s * i / n
        if s < 1e-140:
            s *= 1e140
            eQ[0] -= 140

    s *= math.pow(10., eQ[0])
    return s
