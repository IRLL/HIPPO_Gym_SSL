# HIPPO Gym SSL Certificate Getter
##### Human Input Parsing Platform for Openai Gym
[hippogym.irll.net](http://hippogym.irll.net)

Written by [Nick Nissen](https://nicknissen.com), Payas Singh, Nadeen Mohammed, and Yuan Wang
Supervided by [Matt Taylor](https://drmatttaylor.net) and Neda Navi
For the Intelligent Robot Learning Laboratory [(IRLL)](https://irll.ca) at the University of Alberta [(UofA)](https://ualberta.ca)
Supported by the Alberta Machine Intelligence Institute

For questions or support contact us at [hippogym.irll@gmail.com](mailto:hippogym.irll@gmail.com)

The HIPPO Gym Project contains 4 repositories:

1. The main framework: [HIPPO_Gym](https://github.com/IRLL/HIPPO_Gym)

2. The AWS code and instructions: [HIPPO_Gym_AWS](https://github.com/IRLL/HIPPO_Gym_AWS)

3. The React Front End: [HIPPO_Gym_React_FrontEnd](https://github.com/IRLL/HIPPO_Gym_React_FrontEnd)

4. The SSL Certificate Getter: [HIPPO_Gym_SSL](https://github.com/IRLL/HIPPO_Gym_SSL)

For members of the IRL Lab, or anyone whose organization has already setup the AWS infrastructure, the only repo required is #1.

Anyone is welcome to use the front-end deployed to [irll.net](https://irll.net)


## Purpose:
This script will get new SSL certificates from Let's Encrypt by running certbot and updating the route53 dns entries as required to verify domain ownership.

Once obtained, the updated certificates will be uploaded to S3 for seamless use by researchers.

## Dependencies

certbot must be installed on the machine

boto3 (pip install boto3)
dotenv (pip install dotenv)
pexpect (pip install pexpect)

## AWS credentials

AWS credentials must be placed in a file called .env
a template file called template.env is provided. The variables can be filled in and the file renamed.

## Crontab entry

22 22 22 * * cd PATH_TO/HIPPO_Gym_SSL/ && python3 get_ssl_certs.py >/dev/null 2>&1

This entry will run at 22min 22hrs 22nd day of every month. Note that you must cd to the containing directory because the script does filesystem operations within it's own directory.

Certificates are valid for 90 days, by replacing them monthly it guarantees that a deployed research project will have 60 days of validity before needing to be redeployed.

Since this script interacts with external services, namely AWS, failures are possible, for instance should internet access not be available when the crontab entry is run, then the certificates will not be updated. It is a good practice to check S3 on occaision to ensure up to date certificates.
