#!/usr/bin/python
############################################################################
#    aws_start_stop.py: Start/Stop AWS instances on the->fly with Boto     #
#    Copyright (C) 2014-2015 by Natale Vinto aka bluesman                  #
#    ebballon@gmail.com                                                    #
#                                                                          #
#    This program is free software; you can redistribute it and#or modify  #
#    it under the terms of the GNU General Public License as published by  #
#    the Free Software Foundation; either version 2 of the License, or     #
#    (at your option) any later version.                                   #
#                                                                          #
#    This program is distributed in the hope that it will be useful,       #
#    but WITHOUT ANY WARRANTY; without even the implied warranty of        #
#    MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the         #
#    GNU General Public License for more details.                          #
#                                                                          #
#    You should have received a copy of the GNU General Public License     #
#    along with this program; if not, write to the                         #
#    Free Software Foundation, Inc.,                                       #
#    59 Temple Place - Suite 330, Boston, MA  02111-1307, USA.             #
############################################################################
#
# v. 0.2 : Email alert optional
# v. 0.1 : Support email alert

import boto.ec2, sys, smtplib, time, getopt
from email.mime.text import MIMEText

def send_aws_mail(action, instances):

  	date = time.strftime("%c")
	subject= "Instance(s) %s %s on %s" % (instances, action, date)
	if (action == ACTION_START):
		text = "Happy to hear from me?"
	elif (action == ACTION_STOP):
		text = "Good night!"
		
	return sendmail(mail_sender, mail_receivers, subject, text)

def sendmail(_from, _to, _subject, _text):
      
        message = MIMEText(_text)
        message['From'] = _from
        message['To'] = _to
        message['Subject'] = _subject

        smtpObj = smtplib.SMTP('localhost')
        smtpObj.sendmail(_from, _to, message.as_string())
        smtpObj.quit()

        return

def usage(err):

	print err
	sys.exit(2)

def help():

	usage( "AWS Start Stop Instances by bluesman " + VERSION + "\n"+
	      "Standard use:\t" + sys.argv[0] + " -O accessKey -W secretKey -r eu-west-1 -i i-caf3b4be,i-deadb33f -a start|stop\n" +
	      "Email Alert:\t" + sys.argv[0] + " -O accessKey -W secretKey -r eu-west-1 -i i-caf3b4be,i-deadb33f -a start|stop -e")

def main():

	if (len(sys.argv) < 2):
		help()

 	region_id = ''
	instance_id = ''
	aws_access_key = ''
	aws_secret_key = ''
	instances_id = []
	action = ''
	alert = False

 	try:
        	options, args = getopt.getopt(sys.argv[1:], "O:W:r:i:a:he", ["help", "alert"
									"aws-access-key=", 
									"aws-secret-key=",
									"region_id=", 
									"instances_id=",
									"action="])
	except getopt.GetoptError as err:
        	usage(str(err))


	for opt, arg in options:
			if opt in ('-O', '--aws-access-key'):
					aws_access_key = arg
			elif opt in ('-W', '--aws-secret-key'):
					aws_secret_key = arg
			elif opt in ('-r', '--region-id'):
					region_id = arg
			elif opt in ('-i', '--instances_id'):
					instance_id = arg
			elif opt in ('-a', '--action'):
					action = arg
			elif opt in ('-e', '--email-alert'):
					alert = True
			elif opt in ('-h', '--help'):
					help()


	instances_id = instance_id.split(",")

	

	if (action != ACTION_START and action != ACTION_STOP):
		help();	
	
	conn = boto.ec2.connect_to_region(region_id, aws_access_key_id=aws_access_key, aws_secret_access_key=aws_secret_key)
	if (conn == None):
		if alert: sendmail(mail_sender, mail_receivers, "Unable to connect to AWS to %s instances %s" % (action, str(instances_id)), "Connection aborted")
		sys.exit(-1)
	
	result = []
	
	if (action == ACTION_START):
		result = conn.start_instances(instances_id)
	elif (action == ACTION_STOP):
		result = conn.stop_instances(instances_id)
	
	
	if (len(result) == len(instances_id)):
		print("Success: %s : %s" % (action, str(result)) )
		if alert: send_aws_mail(action, str(result))
	else:
		if alert: sendmail(mail_sender, mail_receivers, "Error %s instances %s" % (action, str(instances_id)), "Some operation failed, check the instance list: %s" % (str(result)))
		print("Error %s instances %s" % (action, str(instances_id)))
	return


if __name__ == "__main__":

	VERSION = "v. 0.2"
	ACTION_START = "start"
	ACTION_STOP = "stop"
	mail_sender = 'aws-alert@yourserver.com'
	mail_receivers = 'you@yourserver.com'
	
	main()
