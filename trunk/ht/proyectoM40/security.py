import bz2
import sys
import getpass

pathXml = 'misc/'
pathSecfile = 'misc/security.txt'

def leerSecurity(path):
    ret = {}
    pwds = open(path, 'r').readlines()
    for pwd in pwds:
        if pwd != '':
            user, pw = pwd.strip().split(':')
            ret[user] = pw
    return ret

def escribirSecurity(path, secs):
    f = open(path, 'w')
    for pwd in secs.keys():
        f.write('%s:%s' %(pwd, secs[pwd]))
        f.write('\n')


def printSecurity(secs):
    for pwd in secs.keys():
        print '%s:%s (%s)' %(pwd, secs[pwd], bz2.decompress(secs[pwd]))

def getUsers(path=pathSecfile):
    return leerSecurity(path).keys()

def getPassword(user, path=pathSecfile):
        return bz2.decompress(leerSecurity(path)[user])

def main():
    secpwds = leerSecurity(pathSecfile)
    printSecurity(secpwds)
    username = raw_input('email: ').strip()
    password = getpass.getpass('password: ').strip()
    secpwds[username] = bz2.compress(password)
    escribirSecurity(pathSecfile, secpwds)

if __name__ == "__main__":
	main()