#!/bin/bash

# 确保tests目录存在
mkdir -p tests

# 运行所有测试
python3 -m unittest discover -s tests -p "test_*.py" -v 