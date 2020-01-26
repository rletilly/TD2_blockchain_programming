class Point:

    def __init__(self, x=0, y=0, z=0):
        self.x = x
        self.y = y
        self.z = z

class Math:

    @classmethod
    def multiply(cls, p, n, N, A, P):
        """
        Fast way to multily point and scalar in elliptic curves
        :param p: First Point to mutiply
        :param n: Scalar to mutiply
        :param N: Order of the elliptic curve
        :param P: Prime number in the module of the equation Y^2 = X^3 + A*X + B (mod p)
        :param A: Coefficient of the first-order term of the equation Y^2 = X^3 + A*X + B (mod p)
        :return: Point that represents the sum of First and Second Point
        """
        return cls._fromJacobian(
            cls._jacobianMultiply(
                cls._toJacobian(p),
                n,
                N,
                A,
                P,
            ),
            P,
        )

    @classmethod
    def add(cls, p, q, A, P):
        """
        Fast way to add two points in elliptic curves
        :param p: First Point you want to add
        :param q: Second Point you want to add
        :param P: Prime number in the module of the equation Y^2 = X^3 + A*X + B (mod p)
        :param A: Coefficient of the first-order term of the equation Y^2 = X^3 + A*X + B (mod p)
        :return: Point that represents the sum of First and Second Point
        """
        return cls._fromJacobian(
            cls._jacobianAdd(
                cls._toJacobian(p),
                cls._toJacobian(q),
                A,
                P,
            ),
            P,
        )

    @classmethod
    def inv(cls, x, n):
        """
        Extended Euclidean Algorithm. It's the 'division' in elliptic curves
        :param x: Divisor
        :param n: Mod for division
        :return: Value representing the division
        """
        if x == 0:
            return 0

        lm, hm = 1, 0
        low, high = x % n, n
        while low > 1:
            r = high // low
            nm, new = hm - lm * r, high - low * r
            lm, low, hm, high = nm, new, lm, low

        return lm % n

    @classmethod
    def _toJacobian(cls, p):
        """
        Convert point to Jacobian coordinates
        :param p: First Point you want to add
        :return: Point in Jacobian coordinates
        """
        return Point(p.x, p.y, 1)

    @classmethod
    def _fromJacobian(cls, p, P):
        """
        Convert point back from Jacobian coordinates
        :param p: First Point you want to add
        :param P: Prime number in the module of the equation Y^2 = X^3 + A*X + B (mod p)
        :return: Point in default coordinates
        """
        z = cls.inv(p.z, P)

        return Point(
            (p.x * z ** 2) % P,
            (p.y * z ** 3) % P,
        )

    @classmethod
    def _jacobianDouble(cls, p, A, P):
        """
        Double a point in elliptic curves
        :param p: Point you want to double
        :param P: Prime number in the module of the equation Y^2 = X^3 + A*X + B (mod p)
        :param A: Coefficient of the first-order term of the equation Y^2 = X^3 + A*X + B (mod p)
        :return: Point that represents the sum of First and Second Point
        """
        if not p.y:
            return Point(0, 0, 0)

        ysq = (p.y ** 2) % P
        S = (4 * p.x * ysq) % P
        M = (3 * p.x ** 2 + A * p.z ** 4) % P
        nx = (M**2 - 2 * S) % P
        ny = (M * (S - nx) - 8 * ysq ** 2) % P
        nz = (2 * p.y * p.z) % P
        return Point(nx, ny, nz)

    @classmethod
    def _jacobianAdd(cls, p, q, A, P):
        """
        Add two points in elliptic curves
        :param p: First Point you want to add
        :param q: Second Point you want to add
        :param P: Prime number in the module of the equation Y^2 = X^3 + A*X + B (mod p)
        :param A: Coefficient of the first-order term of the equation Y^2 = X^3 + A*X + B (mod p)
        :return: Point that represents the sum of First and Second Point
        """

        if not p.y:
            return q
        if not q.y:
            return p

        U1 = (p.x * q.z ** 2) % P
        U2 = (q.x * p.z ** 2) % P
        S1 = (p.y * q.z ** 3) % P
        S2 = (q.y * p.z ** 3) % P

        if U1 == U2:
            if S1 != S2:
                return Point(0, 0, 1)
            return cls._jacobianDouble(p, A, P)

        H = U2 - U1
        R = S2 - S1
        H2 = (H * H) % P
        H3 = (H * H2) % P
        U1H2 = (U1 * H2) % P
        nx = (R ** 2 - H3 - 2 * U1H2) % P
        ny = (R * (U1H2 - nx) - S1 * H3) % P
        nz = (H * p.z * q.z) % P

        return Point(nx, ny, nz)

    @classmethod
    def _jacobianMultiply(cls, p, n, N, A, P):
        """
        Multily point and scalar in elliptic curves
        :param p: First Point to mutiply
        :param n: Scalar to mutiply
        :param N: Order of the elliptic curve
        :param P: Prime number in the module of the equation Y^2 = X^3 + A*X + B (mod p)
        :param A: Coefficient of the first-order term of the equation Y^2 = X^3 + A*X + B (mod p)
        :return: Point that represents the sum of First and Second Point
        """
        if p.y == 0 or n == 0:
            return Point(0, 0, 1)

        if n == 1:
            return p

        if n < 0 or n >= N:
            return cls._jacobianMultiply(p, n % N, N, A, P)

        if (n % 2) == 0:
            return cls._jacobianDouble(
                cls._jacobianMultiply(
                    p,
                    n // 2,
                    N,
                    A,
                    P
                ),
                A,
                P,
            )

        # (n % 2) == 1:
        return cls._jacobianAdd(
            cls._jacobianDouble(
                cls._jacobianMultiply(
                    p,
                    n // 2,
                    N,
                    A,
                    P,
                ),
                A,
                P,
            ),
            p,
            A,
            P,
        )
class CurveFp:

    def __init__(self, A, B, P, N, Gx, Gy, name, oid, nistName=None):
        self.A = A
        self.B = B
        self.P = P
        self.N = N
        self.G = Point(Gx, Gy)
        self.name = name
        self.nistName = nistName
        self.oid = oid

    def contains(self, p):
        """
        Verify if the point `p` is on the curve
        :param p: Point p = Point(x, y)
        :return: boolean
        """
        return (p.y**2 - (p.x**3 + self.A * p.x + self.B)) % self.P == 0

    def length(self):
        return (1 + len("%x" % self.N)) // 2


secp256k1 = CurveFp(
    name="secp256k1",
    A=0x0000000000000000000000000000000000000000000000000000000000000000,
    B=0x0000000000000000000000000000000000000000000000000000000000000007,
    P=0xfffffffffffffffffffffffffffffffffffffffffffffffffffffffefffffc2f,
    N=0xfffffffffffffffffffffffffffffffebaaedce6af48a03bbfd25e8cd0364141,
    Gx=0x79be667ef9dcbbac55a06295ce870b07029bfcdb2dce28d959f2815b16f81798,
    Gy=0x483ada7726a3c4655da4fbfc0e1108a8fd17b448a68554199c47d08ffb10d4b8,
    oid=(1, 3, 132, 0, 10)
)

prime256v1 = CurveFp(
    name="prime256v1",
    nistName="P-256",
    A=0xffffffff00000001000000000000000000000000fffffffffffffffffffffffc,
    B=0x5ac635d8aa3a93e7b3ebbd55769886bc651d06b0cc53b0f63bce3c3e27d2604b,
    P=0xffffffff00000001000000000000000000000000ffffffffffffffffffffffff,
    N=0xffffffff00000000ffffffffffffffffbce6faada7179e84f3b9cac2fc632551,
    Gx=0x6b17d1f2e12c4247f8bce6e563a440f277037d812deb33a0f4a13945d898c296,
    Gy=0x4fe342e2fe1a7f9b8ee7eb4a7c0f9e162bce33576b315ececbb6406837bf51f5,
    oid=(1, 2, 840, 10045, 3, 1, 7),
)
p256 = prime256v1

supportedCurves = [
    secp256k1,
    prime256v1,
]

curvesByOid = {curve.oid: curve for curve in supportedCurves}

