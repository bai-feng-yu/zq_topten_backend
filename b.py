import subprocess

# 定义要执行的指令列表
commands1 = [
    "docker compose down",
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
 
commands2 = [
    "docker rmi zq_topten_backend",
    "docker build -t zq_topten_backend .",
]
work_dir = "zq_topten_backend"
# 逐行执行指令
for command in commands2:
    print(f"Executing: {command}")
    result = subprocess.run(command, shell=True, text=True, capture_output=True,cwd=work_dir)
    
    # 打印输出和错误信息
    print("Output:")
    print(result.stdout)
    print("Error:")
    print(result.stderr)
    print("=" * 40)

commands3= [
    "docker compose up -d"
]

# 逐行执行指令
for command in commands3:
    print(f"Executing: {command}")
    result = subprocess.run(command, shell=True, text=True, capture_output=True)
    
    # 打印输出和错误信息
    print("Output:")
    print(result.stdout)
    print("Error:")
    print(result.stderr)
    print("=" * 40)