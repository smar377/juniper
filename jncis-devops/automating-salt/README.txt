==========================================================================
1. Salt Installation
==========================================================================

The easiest way to set up Salt is through a bootstrap script:

- https://docs.saltstack.com/en/latest/topics/tutorials/salt_bootstrap.html

To install Salt on the master server, issue the following commands:

$ curl -o bootstrap_salt.sh -L https://bootstrap.saltstack.com
$ sudo sh bootstrap_salt.sh -M <-- Option "-M" used to install both "salt-master" and "salt-minion" processes

Output is omitted for brevity. The installation will take a minute or so. When it completes, you can check the Salt version by using the following command:

$ salt --version

On the minion1 server, install Salt by performing similar steps, but for this time do not use the –M key:

$ curl -o bootstrap_salt.sh -L https://bootstrap.saltstack.com
$ sudo sh bootstrap_salt.sh

Similarly check version by issuing:

$ salt-minion --version

NOTE: By default, the bootstrap script installs the latest stable Salt version, so it may differ from the 3004.1 that is used for this chapter. This will typically not be a problem. However, you can enforce the installation of a specific Salt version, if you wish, by modifying the second command as follows:

$ sudo sh bootstrap_salt.sh -M git v2018.3.2

(this is for master; for minion, omit the –M key).

==========================================================================
2. Performing Basic Salt Configuration and Verification
==========================================================================

There is one thing we definitely want to configure on the minion: that's to tell it where the master is (the default is actually to look for host named "salt")". So, let's start configuring the minion process on the "minion1" server by editing the minion's configuration file:

$ sudo vi /etc/salt/minion

Add the following line (in bold) to the file:

...
# Set the location of the salt master server. If the master server cannot be
# resolved, then the minion will fail to start.
#master: salt
master: 10.254.0.200
...

Here, the IP address is the master server's address in the lab setup. Remember that lines starting with a hash are treated as comments. Finally, restart the "salt-minion" process, so it re-reads the configuration:

$ sudo service salt-minion restart

Now, switch to the open terminal session with the master and issue the following command to view the minion's public key status:

$ sudo salt-key --list-all
Accepted Keys:
Denied Keys:
Unaccepted Keys:
minion1.edu.example.com
Rejected Keys:

Note the ID of the minion with an unaccepted key. The security system of Salt will not allow communication until you accept minion's key on master – so let's do that now:

$ sudo salt-key --accept=minion1.edu.example.com

The following keys are going to be accepted:

Unaccepted Keys:
minion1.edu.example.com
Proceed? [n/Y] y
Key for minion minion1.edu.example.com accepted.

Now let's execute some of the Salt commands, using its remote execution capabilities. Note we are testing basic Salt features here – no Junos at all is involved at this point. First, let's ping our minion:

$ sudo salt '*' test.ping
minion1.edu.example.com:
 True

Here, you called the "test.ping" execution function that is used to make sure the minion is up and responding. The communication happens over Salt's ZeroMQ message bus (so this is not an ICMP ping). The argument '*'' means that you want to execute on all minions, it just happens that, so far, we only have one.

Generally speaking, various Salt execution modules allow you to perform (execute) some specific tasks on minions: test is just one of such modules. Let's now try the "cmd.run" function – it allows the running of arbitrary commands on minions. Let’s check minion's Python version, just for an example:

$ sudo salt minion* cmd.run 'python -V'
minion1.edu.example.com:
 Python 3.6.9

You can run any other commands on the minions the same way. Check out the full Salt module index at

- https://docs.saltstack.com/en/latest/salt-modindex.html

for more examples.

** ATTENTION: In case we want to change minion's hostname we need to do the following:

1. Change hostname under "/etc/hosts" and "/etc/hostname" files and reboot machine.
2. If you run command:

$ salt-minion --log-level=debug

on the minion you will see that the "old" hostname is cached under: "/etc/salt/minion_id"

3. Change hostname in "/etc/salt/minion_id" file in order to comply withe the new hostname
4. Delete the accepted minion key on the Salt master node by issuing:

$ sudo salt-key -d <old-hostanme>
OR
$ sudo salt-key -D <-- This ones deletes all key on the master, either Accepted/Denied/Unaccepted/Rejected

Check by issuing:

$ sudo salt-key -L (OR sudo salt-key --list-all)

5. Restart the salt-minion process, so it can send the new hostname to the master (sudo service salt-minion restart).


==========================================================================
3. Adding Proxy Minions to Manage Junos Devices
==========================================================================

Chapter 2 explained how to start managing a Linux server with Salt. However, managing Junos devices with Salt is a bit different. You DO NOT run a Salt minion on-box with Junos devices; instead, a proxy minion process is used. The proxy minion process may run either on the Salt master server or on some other server.

The latter option allows for load distribution in scaled setups and is a bit easier to understand for educational purposes, so let's use it here: proxy minions will run on the minion1 server.

As a prerequisite step, NETCONF over SSH must be enabled on both Junos devices, as follows (this shows configuration for one device – make sure you perform this on the other one as well):

brook@vmx-1> configure
Entering configuration mode
[edit]

brook@vmx-1# set system services netconf ssh
[edit]

brook@vmx-1# commit
commit complete

The minion server (minion1) will now also run two Junos proxy minions, one for each of the two vMX devices in the topology. Proxy minions are just software processes (daemons) used to manage, in this case, a networking device. You need one proxy process per device, and for Junos one such process requires about 100MB of RAM, so we should plan our system accordingly.

From one "side" the proxy minion connects to Salt master using the ZeroMQ bus, while from the other "side" it is connected to the Junos device using NETCONF protocol (Junos PyEZ library is used under the hood). To start configuring Salt proxy, edit the "/etc/salt/proxy" file on the minion1 server:

$ sudo vi /etc/salt/proxy

Add the master setting to it, indicating where the Salt master is:

# Set the location of the salt master server. If the master server cannot be
# resolved, then the minion will fail to start.
#master: salt
master: 10.254.0.200

Before proceeding, it's time to get familiar with one more Salt concept: pillar. The Salt's pillar system provides various data associated with minions. In the simplest case, pillar files will be YAML files with defined variable values, but pillar data can also be stored in a database such as SQL, obtained via REST API from some external system, etc. The location where pillar files are stored can vary. By default, it is in the "/srv/pillar" directory of the master server (this is defined by
pillar_roots parameter in the "/etc/salt/master" configuration file on the Salt master). Let's just use the default directory – to do so, you will have to create it first:

$ sudo mkdir /srv/pillar

In this directory, create the "/srv/pillar/proxy-1.sls" file with the following content (just replace host IP, username, and password with values matching your setup):

$ cat /srv/pillar/proxy-1.sls
proxy:
 proxytype: junos
 host: 10.254.0.41
 username: brook
 password: onepiece123
 port: 830

NOTE: Salt certainly has ways to better secure your passwords, but that is beyond the scope of this chapter. Please consult the following URLs for details: https://docs.saltstack.com/en/latest/topics/best_practices.html#storing-secure-data and https://docs.saltstack.com/en/latest/ref/renderers/all/salt.renderers.gpg.html

Similarly, create the "/srv/pillar/proxy-2.sls" file:

$ cat /srv/pillar/proxy-2.sls
proxy:
 proxytype: junos
 host: 10.254.0.42
 username: brook
 password: onepiece123
 port: 830

The two files that you just created essentially contain some mappings (pairs of keys and corresponding values). For example, the key username maps to value lab, etc. The key proxy has a nested mapping as a value, which is shown by indentation. The format that you just used for these files is YAML (http://yaml.org/), while the file extension is SLS (SaLt State).

Generally, SLS files can be in various formats: in the simplest case it is YAML, or it can be YAML+Jinja (where Jinja is a templates format – see http://jinja.pocoo.org/), or something else if properly customized (maybe even Python code – Salt is very flexible).

Now let's create the pillar top file. This file will define which minions have access to which pillar data. In our case, the content will be as follows:

$ cat /srv/pillar/top.sls
base:
 'vmx-1':
 - proxy-1
 'vmx-2':
 - proxy-2

Here, base is the name of what is called environment in Salt. For example, we can have testing/staging/production environments – here we will just use the default base environment. Note also that the ".sls" extension for the "proxy-1.sls" and "proxy-2.sls" file names must be omitted. Now it's time to perform settings on the minion side. Switch to the "minion1" server.

Remember, this server will host two Junos proxy minion processes. For Junos proxy to successfully communicate with Junos devices, a couple of Python packages are needed – namely, Junos PyEZ and "jxmlease" (and their dependencies as well). To install those libraries, first install the Python PIP tool, and then the packages themselves (output omitted for brevity):

$ sudo apt-get install python-pip
$ sudo pip install junos-eznc
$ sudo python -m easy_install --upgrade pyOpenSSL
$ sudo pip install jxmlease

NOTE: Upgrade the "pyopenssl" package before installing "jxmlease". The explicit upgrade is used here as a workaround, otherwise you may see an error message like this: AttributeError: 'module' object has no attribute 'SSL_ST_INIT'. Okay, it's time to launch the Junos Salt proxy processes:

$ sudo salt-proxy --proxyid=vmx-1 -d
$ sudo salt-proxy --proxyid=vmx-2 -d

NOTE: The "–d" option makes "salt-proxy" run in the daemon mode. If you want the program to just run in the terminal window, omit that key. In this case you will be able to see some of the salt-proxy log messages in real time. You can modify the level of logging using -l key, for example: "sudo salt-proxy --proxyid=vMX-1 -l debug". This approach can be useful for troubleshooting.

And, on the master, accept the minion keys, just as we did before:

$ sudo salt-key -a vmx-1

The following keys are going to be accepted:
Unaccepted Keys:
vmv-1
Proceed? [n/Y] y
Key for minion vmx-1 accepted.

$ sudo salt-key -a vmx-2
The following keys are going to be accepted:
Unaccepted Keys:
vmx-2
Proceed? [n/Y] y
Key for minion vmx-2 accepted.

How many minions do you think you have now? Let’s check with test.ping:

$ sudo salt '*' test.ping
minion1.edu.example.com:
 True
vmx-1:
 True
vmx-2:
 True

So, we have two more minions (proxies) in addition to "minion1".
