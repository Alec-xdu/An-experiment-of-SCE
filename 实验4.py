import random

from Crypto.Util.number import getPrime, isPrime
from math import gcd


class ElGamal:
	def __init__(self, plainText: str):
		self.plainText = plainText
		self.prime = findLargePrime()
		self.publicKey = self.generateKeys()
		self.privateKey = 0

	def findPrimitiveRoot(self) -> int:
		primitiveRoot = random.randint(2, self.prime - 1)
		while not (pow(primitiveRoot, 2, self.prime) != 1 and pow(primitiveRoot, self.prime - 1 // 2, self.prime)):
			primitiveRoot = random.randint(2, self.prime - 1)
		print(f'primitive root is {primitiveRoot}')
		return primitiveRoot

	def generateKeys(self) -> list:
		g = self.findPrimitiveRoot()
		a = random.randint(2, self.prime - 1)
		g_a = pow(g, a, self.prime)
		publicKey = [self.prime, g, g_a]
		print(f'public key is {publicKey}\n')
		self.__setPrivateKey(a)
		return publicKey

	def __setPrivateKey(self, privateKey):
		self.privateKey = privateKey

	def encrypt(self):
		plainText = self.plainText
		k = random.randint(2, self.prime - 2)
		# publicKey [p,g,g^a] privateKey [p,g,a]
		c_1 = pow(self.publicKey[1], k, self.prime)
		c_2 = plainText * pow(self.publicKey[1], self.privateKey * k, self.prime)
		print(f'the encrypted text is')
		print(f'c1:{c_1}\nc2:{c_2}\n')
		return c_1, c_2

	def decrypt(self, c_1, c_2) -> int:
		v = pow(c_1, self.privateKey, self.prime)
		m = invMod(v, self.prime) * c_2
		print(f'The original text is {m}')
		return m


def findLargePrime() -> int:
	finalPrime = getPrime(511) * 2 + 1
	while not isPrime(finalPrime):
		finalPrime = getPrime(511) * 2 + 1
	return finalPrime


def invMod(m: int, n: int) -> int:
	s, t, d = extGcd(m, n)
	if gcd(m, n) != 1:
		exit(1)
	if d == 1:
		while s < 0:
			s += n
		return s


def extGcd(a, b):
	if b == 0:
		return 1, 0, a
	else:
		x, y, egcd = extGcd(b, a % b)
		x, y = y, (x - (a // b) * y)
		return x, y, egcd


if __name__ == '__main__':
	tag = 4
	with open(f'secret{tag}.txt', 'r') as secret:
		text = secret.read()
		print(f'plain text is:\n {text}')
		generator = ElGamal(text)
		c1, c2 = generator.encrypt()
		m = generator.decrypt(c1, c2)
		if m == text:
			print('验证成功')
		else:
			print('失败')
