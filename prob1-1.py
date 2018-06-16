#-*- coding: utf-8 -*-
import re
import requests
from konlpy.tag import Twitter
from konlpy.utils import pprint
import time
from collections import Counter
import pytagcloud

class Main():
	def __init__(self):
		self.word_list = []
		self.noun_list = []

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

	def get_noun(self):
		print("[*] 명사 추출 시작")
		start_time = time.time()
		twitter = Twitter()
		for s in self.word_list:
			temp = twitter.nouns(s)
			for t in temp:
				self.noun_list.append(str(t))

		end_time = time.time()
		print("[*] 명사 추출 완료(소요시간 : {0})".format(str((end_time-start_time))))
		print("[*] 추출된 명사 길이 : {0}".format(str(len(self.noun_list))))

		# 빈도 분석
		count = Counter(self.noun_list)
		#tag = count.most_common( int(len(count)*(15/100)) )
		tag = count.most_common(50)
		taglist = pytagcloud.make_tags(tag, maxsize=100)
		pytagcloud.create_tag_image(taglist, 'wordcloud.jpg', size=(800, 600), fontname='Nanum Gothic Coding', rectangular=False)

	def toFile(self):
		f = open('word.txt', 'w')
		f.write(str(self.word_list))
		f.close()
		f = open('noun.txt', 'w')
		f.write(str(self.noun_list))

	def run(self):
		self.process_news()
		self.process_comment()
		self.process_comment2()
		self.get_noun()
		self.toFile()

if __name__ == '__main__':
	main = Main()
	main.run()
