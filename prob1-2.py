#-*- coding: utf-8 -*-
import re
import requests
from konlpy.tag import Twitter
from konlpy.utils import pprint
import csv

class Main():
	def __init__(self):
		self.word_list = []
		self.csv_list = {}

	def load_csv(self):
		with open('polarity.csv', newline='') as csvfile:
			reader = csv.DictReader(csvfile)
			for row in reader:
				self.csv_list[row['ngram']] = "{0}|{1}".format(row['NEG'], row['POS'])
		# self.csv_list['힘'].split("|")[0] -> NEG
		# self.csv_list['힘'].split("|")[1] -> POS

	def process_news(self):
		print("[*] 뉴스 전처리 시작")
		r = requests.get("http://highfaiv.kr/naver_news.html")
		r.encoding = "utf8"

		pattern = "<td class='normal' valign='top'>(.*?)</td>"
		r1 = re.findall(pattern, r.text)

		# Title
		for i in range(2, len(r1)-24, 6):
			self.word_list.append(r1[i])
		print("[*] Title 수집 완료")

		# article_body
		for i in range(5, len(r1)-20, 6):
			self.word_list.append(r1[i])
		print("[*] article_body 수집 완료")

	def process_comment(self):
		print("[*] 댓글 전처리 시작")
		r = requests.get("http://highfaiv.kr/naver_comment.html")
		r.encoding = "utf8"

		pattern = "<td class='normal' valign='top'>(.*?)</td>"
		r1 = re.findall(pattern, r.text)

		# Reply
		for i in range(3, len(r1)-24, 6):
			self.word_list.append(r1[i])
		print("[*] Reply 수집 완료")

	def process_comment2(self):
		print("[*] 대댓글 전처리 시작")
		r = requests.get("http://highfaiv.kr/naver_comment2.html")
		r.encoding = "utf8"

		pattern = "<td class='normal' valign='top'>(.*?)</td>"
		r1 = re.findall(pattern, r.text)

		# ReRe
		for i in range(4, len(r1)-24, 5):
			self.word_list.append(r1[i])
		print("[*] ReRe 수집 완료")

	def emotion_check(self):
		print("[*] 긍정/부정 검사 시작")
		f = open("check.txt", 'w')
		output = ""
		for i in range(0, len(self.word_list)):
			pos_sum = 0
			neg_sum = 0
			output += self.word_list[i]
			noun_list = self.get_noun(self.word_list[i])
			for noun in noun_list:
				try: # 단어가 없는 경우 대비
					neg_sum += float(self.csv_list[noun].split("|")[0])
					pos_sum += float(self.csv_list[noun].split("|")[1])
				except:
					pass
			if pos_sum > neg_sum:
				output += " -> 긍정"
			elif pos_sum < neg_sum:
				output += " -> 부정"
			elif pos_sum == neg_sum:
				output += " -> 판단 불가"

			output += "(Positive : {0} / Negative : {1})\n".format(pos_sum, neg_sum)

			f.write(output)
			output = ""
		f.close()

	def get_noun(self, sentence):
		twitter = Twitter()
		return twitter.nouns(sentence)


	def run(self):
		self.process_news()
		self.process_comment()
		self.process_comment2()
		self.load_csv()
		self.emotion_check()

if __name__ == '__main__':
	main = Main()
	main.run()