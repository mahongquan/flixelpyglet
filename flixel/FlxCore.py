#@desc        This is the base class for most of the display objects (FlxSprite, FlxText, etc).  It includes some very simple basic attributes about game objects.
from FlxPoint import FlxPoint
from Math import Math
from FlxG import *
from FlxRect import FlxRect
class FlxCore:
    LEFT= 0x0001;
    RIGHT    = 0x0010
    UP= 0x0100;
    DOWN    = 0x1000;
    NONE    = 0;
    CEILING= UP;
    FLOOR    = DOWN;
    WALL    = LEFT | RIGHT;
    ANY    = LEFT | RIGHT | UP | DOWN;
    OVERLAP_BIAS= 4;
    #@desc    Kind of a global on/off switch for any objects descended from FlxCore
    # self.exists=1;
    # #@desc    If an object is not alive, the game loop will not automatically call FlxCore.UPdate() on it
    # self.active=1;
    # #@desc    If an object is not self.visible, the game loop will not automatically call render() on it
    # self.visible=1;
    # #@desc    If an object is self.dead, the functions that automate collisions will skip it (see overlapArrays in FlxSprite and collideArrays in FlxBlock)
    # self.dead=0;
    
    # #Basic attributes variables
    # self.x=0.0;
    # self.y=0.0;
    # self.width=0;
    # self.height=0;
    
    # #@desc    A point that can store numbers from 0 to 1 (for self.x and self.y independently) that governs how much this object is affected by the camera subsystem.  0 means it never moves, like a HUD element or far background graphic.  1 means it scrolls along a tthe same speed as the foreground layer.
    # self.scrollFactor=FlxPoint();
    # self._flicker=0;
    # self._flickerTimer=0.0;
    #@desc        Constructor
    def __init__(self):
        self.mass = 1.0;self.elasticity = 0.0;self.moves = true;
        self.touching=FlxCore.NONE;
        self.allowCollisions=FlxCore.ANY;
        self.immovable=false;
        self.exists = true;
        self.active = true;
        self.visible = true;
        self.dead = false;
        
        self.x = 0;
        self.y = 0;
        self.last=FlxPoint(self.x,self.y);
        self.width = 0;
        self.height = 0;
        
        self.scrollFactor = FlxPoint(1,1);
        self._flicker = false;
        self._flickerTimer = -1;
    #@desc        Just FlxCore.UPdates the flickering.  FlxSprite and other subclasses override this to do more complicated behavior.
    def update(self):
        if(self.flickering()):
            if(self._flickerTimer > 0):
                self._flickerTimer -= FlxG.elapsed;
            if(self._flickerTimer < 0):
                flicker(-1);
            else:
                self._flicker = not self._flicker;
                self.visible = not self._flicker;
    
    #@desc        FlxSprite and other subclasses override this to render their materials to the screen
    def render(self):
        pass
    
    #@desc        Checks to see if some FlxCore object overlaps this FlxCore object
    #@param    Core    The object being tested
    #@return    Whether or not the two objects overlap
    def overlaps(self,Core):
        tx= self.x;
        ty= self.y;
        if((self.scrollFactor.x  <> 1) or (self.scrollFactor.y  <> 1)):
            tx -= Math.floor(FlxG.scroll.x*self.scrollFactor.x);
            ty -= Math.floor(FlxG.scroll.y*self.scrollFactor.y);
        cx = Core.x;
        cy = Core.y;
        if((Core.scrollFactor.x  <> 1) or (Core.scrollFactor.y  <> 1)):
            cx -= Math.floor(FlxG.scroll.x*Core.scrollFactor.x);
            cy -= Math.floor(FlxG.scroll.y*Core.scrollFactor.y);
        if((cx <= tx-Core.width) or (cx >= tx+self.width) or (cy <= ty-Core.height) or (cy >= ty+self.height)):
            return false;
        return true;
    
    #@desc        Checks to see if a point in 2D space overlaps this FlxCore object
    #@param    self.x            The self.x coordinate of the point
    #@param    self.y            The self.y coordinate of the point
    #@param    PerPixel    Whether or not to use per pixel collision checking (only available in FlxSprite subclass, included here because of Flash's F'd FlxCore.UP lack of polymorphism)
    #@return    Whether or not the point overlaps this object
    def overlapsPoint(self,x,y,PerPixel = false):
        tx = x;
        ty = y;
        if((self.scrollFactor.x  <> 1) or (self.scrollFactor.y  <> 1)):
            tx -= Math.floor(FlxG.scroll.x*self.scrollFactor.x);
            ty -= Math.floor(FlxG.scroll.y*self.scrollFactor.y);
        if((self.x < tx+1) or (self.x+1 > tx+self.width) or (self.y < ty+1) or (self.y+1 > ty+self.height)):
            return false;
        return true;
    
    #@desc        Collides a FlxSprite against this block
    #@param    Spr        The FlxSprite you want to collide
    def old_collide(self,Spr):
        #x y not chongdie
        #print "=",self.x,self.y,self.width,self.height,"collide",Spr.x,Spr.y,Spr.width,Spr.height
        if((Math.abs(Spr.x + (Spr.width>>1) - self.x - (self.width>>1)) > (self.width>>1) + (Spr.width>>1)) and (Math.abs(Spr.y + (Spr.height>>1) - self.y - (self.height>>1)) > (self.height>>1) + (Spr.height>>1))):
            return;
        #print FlxG.elapsed,":",self.x,self.y,self.width,self.height,"collide",Spr.x,Spr.y,Spr.width,Spr.height
        yFirst= true;
        if((Math.abs(Spr.velocity.x) > Math.abs(Spr.velocity.y))):
            yFirst = false;
            #print "yfirst=false",Spr.y
        else:
            #print "yfirst=true",Spr.y
            pass
        
        checkForMoreX = false;
        checkForMoreY = false;
        if(yFirst):
            if(Spr.velocity.y > 0):
                #print "velocity.y>0"
                if(self.overlapsPoint(Spr.x + (Spr.width>>1),Spr.y + Spr.height)):
                    if(Spr.hitFloor()):
                        Spr.y = self.y - Spr.height;
                else:
                    checkForMoreY = true;
            elif(Spr.velocity.y < 0):
                #print "velocity.y<0"
                if(self.overlapsPoint(Spr.x + (Spr.width>>1),Spr.y)):
                    if(Spr.hitCeiling()):
                        Spr.y = self.y + self.height;
                else:
                    checkForMoreY = true;

            if(Spr.velocity.x < 0):
                #print "velocity.x<0",self.x,self.y,self.width,self.height,Spr.x,Spr.y,Spr.width,Spr.height
                if(self.overlapsPoint(Spr.x,Spr.y + (Spr.height>>1))):
                    if(Spr.hitWall()):
                        #print "hitwall"
                        Spr.x = self.x + self.width;
                else:
                    #print "check more x"
                    checkForMoreX = true;
            elif(Spr.velocity.x > 0):
                #print "velocity.x>0"
                if(self.overlapsPoint(Spr.x + Spr.width,Spr.y + (Spr.height>>1))):
                    if(Spr.hitWall()):
                        Spr.x = self.x - Spr.width;
                else:
                    checkForMoreX = true;
        else:
            if(Spr.velocity.x < 0):
                if(self.overlapsPoint(Spr.x,Spr.y + (Spr.height>>1))):
                    if(Spr.hitWall()):
                        Spr.x = self.x + self.width;
                else:
                    checkForMoreX = true;
            elif(Spr.velocity.x > 0):
                if(self.overlapsPoint(Spr.x + Spr.width,Spr.y + (Spr.height>>1))):
                    if(Spr.hitWall()):
                        Spr.x = self.x - Spr.width;
                else:
                    checkForMoreX = true;
           
            if(Spr.velocity.y > 0):
                if(self.overlapsPoint(Spr.x + (Spr.width>>1),Spr.y + Spr.height)):
                    if(Spr.hitFloor()):
                        Spr.y = self.y - Spr.height;
                else:
                    checkForMoreY = true;
            elif(Spr.velocity.y < 0):
                if(self.overlapsPoint(Spr.x + (Spr.width>>1),Spr.y)):
                    if(Spr.hitCeiling()):
                        Spr.y = self.y + self.height;
                else:
                    checkForMoreY = true;
        
        if( not checkForMoreY and  not checkForMoreX):
            return;
        bias = Spr.width>>3;
        if(bias < 1):
            bias = 1;
        if(checkForMoreY and checkForMoreX):
            #print "check more y and x",Spr.y
            if(yFirst):
                if(checkForMoreY):
                    if((Spr.x + Spr.width - bias > self.x) and (Spr.x + bias < self.x + self.width)):
                        if((Spr.velocity.y > 0) and (Spr.y + Spr.height > self.y) and (Spr.y + Spr.height < self.y + self.height) and Spr.hitFloor()):
                            Spr.y = self.y - Spr.height;
                        elif((Spr.velocity.y < 0) and (Spr.y > self.y) and (Spr.y < self.y + self.height) and Spr.hitCeiling()):
                            Spr.y = self.y + self.height;
                if(checkForMoreX):
                    if((Spr.y + Spr.height - bias > self.y) and (Spr.y + bias < self.y + self.height)):
                        if((Spr.velocity.x > 0) and (Spr.x + Spr.width > self.x) and (Spr.x + Spr.width < self.x + self.width) and Spr.hitWall()):
                            Spr.x = self.x - Spr.width;
                        elif((Spr.velocity.x < 0) and (Spr.x > self.x) and (Spr.x < self.x + self.width) and Spr.hitWall()):
                            Spr.x = self.x + self.width;
            else:
                if(checkForMoreX):
                    if((Spr.y + Spr.height - bias > self.y) and (Spr.y + bias < self.y + self.height)):
                        if((Spr.velocity.x > 0) and (Spr.x + Spr.width > self.x) and (Spr.x + Spr.width < self.x + self.width) and Spr.hitWall()):
                            Spr.x = self.x - Spr.width;
                        elif((Spr.velocity.x < 0) and (Spr.x > self.x) and (Spr.x < self.x + self.width) and Spr.hitWall()):
                            Spr.x = self.x + self.width;
                if(checkForMoreY):
                    if((Spr.x + Spr.width - bias > self.x) and (Spr.x + bias < self.x + self.width)):
                        if((Spr.velocity.y > 0) and (Spr.y + Spr.height > self.y) and (Spr.y + Spr.height < self.y + self.height) and Spr.hitFloor()):
                            Spr.y = self.y - Spr.height;
                        elif((Spr.velocity.y < 0) and (Spr.y > self.y) and (Spr.y < self.y + self.height) and Spr.hitCeiling()):
                            Spr.y = self.y + self.height;
        elif(checkForMoreY):
            #print "check more y",Spr.y
            if((Spr.x + Spr.width - bias > self.x) and (Spr.x + bias < self.x + self.width)):
                if((Spr.velocity.y > 0) and (Spr.y + Spr.height > self.y) and (Spr.y + Spr.height < self.y + self.height) and Spr.hitFloor()):
                    Spr.y = self.y - Spr.height;
                elif((Spr.velocity.y < 0) and (Spr.y > self.y) and (Spr.y < self.y + self.height) and Spr.hitCeiling()):
                    Spr.y = self.y + self.height;
        elif(checkForMoreX):
            if((Spr.y + Spr.height - bias > self.y) and (Spr.y + bias < self.y + self.height)):
                if((Spr.velocity.x > 0) and (Spr.x + Spr.width > self.x) and (Spr.x + Spr.width < self.x + self.width) and Spr.hitWall()):
                    Spr.x = self.x - Spr.width;
                elif((Spr.velocity.x < 0) and (Spr.x > self.x) and (Spr.x < self.x + self.width) and Spr.hitWall()):
                    Spr.x = self.x + self.width;
        #print "=================",Spr.y
    #@desc        Called when this object collides with a FlxBlock on one of its sides
    #@return    Whether you wish the FlxBlock to collide with it or not
    def hitWall(self):
        return true
    
    #@desc        Called when this object collides with the top of a FlxBlock
    #@return    Whether you wish the FlxBlock to collide with it or not
    def hitFloor(self):
        return touching & FlxCore.UP
        return true    
    #@desc        Called when this object collides with the bottom of a FlxBlock
    #@return    Whether you wish the FlxBlock to collide with it or not
    def hitCeiling(self):
        return touching & FlxCore.DOWN
        return true; 
    
    #@desc        Call this function to "kill" a sprite so that it no longer 'self.exists'
    def kill(self):
        self.exists = false;
        self.dead = true;
    
    #@desc        Tells this object to flicker for the number of seconds requested (0 = infinite, negative number tells it to stop)
    def flicker(self,Duration=1):
        self._flickerTimer = Duration; 
        if(self._flickerTimer < 0):
            self._flicker = false
            self.visible = true
    
    #@desc        Called when this object collides with the bottom of a FlxBlock
    #@return    Whether the object is flickering or not
    def flickering(self):
        return self._flickerTimer >= 0
    
    #@desc        Call this to check and see if this object is currently on screen
    #@return    Whether the object is on screen or not
    def onScreen(self):
        p= FlxPoint();
        getScreenXY(p);
        if((p.x + self.width < 0) or (p.x > FlxG.width) or (p.y + self.height < 0) or (p.y > FlxG.height)):
            return false;
        return true;
    #@desc        Call this function to figure out the post-scrolling "screen" position of the object
    #@param    p    Takes a Flash Point object and assigns the post-scrolled self.x and self.y values of this object to it
    def getScreenXY(self,p):
        #print "getscreenXY",self.x,FlxG.scroll.x,self.scrollFactor.x
        p.x = Math.floor(self.x)+Math.floor(FlxG.scroll.x*self.scrollFactor.x);
        p.y = Math.floor(self.y)+Math.floor(FlxG.scroll.y*self.scrollFactor.y);

