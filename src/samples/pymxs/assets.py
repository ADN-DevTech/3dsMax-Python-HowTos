'''
    Lists all of the assets in a file.
'''
from pymxs import runtime as rt # pylint: disable=import-error

NASSETS = rt.AssetManager.GetNumAssets()
print(f"There are {NASSETS} assets created")
for i in range(NASSETS):
    a = rt.AssetManager.GetAssetByIndex(i + 1)
    print(f"Asset id = {a.GetAssetId()}, type = {a.getType()}, file = {a.getfilename()}")
