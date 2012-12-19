from FlxLayer import FlxLayer
from FlxG import FlxG
#@desc		This is the basic game "state" object - e.g. in a simple game you might have a menu state and a play state
class FlxState():
    #@desc		Constructor	
    def __init__(self):
        self._layer =FlxLayer();
        FlxG.state = self
        #self.schedule(self.update)
    #@desc		Adds a new FlxCore subclass (FlxSprite, FlxBlock, etc) to the game loop
    #@param	Core	The object you want to add to the game loop
    def add(self,Core):
        return self._layer.add(Core);
    
    #@desc		Automatically goes through and calls update on everything you added to the game loop, override this function to handle custom input and perform collisions
    def update(self):
        self._layer.update();
    
    #@desc		Automatically goes through and calls render on everything you added to the game loop, override this loop to do crazy graphical stuffs I guess?
    def render(self):
        self._layer.render();
    
    #@desc		Override this function to handle any deleting or "shutdown" type operations you might need (such as removing traditional Flash children like Sprite objects)
    def destroy(self):
        self._layer.destroy()

