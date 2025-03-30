import random
from math import gcd


class fermat:
	def __init__(self, inputNum):
		self.FermatNum = inputNum  # 需检测的数
		self.Flag = False  # 结果标志
		self.runTime = 0  # 循环次数，k

	def judge(self, inputNum):
		return pow(inputNum, self.FermatNum - 1, self.FermatNum)

	def chooseRandInt(self):
		# 随机数选取
		return random.randint(2, self.FermatNum - 2)

	def FermatJudge(self):
		k = 8
		for i in range(k):
			randNum = self.chooseRandInt()
			gcd1 = gcd(self.FermatNum, randNum)
			if gcd1 != 1:
				break
			if self.judge(randNum) != 1:
				break
			self.runTime += 1
		if self.runTime == k:
			self.Flag = True

	def giveResult(self):
		if self.Flag:
			print("数字", self.FermatNum, "是素数的概率是", "{:.2%}".format(1 - (0.5 ** self.runTime)))
		else:
			print("数字", self.FermatNum, "不是素数")


if __name__ == '__main__':
	tag = 4
	with open(f'{tag}.txt', 'r') as f:
		fuzz = int(f.read())
		if 2 >= fuzz > 0:
			print("数字", fuzz, "是素数")
			exit(0)
		elif fuzz <= 0:
			print("数字", fuzz, "不在自然数的范围内")
			exit(-1)
		else:
			judges = fermat(fuzz)
			judges.FermatJudge()
			judges.giveResult()
