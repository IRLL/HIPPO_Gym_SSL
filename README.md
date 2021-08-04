# HIPPO Gym SSL Certificate Getter

This script will get new SSL certificates from Let's Encrypt by running certbot and updating the route53 dns entries as required to verify domain ownership.

## Dependencies

certbot must be installed on the machine

boto3 (pip install boto3)
dotenv (pip install dotenv)
pexpect (pip install pexpect)

## AWS credentials

AWS credentials must be placed in a file called .env
a template file called template.env is provided. The variables can be filled in and the file renamed.
