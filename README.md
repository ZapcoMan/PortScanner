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
python PortScan.py <目标地址> <起始端口> <结束端口>
```

示例：
```bash
python PortScan.py 192.168.1.1 1 1000
python PortScan.py example.com 21 8080
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