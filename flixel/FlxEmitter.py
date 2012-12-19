from FlxCore import FlxCore
from FlxArray import FlxArray
from FlxSprite import FlxSprite
from FlxG import *
from FlxPoint import FlxPoint
from Math import Math
class FlxEmitter(FlxCore):
    # public var minVelocity:Point;
    # public var maxVelocity:Point;
    # private var _minRotation;
    # private var _maxRotation;
    # private var _gravity;
    # private var _drag;
    # private var _delay;
    # private var _timer;
    # private var self._sprites:FlxArray;
    # private var _particle;
    
    #@desc		Constructor
    #@param	X				The X position of the emitter
    #@param	Y				The Y position of the emitter
    #@param	Width			The width of the emitter (particles are emitted from a random position inside this box)
    #@param	Height			The height of the emitter
    #@param	Sprites			A pre-configured FlxArray of FlxSprite objects for the emitter to use (optional)
    #@param	Delay			A negative number defines the lifespan of the particles that are launched all at once.  A positive number tells it how often to fire a  particle.
    #@param	MinVelocityX	The minimum X velocity of the particles
    #@param	MaxVelocityX	The maximum X velocity of the particles (every particle will have a random X velocity between these values)
    #@param	MinVelocityY	The minimum Y velocity of the particles
    #@param	MaxVelocityY	The maximum Y velocity of the particles (every particle will have a random Y velocity between these values)
    #@param	MinRotation		The minimum angular velocity of the particles
    #@param	MaxRotation		The maximum angular velocity of the particles (you guessed it)
    #@param	Gravity			How much gravity should affect the particles
    #@param	Drag			Sets both the X and Y "Drag" or deceleration on the particles
    #@param	Graphics		If you opted to not pre-configure an array of FlxSprite objects, you can simply pass in a particle image or sprite sheet (ignored if you pass in an array)
    #@param	Quantity		The number of particles to generate when using the "create from image" option (ignored if you pass in an array)
    #@param	Multiple		Whether the image in the Graphics param is a single particle or a bunch of particles (if it's a bunch, they need to be square!)
    def __init__(self,X, Y, Width, Height, Sprites=None, Delay=-1, MinVelocityX=-100, MaxVelocityX=100, MinVelocityY=-100, MaxVelocityY=100, MinRotation=-360, MaxRotation=360, Gravity=500, Drag=0, Graphics=None, Quantity=0, Multiple=false, Parent=None):
        FlxCore.__init__(self);
        
        self.visible = false;
        self.x = X;
        self.y = Y;
        self.width = Width;
        self.height = Height;
        
        self.minVelocity =  FlxPoint(MinVelocityX,MinVelocityY);
        self.maxVelocity =  FlxPoint(MaxVelocityX,MaxVelocityY);
        self._minRotation = MinRotation;
        self._maxRotation = MaxRotation;
        self._gravity = Gravity;
        self._drag = Drag;
        self._delay = Delay;
        self._timer=0
        self._particle = 0;
        if(Graphics != None):
            self._sprites =  FlxArray();
            for  i in range(Quantity):
                if(Multiple):
                    (self._sprites.add( FlxSprite(Graphics,0,0,true))).randomFrame();
                else:
                    self._sprites.add( FlxSprite(Graphics));
            for  i in range(len(self._sprites)):
                if(Parent == None):
                    FlxG.state.add(self._sprites[i]);
                else:
                    Parent.add(self._sprites[i]);
        else:
            self._sprites = Sprites;
        self.kill();
        if(self._delay > 0):
            self.reset();
    
    #@desc		Called automatically by the game loop, decides when to launch particles and when to "die"
    def update(self):
        self._timer += FlxG.elapsed;
        if(self._delay < 0):
            if(self._timer > -self._delay) : 
                self.kill(); 
                return; 
            if(not self._sprites[0].exists):
                for i in range(len(self._sprites)):
                    self.emit();
            return;
        while(self._timer > self._delay):
            self._timer -= self._delay; 
            self.emit();
    
    #@desc		Call this function to reset the emitter (if you used a negative delay, calling this function "Explodes" the emitter again)
    def reset(self):
        self.active = true;
        self._timer = 0;
        self._particle = 0;
    
    #@desc		This function can be used both internally and externally to emit the next particle
    def emit(self):
        s = self._sprites[self._particle];
        s.exists = true;
        s.x = self.x - (s.width>>1);
        if(self.width != 0): 
            s.x += Math.random()*self.width;
        s.y = self.y - (s.height>>1);
        if(self.height != 0): 
            s.y += Math.random()*self.height;
        s.velocity.x = self.minVelocity.x;
        if(self.minVelocity.x != self.maxVelocity.x): 
            s.velocity.x += Math.random()*(self.maxVelocity.x-self.minVelocity.x);
        s.velocity.y = self.minVelocity.y;
        if(self.minVelocity.y != self.maxVelocity.y):
            s.velocity.y += Math.random()*(self.maxVelocity.y-self.minVelocity.y);
        s.acceleration.y = self._gravity;
        s.angularVelocity = self._minRotation;
        if(self._minRotation != self._maxRotation): 
            s.angularVelocity += Math.random()*(self._maxRotation-self._minRotation);
        if(s.angularVelocity != 0): 
            s.angle = Math.random()*360-180;
        s.drag.x = self._drag;
        s.drag.y = self._drag;
        self._particle+=1
        if(self._particle >= len(self._sprites)):
            self._particle = 0;
        s.onEmit();
    
    #@desc		Call this function to turn off all the particles and the emitter
    def kill(self):
        active = false;
        for i in range( len(self._sprites)):
            self._sprites[i].exists = false;
