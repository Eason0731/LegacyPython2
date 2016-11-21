from ci_database.ci_database import find_or_create_build
from fusion_ci_config import FusionCIConfig
import getopt, sys, os
import requests
import json

FUSION_CI_CONFIG = FusionCIConfig()
FUSION_CI_CONFIG.display_config()

CIWebHost = FUSION_CI_CONFIG.fusionciweb_config.hosturl

def getEmailUrl(build_id):
    url = '{0}/api/v1/build/{1}/send_mail/'.format(CIWebHost, build_id)
    return url

def sendEmail(url, emailist=None, jenkins=None):
    body = {
            "emails": [] if emailist is None else emailist,
            "jenkins": "" if jenkins is None else jenkins
            }
    
    headers={'Content-Type': 'application/json'}
    print("===========")
    print(url)
    print(body)
    resp = requests.post(url, data = body)
   
    print(resp.text)
    print(resp.status_code)
    print("End send email")
    
def Usage():
    print('sendEmail.py usage:')
    print('-h, --help: print help message.')
    print('-n, --jobname: the name of jenkins job.')
    print('-b, --buildnumber: the build number of this jenkins job.')
    print('-e, --emaillist: the email list which will be sent, use semicolon to separate emails')

if __name__ == "__main__":
    try:
        opts, args = getopt.getopt(sys.argv[1:], 'hn:b:e:', ['help', 'jobname=', 'buildnumber=', 'emaillist='])
    except getopt.GetoptError as err:
        print(str(err))
        Usage()
        sys.exit(2)
    
    pyFile = os.path.abspath(sys.argv[0])
    workspace = os.path.split(pyFile)[0]
    jobname = ''
    buildnumber = ''
    emails = ''
    for o, a in opts:
        if o in ('-h', '--help'):
            Usage()
            sys.exit(1)
        elif o in ('-n', '--jobname',):
            jobname = a
        elif o in ('-b', '--buildnumber',):
            buildnumber = a
        elif o in ('-e', '--emaillist',):
            emails = a
        else:
            print('unhandled option')
            sys.exit(2)

    if jobname == '' or buildnumber == '':
        print('Lack of parameters')
        Usage()
        sys.exit(2)
    
    try:
        build_number = int(buildnumber)
        build_id = find_or_create_build(jobname, build_number)
        emailurl = getEmailUrl(build_id)
        emaillist = None if emails == '' else emails.split(';')
        sendEmail(emailurl, emaillist)
    except Exception as e:
        print("Failed to send out report email! ")
        print(e)
    
