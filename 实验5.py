import hashlib
from random import randint
from math import ceil, log2


class dot:
	def __init__(self, x, y):
		self.x = x
		self.y = y

	def copy(self, other):
		self.x = other.x
		self.y = other.y


INFINITY = None


class sm_2:
	def __init__(self):
		"""
		椭圆曲线的参数选取了原标准文档第90页使用的参数
		"""
		self.len = None
		self.paramA = 0x787968B4FA32C3FD2417842E73BBFEFF2F3C848B6831D7E0EC65228B3937E498
		self.paramB = 0x63E4C6D3B23B0C849CF84241484BFE48F61D59A5B16BA06E6E12D1DA27C5249A
		self.paramP = 0x8542D69E4C044F18E8B92435BF6FF7DE457283915C45517D722EDB8B08F1DFC3
		self.n = 0x8542D69E4C044F18E8B92435BF6FF7DD297720630485628D5AE74EE7C32E79B7
		self.paramH = 1
		self.v = 256
		self.G = dot(0x421DEBD61B62EAB6746434EBC3CC315E32220B3BADD50BDC4C4E6C147FEDD43D,
		             0x0680512BCBB42C07D47349D2153B70C4E5D7FDFCBFA36EA1A85841B9E46E09A2)
		self.__d = 0
		self.__p = dot(1, 1)
		self.getKeys()

	# 获取随机的k值
	@classmethod
	def getRandK(cls, start: int, end: int) -> int:
		return randint(start, end - 1)

	@classmethod
	def int2Bytes(cls, x: int, k: int):
		"""
		4.2.1整数转字节串
		:param x: 非负整数
		:param k: 字节串的长度
		:return: M：长度为k的字节串
		"""
		M = b''
		for i in range(0, k):
			M += (x % 256).to_bytes(1, 'big')
			x = x // 256
		return M

	@classmethod
	def bytes2Int(cls, M: bytes):
		"""
		4.2.2字节串转整数
		:param M:
		:return:
		"""
		byteSum = 0
		MList = list(M)
		k = len(MList)
		for i in range(0, k):
			byteSum += pow(2, 8 * i) * MList[i]
		return byteSum

	@classmethod
	def bitFill(cls, bits: str):
		"""
		4.2.3比特串转字节串,将二进制比特串转为bytes
		:param bits:比特串
		:return: k字节长的字节串
		"""
		m = len(bits)
		k = ceil(m / 8)
		# 向右对齐，往左补零，凑8倍数位
		bits = bits.rjust(k * 8, "0")
		M = b""
		for i in range(k):
			M = bytes([int(bits[-(i * 8 + 8):][:8], 2)]) + M
		return M

	@classmethod
	def bytes2Bits(cls, ByteStr: bytes) -> str:
		"""
		4.2.4字节串转二进制比特串
		:param ByteStr: 字节串
		:return: 比特串
		"""
		bLen = len(ByteStr)
		bits = str()
		for i in range(0, bLen):
			# bin格式以0b开头，需要从2位开始截取
			bits += (bin(ByteStr[i])[2:]).rjust(8, '0')
		return bits

	def fq2Bytes(self, a):
		"""
		4.2.5域元素转字节串
		:param a: 域中元素alpha
		:return: l长的字节串
		"""
		q = self.paramP  # 定义过的素数，取2的概率极小在这不考虑了
		assert 0 <= a <= q - 1
		# l = [ t / 8 ]
		l = ceil(log2(q) / 8)
		return self.int2Bytes(a, l)

	def bytes2Fq(self, S: bytes):
		"""
		4.2.6将字节串转为域元素
		:param S: 字节串
		:return: a
		"""
		q = self.paramP
		l = ceil(log2(q) / 8)
		assert l == len(S)
		return self.bytes2Int(S)

	"""
	4.2.7,取的q是素数，可以省略
	"""

	def dot2Bytes(self, dotP: dot):
		"""
		4.2.8用未压缩表示形式将点转为字节串
		:param dotP: 点P
		:return: S = PC || X || Y
		"""
		PC = b'\x04'
		x = self.fq2Bytes(dotP.x)
		y = self.fq2Bytes(dotP.y)
		return PC + x + y

	def bytes2Dot(self, S: bytes):
		"""
		4.2.9未压缩表示形式将字节串转换为点
		:param S: 字节串
		:return: 对应的点
		"""
		PC = S[0]
		q = self.paramP
		lth = ceil(log2(q) / 8)
		y = self.bytes2Int(S[lth + 1:])
		x = self.bytes2Int(S[1:lth + 1])
		if not pow(y, 2) % self.paramP == (pow(x, 3) + self.paramA * x + self.paramB) % self.paramP:
			exit(-1)
		return dot(x, y)

	def getKeys(self):
		"""
		生成私钥公钥的函数
		:return:
		"""
		d = self.getRandK(1, self.n - 1)
		self.setPrivateKey(d)
		print(f'private key:\n{d}')
		p = self.kTimesDot(self.G, d)
		print(f'public key:\nx:{p.x}\ny:{p.y}')
		self.setPublicKey(p)

	def setPublicKey(self, publicKey: dot):
		self.__p.copy(publicKey)

	def setPrivateKey(self, privateKey):
		self.__d = privateKey

	def encrypt(self, plainText: bytes):
		message = self.bytes2Bits(plainText)
		print(f'm:\n{self.bitFill(message).hex()}')
		mLth = len(message)
		k = self.getRandK(1, self.n - 1)
		C1 = self.kTimesDot(self.G, k)
		C1 = self.bytes2Bits(self.dot2Bytes(C1))
		S = self.kTimesDot(self.__p, k)
		assert self.dotAdd(S, self.G) != self.G
		PB = self.kTimesDot(self.__p, k)
		x_bits = self.bytes2Bits(self.fq2Bytes(PB.x))
		y_bits = self.bytes2Bits(self.fq2Bytes(PB.y))
		t = self.KDF(x_bits + y_bits, mLth)
		print(f't:\n{self.bitFill(t).hex()}')
		assert t.count('0') != mLth
		C2 = self.xor(message, t)
		self.len = mLth
		C3 = self.sm3Hash(x_bits + message + y_bits)
		cipherText = C1 + C2 + C3
		print(f'c1:\n{self.bitFill(C1).hex()}')
		print(f'c2:\n{self.bitFill(C2).hex()}')
		print(f'c3:\n{self.bitFill(C3).hex()}')
		print(f'cipherText:\n{self.bitFill(cipherText).hex()}')
		return self.bitFill(cipherText)

	def decrypt(self, encText: bytes):
		bits = self.bytes2Bits(encText)
		C1Len = 8 * (2 * ceil(log2(self.paramP) / 8) + 1)  # 由fq2Bytes两次运算+PC得出
		C3Len = self.v  # 定值
		kLen = len(bits) - C1Len - C3Len
		C1, C2, C3 = bits[:C1Len], bits[C1Len: C1Len + kLen], bits[C1Len + kLen:]
		# print(f'C1:{C1}\n')
		# print(1)
		C1Dot = self.bytes2Dot(self.bitFill(C1))
		HC1dot = self.kTimesDot(C1Dot, self.paramH)
		assert C1Dot != INFINITY
		HC1dot = self.kTimesDot(HC1dot, self.__d)
		x_bits = self.bytes2Bits(self.fq2Bytes(HC1dot.x))
		y_bits = self.bytes2Bits(self.fq2Bytes(HC1dot.y))
		t = self.KDF(x_bits + y_bits, kLen)
		assert t.count('0') != kLen
		# print(f't:\n{self.bitFill(t).hex()}')
		plainText = self.xor(C2, t)
		# print(f'C1:\n{self.bitFill(C1).hex()}')
		# print(f'C2:\n{self.bitFill(C2).hex()}')
		# print(f'C3:\n{self.bitFill(C3).hex()}')
		# judge = True if self.sm3Hash(x_bits + plainText + y_bits) == C3 else False
		print(f'p:\n{self.bitFill(plainText)}')
		assert self.sm3Hash(x_bits + plainText + y_bits) == C3
		return self.bitFill(plainText).decode()

	@classmethod
	def xor(cls, m: str, t: str):
		mLen = len(m)
		res = "".join([str(int(m[i]) ^ int(t[i])) for i in range(mLen)])
		return res

	# 密钥派生函数
	def KDF(self, z: str, kLen: int) -> str:
		"""
		:param z: 比特串Z
		:param kLen: 整数表示要获得的密钥数据比特长度
		:return: 密钥数据比特串
		"""
		ct = 0x00000001
		v = self.v
		HaList = list()
		key = str()
		for i in range(0, ceil(kLen / v)):
			HaList.append(self.sm3Hash(z + bin(ct)[2:]))
			ct += 1
			key += HaList[i]
		if not kLen // v == ceil(kLen / v):
			key = key[:kLen]
		return key

	# sm3散列函数
	def sm3Hash(self, plainText: str) -> str:
		"""
		sm3哈希算法
		:param plainText:
		:return:二进制比特字符串形式散列值
		"""
		Bytes = self.bitFill(bits=plainText)
		SM3Generator = hashlib.new(name='sm3')
		SM3Generator.update(Bytes)
		return self.bytes2Bits(SM3Generator.digest())

	# 模加运算
	def modAdd(self, m, n):
		return pow(m + n, 1, self.paramP)

	# 模减运算
	def modMinus(self, m, n):
		return pow(m - n, 1, self.paramP)

	# 模乘运算
	def modMulti(self, m, n):
		return pow(m * n, 1, self.paramP)

	def invMod(self, x):
		return pow(x, self.paramP - 2, self.paramP)

	def negMod(self, x):
		return pow(-x, 1, self.paramP)

	def getMultiLambda(self, dot1: dot):
		"""
		计算点的切线斜率lambda
		:param dot1: 某点
		:return:倍点对应的lambda
		"""
		upper = self.modMulti(3, self.modMulti(dot1.x, dot1.x)) + self.paramA
		lower = self.modMulti(2, dot1.y)
		return self.modMulti(upper, self.invMod(lower))

	def getAddLambda(self, dotA: dot, dotB: dot):
		"""
		计算二点斜率Lambda
		:param dotA: 点A
		:param dotB: 点B
		:return: 对应的Lambda
		"""
		upper = self.modMinus(dotB.y, dotA.y)
		lower = self.modMinus(dotB.x, dotA.x)
		return self.modMulti(upper, self.invMod(lower))

	def dotAdd(self, dotA: dot, dotB: dot):
		"""
		有限域上的点加
		:param dotA: 点A
		:param dotB: 点B
		:return: 计算得到的第三个点
		"""
		if dotA is INFINITY:
			return dotB
		elif dotB is INFINITY:
			return dotA
		if dotA.x == dotB.x and dotA.y == self.invMod(dotB.y):
			return INFINITY
		elif dotA.x == dotB.x:
			Lambda = self.getMultiLambda(dotA)
		else:
			Lambda = self.getAddLambda(dotA, dotB)
		# x_3 = lambda^2 - x_1 - x_2
		x = self.modMinus(self.modMulti(Lambda, Lambda), dotA.x)
		x = self.modMinus(x, dotB.x)
		# y_3 = lambda * (x_1 - x_3) - y_1
		y = self.modMulti(Lambda, self.modMinus(dotA.x, x))
		y = self.modMinus(y, dotA.y)
		return dot(x, y)

	def kTimesDot(self, P: dot, k: int) -> dot:
		"""
		二进制展开法求多倍点
		:param P: 点
		:param k: 倍数
		:return: k倍点
		"""
		if P == INFINITY:
			return P
		Q = INFINITY
		kList = list(bin(k)[2:])
		for i in kList:
			Q = self.dotAdd(Q, Q)
			if int(i) == 1:
				Q = self.dotAdd(Q, P)
		return Q


if __name__ == '__main__':
	sm = sm_2()
	tag = 10
	# PList = list()
	# for i in range(6, 11):
	with open(f'./{tag}.txt', 'r') as f:
		plaintext = f.read().encode()
		print(plaintext)
		encrypted = sm.encrypt(plaintext)
		decrypted = sm.decrypt(encrypted)
		print(decrypted)
		assert decrypted == plaintext.decode()
		print('成功解密')
		# PList.append(decrypted)

	# print(len(PList))
	# print(PList)
