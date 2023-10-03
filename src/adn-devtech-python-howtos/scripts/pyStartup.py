def _python_startup():
    try:
        import pkg_resources
    except ImportError:
        print('startup Python modules require pip to be installed.')
        return	
    for dist in pkg_resources.working_set: 
        entrypt = pkg_resources.get_entry_info(dist, '3dsMax', 'startup')
        if not (entrypt is None):
            try:
                fcn = entrypt.load()
                fcn()
            except Exception as e:
                print(f'skipped package startup for {dist} because {e}, startup not working')

    # configure 2025 menus
    from pymxs import runtime as rt
    from menuhook import register_howtos_menu_2025
    def menu_func():
        menumgr = rt.callbacks.notificationparam()
        register_howtos_menu_2025(menumgr)

    # menu system
    cuiregid = rt.name("cuiRegisterMenus")
    howtoid = rt.name("pyScriptHowtoMenu")
    rt.callbacks.removescripts(id=cuiregid)
    rt.callbacks.addscript(cuiregid, menu_func, id=howtoid)


_python_startup()

