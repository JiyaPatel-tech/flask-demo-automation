import os
import paramiko

host = os.environ["EC2_HOST"]
username = os.environ["EC2_USER"]
private_key = os.environ["EC2_KEY"]

key = paramiko.RSAKey.from_private_key_file(private_key)

ssh = paramiko.SSHClient()
ssh.set_missing_host_key_policy(paramiko.AutoAddPolicy())

ssh.connect(
    hostname=host,
    username=username,
    pkey=key
)

commands = [
    "cd flask-demo",
    "git pull origin main",
    "pip3 install -r requirements.txt",
    "pkill -f app.py || true",
    "nohup python3 app.py > output.log 2>&1 &"
]

command = " && ".join(commands)

stdin, stdout, stderr = ssh.exec_command(command)

print(stdout.read().decode())
print(stderr.read().decode())

ssh.close()
