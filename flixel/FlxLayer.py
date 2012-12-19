from FlxArray import FlxArray
from FlxCore import FlxCore
from FlxG import *
#@desc		This is an organizational class that can update and render a bunch of FlxCore objects
class FlxLayer(FlxCore):

    def __init__(self):
        FlxCore.__init__(self)
        self._children = FlxArray();
    
    #@desc		Adds a new FlxCore subclass (FlxSprite, FlxBlock, etc) to the list of children
    #@param	Core	The object you want to add
    def add(self,Core):
        #Layer.add(self,Core)
        return self._children.add(Core)
    
    #@desc		Automatically goes through and calls update on everything you added, override this function to handle custom input and perform collisions
    def update(self):
        FlxCore.update(self);
        for i in range( len(self._children)):
           
            if((self._children[i] != None) and self._children[i].exists and self._children[i].active):
                self._children[i].update();
    
    #@desc		Automatically goes through and calls render on everything you added, override this loop to do crazy graphical stuffs I guess?
    def render(self):
        FlxCore.render(self);
        for  i in  range(len(self._children)):
            if((self._children[i] != None) and self._children[i].exists and self._children[i].visible):
                self._children[i].render();
    
    #@desc		Override this function to handle any deleting or "shutdown" type operations you might need (such as removing traditional Flash children like Sprite objects)
    def destroy(self): 
        self._children.clear()
