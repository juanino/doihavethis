# doihavethis
Compare multi-level directory structure of pictures to some pile of pictures or videos you just found on a disk.

# How it works
* get python3 for your platform (tested with python 3.4.3)
* git clone the repo
* run ./get_stuff.sh (works for apt-based systems)
* run inventory of your stuff on a machine with inv2pickle.py
* stdout prints -D- when it finds a directory or "F" when it's working on a hash for a file and the resulting comparison data (which is also in the info log)
* stdout also prints -Duplicate- if duplicates are found WITHIN the directories you are running an inventory on
```
root@blah:~# python ./doihavethis-master/inv2pickle.py my_stuff.db /top_level_dir_of_stuff/
-D--D-FFFFFFF-D-FFFFFFFFFFF-D-FFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFF
FFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFF-D-FFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFF
FFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFF
FFFFFFFFFFFFFFFFFFFFFFFFFFFFFFF-D-FFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFF
```
* once the inventory is complete check inventory.log for any duplicates (grep duplicate)
```
root@blah:~# cat inventory.log |grep -i duplicate
```
* inspect your pickledb file that results
```
root@blah:~# ./doihavethis/pickle_list.py my_stuff.db
```
* repeat on all systems or directories where you have photos or files you want to inventory
* run cmp_pickles.py to compare two files. Always list the "master" database last since it only compares one direction.
* cmp_pickles can be read as "compare the newly found files in the first arg with the master db in the second arg"
* you can copy the db files around as needed
* you can run pickle_list.py and grep for any file you have an md5 sum of to see if it's in your master

# Issues
* you can't give it multiple directories. run inv2pickle.py twice and use merge_pickles.py to combine them
* doesn't work with socket files and other special files since a hash can't be generated for those
* has some issues with pickledb used in raspbian

# Why did i do this
Mostly because I seem to rewrite variations of this all the time and i can't find my code.
This way I'm documenting it for myself, my friends and any other shmuck who has to combine a bunch of old disks, drives, sd cards, whatever.
Just copy all your files into a working dir and run an invenotry with inv2pickle.
As drives got bigger, it makes no sense to have bunches of disks laying around or even various USB sticks.

Also, it is handy if you are not sure which files you pulled off an SD card, or if you happen to (like in my case) blow away or corrupt an SD card
and use the wonderful photorec and testdisk to recover the files off the chip, but have no idea which files you already downloaded since recovery
pulls every non-clobbered file off that chip, even if you meant to delete it previously.

# links
* [Tool for recovering photos](https://www.cgsecurity.org/wiki/PhotoRec_Step_By_Step)
* [Using config files in python](https://martin-thoma.com/configuration-files-in-python)
