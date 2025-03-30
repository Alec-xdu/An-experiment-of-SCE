from random import randint, sample
from math import gcd, prod


# 扩展欧几里得算法求模逆
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


# 检验互素
def listPrimeCheck(inputList: list) -> bool:
	flag = True
	listSize = len(inputList)
	for i in range(0, listSize):
		for j in range(i + 1, listSize):
			if gcd(inputList[i], inputList[j]) != 1:
				flag = False
				break
	return flag


def intPrimeCheck(inputList: list, inputNum: int) -> bool:
	flag = True
	listSize = len(inputList)
	for i in range(0, listSize):
		if gcd(inputList[i], inputNum) != 1:
			flag = False
			break
	return flag


# 中国剩余定理
def crt(aiList: list, miList: list) -> int:
	if len(aiList) != len(miList):
		print('输入的m和a需成对')
		exit(1)
	else:
		for i in range(0, len(aiList)):
			print(f'a{i}:{aiList[i]}')
			print(f'm{i}:{miList[i]}')
		print()
	if not listPrimeCheck(miList):
		print('m_i不互素')
		exit(1)
	M = prod(miList)
	m_j = [M // m_i for m_i in miList]
	m_1_j = [invMod(m_j, m_i) for m_j, m_i in zip(m_j, miList)]
	x_j = [a_i * m_i * m_1_i for a_i, m_i, m_1_i in zip(aiList, m_j, m_1_j)]
	return sum(x_j) % M


def enc(t, n, plaintext):
	dList = initDList(n, t)
	preNKey = prod(dList[:t])
	lastNKey = prod(dList[n - t + 1:])
	print(f'N:{preNKey}')
	print(f'M:{lastNKey}\n')
	kList = [p % d for p, d in zip([plaintext] * n, dList)]
	return list(zip(kList, dList))


def dec(encryptedKey, t):
	if len(encryptedKey) < t:
		print(f'不足{t}组，解密失败')
		exit(1)
	aiList = [encryptedKey[i][0] for i in range(t)]
	miList = [encryptedKey[i][1] for i in range(t)]
	return crt(aiList=aiList, miList=miList)


# 生成D_i
def initDList(n, t):
	x = 1
	dList = list()
	for i in range(0, 500):
		if (i * t > 502) & (i * (t - 1) < 502):
			x = i
			break
	print(f'x:{x}')
	dList.append(randint(pow(10, x), pow(10, x + 1)))
	for i in range(0, n):
		m = randint(pow(10, x), pow(10, x + 1))
		if intPrimeCheck(dList, m):
			dList.append(m)
	return dList


if __name__ == '__main__':
	t = int(input('t=?\n'))
	n = int(input('n=?\n'))
	dList = initDList(n=n, t=t)
	print(dList)
	tag = 4
	with open(f'secret{tag}.txt', 'r') as secret:
		plainKey = int(secret.read())
		print(f'plainText={plainKey}\n')
		encryptKey = enc(t=t, n=n, plaintext=plainKey)
		print(f'encryptedKey={encryptKey}\n')
		decryptKey = dec(encryptedKey=encryptKey, t=t)
		print(f'decryptedKey={decryptKey}\n')
	if decryptKey == plainKey:
		print('成功！')
