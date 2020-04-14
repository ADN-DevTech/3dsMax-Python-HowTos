if isProperty python "execute" then (
    python.execute ("def _python_startup():\n" +
	"    try:\n" +
    "        import pkg_resources\n" +
    "    except ImportError:\n" +
    "        print('startup Python modules require pip to be installed.')\n" +
    "        return\n" +	
    "    for dist in pkg_resources.working_set: \n" +
    "        entrypt = pkg_resources.get_entry_info(dist, '3dsMax', 'startup')\n" +
    "        if not (entrypt is None):\n" +
    "            try:\n" +
    "                fcn = entrypt.load()\n" +
    "                fcn()\n" +
    "            except:\n" +
	"                print('skipped package startup for {}, startup not working'.format(dist))\n" +
    "_python_startup()\n" +
    "del _python_startup")
)
