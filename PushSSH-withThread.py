# Import Library
import paramiko
import sys, os, string, threading
from getpass import getpass

try:
	# Import list IP Address
	input_file = "ip.txt"
	ip_list = open(input_file, "r").readlines()

	input_config = "config.txt"

	r_input_config = open(input_config, "r").readlines()

	#Get username & password from user
	username = raw_input("Username: ")
	password = getpass()
	port = 22

	outlock = threading.Lock()

	def workon(host):
		try:
			ssh = paramiko.SSHClient()
			ssh.set_missing_host_key_policy(paramiko.AutoAddPolicy())
			ssh.connect(hostname=host,port= port, username=username, password=password, timeout = 20, compress = True)
			print ("Successfull Login to ..{}..").format(host)
			
			for config in r_input_config:
			   ssh.exec_command(config, timeout = 60)
			   print ("Configuring..{}..").format(host)

			with outlock:
				#print stdout.readlines()
				print "End Configuring ..{}..\n".format(host)
				ssh.close()
				
		except paramiko.AuthenticationException:
			print("Authentication failed on {}, please verify your credentials: {}").format(host, username)
		except paramiko.SSHException as sshException:
			print("Unable to establish SSH connection on {}.").format(host)
		except paramiko.BadHostKeyException as badHostKeyException:
			print("Unable to verify server's host key on {}.").format(host)
		except Exception as e:
			print(e.args)

	def main():
		threads = []
		for ip in ip_list:
			t = threading.Thread(target=workon, args=(ip,))
			threads.append(t)

		for t in threads:
			t.start()

		for t in threads:
			t.join()

		print "Finish"

	main()

except KeyboardInterrupt:
    print "\n\nProgram Cancelled by user, Exiting...\n\n"
    sys.exit()
