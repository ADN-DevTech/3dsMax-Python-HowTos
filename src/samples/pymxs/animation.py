'''
    Demonstrates simple animation.
'''
from pymxs import runtime as rt # pylint: disable=import-error
import pymxs as mx # pylint: disable=import-error

print("Hello World Animation")

def print_interval(interval):
    '''Prints an animation interval'''
    print(f"Current Animation Range: [{interval.start},{interval.end}]")

def set_animation_ranges():
    '''Changes the animation range from the default of 100 frames to 200 frames'''
    frames = 200
    print_interval(rt.animationRange)
    rt.animationRange = rt.Interval(0, frames)
    # The animation slider now shows 200 frames
    print_interval(rt.animationRange)


def animate_transform(thing):
    '''Records an animation on the provided object'''
    # select the object to animate so we will see the keyframes in the timeslider
    rt.select(thing)

    # animate
    with mx.animate(True):
        with mx.redraw(True):
            with mx.attime(30):
                thing.pos = rt.Point3(50, 0, 0)

            with mx.attime(60):
                thing.Pos = rt.Point3(100, 50, 0)

            with mx.attime(90):
                thing.Pos = rt.Point3(50, 100, 0)

            with mx.attime(120):
                thing.Pos = rt.Point3(0, 100, 0)

            with mx.attime(150):
                thing.Pos = rt.Point3(-50, 50, 0)

            with mx.attime(180):
                thing.Pos = rt.Point3(0, 0, 0)

def playback_animation():
    '''Play back the animation 3 times'''
    rt.playbackLoop = False
    # play animation
    print("Playing back Animation first time")
    rt.sliderTime = 0
    rt.timeConfiguration.playbackSpeed = 3 # normal speed
    rt.playAnimation()

    # replay it
    print("Playing back Animation second time")
    rt.timeConfiguration.playbackSpeed = 4 # double speed
    rt.sliderTime = 0
    rt.playAnimation()

    # replay it, faster
    print("Playing back Animation third time, faster")
    rt.sliderTime = 0
    rt.timeConfiguration.playbackSpeed = 5 # 4x speed
    rt.playAnimation()

def demo_animation():
    '''Show how to do animation'''
    rt.resetMaxFile(rt.Name('noPrompt'))
    sphere = rt.sphere()
    set_animation_ranges()
    animate_transform(sphere)
    playback_animation()

demo_animation()
