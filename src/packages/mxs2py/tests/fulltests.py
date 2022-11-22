#! /usr/bin/env python3
import mxs2py


CASES = [
    (
        """2+2""",
        """from pymxs import runtime as rt\nimport mxsshim\nimport pymxs\n2 + 2"""
    ),
    (
        """a=2""",
        """from pymxs import runtime as rt\nimport mxsshim\nimport pymxs\na = 2"""
    ),
    (
"""fn abc a b = (
print a
print b
a = 1
b = 2
b)""",
"""from pymxs import runtime as rt
import mxsshim
def abc(a, b):
    rt.print(a)
    rt.print(b)
    a = 1
    b = 2
    return b
"""
    ),
    (
"""zozo = 2
struct mystruct (
    adatamember,
    fn zwa o = 1,
    fn zwi a = (
        zwi (adatamember + a + zozo + coco + mystruct + (zwa 1))
    )
)""",
"""from pymxs import runtime as rt\nimport mxsshim\nimport pymxs\nzozo = 2\nclass mystruct:\n    adatamember = None\n    def zwa(self, o):\n        1\n    \n    def zwi(self, a):\n        return self.zwi(self.adatamember + a + zozo + rt.coco + mystruct + (self.zwa(1)))\n    """
    ),
    (
"""
   fn test4b inVal =
   (
   local res = 2 * inVal
   )
""",
"""from pymxs import runtime as rt\nimport mxsshim\nimport pymxs\ndef test4b(inval):\n    res = 2 * inval\n"""
    ),
    (
"""
max file open
max unhide all
max quick render
max ?
""",
"""from pymxs import runtime as rt\nimport mxsshim\nimport pymxs\nmxsshim.max("file open")\nmxsshim.max("unhide all")\nmxsshim.max("quick render")\nmxsshim.max("?")"""
    ),
    (
"""selection[1].baseobject""",
"""from pymxs import runtime as rt\nimport mxsshim\nimport pymxs\nrt.selection[1 - 1].baseobject"""
    ),
    (
    """classOf selection[1].baseobject == Editable_Poly""",
    """from pymxs import runtime as rt\nimport mxsshim\nimport pymxs\nrt.classof(rt.selection[1 - 1].baseobject) == rt.editable_poly"""
    ),
    (
    """print a + 2""",
    """from pymxs import runtime as rt\nimport mxsshim\nimport pymxs\nrt.print(a) + 2"""
    ),
    (
    """print "2" as float + 12.3""",
    """from pymxs import runtime as rt\nimport mxsshim\nimport pymxs\nmxsshim.as(rt.print("2"), rt.float) + 12.3"""
    ),
    (
    """delete $VoxelBox*""",
    """from pymxs import runtime as rt\nimport mxsshim\nimport pymxs\nrt.delete(mxsshim.path("$VoxelBox*"))"""
    ),
    (
    """a = not a""",
    """from pymxs import runtime as rt\nimport mxsshim\nimport pymxs\na = not a"""
    ),
    (
    """$*.material = undefined""",
    """from pymxs import runtime as rt\nimport mxsshim\nimport pymxs\nmxsshim.path("$*").material = None"""
    ),
    (
        """macroScript AutoMat category: "HowTo"
(
   local AutoMat_Enabled
   on isChecked return AutoMat_Enabled
   on Execute do
   (
      updateToolbarButtons()
   )
)""",
    """from pymxs import runtime as rt\nimport mxsshim\nimport pymxs\nclass MacroScript_automat(mxsshim.MacroScript):\n    def __init__(self, **kwargs):\n        self.on("ischecked", self.ischecked)\n        self.on("execute", self.execute)\n        mxsshim.MacroScript.__init__(self, "automat", **kwargs)\n    automat_enabled = None\n    def ischecked(self):\n        return self.automat_enabled\n    \n    def execute(self):\n        return rt.updatetoolbarbuttons()\n    \nMacroScript_automat(category="HowTo")"""
    ),
(
"""at time t current_pos = selection.center""",
"""from pymxs import runtime as rt\nimport mxsshim\nimport pymxs\nwith pymxs.attime(rt.t):\n    current_pos = rt.selection.center"""
),
(
"""undo on print 1""",
"""from pymxs import runtime as rt\nimport mxsshim\nimport pymxs\nwith pymxs.undo(True):\n    rt.print(1)"""
),
(
"""iundo on (
   delete $box*
   delete $sphere*
   clearUndoBuffer()
   )""",
"""from pymxs import runtime as rt\nimport mxsshim\nimport pymxs\nrt.iundo(True, rt.delete(mxsshim.path("$box*"))\nrt.delete(mxsshim.path("$sphere*"))\nrt.clearundobuffer())""" 
),
(
"""renderers.current = Default_Scanline_Renderer()""",
"""from pymxs import runtime as rt\nimport mxsshim\nimport pymxs\nrt.renderers.current = rt.default_scanline_renderer()"""
),
(
"""blah[123] = 1""",
"""from pymxs import runtime as rt\nimport mxsshim\nimport pymxs\nrt.blah[123 - 1] = 1"""
),
(
"""blah = 1""",
"""from pymxs import runtime as rt\nimport mxsshim\nimport pymxs\nblah = 1"""
),
(
"""a = y - 1""",
"""from pymxs import runtime as rt\nimport mxsshim\nimport pymxs\na = rt.y - 1"""
),
(
"""for b in c to d do (print b)""",
"""from pymxs import runtime as rt\nimport mxsshim\nimport pymxs\nfor b in range(int(rt.c), 1 + int(rt.d)):\n    rt.print(b)"""
),
(
"""if dot (getNormal obj v) [0,0,1] <= -0.25 do deleteVert obj v
""",
"""from pymxs import runtime as rt\nimport mxsshim\nimport pymxs\nif rt.dot(rt.getnormal(rt.obj, rt.v), rt.point3(0, 0, 1)) <= -0.25:\n    rt.deletevert(rt.obj, rt.v)"""
),
(
"""    if 1 then
    (
        if 2 then
        (
            if 3 then
            (
                if 4 then
                (
                    foundIt = abc
                )
            )
        )
    )
""",
"""from pymxs import runtime as rt\nimport mxsshim\nimport pymxs\nif 1:\n    if 2:\n        if 3:\n            if 4:\n                foundit = abc"""
),
(
        """print #'Tall Straw (breeze)'""",
        """from pymxs import runtime as rt\nimport mxsshim\nimport pymxs\nrt.print(rt.name("Tall Straw (breeze)"))"""
),
(
        """if 1 then () else ()""",
        """from pymxs import runtime as rt\nimport mxsshim\nimport pymxs\nif 1:\n    pass\nelse:\n    pass"""
),
(
        """fn broken = ( if 1 then () else () )""",
        """from pymxs import runtime as rt\nimport mxsshim\nimport pymxs\ndef broken():\n    if 1:\n        pass\n    else:\n        pass\n"""
),
(
        """oiiotool_exe = pathConfig.appendPath (pathConfig.appendPath (pathConfig.appendPath (pathConfig.appendPath (pathConfig.appendPath (pathConfig.appendPath (getDir #scripts) "autoMXS") "TestSuites") "TestUtils") "OiioTool") "bin") "oiiotool.exe" """,
        """from pymxs import runtime as rt\nimport mxsshim\nimport pymxs\noiiotool_exe = rt.pathconfig.appendpath(rt.pathconfig.appendpath(rt.pathconfig.appendpath(rt.pathconfig.appendpath(rt.pathconfig.appendpath(rt.pathconfig.appendpath(rt.getdir(rt.name("scripts")), "autoMXS"), "TestSuites"), "TestUtils"), "OiioTool"), "bin"), "oiiotool.exe")"""
),
(
	"""fncall 1 2 \\   -- kfsfsdklfjsdlfsd fdskljfdslfjds      \n  3""",
	"""from pymxs import runtime as rt\nimport mxsshim\nimport pymxs\n#  kfsfsdklfjsdlfsd fdskljfdslfjds      \nrt.fncall(1, 2, 3)"""
),
(
        """print 0.""",
        """from pymxs import runtime as rt\nimport mxsshim\nimport pymxs\nrt.print(0.)"""
),
(
        """print (arr[1]).pos""",
        """from pymxs import runtime as rt\nimport mxsshim\nimport pymxs\nrt.print((rt.arr[1 - 1]).pos)"""
),
(
        """coordsys targ fill.pos = key.pos * ((eulerangles 0 0 p) as quat)""",
        """from pymxs import runtime as rt\nimport mxsshim\nimport pymxs\nwith mxsshim.in_coordsys(rt.targ):\n    rt.fill.pos = rt.key.pos * (mxsshim.as(rt.eulerangles(0, 0, rt.p), rt.quat))"""
),
(
        """coordsys grid key.pos = gridPoint""",
        """from pymxs import runtime as rt\nimport mxsshim\nimport pymxs\nwith mxsshim.in_coordsys(rt.name("grid")):\n    rt.key.pos = rt.gridpoint'"""
),
(
        """coordsys targ back.pos = - key.pos""",
        """from pymxs import runtime as rt\nimport mxsshim\nimport pymxs\nwith mxsshim.in_coordsys(rt.targ):\n    rt.back.pos = -rt.key.pos"""
),
(
        """iniVals [i] = 1""",
        """from pymxs import runtime as rt\nimport mxsshim\nimport pymxs\nrt.inivals[rt.i - 1] = 1"""
),
(

"""struct mystruct (
    public adatamember,
    private adatamember2,
    private fn zwa o = 1,
    public fn zwi a = (
        zwi (adatamember + a + zozo + coco + mystruct + (zwa 1))
    )
)""",
"""from pymxs import runtime as rt\nimport mxsshim\nimport pymxs\nclass mystruct:\n    adatamember = None\n    adatamember2 = None\n    def zwa(self, o):\n        1\n    \n    def zwi(self, a):\n        return self.zwi(self.adatamember + a + zozo + rt.coco + mystruct + (self.zwa(1)))\n    """
),
(
        """function TestIndexMatchCategories rendererType = (throw (ss as string) )""",
        """from pymxs import runtime as rt\nimport mxsshim\nimport pymxs\ndef testindexmatchcategories(renderertype):\n    raise RuntimeError((mxsshim.as(rt.ss, rt.string)))\n"""
),
(
        """function TestIndexMatchCategories rendererType = (throw () )""",
        """from pymxs import runtime as rt\nimport mxsshim\nimport pymxs\ndef testindexmatchcategories(renderertype):\n    raise RuntimeError()\n"""
),
(
        """print ::abc""",
        """from pymxs import runtime as rt\nimport mxsshim\nimport pymxs\nrt.print(rt.abc)"""
),
(
        """::abc = 3""",
        """from pymxs import runtime as rt\nimport mxsshim\nimport pymxs\nrt.abc = 3"""
),
(
        """
max undo
max undo
print "yeah"
""",
        """from pymxs import runtime as rt\nimport mxsshim\nimport pymxs\nmxsshim.max("undo")\nmxsshim.max("undo")\nrt.print("yeah")"""
),
(
    """b = &a""",
    """from pymxs import runtime as rt\nimport mxsshim\nimport pymxs\nb = pymxs.byref(a)"""
),
(
    """a.set 123""",
    """from pymxs import runtime as rt\nimport mxsshim\nimport pymxs\na.set(123)"""
),
(
    """for i=2 to 9 do r[i] /= (1024*1024.)""",
    """from pymxs import runtime as rt\nimport mxsshim\nimport pymxs\nfor i in range(int(2), 1 + int(9)):\n    rt.r[i - 1] /= (1024 * 1024.)"""
),
(
    """print $baz.'abcd'""",
    """from pymxs import runtime as rt\nimport mxsshim\nimport pymxs\nrt.print(mxsshim.path("$baz").abcd)"""
),
(
    """a = b = c = 2 + 2""",
    """from pymxs import runtime as rt\nimport mxsshim\nimport pymxs\na = b = c = 2 + 2"""
),
(
    """a = 2 +
2 +
3""",
    """from pymxs import runtime as rt\nimport mxsshim\nimport pymxs\na = 2 + 2 + 3"""
),
(
    """# 
( 1 , 2, 3)""",
"""from pymxs import runtime as rt\nimport mxsshim\nimport pymxs\nrt.array(1, 2, 3)"""
),
(
    """#(0x0E, 0xFFE0, 0xffff)""",
    """from pymxs import runtime as rt\nimport mxsshim\nimport pymxs\nrt.array(0x0E, 0xFFE0, 0xffff)"""
),
(
    """#(.2, -.2, .2e-6, -.2e-6 )""",
    """from pymxs import runtime as rt\nimport mxsshim\nimport pymxs\nrt.array(.2, -.2, .2e-6, -.2e-6)"""
),
(
    """print $'Bip01 Head'""",
    """from pymxs import runtime as rt\nimport mxsshim\nimport pymxs\nrt.print(mxsshim.path("$\'Bip01 Head\'"))"""
),
(
    """1 + \
1""",
    """from pymxs import runtime as rt\nimport mxsshim\nimport pymxs\n1 + 1"""
),
(
        """ print 2.5s
print 1m15s
print 2m30s5f2t
print 125f
print 17.25f
print 1f20t
print 2:10.0
print 0:0.29
""",
"""from pymxs import runtime as rt\nimport mxsshim\nimport pymxs\nrt.print(mxsshim.time("2.5s"))\nrt.print(mxsshim.time("1m15s"))\nrt.print(mxsshim.time("2m30s5f2t"))\nrt.print(mxsshim.time("125f"))\nrt.print(mxsshim.time("17.25f"))\nrt.print(mxsshim.time("1f20t"))\nrt.print(mxsshim.time("2:10.0"))\nrt.print(mxsshim.time("0:0.29"))""" ),
(
    "#{1..6, 15, 18}",
    """from pymxs import runtime as rt\nimport mxsshim\nimport pymxs\nrt.bitarray(*(list(range(1, 6 + 1)) + [15] + [18]))"""
),
("""function test_batch messageMode 
	expectedExitCode 
	scriptFilename:undefined
	tempLogFile:undefined =
(
print "ya"
)""",
"""from pymxs import runtime as rt\nimport mxsshim\nimport pymxs\ndef test_batch(messagemode, expectedexitcode, scriptfilename=None, templogfile=None):\n    return rt.print("ya")\n"""
),
(
"""a = #9a
b = #aa
c = #a9
""",
"""from pymxs import runtime as rt\nimport mxsshim\nimport pymxs\na = rt.name("9a")\nb = rt.name("aa")\nc = rt.name("a9")"""
),
(
"""adpSharedBin = @"Autodesk\ADPSDK\bin\"

function setUp =
(
-- Delete results of any previous test run
local oldFiles = 3
)
""",
"""from pymxs import runtime as rt\nimport mxsshim\nimport pymxs\nadpsharedbin = "Autodesk\\\\ADPSDK\x08in"\ndef setup():\n    #  Delete results of any previous test run\n    oldfiles = 3\n"""
),
(
"""fn assert_equal_array a1 a2 message: = ()""",
"""from pymxs import runtime as rt\nimport mxsshim\nimport pymxs\ndef assert_equal_array(a1, a2, message=None):\n    pass\n"""
),
(
"""fn map t = return t * scale * offset""",
"""from pymxs import runtime as rt\nimport mxsshim\nimport pymxs\ndef map(t):\n    return t * rt.scale * rt.offset\n"""
),
(
    """set undo on\n""",
    """from pymxs import runtime as rt\nimport mxsshim\nimport pymxs\nmxsshim.setcontext()"""
),
(
    """00.0""",
    """from pymxs import runtime as rt\nimport mxsshim\nimport pymxs\n00.0"""
),
(
    """#{0..$a.b}""",
    """from pymxs import runtime as rt\nimport mxsshim\nimport pymxs\nrt.bitarray(*(list(range(0, mxsshim.path("$a").b + 1))))"""
),
(
    """#{0..a.b  + 1}""",
    """from pymxs import runtime as rt\nimport mxsshim\nimport pymxs\nrt.bitarray(*(list(range(0, a.b + 1 + 1))))"""
),
(
    """function abc &aa &bb &cc:0 = ( )""",
    """from pymxs import runtime as rt\nimport mxsshim\nimport pymxs\ndef abc(rt.aa, rt.bb, cc=0):\n    pass\n"""
),
(
    """#(45447852L, 940627748L)""",
    """from pymxs import runtime as rt\nimport mxsshim\nimport pymxs\nrt.array(45447852L, 940627748L)"""
),
(
    """&(abc[2])""",
    """from pymxs import runtime as rt\nimport mxsshim\nimport pymxs\npymxs.byref(abc[2 - 1])"""
),
(
    """fn ab a b = (a + b)""",
    """from pymxs import runtime as rt\nimport mxsshim\nimport pymxs\ndef ab(a, b):\n    return a + b\n"""
),
(
    """(
    print 1
    print 2
    )""",
    """from pymxs import runtime as rt\nimport mxsshim\nimport pymxs\nrt.print(1)\nrt.print(2)"""
),
(
    """y-1""",
    """from pymxs import runtime as rt\nimport mxsshim\nimport pymxs\nrt.y - 1"""
),
(
    """y- 1""",
    """from pymxs import runtime as rt\nimport mxsshim\nimport pymxs\nrt.y - 1"""
),
(
    """y - 1""",
    """from pymxs import runtime as rt\nimport mxsshim\nimport pymxs\nrt.y - 1"""
),
(
    """y -1""",
    """from pymxs import runtime as rt\nimport mxsshim\nimport pymxs\nrt.y(-1)"""
),
(
    """subobjectlevel=2""",
    """from pymxs import runtime as rt\nimport mxsshim\nimport pymxs\nrt.subobjectlevel = 2"""
),
(
    """struct mapper
(
scale,
offset,
fn map t = return t * scale * offset
)""",
"""from pymxs import runtime as rt\nimport mxsshim\nimport pymxs\nclass mapper:\n    scale = None\n    offset = None\n    def map(self, t):\n        return t * self.scale * self.offset\n    \n    def __init__(self, **kwargs):\n        for key, value in kwargs.items():\n            setattr(self, key, value)\n"""
),
( 
    """$torso...*""", 
    """from pymxs import runtime as rt\nimport mxsshim\nimport pymxs\nmxsshim.path("$torso...*")""" 
)

]


def check(item):
    check = mxs2py.topy(item[0], file_header=None)
    if check[0] != item[1]:
        print(item[0])
        print(check)
        return

for c in CASES:
    check(c)
