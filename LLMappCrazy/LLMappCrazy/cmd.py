import pandas as pd
import subprocess

def extract_app_names(file_path):
    try:
        # 尝试使用utf-8编码读取CSV文件，如果失败则使用latin1编码
        try:
            df = pd.read_csv(file_path, encoding='utf-8')
        except UnicodeDecodeError:
            df = pd.read_csv(file_path, encoding='gbk')
        # 提取第二列的应用名称
        app_names = df.iloc[:, 1].tolist()  # 假设第二列为应用名称列
        return app_names
    except Exception as e:
        print(f"读取文件时出错: {e}")
        return []

# 设置文件路径
file_path = 'top_1000_gpts.csv'

# 调用函数并打印应用名称列表
app_names = extract_app_names(file_path)
# print(app_names)

counter = 1
with open("cmd.txt", "w", encoding="gbk") as file:
    for name in app_names:
        command = f'python llmappcrazy.py --appname "{name}" --file "output_add_4/{counter}.csv"'
        file.write(command + "\n")
        counter += 1
        if counter == 11:
            break

def execute_commands_from_file(file_path):
    # 打开文件并逐行读取命令
    with open(file_path, 'r', encoding='gbk') as file:
        i = 1
        for line in file:
            command = line.strip()  # 去除首尾空白字符
            if command:  # 确保命令不为空
                try:
                    # 执行命令并等待完成
                    result = subprocess.run(command, shell=True, check=True, text=True, capture_output=True)
                    print(f"执行成功: {i}\n")
                    i += 1
                except subprocess.CalledProcessError as e:
                    print(f"执行失败: {command}\n")

# 使用函数执行命令
file_path = 'cmd.txt'  # 你的 txt 文件路径
execute_commands_from_file(file_path)