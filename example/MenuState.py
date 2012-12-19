from flixel import *;
class MenuState(FlxState):
    def __init__(self):
        FlxState.__init__(self)
        self.add(FlxText( 10, 160, "Green ninja"))
        self.add(FlxText( 10,120, "don't like the"))
        self.add(FlxText(10, 80, "blue ninja") )
        self.add(FlxText( 10 , 40, "PRESS DOWN TO START"))
    
    def update(self):
        FlxState.update(self);
        if (FlxG.kDown):
            from PlayState import PlayState
            FlxG.switchState(PlayState);
