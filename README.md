
---

# SSH 低速口令爆破工具使用手册

欢迎使用 SSH 登录工具，这是一个 Python 脚本，旨在帮助用户通过 SSH 协议尝试登录到指定的服务器。本手册将指导您如何安装、配置和使用此工具。

## 1. 环境要求

- Python 3.x
- 安装 `paramiko` 库（用于 SSH 连接）
- 安装 `argparse` 库（用于命令行参数解析）

## 2. 安装指南

### 2.1 安装 Python

确保您的系统中已安装 Python 3。您可以从 [python.org](https://www.python.org/downloads/) 下载并安装。

### 2.2 安装依赖库

打开终端或命令提示符，运行以下命令安装所需的依赖库(根据自己环境选择)：

```bash
pip install paramiko
pip3 install paramiko
```

## 3. 配置工具

### 3.1 准备用户名和密码文件

您需要准备两个文本文件，一个包含用户名列表，另一个包含密码列表。每行一个用户名或密码。

- 默认文件名：`default_usernames.txt` 和 `default_passwords.txt`

### 3.2 配置参数

编辑脚本中的 `DEFAULT_USERNAME_FILE` 和 `DEFAULT_PASSWORD_FILE` 变量，以指向您的用户名和密码字典文件。

## 4. 使用指南

### 4.1 运行脚本

在终端或命令提示符中，导航到脚本所在的目录，然后运行以下命令：

```bash
python LowRateBruteForce.py <IP地址>
```

### 4.2 命令行参数

以下是您可以使用的命令行参数：

- `ip`：指定要连接的 IP 地址。
- `-p` 或 `--port`：指定 SSH 端口，默认为 22。
- `-u` 或 `--user-file`：指定包含用户名字典的文件路径。
- `-d` 或 `--password-file`：指定包含密码字典的文件路径。
- `-m` 或 `--threads`：指定要使用的线程数，默认为 10。
- `-t` 或 `--delay`：指定登录尝试之间的延迟时间，默认为 0.5 秒。
- `-a` 或 `--max-attempts`：指定最大登录尝试次数，默认为 100。
- `-l` 或 `--time-limit`：指定爆破尝试的时间限制，默认为 60 秒。

### 4.3 示例

```bash
python LowRateBruteForce.tpy 192.168.1.1 -p 2222 -u users.txt -d passwords.txt -m 5 -t 5 -a 50 -l 120
```

## 5. 注意事项

- 本工具仅供学习和测试使用，不得用于非法入侵或未经授权的访问。
- 使用前请确保您有合法权限进行 SSH 登录尝试。
- 请根据实际情况调整用户名和密码文件的路径。

## 6. 联系我们

如有任何问题或建议，请通过 [联系我们](https://github.com/GitHub-LP/LowRateBruteForce/issues) 获取支持。

