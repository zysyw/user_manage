import sys

if hasattr(sys, 'real_prefix') or (hasattr(sys, 'base_prefix') and sys.base_prefix != sys.prefix):
    print("在虚拟环境中")
    print(f"虚拟环境路径: {sys.prefix}")
else:
    print("不在虚拟环境中")