# 新增绕过CDN的方法
import dns


def bypass_cdn(self):
    """尝试绕过CDN获取真实IP"""
    real_ips = []

    # 方法1: 尝试常见的子域名
    common_subdomains = [
        'www', 'mail', 'ftp', 'smtp', 'pop', 'm', 'blog',
        'dev', 'test', 'admin', 'api', 'cdn', 'img', 'static',
        'news', 'shop', 'forum', 'wiki', 'docs', 'portal'
    ]

    print(u'{}[-] 尝试绕过CDN...{}'.format(self.O, self.W))

    for subdomain in common_subdomains:
        try:
            full_domain = '{}.{}'.format(subdomain, self.url)
            ips = []

            # 使用多个DNS服务器查询
            dnsserver = [['114.114.114.114'], ['8.8.8.8'], ['223.6.6.6']]
            for dns_server in dnsserver:
                try:
                    myResolver = dns.resolver.Resolver()
                    myResolver.lifetime = myResolver.timeout = 2.0
                    myResolver.nameservers = dns_server
                    record = myResolver.resolve(full_domain)
                    for ip in record:
                        ips.append(str(ip.address))
                except:
                    continue

            for ip in ips:
                if ip not in real_ips:
                    real_ips.append(ip)
                    print(u'{}[+] 通过子域名 {} 发现IP: {}{}'.format(self.G, full_domain, ip, self.W))

        except Exception as e:
            continue

    # 方法2: 尝试直接查询NS记录
    try:
        ns_records = dns.resolver.resolve(self.url, 'NS')
        print(u'{}[+] NS记录: {}{}'.format(self.G, ', '.join([str(ns) for ns in ns_records]), self.W))
    except:
        pass

    return real_ips