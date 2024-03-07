import requests
import json

# 下载直链地址中的内容
response = requests.get('https://m3u.ibert.me/txt/fmml_ipv6.txt')
lines = response.text.splitlines()



# 读取原始配置
with open('config.json', 'r', encoding='utf-8') as f:
    config = json.load(f)

for group in config['lives']:
    if group['group'] == 'IPTV':
        custom_group = group
        break
else:  # 如果没有找到 "自定义" 组，创建一个新的
    custom_group = {'group': 'IPTV', 'channels': []}
    config['lives'].append(custom_group)

# 清空 "自定义" 组的频道
custom_group['channels'] = []

# 添加新的频道到 "自定义" 组
for line in lines[1:]:  # 从第二行开始
    if line.startswith('#') or not line.strip():
        continue
    name, url = line.split(',', 1)  # 只分割第一个逗号
    # 添加新的频道
    custom_group['channels'].append({
        'name': name.strip(),
        'urls': [url.strip()]
    })

# 将更新的配置写回文件
with open('config.json', 'w', encoding='utf-8') as f:
    json.dump(config, f, indent=2, ensure_ascii=False)
