from FlxPoint import FlxPoint
from FlxCore import FlxCore
from FlxArray import FlxArray
from FlxG import *
from FlxAnim import FlxAnim
from Math import Math
import pyglet
from FlxRect import FlxRect
class FlxSprite(FlxCore):
    LEFT= false;
    RIGHT = true;
    
    # #@desc If you changed the size of your sprite object to shrink the bounding box, you might need to offset the new bounding box from the top-left corner of the sprite
    # public var offset:Point;
    # public var self.velocity:Point;
    # public var aself.acceleration:Point;
    # #@desc    This isn't self.drag exactly, more like deceleration that is only applied when aself.acceleration is not affecting the sprite
    # public var self.drag:Point;
    # public var maxself.velocity:Point;
    # #@desc WARNING: rotating sprites decreases rendering performance for this sprite by a factor of 10x!
    # public var self.angle:Number;
    # public var self.angularself.velocity:Number;
    # public var self.angularAself.acceleration:Number;
    # public var self.angularDrag:Number;
    # public var self.maxAngular:Number;
    # #@desc    If you want to do Asteroids style stuff, check out self.thrust (instead of directly accessing the object's self.velocity or aself.acceleration)
    # public var self.thrust:Number;
    # public var maxself.thrust:Number;
    # public var health:Number;
    # #@desc    self.scale doesn't currently affect collisions automatically, you will need to adjust the width, height and offset manually.  WARNING: scaling sprites decreases rendering performance for this sprite by a factor of 10x!
    # public var self.scale:Point;
    
    # #@desc    Whether the current animation has finished its first (or only) loop
    # public var finished:Boolean;
    # private var self._animations:FlxArray;
    # private var _flipped:uint;
    # protected var self._curAnim:FlxAnim;
    # protected var self._curFrame:uint;
    # private var self._frameTimer:Number;
    # private var _callback:Function;
    # private var self._facing:Boolean;
    
    # #helpers
    # private var self._bw:uint;
    # private var self._bh:uint;
    # private var _r:Rectself.angle;
    # private var self._p:Point;
    # private var self._pZero:Point;
    # public var pixels:BitmapData;
    # private var self._pixels:BitmapData;
    # private var self._alpha:Number;
    
    #@desc        Constructor
    #@param    Graphic        The image you want to use
    #@param    X            The initial X position of the sprite
    #@param    Y            The initial Y position of the sprite
    #@param    Animated    Whether the Graphic parameter is a single sprite or a row of sprites
    #@param    Reverse        Whether you need this class to generate horizontally flipped versions of the animation frames
    #@param    Width        If you opt to NOT use an image and want to generate a colored block, or your sprite's frames are not square, you can specify a width here 
    #@param    Height        If you opt to NOT use an image you can specify the height of the colored block here (ignored if Graphic is not null)
    #@param    Color        Specifies the color of the generated block (ignored if Graphic is not null)
    def __init__(self,Graphic=None,X=0,Y=0,Animated=false,Reverse=false,Width=0,Height=0,Color=0):
        
        if(Graphic != None):
            #image = pyglet.resource.image(Graphic)
            self.pixels = Graphic;
            pass
        else:
            self.pixels= pygame.image.load("data/logo.png")
            #pixels = FlxG.createBitmap(Width,Height,Color);
        FlxCore.__init__(self)
        
        #self.position=(X,FlxG.height-Y);
        #self.anchor=(0,0)
        #print dir(self.pixels)
        self.x = X;
        self.y = Y;
        
        if(Width == 0):
            if(Animated):
                Width = self.pixels.height;
            else:
                Width = self.pixels.width;
        self.width =Width 
        self._bw = Width;
        self.height = self.pixels.height;
        self._bh = self.height;
        self.offset = FlxPoint();
        
        self.velocity = FlxPoint();
        self.acceleration = FlxPoint();
        self.drag = FlxPoint();
        self.maxVelocity = FlxPoint(10000,10000);
        
        self.angle = 0;
        self.angularVelocity = 0;
        self.angularAacceleration = 0;
        self.angularDrag = 0;
        self.maxAngular = 10000;
        
        self.thrust = 0;
        
        self.scale = FlxPoint(1,1);
        
        self.finished = false;
        self._facing = true;
        self._animations = FlxArray();
        if(Reverse):
            #pass
            self._flipped = self.pixels.width>>1;
        else:
            self._flipped = 0;
        
        self._curAnim = None;
        self._curFrame = 0;
        self._frameTimer = 0;
        
        self._p = FlxPoint(self.x,self.y);
        self._pZero = FlxPoint();
        self._r = FlxRect(0,0,self._bw,self._bh);
        #self._pixels = BitmapData(width,height);
        #print self._bw,self._bh
        
        #raw_input()
        self._pixels=self.pixels.get_region(0,0,self._bw,self._bh)#,self._pZero);
        
        self.health = 1;
        self._alpha = 1;
        
        self._callback = None;
    
    #@desc        Called by game loop, handles animation and physics
    def update(self):
        self.last.x=self.x
        self.last.y=self.y
        #print "last",self,self.last.x,self.last.y
        FlxCore.update(self);
        
        if(not self.active): 
            return;
        
        #animation
        if((self._curAnim != None) and (self._curAnim.delay > 0) and (self._curAnim.looped or not self.finished)):
            self._frameTimer += FlxG.elapsed;
            #print self._frameTimer,self._curAnim.delay,FlxG.elapsed
            #raw_input()
            if(self._frameTimer > self._curAnim.delay):
                self._frameTimer -= self._curAnim.delay;
                if(self._curFrame == len(self._curAnim.frames)-1):
                    if(self._curAnim.looped):
                        self._curFrame = 0;
                    self.finished = true;
                else:
                    self._curFrame+=1;
                self.calcFrame();
                #print "curframe",self._curFrame
        
        #motion + physics
        self.angularVelocity = FlxG.computeVelocity(self.angularVelocity,self.angularAacceleration,self.angularDrag,self.maxAngular)
        self.angle += (self.angularVelocity)*FlxG.elapsed;
        self.thrustComponents=FlxPoint();
        if(self.thrust != 0):
            self.thrustComponents = FlxG.rotatePoint(-self.thrust,0,0,0,self.angle);
            maxComponents = FlxG.rotatePoint(-maxself.thrust,0,0,0,self.angle);
            maxself.velocity.x = Math.abs(maxComponents.x);
            maxself.velocity.y = Math.abs(maxComponents.y);
        else:
            self.thrustComponents = self._pZero;
        self.velocity.x = FlxG.computeVelocity(self.velocity.x,self.acceleration.x+self.thrustComponents.x,self.drag.x,self.maxVelocity.x)
        self.x += (self.velocity.x)*FlxG.elapsed;
        self.velocity.y = FlxG.computeVelocity(self.velocity.y,self.acceleration.y+self.thrustComponents.y,self.drag.y,self.maxVelocity.y)
        self.y += (self.velocity.y)*FlxG.elapsed;
        #print "x,y",self,self.x,self.y
    #@desc        Called by game loop, blits current frame of animation to the screen (and handles rotation)
    def render(self):
        if(not self.visible):
            return;
        self.getScreenXY(self._p);
        #ma todo
        # if((self.angle != 0) or (self.scale.x != 1) or (self.scale.y != 1)):
            # mtx = Matrix();
            # mtx.translate(-(self._bw>>1),-(self._bh>>1));
            # mtx.self.scale(self.scale.x,self.scale.y);
            # if(self.angle != 0):mtx.rotate(Math.PI * 2 * (self.angle / 360));
            # mtx.translate(self._p.x+(self._bw>>1),self._p.y+(self._bh>>1));
            # FlxG.buffer.draw(self._pixels,mtx);
            # return;
        #print dir(FlxG.buffer)
        #print dir(self._pixels)
        #print self._r,dir(self._r)
        r=FlxRect(self._p.x,self._p.y,self._r.width,self._r.height)
        #FlxG.buffer.blit(self._pixels,r);
        self._pixels.blit(self._p.x,self._p.y)
        #r=Rect(self._p.x,self._p.y,self._r.width,self._r.height)
        #FlxG.buffer.blit(self.pixels,r);
    
    #@desc        Checks to see if a point in 2D space overlaps this FlxCore object
    #@param    X            The X coordinate of the point
    #@param    Y            The Y coordinate of the point
    #@param    PerPixel    Whether or not to use per pixel collision checking
    #@return    Whether or not the point overlaps this object
    def overlapsPoint(self,X,Y,PerPixel = false):
        tx = self.x;
        ty = self.y;
        if((self.scrollFactor.x != 1) or (self.scrollFactor.y != 1)):
            tx -= Math.floor(FlxG.scroll.x*self.scrollFactor.x);
            ty -= Math.floor(FlxG.scroll.y*self.scrollFactor.y);
        if(PerPixel):
            return self._pixels.hitTest(Point(0,0),0xFF,Point(X-tx,Y-ty));
        elif((X <= tx) or (X >= tx+self.width) or (Y <= ty) or (Y >= ty+self.height)):
            return false;
        return true;
    
    #@desc        Called when this object collides with a FlxBlock on one of its sides
    #@return    Whether you wish the FlxBlock to collide with it or not
    def hitWall(self):
        self.velocity.x = 0; 
        return true; 
    
    #@desc        Called when this object collides with the top of a FlxBlock
    #@return    Whether you wish the FlxBlock to collide with it or not
    def hitFloor(self):
        self.velocity.y = 0; 
        return true; 
    
    #@desc        Called when this object collides with the bottom of a FlxBlock
    #@return    Whether you wish the FlxBlock to collide with it or not
    def hitCeiling(self):
        self.velocity.y = 0; 
        return true;
    
    #@desc        Call this function to "damage" (or give health bonus) to this sprite
    #@param    Damage        How much health to take away (use a negative number to give a health bonus)
    def hurt(self,Damage):
        self.health -= Damage
        if(self.health<= 0):
            self.kill();
    
    #@desc        Called if/when this sprite is launched by a FlxEmitter
    def onEmit(self):
        pass
    
    #@desc        Adds a animation to the sprite
    #@param    Name        What this animation should be called (e.g. "run")
    #@param    Frames        An array of numbers indicating what frames to play in what order (e.g. 1, 2, 3)
    #@param    FrameRate    The speed in frames per second that the animation should play at (e.g. 40 fps)
    #@param    Looped        Whether or not the animation is looped or just plays once
    def addAnimation(self,Name, Frames, FrameRate=30, Looped=true):
        self._animations.add(FlxAnim(Name,Frames,FrameRate,Looped));
    
    #@desc        Pass in a function to be called whenever this sprite's animation changes
    #@param    AnimationCallback        A function that has 3 parameters: a string name, a uint frame number, and a uint frame index
    def addAnimationCallback(self,AnimationCallback):
        self._callback = AnimationCallback;
    
    #@desc        Plays an existing animation (e.g. "run") - if you call an animation that is already playing it will be ignored
    #@param    AnimName    The string name of the animation you want to play
    #@param    Force        Whether to force the animation to restart
    def play(self,AnimName,Force=false):
        if(not Force and (self._curAnim != None) and (AnimName == self._curAnim.name)): 
            return;
        self._curFrame = 0;
        self._frameTimer = 0;
        for i in range( len(self._animations)):
            if(self._animations[i].name == AnimName):
                self.finished = false;
                self._curAnim = self._animations[i];
                self.calcFrame();
                return;
    
    #@desc        Tell the sprite which way to face (you can just set 'facing' but this function also updates the animation instantly)
    #@param    Direction        True is Right, False is Left (see static const members RIGHT and LEFT)        
    def setfacing(self,Direction):
        c = self._facing != Direction;
        self._facing = Direction;
        if(c): 
            self.calcFrame();
    
    #@desc        Get the direction the sprite is facing
    #@return    True means facing right, False means facing left (see static const members RIGHT and LEFT)
    def getfacing(self):
        return self._facing;
    
    #@desc        Tell the sprite to change to a random frame of animation (useful for instantiating particles or other weird things)
    def randomFrame(self):
        self._pixels=self.pixels.get_region(Math.floor(Math.random()*(self.pixels.width/self._bw))*self._bw,0,self._bw,self._bh)
    
    #@desc        Tell the sprite to change to a specific frame of animation (useful for instantiating particles)
    #@param    Frame    The frame you want to display
    def specificFrame(self,Frame):
        self._pixels=self.pixels.get_region(Frame*self._bw,0,self._bw,self._bh);
    
    #@desc        Call this function to figure out the post-scrolling "screen" position of the object
    #@param    P    Takes a Flash Point object and assigns the post-scrolled X and Y values of this object to it
    def getScreenXY(self,P):
        P.x = Math.floor(self.x-self.offset.x)+Math.floor(FlxG.scroll.x*self.scrollFactor.x);
        P.y = Math.floor(self.y-self.offset.y)+Math.floor(FlxG.scroll.y*self.scrollFactor.y);
    
    #@desc        Internal function to update the current animation frame
    def calcFrame(self):
        if(self._curAnim == None):
            self._pixels=self.pixels.get_region(self._r.x,self._r.y,self._r.width,self._r.height)#,self._pZero);
        else:
            rx = self._curAnim.frames[self._curFrame]*self._bw;
            if(not self._facing and (self._flipped > 0)):
                rx = (self._flipped<<1)-rx-self._bw;
            #print rx,self._bw,self._bh;
            #raw_input()
            self._pixels=self.pixels.get_region(rx,0,self._bw,self._bh)
        #if(self._alpha != 1): self._pixels.colorTransform(_r,ColorTransform(1,1,1,self._alpha));
        if(self._callback != None): 
            self._callback(self._curAnim.name,self._curFrame,self._curAnim.frames[self._curFrame]);
    
    #@desc        The setter for alpha
    #@param    Alpha    The opacity value of the sprite (between 0 and 1)
    def setalpha(self,Alpha):
        if(Alpha > 1): 
            Alpha = 1;
        if(Alpha < 0):
            Alpha = 0;
        self._alpha = Alpha;
        self.calcFrame();
    
    #@desc        The getter for alpha
    #@return    The value of this sprite's opacity
    def getalpha(self):
        return self._alpha;
