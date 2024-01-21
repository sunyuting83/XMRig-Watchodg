# XMRig Watchdog
---
### 说明
一个使用python + pyqt5开发的xmrig可视化监工程序,配置简单 自动启动并检测xmrig运行情况

### 更新日志
##### 2024/1/21
- 添加更新检测

### 自行构建
clone本项目到本机
下载python-3.12.0-embed-amd64.zip并解压 修改目录名为libs 拷贝至程序目录

修改libs目录中的python312._pth文件 去掉 import site 前面的 #
```python
python312.zip
.

# Uncomment to run site.main() automatically
import site
```

下载get-pip.py到libs目录中

打开cmd窗口并cd到libs目录下 运行
```bash
python get-pip.py
# 等待pip安装完成 速度可能很慢 需要魔法
# 设置国内源
python -m pip config set global.index-url https://pypi.tuna.tsinghua.edu.cn/simple

#安装virtualenv
python -m pip install virtualenv
```

双击install.bat

将public.py文件中的DEV变量值改成True
```python
DEV = True
```
##### 测试
打开cmd窗口并cd到程序目录 运行
```bash
# 先运行虚拟环境
.libs\scripts\activate
# 安装依赖
pip install -r requirements.txt
# 运行并测试
python main.py
```
##### 打包
```bash
pyinstaller --noconfirm --windowed --icon "icon/icon.ico" --name "XMRigWatchdog" --upx-dir "你的upx路径"  --add-data "icon;."  "main.py"
```
如果不使用upx就把 --upx-dir "你的upx路径" 从命令中去掉

打包好的程序在dist目录中

### 捐赠
zeph
```
ZEPHs9Fkw8PAB1n2qx5m8FLXrYpZqWh7Na9W5uoSbTNtVuHiHc8fPBhgSsByWJti6RNGf8zfbAHc1d3AawnfWyMCaV16LomPqRq
```

xmr
```
88zqFaxMu9W4zaX6pxs2THV8XCnoE2a2Hgd1gSo4rP5kRfoBwXpHAVGAexEa1vcDexAZ1nsB4wK3BeqajJKnsnheUkq4oqb
```