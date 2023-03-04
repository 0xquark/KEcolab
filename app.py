from flask import Flask, request, render_template
import paramiko
import os
from celery import Celery

app = Flask(__name__)

# configure Celery
app.config['CELERY_BROKER_URL'] = 'redis://localhost:6379/0'
app.config['CELERY_RESULT_BACKEND'] = 'redis://localhost:6379/0'
celery = Celery(app.name, broker=app.config['CELERY_BROKER_URL'])
celery.conf.update(app.config)

@celery.task
def execute_script(script):
    # execute script using SSH
    ssh = paramiko.SSHClient()
    ssh.set_missing_host_key_policy(paramiko.AutoAddPolicy())
    ssh.connect('172.16.191.132', username='alethe', key_filename='EcoLab')
    stdin, stdout, stderr = ssh.exec_command(f'bash {script}')
    stdout_lines = stdout.readlines()
    stderr_lines = stderr.readlines()
    print(f'STDOUT: {"".join(stdout_lines)}')
    print(f'STDERR: {"".join(stderr_lines)}')
    ssh.close()

@app.route('/', methods=['GET', 'POST'])
def upload_files():
    if request.method == 'POST':
        file1 = request.files['file1']
        file2 = request.files['file2']
        file3 = request.files['file3']

        app_name = request.form['app_name']
        app_version = request.form['app_version']
        
        # tunnel files to remote server
        ssh = paramiko.SSHClient()
        ssh.set_missing_host_key_policy(paramiko.AutoAddPolicy())
        ssh.connect('172.16.191.132', username='alethe', key_filename='EcoLab')
        sftp = ssh.open_sftp()
        path1 = os.path.join('', file1.filename)
        path2 = os.path.join('', file2.filename)
        path3 = os.path.join('', file3.filename)
        file1.save('/tmp/' + file1.filename)
        file2.save('/tmp/' + file2.filename)
        file3.save('/tmp/' + file3.filename)
        sftp.put('/tmp/' + file1.filename, path1)
        sftp.put('/tmp/' + file2.filename, path2)
        sftp.put('/tmp/' + file3.filename, path3)
        sftp.close()
        
        # install application using flatpak
        stdin, stdout, stderr = ssh.exec_command(f"sudo flatpak install -y flathub {app_name}/{app_version}")
        output = stdout.read().decode('utf-8')
        error = stderr.read().decode('utf-8')

        # execute scripts asynchronously
        scripts = [path1, path2, path3]
        for script in scripts:
            execute_script.delay(script)

        ssh.close()
        
    return render_template('upload.html')

if __name__ == '__main__':
    app.run(debug=True)
