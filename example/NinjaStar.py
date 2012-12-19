from flixel import *
import pyglet
class NinjaStar(FlxSprite):
    ImgStar = pyglet.resource.image('data/NinjaStar.png') #private var ImgStar:Class;
    ImgSpark = pyglet.resource.image('data/Spark.png') #private var ImgSpark:Class;
    #[Embed(source = 'data/SonicPunch1.mp3'# private var SndStar:Class;
    #[Embed(source = 'data/IceCubeExploding.mp3'# private var SndKillStar:Class;
    
    
    
    def __init__(self,X, Y, XVelocity, YVelocity):
        FlxSprite.__init__(self,NinjaStar.ImgStar, X, Y, true, true);
        # Basic movement speeds
        # How fast left and right it can travel
        self.maxVelocity.x = 200;
        # How fast up and down it can travel
        self.maxVelocity.y = 200;
        # How many degrees the object rotates
        self.angularVelocity = 100;
        # Bouding box tweaks
        # Width of the bounding box
        #self.width = 5;
        # Height of the bounding box
        #self.height = 5;
        # Where in the sprite the bouding box starts on the X axis
        self.offset.x = 6;
        # Where in the sprite the bouding box starts on the Y axis
        self.offset.y = 6;
        # Create and name and animation "normal"
        self.addAnimation("normal", [0]);
        self._sparks = FlxG.state.add(FlxEmitter(0, 0, 0, 0, None, -0.1, -150, 150, -200, 0, -720, 720, 400, 0, NinjaStar.ImgSpark, 10, true))
        self.facing = true;
        # The object now is removed from the render and update functions. It returns only when reset is called.
        # We do this so we can precreate serveral instances of this object to help speed things up a little
        self.exists = false;
    
    def hitFloor(self):
        self.kill();
        return FlxSprite.hitFloor(self);
    
    def hitWall(self):
        self.kill();
        return FlxSprite.hitWall(self);
    
    def hitCeiling(self):
        self.kill();
        return FlxSprite.hitCeiling(self);
    
    def kill(self):
        if (self.dead):
            return;
        
        self._sparks.x = self.x + 5;
        self._sparks.y = self.y + 5;
        self._sparks.reset();
        #FlxG.play(SndKillStar);
        FlxSprite.kill(self);
    
    def reset(self,X, Y, XVelocity, YVelocity):
        self.x = X;
        self.y = Y;
        self.dead = false;
        self.exists = true;
        self.visible = true;
        # Set the left and right speed
        self.velocity.x = XVelocity;
        # Play the animation
        self.play("normal");
        #FlxG.play(SndStar);
