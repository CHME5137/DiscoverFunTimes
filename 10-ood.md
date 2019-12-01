# Using Open OnDemand
A recently added (and still under devepment) way of accessing the discovery cluster is via an "Open OnDemand" web portal.
This should work from any computer, without complicated ssh tunneling.
It will not work with Safari, so Mac users must download [Chrome](https://www.google.com/chrome/) or Firefox.
Access it at:

https://ood.discovery.neu.edu/ |
-------------------------------|

## Shell access
From the main portal you can access a shell terminal (as if you have connected via ssh) 
by choosing "Discovery Shell Access" from the "Clusters" menu.
From there you can do things like `conda install` and `git clone`.

## File editing
You can edit files, such as your `.bashrc` file, through this interface:

- From the "Files" menu choose "Home Directory"
- In the bar at the top choose "Show Dotfiles"
- Select the file (eg. `.bashrc`)
- Click the "Edit" button in the bar near the top of the directory listing.
- Edit the file
- Click the "Save" button near the top left.

## Jupyter Notebooks
By selecting "Interactive Apps" then "Jupyter Notebook" you can launch a jupyter notebook server.
Because it's (currently) set up to run on the `test` partition, you must select a run time of no more than 1 hour, or your job will never start.
