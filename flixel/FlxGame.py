from FlxG import *
import pyglet
fps_display = pyglet.clock.ClockDisplay()
class FlxGame(pyglet.window.Window):
    MAX_CONSOLE_LINES = 256;
    MAX_elapsed= 0.0333;
    def log(self,data):
        print data
    #@desc		Constructor
    #@param	GameSizeX		The width of your game in pixels (e.g. 320)
    #@param	GameSizeY		The height of your game in pixels (e.g. 240)
    #@param	InitialState	The class name of the state you want to create and switch to first (e.g. MenuState)
    #@param	Zoom			The level of zoom (e.g. 2 means all pixels are now rendered twice as big)
    #@param	BGColor			The color of the Flash app's background
    #@param	FlixelColor		The color of the great big 'f' in the flixel logo
    #@param	FlixelSound		The sound that is played over the flixel 'f' logo
    #@param	Frame			If you want you can add a little graphical frame to the outside edges of your game
    #@param	ScreenOffsetX	If you use a frame, you're probably going to want to scoot your game down to fit properly inside it
    #@param	ScreenOffsetY	These variables do exactly that!		
    def __init__(self,GameSizeX,GameSizeY,InitialState,Zoom=2,BGColor=0xff000000,ShowFlixelLogo=true,FlixelColor=0xffffffff,FlixelSound=None,Frame=None,ScreenOffsetX=0,ScreenOffsetY=0):
        pyglet.window.Window.__init__(self,width=GameSizeX, height=GameSizeY)
        FlxG.setGameData(GameSizeX,GameSizeY,self.switchState,self.log)
        self._total=0;
        self._elapsed=0
        self._iState = InitialState
        self._paused = false
        self._showLogo=false
        self._created = false;#step 1
        self._logoComplete=false;#step 2
        self._curState = None
        pyglet.clock.schedule(self.update)
    # #@desc		Switch from one FlxState to another
    # #@param	State		The class name of the state you want (e.g. PlayState)
    def switchState(self,state):
        print "switch state============"
        FlxG.unfollow();
        FlxG.resetKeys();
        self._quakeTimer = 0;
        newState = state();
        if(self._curState != None):
            self._curState.destroy();
        self._curState = newState;
    
    # #@desc		This function is only used by the FlxGame class to do important internal management stuff
    def on_key_release (self, key, modifiers):
        kn=pyglet.window.key.symbol_string(key)
        if (kn=="LEFT"):
            FlxG.kLeft = false;
            FlxG.releaseKey(0); #left
        elif (kn=="RIGHT"):
            FlxG.kRight = false;
            FlxG.releaseKey(1); #right
        elif (kn=="UP"):
            FlxG.kUp = false;
            FlxG.releaseKey(2); #up
        elif (kn=="DOWN"):
            FlxG.kDown = false;
            FlxG.releaseKey(3); #down
        elif (kn == 'X'):
            FlxG.kA = false;
            FlxG.releaseKey(4); #A
        elif (kn == 'C') :
            FlxG.kB = false;
            FlxG.releaseKey(5); #B
    # #@desc		This function is only used by the FlxGame class to do important internal management stuff
    def on_key_press(self,key, modifiers):
        kn=pyglet.window.key.symbol_string(key)
        #print kn
        if (kn=="LEFT"):
            FlxG.kLeft = true;
            FlxG.pressKey(0); #left
        elif (kn=="RIGHT"):
            FlxG.kRight = true;
            FlxG.pressKey(1); #right
        elif (kn=="UP"):
            FlxG.kUp = true;
            FlxG.pressKey(2); #up
        elif (kn=="DOWN"):
            FlxG.kDown = true;
            FlxG.pressKey(3); #down
        elif (kn == 'X'):
            FlxG.kA = true;
            FlxG.pressKey(4); #A
        elif (kn == 'C') :
            FlxG.kB = true;
            FlxG.pressKey(5); #B
    def update(self,dt):
        #print "flxga update",dt
        FlxG.elapsed=dt
        if(FlxG.elapsed > FlxGame.MAX_elapsed):
                    FlxG.elapsed = FlxGame.MAX_elapsed;
        self.clear()
        if(self._logoComplete):
            if(not self._paused):
                FlxG.updateKeys();
                FlxG.doFollow();
                self._curState.update();
                self._curState.render();
                fps_display.draw()
        elif(self._created):
            self._logoComplete = true;
            self.switchState(self._iState);
        else:
            self._created = true;
