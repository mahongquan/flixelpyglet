import sys
sys.path.insert(0,"..")
from flixel.FlxGame import FlxGame
from MenuState import MenuState
from PlayState import PlayState 
import pyglet
class g1(FlxGame):
    def __init__(self):
        FlxGame.__init__(self,320,240,MenuState,2)
g=g1()
pyglet.gl.glClearColor(0, 0, 0, 1)
pyglet.gl.glEnable(pyglet.gl.GL_BLEND)
pyglet.gl.glBlendFunc(pyglet.gl.GL_SRC_ALPHA, pyglet.gl.GL_ONE_MINUS_SRC_ALPHA)
pyglet.app.run()