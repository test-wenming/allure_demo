#!/usr/bin/env python3
# -*- coding:utf-8 -*-
import sys
import subprocess
import pytest


# 获取当前系统平台,startswith以什么开头

WIN = sys.platform.startswith('win')


def main():
    """主函数"""
    steps = [
       "venv\\Script\\activate" if WIN else "source venv/bin/activate",
       "pytest --alluredir allure-results --clean-alluredir",
       "allure generate allure-results -c -o allure-report",
       "allure open allure-report"
   ]
    for step in steps:
        subprocess.run("call " + step if WIN else step, shell=True)


# 要生成allure报告，执行这个
if __name__ == "__main__":
    main()

    # 调试时用这个
    # pytest.main()

