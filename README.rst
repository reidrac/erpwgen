Easy to Remember Password Generator
===================================

This tool was inspired by::

 - http://xkcd.com/936/
 - http://www.openwall.com/lists/oss-security/2012/01/19/24
 - https://www.memset.com/tools/password-generator/

So yes: yet another password generator. This time in Python and because
I thought it would be fun to programm it (and indeed it was!).

It requires a MySpell (or Hunspell) dictionary. More information::

 http://wiki.openoffice.org/wiki/Dictionaries

By default the dictionaries are loaded from their usual location::

 - /usr/share/myspell/dicts
 - /usr/share/myspell/

But you can provide the full path to the dictionary with --dictionary option
(and the --lang option will be ignored).

Example::

    $ ./erpwgen.py -v
    48359 lines read from en_US
    11382 valid words in the dictionary, (5, 6) letters
    14741486079600 possible passwords, entropy ~43 bits

    FultonHonerEvince6
    CookieDariusVanity4
    PelmetSnickEnrico8
    ConleyAspicSilty2
    MizzenSatoriRecon9
    MenaceCyrilBatted3
    FigureChoosySwivel5
    WatersBbsesAssess4
    SwitchBaselyDemean4
    BywayGruelDraggy4

Or from Python::

    >>> from erpwgen import Pwgen
    >>> gen = Pwgen('en_US')
    >>> gen.passwd()
    'JarrodDowseDwelt1'

Run erpwgen.py -h for help.


License
-------

This is free software under the terms of MIT license (check COPYING file
included in this package).


Author
------

- Juan J. Martinez <jjm@usebox.net>

