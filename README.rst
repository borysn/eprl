eprl
====

**edit portage resume list**

*list, add, remove portage resume items*

*clear, export, import portage resume list*

install
-------

..

1. add `oxenfree <https://github.com/borysn/oxenfree>`_ overlay
2. ``$ sudo emerge -a eprl``

run
----

..

    ``$ sudo eprl -h``
    
usage
-----

..

    **eprl.py:**

            ``[-h] [-l] [-c]``

            ``[-a ITEMS [ITEMS ...]]``

            ``[-r ITEMNUMS [ITEMNUMS ...]]``

            ``[-e] [-i] [-b] [-v]``

    **optional arguments:**

        -h, --help              show this help message and exit
        -l, --list              list portage resume items
        -c, --clear             clear portage resume list
        -r ITEMNUMS, --remove ITEMNUMS
                                remove portage resume item(s)
        -a ITEMS, --add ITEMS
                                add resume item(s) to a resume list
        -e, --export            export portage resume list
        -i, --import            import portage resume list
        -b, --backup            perform operations on backup list
        -v, --version           show program's version number and exit

    **example usage:**

    ..

        $ eprl -bl
            - ``list items in backup resume list``
        $ eprl -br 0 1 2 3 4
            - ``remove items in backup resume list``
        $ eprl -a asdf watchdog systemd
            - ``add items to resume list``

license
-------

`MIT </LICENSE>`__
