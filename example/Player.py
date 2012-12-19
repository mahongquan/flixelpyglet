from flixel import *
import pyglet
class Player(FlxSprite):
    ImgPlayer = pyglet.resource.image('data/Player0.png')#)] private var ImgPlayer:Class;
    #[Embed(source = '../../data/jump.mp3')] private var SndJump:Class;
    #[Embed(source = '../../data/hurt.mp3')] private var SndHurt:Class;

    
    def __init__(self,X    , Y    , Stars):
        FlxSprite.__init__(self,Player.ImgPlayer, X, Y, true, true);
        self._move_speed     = 400;
        self._jump_power     = 300;
        self._max_health     = 10;
        self._hurt_counter     = 0;
        self._attack_counter     = 0;
        
        self._stars = Stars;
        
        # Max speeds
        self.maxVelocity.x = 200;
        self.maxVelocity.y = 300;
        # Set the player health
        self.health = 10;
        # Gravity
        self.acceleration.y = -420;
        # Friction
        self.drag.x = 300;
        # Bounding box tweaks
        self.width = 8;
        self.height = 14;
        self.offset.x = 4;
        self.offset.y = 2;
        
        self.addAnimation("normal", [0, 1, 2, 3], 10);
        self.addAnimation("jump", [2]);
        self.addAnimation("attack", [4, 5, 6], 10);
        self.addAnimation("stopped", [0]);
        self.addAnimation("hurt", [2, 7], 10);
        self.addAnimation("dead", [7, 7, 7], 5);
        
        self.facing = true;

    def update(self):
        #print "player touching:",self.touching
        if (self.dead):
            if (self.finished):
                self.exists = false;
            else:
                FlxSprite.update(self);
            return
        
        if (self._hurt_counter > 0):
            self._hurt_counter -= FlxG.elapsed * 3;
        
        if (self._attack_counter > 0):
            self._attack_counter -= FlxG.elapsed * 3;

        if (FlxG.kLeft):
            self.facing = false;
            self.velocity.x -= self._move_speed * FlxG.elapsed;
        elif (FlxG.kRight):
            self.facing = true;
            self.velocity.x += self._move_speed * FlxG.elapsed;

        if (FlxG.kUp and (self.touching & FlxCore.DOWN)):
            #FlxG.play(SndJump);
            self.velocity.y = self._jump_power;
        #if (FlxG.kDown):# and self.velocity.y == 0):
            #FlxG.play(SndJump);
        #    self.velocity.y = +self._jump_power;
        if (FlxG.justPressed(FlxG.B) and self._attack_counter <= 0):
            self._attack_counter = 1;
            self.play("attack");
            self.throwStar(self.facing);
        
        if (self._hurt_counter > 0 ):
            self.play("hurt");
        elif (self._attack_counter > 0):
            self.play("attack");
        else:
            if (self.velocity.y != 0):
                self.play("jump");
            else:
                if (self.velocity.x == 0):
                    self.play("stopped");
                else:
                    self.play("normal");
        #print "before update x,y:",self.x,self.y,self.last.x,self.last.y
        self.touching=0x0000
        FlxSprite.update(self);
        
        #print "after update player x,y:",self.x,self.y,self.last.x,self.last.y
    def hitFloor(self):
        return FlxSprite.hitFloor(self)
    
    def hurt(self,Damage    ):
        self._hurt_counter = 1;
        #FlxG.play(SndHurt);
        return FlxSprite.hurt(self,Damage);
    
    def throwStar(self,dir):
        from NinjaStar import NinjaStar
        from PlayState import PlayState
        XVelocity=0
        if (dir):
            XVelocity = 200;
        else:
            XVelocity = -200;
        
        for  i in range( len(self._stars)):
            if (not self._stars[i].exists):
                self._stars[i].reset(self.x, self.y + 2, XVelocity, 0);
                return;
            
            star = NinjaStar(self.x, self.y + 2, XVelocity, 0);
            star.reset(self.x, self.y, XVelocity, 0);
            PlayState.instance.lyrSprites.add(star)
            self._stars.add(star);
