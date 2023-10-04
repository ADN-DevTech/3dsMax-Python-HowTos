if isProperty python "execute" and ((maxversion())[8]<2025) then (
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
    "            except Exception as e:\n" +
	"                print(f'skipped package startup for {dist} because {e}, startup not working')\n" +
    "_python_startup()\n" +
    "del _python_startup")
)
