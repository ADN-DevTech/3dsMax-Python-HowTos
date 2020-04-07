'''
    Lists all of the notification codes broadcast by 3ds Max,
    and registers a callback function for each and every one.
'''
import os
from pymxs import runtime as rt # pylint: disable=import-error

# sadly, maxscript does not expose this list
NOTIFICATIONS = [
    "unitsChange",
    "timeunitsChange",
    "viewportChange",
    "spacemodeChange",
    "systemPreReset",
    "systemPostReset",
    "systemPreNew",
    "systemPostNew",
    "filePreOpen",
    "filePostOpen",
    "filePreMerge",
    "filePostMerge",
    "filePreSave",
    "filePostSave",
    "selectionSetChanged",
    "bitmapChanged",
    "preRender",
    "preRenderFrame",
    "postRender",
    "postRenderFrame",
    "preImport",
    "postImport",
    "importFailed",
    "preExport",
    "postExport",
    "exportFailed",
    "nodeRenamed",
    "modPanelSelChanged",
    "animateOn",
    "animateOff",
    "mtlLibPreOpen",
    "mtlLibPostOpen",
    "mtlLibPreSave",
    "mtlLibPostSave",
    "mtlLibPreMerge",
    "mtlLibPostMerge",
    "preRenderEval",
    "renderParamsChanged",
    "nodeCreated",
    "nodeLinked",
    "nodeUnlinked",
    "nodeHide",
    "nodeUnhide",
    "nodeFreeze",
    "nodeUnfreeze",
    "nodePreMaterial",
    "nodePostMaterial",
    "sceneNodeAdded",
    "selectedNodesPreDelete",
    "selectedNodesPostDelete",
    "mainWindowEnabled",
    "preSystemShutdown",
    "postSystemStartup",
    "pluginLoaded",
    "postSystemShutdown",
    "colorChanged",
    "heightMenuChanged",
    "fileLinkPreBind",
    "fileLinkPostBind",
    "fileLinkPreDetatch",
    "fileLinkPostDetatch",
    "fileLinkPreReload",
    "fileLinkPostReload",
    "fileLinkPreAttach",
    "fileLinkPostAttach",
    "nodePreDelete",
    "nodePostDelete",
    "radiosityProcessStart",
    "radiosityProcessStopped",
    "radiosityProcessReset",
    "radiosityProcessDone",
    "modPanelObjPreChange",
    "modPanelObjPostChange",
    "sceneUndo",
    "sceneRedo",
    "manipulateModeOn",
    "manipulateModeOff",
    "animationRangeChange",
    "filePostMergeProcess",
    "filePostOpenProcess",
    "svSelectionSetChanged",
    "svDoubleClickGraphNode",
    "preModifierAdded",
    "postModifierAdded",
    "preModifierDeleted",
    "postModifierDeleted",
    "postNodesCloned",
    "preRendererChange",
    "postRendererChange",
    "svPreLayoutChange",
    "svPostLayoutChange",
    "layerCreated",
    "layerDeleted",
    "nodeLayerChanged",
    "beginRenderingActualFrame",
    "beginRenderingReflectRefractMap",
    "beginRenderingTonemappingImage",
    "byCategoryDisplayFilterChanged",
    "customDisplayFilterChanged",
    "filePreSaveOld",
    "filePostSaveOld",
    "filelinkPostReloadPrePrune",
    "lightingUnitDisplaySystemChange",
    "mtlRefAdded",
    "mtlRefDeleted",
    "nodeCloned",
    "objectXrefPreMerge",
    "objectXrefPostMerge",
    "preMirrorNodes",
    "postMirrorNodes",
    "preNodeBonePropChanged",
    "postNodeBonePropChanged",
    "preNodeGeneralPropChanged",
    "postNodeGeneralPropChanged",
    "preNodeGiPropChanged",
    "postNodeGiPropChanged",
    "preNodeMentalrayPropChanged",
    "postNodeMentalrayPropChanged",
    "preNodeUserPropChanged",
    "postNodeUserPropChanged",
    "preProgress",
    "postProgress",
    "preNodesCloned",
    "radiosityPluginChanged",
    "sceneXrefPostMerge",
    "sceneXrefPreMerge",
    "systemPostDirChange",
    "systemPreDirChange",
    "tabbedDialogCreated",
    "tabbedDialogDeleted",
    "nodeNameSet",
    "preSceneUndo",
    "preSceneRedo",
    "preSceneStateSave",
    "postSceneStateSave",
    "preSceneStateRestore",
    "postSceneStateRestore",
    "sceneStateDelete",
    "sceneStateRename",
    "filePreOpenProcess",
    "filePreSaveProcess",
    "filePostSaveProcess",
    "classDescLoaded",
    "atsPreRepathPhase",
    "atsPostRepathPhase",
    "proxyTempDisableStart",
    "proxyTempDisableEnd",
    "NamedSelSetCreated",
    "NamedSelSetDeleted",
    "NamedSelSetRenamed",
    "ModPanelSubObjectLevelChanged",
    "FailedDirectXMaterialTextureLoad",
    "D3DPreDeviceReset",
    "D3DPostDeviceReset",
    "postSceneReset",
    "animLayersEnabled",
    "animLayersDisabled",
    "selectionLocked",
    "selectionUnlocked",
    "preImageViewerDisplay",
    "postImageViewerDisplay",
    "imageViewerUpdate",
    "activeViewportChanged",
    "NamedSelSetPreModify",
    "NamedSelSetPostModify",
    "ClassDescAdded",
    "ObjectDefinitionChangeBegin",
    "ObjectDefinitionChangeEnd",
    "preAppThemeChange",
    "postAppThemeChange",
    "preViewPanelDelete",
    "preWorkspaceChange",
    "postWorkspaceChange",
    "preWorkspaceCollectionChange",
    "postWorkspaceCollectionChange",
    "mouseSettingsChanged",
    "preSavingCuiToolbars",
    "postSavingCuiToolbars",
    "preLoadingCuiToolbars",
    "postLoadingCuiToolbars",
    "appActivated",
    "appDeactivated",
    "cuiMenusUpdate",
    "fileOpenFailed",
    "postRestoreObjsDeleted",
    "preSavingMenus",
    "postSavingMenus",
    "viewportSafeFrameToggle",
    "postLoadingMenus",
    "layerParentChanged",
    "actionItemHotkeyPreExecute",
    "actionItemHotKeyPostExecute",
    "actionItemExecutionStarted",
    "actionItemExecutionEnded",
    "interactivePluginCreationStarted",
    "interactivePluginCreationEnded",
    "filePostMerge2",
    "postNodeSelectOperation",
    "preViewportTooltip",
    "welcomeScreenDone",
    "playbackStart",
    "playbackEnd",
    "sceneExplorerNeedsUpdate",
    "filePostOpenProcessFinalized",
    "filePostMergeProcessFinalized",
    "preProjectFolderChange",
    "postProjectFolderChange",
    "preStartupScriptLoad",
    "activeShadeInViewportToggled",
    "systemShutdownCheck",
    "systemShutdownCheckFailed",
    "systemShutdownCheckPassed",
    "filePostMerge3",
    "matLibPreOpen",
    "matLibPostOpen",
    "matLibPreSave",
    "matLibPostSave",
    "matLibPreMerge",
    "matLibPostMerge",
    "selNodesPreDelete",
    "selNodesPostDelete",
    "wmEnable"]

def list_codes():
    """List all known notification names."""
    print(NOTIFICATIONS)
    print(f"Number Notifications registered: {len(NOTIFICATIONS)}")

def handle_notification(code):
    """Handle a specific notification."""
    print(f"Notification handled: {code}")
    
def handle_callback():
    """Generic callback Python handler."""
    # note: less generic callback function shall be defined for specific events
    #       the notificationParams() returned elements are specific to event name/type
    print(f"Received event notification\n with notification parameters being {rt.callbacks.notificationParam()}")

def create_maxscript_callback_function():
    """Register a maxscript function to a Python callcack."""
    # Create a maxscript function (called 'pcb') referencing a Python function
    rt.pcb = handle_notification

def register_all_callbacks():
    """Register all the callbacks that we know."""
    create_maxscript_callback_function()
    for name in NOTIFICATIONS:
        # register a maxscript line to call for specified event name
        # calls the referenced Python function with an hardcoded argument
        # the optional named 'id' argument is used as a best practice,
        # to make it easier to find and remove callbacks later
        rt.callbacks.addScript(rt.Name(name), "pcb(\"{}\")".format(name), id=rt.Name("my_mxs_handler"))

        # register a Python function to call for event name
        # the registered function cannot take any arguments
        # the optional named 'id' argument is used as a best practice,
        # to make it easier to find and remove callbacks later
        rt.callbacks.addScript(rt.Name(name), handle_callback, id=rt.Name("my_python_handler"))

def unregister_all_callbacks():
    """Unregister all the callbacks that we know."""
    for name in NOTIFICATIONS:
        rt.callbacks.removeScripts(rt.Name(name), id=rt.Name("my_mxs_handler"))
        rt.callbacks.removeScripts(rt.Name(name), id=rt.Name("my_python_handler"))

def main():
    """Demonstrate callback registration."""
    # List all callback names that we know
    list_codes()
    # Register all callback names
    register_all_callbacks()

    # Do some things
    print("Creating sphere")
    sphere1 = rt.sphere()
    print("Setting radius for sphere 1")
    sphere1.radius = 2.0
    print("Creating sphere 2")
    sphere2 = rt.sphere()
    print("Setting radius on sphere 2")
    sphere2.radius = 2.0
    print("Setting parent of node 2 to node 1")
    sphere2.Parent = sphere1

    print("Saving file")
    output_path = os.path.join(rt.sysInfo.tempdir, 'temp.max')
    rt.saveMaxFile(output_path)
    print("Opening file")
    rt.loadMaxFile(output_path)

    print('unregistering notification handlers')
    unregister_all_callbacks()

main()
