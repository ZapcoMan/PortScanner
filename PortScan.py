#!/usr/bin/python3
#coding:utf-8
#Author:se55i0n
#目标tcp端口开放扫描及应用端口banner识别

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

from src.portScanner.Scanner import Scanner
# 导入banner
from src.portScanner.banner import print_banner,version

urllib3.disable_warnings(urllib3.exceptions.InsecureRequestWarning)

logger = logging.getLogger(__name__)

def parse_args():
	parser = argparse.ArgumentParser(description='TCP端口扫描工具')
	parser.add_argument('-u', '--url', required=True, help='目标IP地址或域名')
	parser.add_argument('-p', '--port', required=True, help='端口范围 (例如: 21-8080 或 80)')
	parser.add_argument('-T', '--threads', type=int, default=100, help='线程数 (默认: 100)')
	parser.add_argument('-v', '--version', action='version', version=f'Version: {version}', help='显示版本信息并退出')
	return parser.parse_args()

def parse_port_range(port_str):
	"""解析端口范围字符串"""
	if '-' in port_str:
		start, end = port_str.split('-', 1)
		return int(start), int(end)
	else:
		port = int(port_str)
		return port, port

if __name__ == '__main__':
	print_banner()
	
	# // 删除旧的使用方式，只保留命令行参数解析
	try:
		# // 解析命令行参数
		args = parse_args()
		
		# // 解析端口范围
		start_port, end_port = parse_port_range(args.port)
		
		# // 创建扫描器实例
		myscan = Scanner(args.url, start_port, end_port, args.threads)
		myscan.check_target()
	except KeyboardInterrupt:
		print("\nExit...")
		sys.exit(0)
	except Exception as e:
		print("Error:", str(e))
		sys.exit(1)