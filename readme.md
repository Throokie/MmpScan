# 介绍'

如果你有很多电脑。如果你不想让他们浪费。如果你刚好看某个网站不顺眼，但眼下没空对他进行信息收集和攻击。

那么，该工具能够很好的帮助你。他能帮你对目标进行信息收集，并且自动攻击。再将结果梳理给你。

这款工具的亮点就是，能够利用其他工具的优点。调用他们，为这款工具所用。

我认为没有最好的工具，如果在同类工具之间互补。那才能发挥出整体最大威力。但缺点也显而易见，简单的调用势必会有很多重复的IO请求。是的，所以该脚本推荐挂机时用，挖点漏洞碰下运气什么的。

TODO
  1、添加更多调用工具
  2、添加web端


# 设计思路
主程序MmpScan.py下生成两个进程，分别是
1. Scan
2. Crack

Scan负责信息收集（子域名、ip、C段）等信息
Crack负责爆破和攻击（目录，rdp，xray）等工具

调用脚本：指的是集成进来的工具

目前Scan模块集成了Oneforall,subfinger,subdomainbrute调用脚本
Crack模块暂未集成

如果需要添加自己的调用脚本，请将脚本以class格式写进Mmp_Scripy.py里，并且MmpScan主程序调用这个类。当然Config.py也需要进行相关配置

# 以后具体功能

1. 加入dirsearch
2. 加入Xray
3. 加入C段扫描
4. 加入rdp、ssh等可登陆端口爆破

# 使用方法

创建python venv虚拟环境(可选)

```python
'''
    virtualenv venv  创建虚拟环境，名字为venv
    .\venv\Scripts\activate.bat  进入虚拟环境（windows环境）
    .\Scripts\deactivate.bat 退出虚拟环境
'''
```

1、 安装依赖

```python
'''
pip install -r requirements.txt
'''
```

2、 运行脚本

- `python MmpScan.py --target www.target.com`

  输入单个url

- `python MmpScan.py --file targets.txt`

  输入文件，读取多个主域名不同的url。

- `python MmpScan.py --venv  True`

  为调用脚本自动生成venv环境并且安装相关依赖。（还未完全测试，不推荐使用）