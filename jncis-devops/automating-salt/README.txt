==========================================================================
1. Salt Installation
==========================================================================

The easiest way to set up Salt is through a bootstrap script:

- https://docs.saltstack.com/en/latest/topics/tutorials/salt_bootstrap.html

To install Salt on the master server, issue the following commands:

$ curl -o bootstrap_salt.sh -L https://bootstrap.saltstack.com
$ sudo sh bootstrap_salt.sh -M

Output is omitted for brevity. The installation will take a minute or so. When it completes, you can check the Salt version by using the following command:

$ salt --version

On the minion1 server, install Salt by performing similar steps, but for this time do not use the –M key:

$ curl -o bootstrap_salt.sh -L https://bootstrap.saltstack.com
$ sudo sh bootstrap_salt.sh

$ salt-minion --version

NOTE: By default, the bootstrap script installs the latest stable Salt version, so it may differ from the 2018.3.2 that is used for this chapter. This will typically not be a problem. However, you can enforce the installation of a specific Salt version, if you wish, by modifying the second command as follows: 

$ sudo sh bootstrap_salt.sh -M git v2018.3.2

(this is for master; for minion, omit the –M key).


==========================================================================
2. Performing Basic Salt Configuration and Verification
==========================================================================

There is one thing you definitely want to configure on the minion: that’s to tell it where the master is (the default is actually to look for host named "salt")". So, start configuring the minion process on the minion1 server by editing the minion's configuration file:

$ sudo vi /etc/salt/minion

Add the following line (in bold) to the file:

...
# Set the location of the salt master server. If the master server cannot be
# resolved, then the minion will fail to start.
#master: salt
master: 10.254.0.200
...

Here, the IP address is the master server's address in the lab setup. Replace it with the address in your lab. Remember that lines starting with a hash are treated as comments. Do not forget to save the changes. Finally, restart the salt-minion process so it re-reads the configuration:

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
 Python 2.7.12

You can run any other commands on the minions the same way. Check out the full Salt module index at 

- https://docs.saltstack.com/en/latest/salt-modindex.html

for more examples.
