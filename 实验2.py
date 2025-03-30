from math import gcd


class CRT:
	def __init__(self):
		with open('8.txt', 'r') as inputData:
			dataList = inputData.read().split('\n')
			dataLen = len(dataList) // 2
			self.AiList = list(map(int, dataList[:dataLen]))
			self.MiList = list(map(int, dataList[dataLen:]))
		self.len = len(self.MiList)
		self.X_i = []
		self.M_jList = []
		self.M_Res = []
		self.m = 1

	# 判断是否能满足中国剩余定理的使用条件
	def whetherGcd(self) -> bool:
		flag = False
		if len(self.MiList) != len(self.AiList):
			print('输入的m和a需成对')
		else:
			for M_i in range(0, len(self.MiList)):
				for nextM_i in range(M_i + 1, len(self.MiList)):
					if gcd(self.MiList[M_i], self.MiList[nextM_i]) != 1:
						print('无法直接使用中国剩余定理')
						return flag
			flag = True
		return flag

	def getResult(self) -> int:
		result = 0
		for i in range(0, self.len):
			result += self.M_jList[i] * self.M_Res[i] * self.AiList[i]
		return result % self.m

	def setM(self):
		for M_i in self.MiList:
			self.m *= M_i

	def setM_jList(self):
		for i in range(0, self.len):
			self.M_jList.append(self.m // self.MiList[i])

	def setM_ResList(self):
		for i in range(0, self.len):
			self.M_Res.append(extGcd(self.MiList[i], self.M_jList[i])[1])

	def setX_iList(self):
		for i in range(0, self.len):
			self.X_i.append((self.M_jList[i] * self.M_Res[i] * self.AiList[i]) % self.m)


# 用扩展欧几里得算法算逆元
def extGcd(a, b):
	if b == 0:
		return 1, 0, a
	else:
		x, y, egcd = extGcd(b, a % b)
		x, y = y, (x - (a // b) * y)
		return x, y, egcd


def main():
	CRTcalc = CRT()
	if not CRTcalc.whetherGcd():
		exit(1)
	else:
		CRTcalc.setM()
		CRTcalc.setM_jList()
		CRTcalc.setM_ResList()
		CRTcalc.setX_iList()
		print('x=' + str(CRTcalc.getResult()) + '(mod ' + str(CRTcalc.m) + ')')


if __name__ == '__main__':
	main()
