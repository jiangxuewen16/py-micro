# -*- coding:utf-8 -*-
try:
    from setuptools import setup, find_packages
except:
    from distutils.core import setup
from codecs import open
from os import path

# 版本号
VERSION = '0.0.3'

# 发布作者
AUTHOR = "jiangxuewen"

# 邮箱
AUTHOR_EMAIL = "445251692@qq.com"

# 项目网址
URL = "https://github.com/jiangxuewen16/py-micro"

# 项目名称
NAME = "py-micro"

# 项目简介
DESCRIPTION = "基于grpc的Python微服务"

# LONG_DESCRIPTION为项目详细介绍，这里取README.md作为介绍
here = path.abspath(path.dirname(__file__))
with open(path.join(here, 'README.md'), encoding='utf-8') as f:
    LONG_DESCRIPTION = f.read()

# 搜索关键词
KEYWORDS = "py-micro micro"

# 发布LICENSE
LICENSE = "MIT"

# 包
PACKAGES = ["py_micro"]

# 具体的设置
setup(
    name=NAME,
    version=VERSION,
    description=DESCRIPTION,
    long_description=LONG_DESCRIPTION,
    classifiers=[
        'License :: OSI Approved :: MIT License',
        'Programming Language :: Python',
        'Intended Audience :: Developers',
        'Operating System :: OS Independent',

    ],
    # 指定控制台命令
    entry_points={
        'console_scripts': [
            # 'demo = demo:main',  # pip安装完成后可使用demo命令调用demo下的main方法
        ],
    },
    keywords=KEYWORDS,
    author=AUTHOR,
    author_email=AUTHOR_EMAIL,
    url=URL,
    license=LICENSE,
    packages=PACKAGES,
    install_requires=['grpcio', 'python-consul', 'grpcio-tools'],  # 依赖的第三方包
    include_package_data=True,
    zip_safe=True,
)
