import sys
import os

# 获取当前文件的目录
current_dir = os.path.dirname(os.path.abspath(__file__))

# 将 fun 文件夹添加到 sys.path
sys.path.append(current_dir)
