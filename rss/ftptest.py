# Import the FTP object from ftplib
from ftplib import FTP
print 'hola'

# This will handle the data being downloaded
# It will be explained shortly
def handleDownload(block):
    file.write(block)
    print ".",
ftp = FTP('ftp.cdrom.com')

print 'Welcome to Matt\'s ftplib example'
# Log in to the server
print 'Logging in.'
# You can specify username and password here if you like:
# ftp.login('username', 'password')
# Otherwise, it defaults to Anonymous
print ftp.login()

# This is the directory that we want to go to
directory = 'pub/simtelnet/trumpet/winsock'
# Let's change to that directory.  You kids might call these 'folders'
print 'Changing to ' + directory
ftp.cwd(directory)

# Print the contents of the directory
ftp.retrlines('LIST')

# Here's a file for us to play with.  Remember Trumpet Winsock?
filename = 'twsk30d.exe'

# Open the file for writing in binary mode
print 'Opening local file ' + filename
file = open(filename, 'wb')

# Download the file a chunk at a time
# Each chunk is sent to handleDownload
# We append the chunk to the file and then print a '.' for progress
# RETR is an FTP command
print 'Getting ' + filename
ftp.retrbinary('RETR ' + filename, handleDownload)

# Clean up time
print 'Closing file ' + filename
file.close()

print 'Closing FTP connection'
print ftp.close()