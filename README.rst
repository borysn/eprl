eprl
====

**edit portage resume list**

*list, add, remove portage resume items*

install
-------

..

    ``$ pip install eprl``

run
----

..

    ``$ sudo -H python -m eprl -h``
    
usage
-----

..

    **usage:**
        *eprl.py*

            ``[-h] [-l] [-b] [-v]``

            ``[-a *ITEMS* [*ITEMS* ...]]``

            ``[-r *ITEMNUMS* [*ITEMNUMS* ...]]``

    **optional arguments:**
        -h, --help              show this help message and exit
        -l, --list              list portage resume items
        -r ITEMNUMS, --remove ITEMNUMS
                                remove portage resume item(s)
        -a ITEMS, --add ITEMS
                                add resume item(s) to a resume list
        -b, --backup            perform operations on backup list
        -v, --version           show program's version number and exit

    **example usage:**

    ..

        $ eprl -b
            - ``list items in backup resume list``
        $ eprl -br 0 1 2 3 4
            - ``remove items in backup resume list``
        $ eprl -a asdf watchdog systemd
            - ``add items to resume list``

license
-------

`MIT </LICENSE>`__
