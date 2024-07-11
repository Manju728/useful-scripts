import paramiko
import os

current_dir = os.getcwd()
ssh_key_path = os.path.join(current_dir, "ssh_key1.pem")
private_key = paramiko.RSAKey.from_private_key_file(ssh_key_path)
ssh_client = paramiko.SSHClient()
ssh_client.set_missing_host_key_policy(paramiko.AutoAddPolicy())
ssh_client.connect(hostname='hostname', username='username', pkey=private_key, port=22)
stdin, stdout, stderr = ssh_client.exec_command("pwd && ls")
print(stdout.read().decode("utf-8"))
ftp_client = ssh_client.open_sftp()
for file in ftp_client.listdir("test"):
    with ftp_client.open("test/" + file, mode='r') as f:
        data = f.read().decode("utf-8")
        data = data.split("\n")
        print(len(data))
