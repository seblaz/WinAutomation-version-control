# WinAutomation Version Control Helper
## Prerequisites
- python 3
- untangle
```
pip install untangle
```

## Getting started

This scripts help using a version control with WinAutomation. Some of the commands need administration privileges, therefore it's recommended to run all of them with administration privileges.

### Export processes

To **export** the processes in the \processes folder run:
```
python export.py
```
This will export all the processes in your WinAutomation console and delete all previous files in \processes.

Then you should commit and/or merge any changes to your git repository.

### Import processes

Once you are done commiting and merging changes  you can **import** them:
```
python import.py
```
This will **delete** all the processes on your console and replace them with the ones in the \processes folder.

Side effect: this will also **delete** the triggers, schedules and logs on your console.

In order to  recover any lost processes, triggers, schedules or logs, a backup is made in the \backups folder.

### Restoring data from a backup

If you want to restore the data from a backup you can run:
```
python restore.py path_to_backup
```
For example:
```
python restore.py backups\2018-09-28-09-58.dat
```