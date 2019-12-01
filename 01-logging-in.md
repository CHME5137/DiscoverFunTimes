# Logging in

Request an account through [ServiceNow](https://northeastern.service-now.com/research) following the [instructions](https://rc.northeastern.edu/support/documentation/), have your account sponsor approve the request, then wait for an email saying your account is ready.

To log in, use your husky username such as `surname.f` and your husky password.

Connecting as `ssh surname.f@login.discovery.neu.edu` will usually work fine.

If you see a message like
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
it might be that you've been assigned a different login node than last time you connected. The simplest way to avoid this is to explicitly pick one of the login nodes, eg. connect using
`ssh surname.f@login-01.discovery.neu.edu`.

Instead of using `ssh` in a linux terminal, you may wish to use a standalone SSH program
such as [MobaXterm](https://mobaxterm.mobatek.net) or http://www.putty.org or one of the [many others](https://en.wikipedia.org/wiki/Comparison_of_SSH_clients).
Research Computing are now recommending MobaXterm, which has X11 window system built in (see next section).

Should you need to run graphical programs, such as the user interface for the molecular modeling software Gaussian,
on the remote server and have the graphical window appear on your local screen, you need to connect
with X11 forwarding. This is done with `ssh -X surname.f@login.discovery.neu.edu`. You will need
to install X11 window system on your local computer, eg. [XQuartz](https://www.xquartz.org) for MacOS X and perhaps [Xming](http://www.straightrunning.com/XmingNotes/) for Windows (untested) or [MobaXterm](https://mobaxterm.mobatek.net)  (untested).
Otherwise, for command line programs only, you can just omit the `-X`. If `-X` doesn't work then try `-Y` (don't ask why).

Once you log in you should see a welcome message such as

```
Last login: Sun Dec  1 16:15:51 2019 from 209.6.146.176
+-----------------------------------------------------------+
| You're now connected to the Discovery cluster. Visit our  |
| website http://rc.northeastern.edu/support for links to   |
| our service catalog, documentation, training, and consul- |
| tations. You can also email us at rchelp@northeastern.edu |
| to generate a help ticket.                                |
|                                                           |
| The Research Computing Team                               |
+-----------------------------------------------------------+
[r.west@login-01 ~]$
```

Note that when transferring data (e.g. using SCP or SFTP) you should connect to xfer.discovery.neu.edu not login.discovery.neu.edu.

More details on how to log in, are in the Research Computing getting started guide [currently here](https://cpb-us-w2.wpmucdn.com/express.northeastern.edu/dist/1/43/files/2019/08/GettingStartedGuide-1.pdf).

For an alternative way to get a terminal with just your web browser, see [Chapter 10](10-ood.md) about the Open OnDemand portal.

---
Next: [2. Loading modules](02-modules.md)
