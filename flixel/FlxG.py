from FlxPoint import FlxPoint
from FlxArray import FlxArray
true=1
false=0
class FlxG:
    #@desc Represents the amount of time in seconds that passed since last frame
    elapsed=0.0;
    #@desc A reference or pointer to the current FlxFlxG.state object being used by the game
    state=None;
    width=0;
    height=0;
    level=0;
    levels=FlxArray();
    score=0;
    scores=FlxArray();
    
    #@desc These are the constants for use with the Pressed and Releases functions
    LEFT = 0;
    #@desc These are the constants for use with the Pressed and Releases functions
    RIGHT = 1;
    #@desc These are the constants for use with the Pressed and Releases functions
    UP = 2;
    #@desc These are the constants for use with the Pressed and Releases functions
    DOWN = 3;
    #@desc These are the constants for use with the Pressed and Releases functions
    A = 4;
    #@desc These are the constants for use with the Pressed and Releases functions
    B = 5;
    #@desc These are the constants for use with the Pressed and Releases functions
    MOUSE = 6;
    
    #@desc A shortcut way of checking if a particular key is pressed
    kUp=false;
    #@desc A shortcut way of checking if a particular key is pressed
    kDown=false;
    #@desc A shortcut way of checking if a particular key is pressed
    kLeft=false;
    #@desc A shortcut way of checking if a particular key is pressed
    kRight=false;
    #@desc A shortcut way of checking if a particular key is pressed
    kA=false;
    #@desc A shortcut way of checking if a particular key is pressed
    kB=false;
    #@desc A shortcut way of checking if a particular key is pressed
    kMouse=false;
    #@desc The current game coordinates of the mouse pointer (not necessarily the screen coordinates)
    # mouse=FlxPoint();
    _keys=[];
    _oldKeys=[];
    
    # #audio
    # _muted;
    # _music:Sound;
    _musicChannel=None;
    _musicPosition=None
    # _volume;
    # _musicVolume;
    # _masterVolume;
    
    # #Ccmera system variables
    followTarget=None;
    followLead=FlxPoint();
    followLerp=1;
    followMin=FlxPoint();
    followMax=FlxPoint();
    _scrollTarget=FlxPoint();
    
    # #graphics stuff
    scroll=FlxPoint();
    # buffer:BitmapData;
    _cache={};
    
    # #function reflectors
    # _quake;
    # _flash;
    # _fade;
    # _switchFlxG.state;
    # _log;
    # _setCursor;
    
    #@desc        Resets the key register and shortcut booleans to "off"
    @staticmethod 
    def resetKeys():
        kUp = kDown = kLeft = kRight = kA = kB = kMouse = false;
        for i in range(len( FlxG._keys)):
            FlxG._keys[i] = 0;
    
    #@desc        Check to see if this key is pressed
    #@param    Key        One of the key constants listed above (e.g. LEFT or A)
    #@return    Whether the key is pressed
    @staticmethod 
    def pressed(Key): 
        return FlxG._keys[Key] > 0
    
    #@desc        Check to see if this key was JUST pressed
    #@param    Key        One of the key constants listed above (e.g. LEFT or A)
    #@return    Whether the key was just pressed
    @staticmethod 
    def justPressed(Key):  
        return FlxG._keys[Key] == 2
    
    #@desc        Check to see if this key is NOT pressed
    #@param    Key        One of the key constants listed above (e.g. LEFT or A)
    #@return    Whether the key is not pressed
    @staticmethod 
    def justReleased(Key): 
        return FlxG._keys[Key] == -1
    
    #@desc        Set up and autoplay a music track
    #@param    Music        The sound file you want to loop in the background
    #@param    Volume        How loud the sound should be, from 0 to 1
    #@param    Autoplay    Whether to automatically start the music or not (defaults to true)
    @staticmethod 
    def setMusic(Music,Volume=1,Autoplay=true):
        FlxG.stopMusic();
        FlxG._music = Music;
        FlxG._musicVolume = Volume;
        if(Autoplay):
            FlxG.playMusic();
    
    #@desc        Plays a sound effect once
    #@param    SoundEffect        The sound you want to play
    #@param    Volume            How loud to play it (0 to 1)
    @staticmethod 
    def play(SoundEffect,Volume=1):
        SoundEffect().play(0,0,SoundTransform(Volume*_muted*_volume*_masterVolume));
    
    #@desc        Plays or resumes the music file set up using setMusic()
    @staticmethod 
    def playMusic():
        if(FlxG._musicPosition < 0):
            return;
        if(FlxG._musicPosition == 0):
            if(FlxG._musicChannel == None): 
                FlxG._musicChannel = _music.play(0,9999,SoundTransform(_muted*_volume*_musicVolume*_masterVolume));
        else:
            FlxG._musicChannel = _music.play(FlxG._musicPosition,0,SoundTransform(_muted*_volume*_musicVolume*_masterVolume));
            FlxG._musicChannel.addEventListener(Event.SOUND_COMPLETE, loopMusic);
        FlxG._musicPosition = 0;
    
    #@desc        An internal helper function used to help Flash resume playing a looped music track
    @staticmethod 
    def loopMusic(event=None):
        if (FlxG._musicChannel == None):
            return;
        FlxG._musicChannel.removeEventListener(Event.SOUND_COMPLETE,loopMusic);
        FlxG._musicChannel = None;
        playMusic();
    
    #@desc        Pauses the current music track
    @staticmethod 
    def pauseMusic():
        if(FlxG._musicChannel == None):
            FlxG._musicPosition = -1;
            return;
        FlxG._musicPosition = FlxG._musicChannel.position;
        FlxG._musicChannel.stop();
        while(FlxG._musicPosition >= _music.length):
            FlxG._musicPosition -= _music.length;
        FlxG._musicChannel = None;
    
    #@desc        Stops the current music track
    @staticmethod 
    def stopMusic():
        FlxG._musicPosition = 0;
        if(FlxG._musicChannel  <> None):
            FlxG._musicChannel.stop();
            FlxG._musicChannel = None;
    
    #@desc        Mutes the sound
    #@param    SoundOff    Whether the sound should be off or on
    @staticmethod 
    def setMute(SoundOff): 
        if(SoundOff):
            _muted = 0; 
        else: 
            _muted = 1; 
        adjustMusicVolume()
    
    #@desc        Check to see if the game is muted
    #@return    Whether the game is muted
    @staticmethod 
    def getMute():  
        if(_muted == 0): 
            return true; 
        return false
    
    #@desc        Change the volume of the game
    #@param    Volume        A number from 0 to 1
    @staticmethod 
    def setVolume(Volume): 
        _volume = Volume; 
        adjustMusicVolume(); 
    
    #@desc        Find out how load the game is currently
    #@param    A number from 0 to 1
    @staticmethod 
    def getVolume():  
        return _volume; 
    
    #@desc        Change the volume of just the music
    #@param    Volume        A number from 0 to 1
    @staticmethod 
    def setMusicVolume(Volume): 
        _musicVolume = Volume; 
        adjustMusicVolume(); 
    
    #@desc        Find out how loud the music is
    #@return    A number from 0 to 1
    @staticmethod 
    def getMusicVolume(): 
        return _musicVolume
    
    #@desc        An internal function that adjust the volume levels and the music channel after a change
    @staticmethod
    def adjustMusicVolume():
        if(_muted < 0):
            _muted = 0;
        elif(_muted > 1):
            _muted = 1;
        if(_volume < 0):
            _volume = 0;
        elif(_volume > 1):
            _volume = 1;
        if(_musicVolume < 0):
            _musicVolume = 0;
        elif(_musicVolume > 1):
            _musicVolume = 1;
        if(_masterVolume < 0):
            _masterVolume = 0;
        elif(_masterVolume > 1):
            _masterVolume = 1;
        if(FlxG._musicChannel  <> None):
            FlxG._musicChannel.soundTransform = SoundTransform(_muted*_volume*_musicVolume*_masterVolume);
    
    #@desc        Generates a BitmapData object (basically a colored square :P) and caches it
    #@param    FlxG.width    How wide the square should be
    #@param    FlxG.height    How high the square should be
    #@param    Color    What color the square should be
    #@return    This object is used during the sprite blitting process
    @staticmethod 
    def createBitmap(width, height, Color):
        key = str(width)+"x"+str(height)+":"+str(Color);
        if(FlxG._cache.get(key) == None):
            FlxG._cache[key] =BitmapData(width,height,true,Color);
        return FlxG._cache[key];
    
    #@desc        Loads a bitmap from a file, caches it, and generates a horizontally flipped version if necessary
    #@param    Graphic        The image file that you want to load
    #@param    Reverse        Whether to generate a flipped version
    @staticmethod 
    def addBitmap(Graphic,Reverse=false):
        needReverse = false;
        key = str(Graphic);
        print Graphic
        if(FlxG._cache.get(key) == None):
            FlxG._cache[key] = Graphic().bitmapData;
            if(Reverse):
                needReverse = true;
        pixels= FlxG._cache[key];
        if( not needReverse and Reverse and (pixels.width == (Graphic).bitmapData.width)):
            needReverse = true;
        if(needReverse):
            newPixels=BitmapData(pixels.width<<1,pixels.height,true,0x00000000);
            newPixels.draw(pixels);
            mtx =Matrix();
            mtx.scale(-1,1);
            mtx.translate(newPixels.width,0);
            newPixels.draw(pixels,mtx);
            pixels = newPixels;
        return pixels;
    
    #@desc        Rotates a point in 2D space around another point by the given angle
    #@param    X        The X coordinate of the point you want to rotate
    #@param    Y        The Y coordinate of the point you want to rotate
    #@param    PivotX    The X coordinate of the point you want to rotate around
    #@param    PivotY    The Y coordinate of the point you want to rotate around
    #@param    Angle    Rotate the point by this many degrees
    #@return    A Flash Point object containing the coordinates of the rotated point
    @staticmethod 
    def rotatePoint(X, Y, PivotX, PivotY, Angle):
        radians = -Angle / 180 * math.PI;
        dx = X-PivotX;
        dy = PivotY-Y;
        return Point(PivotX + math.cos(radians)*dx - math.sin(radians)*dy, PivotY - (math.sin(radians)*dx + math.cos(radians)*dy));

    
    #@desc        Calculates the angle between a point and the origin (0,0)
    #@param    X        The X coordinate of the point
    #@param    Y        The Y coordinate of the point
    #@return    The angle in degrees
    @staticmethod 
    def getAngle(X, Y):
        return math.atan2(Y,X) * 180 / math.PI;

    #@desc        Tells the camera subsystem what FlxCore object to follow
    #@param    Target        The object to follow
    #@param    Lerp        How much lag the camera should have (can help smooth out the camera movement)
    @staticmethod 
    def follow(Target, Lerp=1):
        FlxG.followTarget = Target;
        FlxG.followLerp = Lerp;
        FlxG._scrollTarget.x = (FlxG.width>>1)-FlxG.followTarget.x-(FlxG.followTarget.width>>1);
        FlxG.scroll.x = FlxG._scrollTarget.x
        FlxG._scrollTarget.y = (FlxG.height>>1)-FlxG.followTarget.y-(FlxG.followTarget.height>>1);
        FlxG.scroll.y = FlxG._scrollTarget.y
    
    #@desc        Specify an additional camera component - the velocity-based "lead", or amount the camera should track in front of a sprite
    #@param    LeadX        Percentage of X velocity to add to the camera's motion
    #@param    LeadY        Percentage of Y velocity to add to the camera's motion
    @staticmethod 
    def followAdjust(LeadX = 0, LeadY = 0):
        FlxG.followLead = FlxPoint(LeadX,LeadY);
    
    #@desc        Specify an additional camera component - the boundaries of the level or where the camera is allowed to move
    #@param    MinX    The smallest X value of your level (usually 0)
    #@param    MinY    The smallest Y value of your level (usually 0)
    #@param    MaxX    The largest X value of your level (usually the level FlxG.width)
    #@param    MaxY    The largest Y value of your level (usually the level FlxG.height)
    @staticmethod 
    def followBounds(MinX=0, MinY=0, MaxX=0, MaxY=0):
        FlxG.followMin = FlxPoint(-MinX,-MinY);
        FlxG.followMax = FlxPoint(-MaxX+FlxG.width,-MaxY+FlxG.height);
        if(FlxG.followMax.x > FlxG.followMin.x):
            FlxG.followMax.x = FlxG.followMin.x;
        if(FlxG.followMax.y > FlxG.followMin.y):
            FlxG.followMax.y = FlxG.followMin.y;
    
    #@desc        A fairly stupid tween-like function that takes a starting velocity and some other factors and returns an altered velocity
    #@param    Velocity        Any component of velocity (e.g. 20)
    #@param    Acceleration    Rate at which the velocity is changing
    #@param    Drag            Really kind of a deceleration, this is how much the velocity changes if Acceleration is not set
    #@param    Max                An absolute value cap for the velocity
    @staticmethod 
    def computeVelocity(Velocity, Acceleration=0, Drag=0, Max=10000):
        if(Acceleration  <> 0):
            Velocity += Acceleration*FlxG.elapsed;
        elif(Drag  <> 0):
            d = Drag*FlxG.elapsed;
            if(Velocity - d > 0):
                Velocity -= d;
            elif(Velocity + d < 0):
                Velocity += d;
            else:
                Velocity = 0;
        if((Velocity  <> 0) and (Max  <> 10000)):
            if(Velocity > Max):
                Velocity = Max;
            elif(Velocity < -Max):
                Velocity = -Max;
        return Velocity;
    
    #@desc        Checks to see if a FlxCore overlaps any of the FlxCores in the array, and calls a function when they do
    #@param    Array        An array of FlxCore objects
    #@param    Core        A FlxCore object
    #@param    Collide        A function that takes two sprites as parameters (first the one from Array, then Sprite)
    @staticmethod 
    def overlapArray(Array,Core,Collide):
        if((Core == None) or  not Core.exists or Core.dead): 
            return;
        for i in range(len( Array)):
            c = Array[i];
            if((c == Core) or (c == None) or  not c.exists or c.dead): 
                continue;
            if(c.overlaps(Core)): 
                Collide(c,Core);
    
    #@desc        Checks to see if any FlxCore in Array1 overlaps any FlxCore in Array2, and calls Collide when they do
    #@param    Array1        An array of FlxCore objects
    #@param    Array2        Another array of FlxCore objects
    #@param    Collide        A function that takes two FlxCore objects as parameters (first the one from Array1, then the one from Array2)
    @staticmethod 
    def overlapArrays(Array1,Array2,Collide):
        if(Array1 == Array2):
            for i in range(len( Array1)):
                core1 = Array1[i];
                if((core1 == None) or  not core1.exists or core1.dead): 
                    continue;
                j = i+1;
                while( j < Array2.length):
                    core2 = Array2[j];
                    if((core2 == None) or  not core2.exists or core2.dead): 
                        continue;
                    if(core1.overlaps(core2)): 
                        Collide(core1,core2);
                    j+=1;
        else:
            for i in range(len( Array1)):
                core1 = Array1[i];
                if((core1 == None) or  not core1.exists or core1.dead): 
                    continue;
                for j in range(len( Array2)):
                    core2 = Array2[j];
                    if((core1 == core2) or (core2 == None) or  not core2.exists or core2.dead): 
                        continue;
                    if(core1.overlaps(core2)): 
                        Collide(core1,core2);
    
    #@desc        Collides a FlxSprite against the FlxCores in the array 
    #@param    Array        An array of FlxCore objects
    #@param    Sprite        A FlxSprite object
    @staticmethod 
    def collideArray(Cores,Sprite):
        #print "collideArray"
        if((Sprite == None) or  not Sprite.exists or Sprite.dead): 
            return;
        for i in range(len( Cores)):
            core = Cores[i];
            if((core == Sprite) or (core == None) or  not core.exists or core.dead): 
                continue;
            core.collide(Sprite);
    
    #@desc        Collides an array of FlxSprites against a FlxCore object
    #@param    Sprites        An array of FlxSprites
    #@param    Core        A FlxCore object
    @staticmethod 
    def collideArray2(Core,Sprites):
        if((Core == None) or  not Core.exists or Core.dead):
            return;
        for  i in range(len(Sprites)):
            sprite = Sprites[i];
            if((Core == sprite) or (sprite == None) or  (not sprite.exists) or sprite.dead):
                continue;
            Core.collide(sprite);
    
    #@desc        Collides the array of FlxSprites against the array of FlxCores
    #@param    Cores        An array of FlxCore objects
    #@param    Sprites        An array of FlxSprite objects
    @staticmethod 
    def collideArrays(Cores,Sprites):
        if(Cores == Sprites):
            for i in range(len(Cores)):
                core = Cores[i];
                if((core == None) or  not core.exists or core.dead): 
                    continue;
                j=i+1;
                while( j < Sprites.length):
                    sprite = Sprites[j];
                    if((sprite == None) or  not sprite.exists or sprite.dead):
                        continue;
                    core.collide(sprite);
                    j+=1;
        else:
             for i in range(len(Cores)):
                core = Cores[i];
                if((core == None) or  not core.exists or core.dead): 
                    continue;
                for j in range(len(Sprites)):
                    sprite = Sprites[j];
                    if((core == sprite) or (sprite == None) or  not sprite.exists or sprite.dead): 
                        continue;
                    core.collide(sprite);
    
    #@desc        Switch from one FlxFlxG.state to another
    #@param    FlxG.state        The class name of the FlxG.state you want (e.g. PlayFlxG.state)
    @staticmethod 
    def switchState(state):  
        FlxG._switchState(state); 
    
    #@desc        Log data to the developer console
    #@param    Data        The data (in string format) that you wanted to write to the console
    @staticmethod 
    def log(Data): 
        FlxG._log(Data); 
    
    #@desc        Shake the screen
    #@param    Intensity    Percentage of screen size representing the maximum distance that the screen can move during the 'quake'
    #@param    Duration    The length in seconds that the "quake" should last
    @staticmethod 
    def quake(Intensity,Duration=0.5): 
        pass
        #FlxG._quake(Intensity,Duration)
    
    #@desc        Temporarily fill the screen with a certain color, then fade it out
    #@param    Color            The color you want to use
    #@param    Duration        How long it takes for the flash to fade
    #@param    FlashComplete    A function you want to run when the flash finishes
    #@param    Force            Force the effect to reset
    @staticmethod 
    def flash(Color, Duration=1, FlashComplete=None, Force=false): 
        pass
        #FlxG._flash(Color,Duration,FlashComplete,Force); 
    
    #@desc        Fade the screen out to this color
    #@param    Color            The color you want to use
    #@param    Duration        How long it should take to fade the screen out
    #@param    FadeComplete    A function you want to run when the fade finishes
    #@param    Force            Force the effect to reset
    @staticmethod 
    def fade(Color, Duration=1, FadeComplete=None, Force=false): 
        pass
        #_fade(Color,Duration,FadeComplete,Force)
    
    #@desc        Set the mouse cursor to some graphic file
    #@param    CursorGraphic    The image you want to use for the cursor
    @staticmethod 
    def setCursor(CursorGraphic): 
        _setCursor(CursorGraphic); 
    
    #@desc        Switch to a different web page
    @staticmethod 
    def openURL(URL):
        navigateToURL(URLRequest(URL));

    #@desc        This function is only used by the FlxGame class to do important internal management stuff
    @staticmethod 
    def setGameData(w,h,Switchstate=None,Log=None,Quake=None,Flash=None,Fade=None,SetCursor=None):
        FlxG._cache = {};
        FlxG.width = w;
        FlxG.height = h;
        _muted = 1.0;
        _volume = 1.0;
        _musicVolume = 1.0;
        _masterVolume = 0.5;
        FlxG._musicPosition = -1;
        mouse = FlxPoint();
        FlxG._switchState = Switchstate;
        FlxG._log = Log;
        _quake = Quake;
        _flash = Flash;
        _fade = Fade;
        _setCursor = SetCursor;
        FlxG.unfollow();
        FlxG._keys = [];
        FlxG._oldKeys = [];
        for i in range(7):
            FlxG._keys.append(0);
            FlxG._oldKeys.append(0);
        FlxG.levels = FlxArray();
        FlxG.scores = FlxArray();
        level = 0;
        score = 0;
    
    #@desc        This function is only used by the FlxGame class to do important internal management stuff
    @staticmethod 
    def setMasterVolume(Volume): 
        FlxG._masterVolume = Volume; 
        FlxG.adjustMusicVolume(); 
    
    #@desc        This function is only used by the FlxGame class to do important internal management stuff
    @staticmethod 
    def getMasterVolume():
        return FlxG._masterVolume;
    
    #@desc        This function is only used by the FlxGame class to do important internal management stuff
    @staticmethod 
    def doFollow():
        from FlxSprite import FlxSprite
        if(FlxG.followTarget  <> None):
            if(FlxG.followTarget.exists and  not FlxG.followTarget.dead):
                FlxG._scrollTarget.x = (FlxG.width>>1)-FlxG.followTarget.x-(FlxG.followTarget.width>>1);
                FlxG._scrollTarget.y = (FlxG.height>>1)-FlxG.followTarget.y-(FlxG.followTarget.height>>1);
                if((FlxG.followLead  <> None) and (type(FlxG.followTarget)==FlxSprite)):
                    FlxG._scrollTarget.x -= (FlxG.followTarget).velocity.x*FlxG.followLead.x;
                    FlxG._scrollTarget.y -= (FlxG.followTarget).velocity.y*FlxG.followLead.y;
            FlxG.scroll.x += (FlxG._scrollTarget.x-FlxG.scroll.x)*FlxG.followLerp*FlxG.elapsed;
            FlxG.scroll.y += (FlxG._scrollTarget.y-FlxG.scroll.y)*FlxG.followLerp*FlxG.elapsed;
            
            if(FlxG.followMin  <> None):
                if(FlxG.scroll.x > FlxG.followMin.x):
                    FlxG.scroll.x = FlxG.followMin.x;
                if(FlxG.scroll.y > FlxG.followMin.y):
                    FlxG.scroll.y = FlxG.followMin.y;
            
            if(FlxG.followMax  <> None):
                if(FlxG.scroll.x < FlxG.followMax.x):
                    FlxG.scroll.x = FlxG.followMax.x;
                if(FlxG.scroll.y < FlxG.followMax.y):
                    FlxG.scroll.y = FlxG.followMax.y;
    
    #@desc        This function is only used by the FlxGame class to do important internal management stuff
    @staticmethod 
    def unfollow():
        FlxG.followTarget = None;
        FlxG.followLead = None;
        FlxG.followLerp = 1;
        FlxG.followMin = None;
        FlxG.followMax = None;
        FlxG.scroll = FlxPoint();
        FlxG._scrollTarget = FlxPoint();
    
    #@desc        This function is only used by the FlxGame class to do important internal management stuff
    @staticmethod 
    def pressKey(k):
        if(FlxG._keys[k] > 0):
            FlxG._keys[k] = 1;
        else:
            FlxG._keys[k] = 2;
    
    #@desc        This function is only used by the FlxGame class to do important internal management stuff
    @staticmethod 
    def releaseKey(k):
        if(FlxG._keys[k] > 0):
            FlxG._keys[k] = -1;
        else:
            FlxG._keys[k] = 0;
    
    #@desc        This function is only used by the FlxGame class to do important internal management stuff
    @staticmethod 
    def updateKeys():
        for i in range(7):
            if((FlxG._oldKeys[i] == -1) and (FlxG._keys[i] == -1)):
                FlxG._keys[i] = 0;
            elif((FlxG._oldKeys[i] == 2) and (FlxG._keys[i] == 2)):
                FlxG._keys[i] = 1;
            FlxG._oldKeys[i] = FlxG._keys[i];
        # mouse.x = FlxG.state.mouseX-FlxG.scroll.x;
        # mouse.y = FlxG.state.mouseY-FlxG.scroll.y;
