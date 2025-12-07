# PortScanner

TCP端口扫描工具，支持端口扫描、Banner识别和CDN检测功能。

## 功能特点

- TCP端口开放扫描
- 应用服务Banner识别
- CDN技术检测
- 多线程快速扫描
- 域名和IP地址支持

## 项目结构

```
PortScanner/
├── PortScan.py          # 主程序文件
├── README.md            # 项目说明文档
├── LICENSE              # 许可证文件
├── requirements.txt     # 依赖包列表
└── .gitignore          # Git忽略文件配置

```

## 安装依赖

```bash
pip install -r requirements.txt
```

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



## 许可证

本项目采用 GNU General Public License v3.0 许可证，详见 [LICENSE](LICENSE) 文件。