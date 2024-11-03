import subprocess

# 定义要执行的指令列表
commands1 = [
    "docker pull crpi-wxrbci75b2ofu1me.cn-hangzhou.personal.cr.aliyuncs.com/topten/topten:0.1.3",
]

# 逐行执行指令
for command in commands1:
    print(f"Executing: {command}")
    result = subprocess.run(command, shell=True, text=True, capture_output=True)
    
    # 打印输出和错误信息
    print("Output:")
    print(result.stdout)
    print("Error:")
    print(result.stderr)
    print("=" * 40)
 