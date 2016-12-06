# Logging in

Request an account following the [instructions](http://www.northeastern.edu/rc/), have your account sponsor approve the request, then wait for an email saying your account is ready.

To log in, use your husky username such as `surname.f` and your husky password.

Connecting as `ssh surname.f@discovery.neu.edu` will randomly assign you to one of the two login nodes,
`discovery2` or `discovery4`. If you get one that is different from the one you got the first time
you connected, you may see a message like
```
@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@
@    WARNING: REMOTE HOST IDENTIFICATION HAS CHANGED!     @
@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@
IT IS POSSIBLE THAT SOMEONE IS DOING SOMETHING NASTY!
Someone could be eavesdropping on you right now (man-in-the-middle attack)!
It is also possible that a host key has just been changed.
The fingerprint for the RSA key sent by the remote host is
SHA256:iLtKeAxsiy9b3J5AAxI5jmhCkcMMF2dEk2QowHGsLl4.
Please contact your system administrator.
```

Simplest way to avoid this is to explicitly pick one of the login nodes, eg. connect using
`ssh surname.f@discovery2.neu.edu`  or `ssh surname.f@discovery4.neu.edu`.

Instead of using `ssh` in a linux terminal, you may wish to use a standalone SSH program
such as http://www.putty.org or one of the [many others](https://en.wikipedia.org/wiki/Comparison_of_SSH_clients).

Should you need to run graphical programs, such as the user interface for the molecular modeling software Gaussian,
on the remote server and have the graphical window appear on your local screen, you need to connect
with X11 forwarding. This is done with `ssh -X surname.f@discovery2.neu.edu`. You will need
to install X11 window system on your local computer, eg. [XQuartz](https://www.xquartz.org) for MacOS X and perhaps [Xming](http://www.straightrunning.com/XmingNotes/) for Windows (untested).
Otherwise, for command line programs only, you can just omit the `-X`. If `-X` doesn't work then try `-Y` (don't ask why).

Once you log in you should see a welcome message such as

```
Last login: Wed Nov 30 17:39:05 2016 from 129.10.10.10
+---------------------------------------------------------------------------+
| Northeastern University Research Computing Cluster (discovery.neu.edu)    |
| Login Node                                                                |
+---------------------------------------------------------------------------+
| Usage of this cluster assumes you have read and agree to usage guidelines |
| at http://www.northeastern.edu/rc.                                        |
|                                                                           |
| Please do not run interactive jobs or GUIs on this node, it is against    |
| usage policy that you agreed to when applying for the cluster account.    |
|                                                                           |
| See "Submitting Jobs on Discovery Cluster" page at                        |
| http://www.northeastern.edu/rc or contact researchcomputing@neu.edu.      |
|                                                                           |
| If you have reached this node in error please logout now and send an      |
| email with your login id to researchcomputing@neu.edu.                    |
|                                                                           |
| All other requests should be directed to researchcomputing@neu.edu.       |
|                                                                           |
| Thank you,                                                                |
| NU Research Computing Team (researchcomputing@neu.edu)                    |
+---------------------------------------------------------------------------+
[r.west@discovery2 ~]$
```

More details on how to log in, including X11 forwarding with Xming in Windows, are on the Research Computing website [here](http://nuweb12.neu.edu/rc/?page_id=75).

---
Next: [2. Loading modules](02-modules.md)
