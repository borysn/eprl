eprl
====

*edit portage resume list*

list, add, remove portage resume items

install
-------
..

    $ pip install eprl

run
-----

..

     $ sudo -H python -m eprl -h

usage
-----

..

  usage: 
    eprl.py 

      [-h] [-l] 

      [-r ITEMNUMS [ITEMNUMS ...]] 

      [-a ITEMS [ITEMS ...]] 

      [-b] [-v]

  optional arguments:
    -h, --help            show this help message and exit
    -l, --list            list portage resume items
    -r ITEMNUMS, --remove ITEMNUMS
                          remove portage resume item(s)
    -a ITEMS, --add ITEMS
                          add resume item(s) to a resume list
    -b, --backup          perform operations on backup list
    -v, --version         show program's version number and exit

license
-------

`MIT </LICENSE>`__
