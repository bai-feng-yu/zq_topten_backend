import subprocess

# 定义命令列表
commands = [
    "docker compose exec django /bin/sh -c 'cp db.sqlite3 /tmp/'",  # 进入容器并复制数据库
    "docker compose cp django:/tmp/db.sqlite3 .",  # 从容器中将文件复制到宿主机
]

# 执行每个命令并检查是否成功
for command in commands:
    print(f"Executing: {command}")
    result = subprocess.run(command, shell=True, text=True, capture_output=True)
    
    # 打印输出和错误信息
    if result.returncode == 0:
        print("Command executed successfully.")
        print("Output:")
        print(result.stdout)
    else:
        print("Command failed.")
        print("Error:")
        print(result.stderr)
    
    print("=" * 40)
