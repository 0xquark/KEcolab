from flask import Flask, request, render_template
import paramiko
import os

app = Flask(__name__)

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
        ssh.connect('3.108.54.0', username='kali', key_filename='Delorean.pem')
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
        stdin, stdout, stderr = ssh.exec_command(f"flatpak install -y flathub {app_name}/{app_version}")
        output = stdout.read().decode('utf-8')
        error = stderr.read().decode('utf-8')

        # execute scripts one by one
        scripts = [path1, path2, path3]
        for script in scripts:
            stdin, stdout, stderr = ssh.exec_command(f'bash {script}')
            stdout_lines = stdout.readlines()
            stderr_lines = stderr.readlines()
            print(f'STDOUT: {"".join(stdout_lines)}')
            print(f'STDERR: {"".join(stderr_lines)}')

        ssh.close()
        
    return render_template('upload.html')

if __name__ == '__main__':
    app.run(debug=True)
