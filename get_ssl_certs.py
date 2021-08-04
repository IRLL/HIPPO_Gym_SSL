import pexpect
from os import mkdir, getenv
from shutil import rmtree
import boto3
from dotenv import load_dotenv

load_dotenv()

def get_session():
    session = boto3.Session(
            aws_access_key_id= getenv('AWS_ACCESS_KEY_ID'),
            aws_secret_access_key= getenv('AWS_SECRET_ACCESS_KEY')
            )

    return session
            

def set_dns(session, record1, record2):
    client = session.client('route53')
    response = client.change_resource_record_sets(
        HostedZoneId=getenv('HOSTED_ZONE_ID'),
        ChangeBatch={
            'Changes': [
                {
                    'Action': 'UPSERT',
                    'ResourceRecordSet': {
                        'Name': '_acme-challenge.irll.net',
                        'Type': 'TXT',
                        'TTL': 10,
                        'ResourceRecords': [
                            {
                                'Value': f'"{record1}" "{record2}"'
                            }
                        ]
                    },
                }
            ]
        }
    )

def upload(session):
    client = session.client('s3')
    response = client.upload_file('fullchain.pem', getenv('BUCKET'), 'SSL/fullchain.pem')
    response = client.upload_file('privkey.pem', getenv('BUCKET'), 'SSL/privkey.pem')

def main():
    session = get_session()
    try:
        rmtree('Cert')
        print('Cert Removed')
    except:
        pass
    try:
        mkdir('Cert')
        print('Cert created')
    except:
        pass
    ssl = pexpect.spawn('certbot certonly --preferred-challenges dns --manual --domain "irll.net" --domain "*.irll.net" --work-dir Cert/ --logs-dir Cert/ --config-dir Cert/ --fullchain-path ./ --key-path ./', encoding='utf-8')

#'''
#Enter email address (used for urgent renewal and security notices) (Enter 'c' to cancel):
#'''
    ssl.expect("(Enter 'c' to cancel):*")
    ssl.sendline(getenv('EMAIL'))
    print('email')

#    '''
#    Please read the Terms of Service at
#    https://letsencrypt.org/documents/LE-SA-v1.2-November-15-2017.pdf. You must
#    agree in order to register with the ACME server. Do you agree?
#    - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - -
#    (Y)es/(N)o:.sendline('y')
#
#    '''
    ssl.expect('- - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - -*')
    ssl.sendline('y')
    print('yes')
    
#    '''
#    Would you be willing, once your first certificate is successfully issued, to
#    share your email address with the Electronic Frontier Foundation, a founding
#    partner of the Let's Encrypt project and the non-profit organization that
#    develops Certbot? We'd like to send you email about our work encrypting the web,
#    EFF news, campaigns, and ways to support digital freedom.
#    - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - -
#    (Y)es/(N)o:
#    '''
    ssl.expect('- - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - -*')
    ssl.sendline('n')
    print('no')

#    '''
#    Account registered.
#    Requesting a certificate for irll.net and *.irll.net
#    Performing the following challenges:
#    dns-01 challenge for irll.net
#    dns-01 challenge for irll.net
#    
#    - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - -
#    Please deploy a DNS TXT record under the name:
#    
#            _acme-challenge.irll.net.
#    
#            with the following value:
#    '''
    ssl.expect('with the following value:*')
    print(ssl.readline())
    print(ssl.readline())
    record1 = ssl.readline().strip()
    print("first record", record1)
    ssl.sendline()

#    '''
#    Please deploy a DNS TXT record under the name:
#
#    _acme-challenge.irll.net.
#
#    with the following value:
#    '''
    ssl.expect('with the following value:*')
    print(ssl.readline())
    print(ssl.readline())
    record2 = ssl.readline().strip()
    print("second record", record2)

    # do boto3 stuff
    set_dns(session, record1, record2)
    # wait
    time.sleep(30)
    ssl.sendline()
    time.sleep(10)

    if 'fullchain.pem' in os.listdir('.'):
        upload(session)

    rmtree('Cert')



if __name__ == '__main__':
    main()


