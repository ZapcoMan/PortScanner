# PortScanner

TCP端口扫描工具，支持端口扫描、Banner识别和CDN检测功能。

## 功能特点

- TCP端口开放扫描
- 应用服务Banner识别
- CDN技术检测
- 多线程快速扫描
- 域名和IP地址支持

## 使用方法

```bash
python PortScan.py -u <目标地址> -p <端口范围> [-T 线程数]
```

参数说明：
- `-u, --url`: 目标IP地址或域名
- `-p, --port`: 端口范围，可以是单个端口(如: 80)或端口范围(如: 21-8080)
- `-T, --threads`: 线程数，默认为100
- `-v, --version`: 显示程序版本
- `-h, --help`: 显示帮助信息

示例：
```bash
python PortScan.py -u 192.168.1.1 -p 1-1000
python PortScan.py -u example.com -p 21-8080
python PortScan.py -u google.com -p 80
python PortScan.py -u 192.168.1.1 -p 1-65535 -T 200
```

## 工作原理

1. **端口扫描**: 使用TCP连接扫描目标主机指定范围内的端口
2. **Banner识别**: 
   - 首先尝试通过HTTP协议获取Banner信息
   - 如果失败，则尝试通过HTTPS协议获取
   - 最后使用原生Socket发送探测包获取Banner
3. **CDN检测**: 通过多DNS服务器解析目标域名，如果返回多个不同IP地址则判定使用了CDN技术

## 依赖库

- requests
- beautifulsoup4
- lxml
- dnspython
- fake-useragent

安装依赖：
```bash
pip install requests beautifulsoup4 lxml dnspython fake-useragent
```