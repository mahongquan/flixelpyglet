from FlxCore import FlxCore
from FlxG import *
import pyglet
#@desc		A basic text display class, can do some fun stuff though like flicker and rotate
class FlxText(FlxCore,pyglet.text.Label):
    def __init__(self,X, Y, Text="", Color=0xffffffff, Font=None, Size=18, Justification=None, Angle=0):
        pyglet.text.Label.__init__(self,Text,font_name=Font,font_size=Size,x=X,y=Y)
        FlxCore.__init__(self);
        self.x=X
        self.y=Y
        
    # #@desc		Called by the game loop automatically, updates the position and angle of the text
    def update(self,):
        pass
        # super.update();
        # n= Point();
        # getScreenXY(n);
        # if((_ox != n.x) or (_oy != n.y) or (_oa != angle)):
            # _mtx = Matrix();
            # _mtx.translate(-(width>>1),-(height>>1));
            # _mtx.rotate(Math.PI * 2 * (angle / 360));
            # _mtx.translate(n.x+(width>>1),n.y+(height>>1));
            # _ox = n.x;
            # _oy = n.y;
    
    # #@desc		Called by the game loop automatically, blits the text object to the screen
    def render(self):
        self.draw()
