import sys
import socket
import logging
import requests
import dns.resolver
import urllib3
import argparse
from time import time
from bs4 import BeautifulSoup
from fake_useragent import UserAgent
# 线程池
from multiprocessing.dummy import Pool as ThreadPool
from multiprocessing.dummy import Lock

# 导入CDN绕过功能
from .bypass_cdn import bypass_cdn

urllib3.disable_warnings(urllib3.exceptions.InsecureRequestWarning)

class Scanner(object):
	def __init__(self, url, start, end, threads=100):
		self.url = url
		self.start  = start
		self.end    = end
		self.threads = threads
		self.W 	 	= '\033[0m'
		self.G  	= '\033[1;32m'
		self.O  	= '\033[1;33m'
		self.R  	= '\033[1;31m'
		self.time   = time()
		self.ports  = []
		self.result = []
		self.mutex  = Lock()
		self.get_ports()

	# 绑定CDN绕过方法
	bypass_cdn = bypass_cdn

	def get_ports(self):
		for i in range(int(self.start), int(self.end)+1):
			self.ports.append(i)

	def check_cdn(self):
		# 目标域名cdn检测
		myResolver = dns.resolver.Resolver()
		myResolver.lifetime = myResolver.timeout = 2.0
		dnsserver = [['114.114.114.114'],['8.8.8.8'],['223.6.6.6']]
		try:
			for i in dnsserver:
				myResolver.nameservers = i
				record = myResolver.resolve(self.url)
				self.result.append(record[0].address)
		except Exception as e:
			pass
		finally:
			return True if len(set(list(self.result))) > 1 else False

	def resolve_host(self, hostname):
		"""使用指定的DNS服务器解析主机名"""
		dnsserver = ['114.114.114.114', '8.8.8.8', '223.6.6.6']
		try:
			# 尝试使用指定的DNS服务器解析
			for dns_ip in dnsserver:
				myResolver = dns.resolver.Resolver()
				myResolver.lifetime = myResolver.timeout = 2.0
				myResolver.nameservers = [dns_ip]
				try:
					record = myResolver.resolve(hostname)
					return str(record[0].address)
				except:
					continue
			# 如果指定的DNS服务器都无法解析，则回退到系统默认
			return socket.gethostbyname(hostname)
		except:
			return hostname  # 如果解析失败，直接返回原hostname

	def scan_port(self, port):
		# 端口扫描
		try:
			s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
			s.settimeout(0.2)
			return True if s.connect_ex((self.url, port)) == 0 else False
		except Exception as e:
			pass
		finally:
			s.close()

	def get_http_banner(self, url):
		# http/https请求获取banner
		try:
			r = requests.get(url, headers={'UserAgent':UserAgent().random},
				timeout=2, verify=False, allow_redirects=True)
			soup = BeautifulSoup(r.content,'lxml')
			return soup.title.text.strip('\n').strip()
		except Exception as e:
			pass

	def get_socket_info(self, port):
		# socket获取banner
		try:
			s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
			s.settimeout(0.2)
			s.connect((self.url, port))
			s.send('HELLO\r\n')
			return s.recv(1024).split('\r\n')[0].strip('\r\n')
		except Exception as e:
			pass
		finally:
			s.close()

	def run(self, port):
		try:
			if self.scan_port(port):
				banner = self.get_http_banner('http://{}:{}'.format(self.url, port))
				self.mutex.acquire()
				if banner:
					print('{}[+] {} ---- open   {}{}'.format(self.G,
						str(port).rjust(6), banner[:18], self.W))
				else:
					banner = self.get_http_banner('https://{}:{}'.format(
						self.url, port))
					if banner:
						print('{}[+] {} ---- open   {}{}'.format(self.G,
							str(port).rjust(6), banner[:18], self.W))
					else:
						banner = self.get_socket_info(port)
						if banner:
							print('{}[+] {} ---- open   {}{}'.format(
								self.G, str(port).rjust(6), banner[:18], self.W))
						else:
							print('{}[+] {} ---- open   {}'.format(
								self.G, str(port).rjust(6), self.W))
				self.mutex.release()
		except Exception as e:
			pass

	def _start(self):
		try:
			print('-'*60)
			print(u'{}[-] 当前出网地址: {}{} '.format(self.O,
				self.resolve_host(self.url), self.W))
			print('-'*60)
			# 线程数
			pool = ThreadPool(processes=self.threads)
			# get传递超时时间，用于捕捉ctrl+c
			pool.map_async(self.run, self.ports).get(0xffff)
			pool.close()
			pool.join()
			print('-'*60)
			print(u'{}[-] 扫描完成耗时: {} 秒.{}'.format(self.O,
				time()-self.time, self.W))
		except KeyboardInterrupt:
			# 修改键盘中断处理逻辑，确保程序可以快速结束
			pool.terminate()
			pool.join()
			print(self.R + u'\n[-] 用户终止扫描...')
			sys.exit(1)

	def check_target(self):
		# 判断目标是域名还是还是ip地址
		flag = self.url.split('.')[-1]
		try:
			# ip地址
			if int(flag) >= 0:
				self._start()
		except:
			# 域名地址
			if not self.check_cdn():
				self._start()
			else:
				print('-'*60)
				print(u'{}[-] 目标使用了CDN技术,尝试绕过...{}'.format(self.R, self.W))
				print('-'*60)
				# 尝试绕过CDN
				real_ips = self.bypass_cdn()
				if real_ips:
					print(u'{}[-] 发现 {} 个可能的真实IP，开始扫描...{}'.format(self.G, len(real_ips), self.W))
					# 对发现的真实IP进行扫描
					for ip in real_ips:
						print(u'{}[-] 扫描IP: {}{}'.format(self.O, ip, self.W))
						old_url = self.url
						self.url = ip  # 临时替换为目标IP
						self._start()
						self.url = old_url  # 恢复原始URL
				else:
					print(u'{}[-] 未能绕过CDN，停止扫描.{}'.format(self.R, self.W))