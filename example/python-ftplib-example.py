from ftplib import FTP
import time
import tarfile

from ftplib import FTP

def ftpconnect(host, username, password)
    ftp = FTP()
    ftp.connect(host, 21)
    ftp.login(username, password)
    return ftp

def downloadfile(ftp, remotepath, localpath):
    bufsize = 1024
    fp = open(localpath, 'wb')
    ftp.retrbinary('RETR'+remotepath, fp.write, bufsize)

    ftp.set_debuglevel(0)
    fp.close()

def uploadfile(ftp, remotepath, localpath):
    bufsize = 1024
    fp = open(localpath, 'rb')
    ftp.storbinary('STOR'+remotepath, fp, bufsize)
    ftp.set_debuglevel(0)
    fp.close()

if __name__ == '__main__':
    ftp = ftpconnect("******", "***", "***")
    downloadfile(ftp, "***", "***")
    uploadfile(ftp, "***", "***")

    ftp.quit()