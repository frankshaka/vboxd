vboxd
=====

A [launchd](https://developer.apple.com/library/mac/documentation/Darwin/Reference/ManPages/man8/launchd.8.html#//apple_ref/doc/man/8/launchd) agent for Mac OS X to automatically starts/stops [VirtualBox](http://www.virtualbox.org) managed virtual machines on user logging in/out.


Why vboxd?
----------
If you log out or shut down your Mac, all running VMs managed by VirtualBox are aborted and forcedly shut down, so that all runtime states of these VMs are lost (e.g. Windows will report this as an abnormal shutdown on next launch) and you have to reboot them manually next time you log in. The 'vboxd' intends to save running VMs' states when you log out by keeping a little launch agent(daemon) running in the background and listening for logging out signal.

Another benefit of using 'vboxd' is that you can specify which VMs should be automatically started once you boot up and log in your Mac, so that you don't have to start them manually.


To Install
----------

    $ python setup.py install


To Configure
------------
Edit `~/Library/Application Support/org.virtualbox.custom.vboxd/etc/vboxd-start.conf` to specify which virtual machines should be started on daemon starting.


To Reload
---------

    $ launchctl unload ~/Library/LaunchAgents/org.virtualbox.custom.vboxd.plist
    $ launchctl load ~/Library/LaunchAgents/org.virtualbox.custom.vboxd.plist


To Uninstall
------------

    $ python setup.py uninstall

to get launch agent unloaded and executable file deleted while config and log files are kept, or

    $ python setup.py uninstall -a

if you want all related files to be deleted.
