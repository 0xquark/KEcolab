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
        ssh.close()
        
    return render_template('upload.html')

if __name__ == '__main__':
    app.run(debug=True)