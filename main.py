# -*- coding: utf-8 -*-
# 填空题练习软件 - 移动版入口文件
# 基于TEST_V4.0的移动版本

import importlib.util
import sys

# 动态导入包含点号的模块
spec = importlib.util.spec_from_file_location("TEST_V4_0_mobile", "TEST_V4.0_mobile.py")
module = importlib.util.module_from_spec(spec)
sys.modules["TEST_V4_0_mobile"] = module
spec.loader.exec_module(module)

PracticeApp = module.PracticeApp

if __name__ == '__main__':
    PracticeApp().run()