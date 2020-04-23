#!/usr/bin/python 
# -*- coding: utf-8 -*-
'''
@Author: Fei Pei
@Date: 2020-04-14 16:54:13
@LastEditTime: 2020-04-23 18:05:22
@LastEditors: Fei Pei
'''

import os
import sys
import platform


def is_windows():
    uname = platform.uname()
    return uname[0].lower() == 'windows'


def get_env(name):
    """查看环境变量"""
    return os.environ.get(name, '')


def set_env(name, new_value):
    """设置环境变量"""
    os.environ[name] = new_value


def get_relative_folder(base_path, relative_path):
    """根据 base 目录，以及目标目录相对该目录的相对路径，得到目标目录的绝对路径。"""
    fullname = os.path.abspath(base_path)

    if os.path.isdir(fullname):
        folder = fullname
    else:
        folder, _filename = os.path.split(fullname)

    abs_folder = os.path.abspath(os.path.join(folder, relative_path))

    return abs_folder


def insert_python_source_folder(newt_src_folder):
    """增加新的 python source folder."""
    sys.path.insert(0, newt_src_folder)


def get_folder(fullname):
    """返回路径所对应的目录（去除文件名）。"""
    if os.path.isdir(fullname):
        folder = fullname
    else:
        folder, _filename = os.path.split(fullname)

    return os.path.abspath(folder)

def get_pids(g_info):
    """以列表形式返回符合grep 要求的所有pid"""
    pids = os.popen(
        "ps aux|grep %s |grep -v 'grep'|awk -F ' ' '{print $2}'" % g_info).read().split('\n')
        
    return pids
