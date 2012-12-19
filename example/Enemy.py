from flixel import *
import pyglet
class Enemy (FlxSprite):
    ImgEnemy = pyglet.resource.image('data/Enemy.png')#] private var ImgEnemy:Class;
    def __init__(self,X    , Y    , ThePlayer    , EnemyStars    ):
        FlxSprite.__init__(self,Enemy.ImgEnemy, X, Y, true, true)
        self._move_speed     = 400;
        self._jump_power     = 800;
        self._max_health     = 10;
        self._hurt_counter     = 0;
        self._can_jump     = true;
        self._last_jump     = 0;
        self._attack_counter     = 0;
        self._eStars = EnemyStars;
        
        #Max speeds
        self._player = ThePlayer;
        self.maxVelocity.x = 200;
        self.maxVelocity.y = 400;
        
        self.health = 1;
        self.acceleration.y = -420;
        self.drag.x = 200;
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
    
    def update(self):
        if (self.dead):
            if (self.finished):
                self.exists = false;
            else:
                FlxSprite.update(self);
            return;
        if (self.touching & FlxCore.DOWN):
            self._can_jump = true;
        print "can jump",self._can_jump
        
        if (self._hurt_counter > 0):
            self._hurt_counter -= FlxG.elapsed * 3;
        self._attack_counter-= FlxG.elapsed
        #print "attack or no:",self._attack_counter,self._player.y,self.y
        if (self._attack_counter <= 0 and self._player.y > self.y - 1 and self._player.y < self.y + 1):
            self._attack_counter = 2;
            self.play("attack");
            self.throwStar(self.getfacing());
        
        if (self._player.x < self.x - 36):
            self.setfacing(false);
            self.velocity.x -= self._move_speed * FlxG.elapsed;
        elif (self._player.x > self.x + 36):
            self.setfacing(true);
            self.velocity.x += self._move_speed * FlxG.elapsed;
        
        if (self._last_jump > 0):
            self._last_jump -= FlxG.elapsed;
        
        if (self.velocity.y != 0 or self._last_jump > 0):
            self._can_jump = false;
        
        if (self._player.y > self.y and self._can_jump):
            self.velocity.y = self._jump_power;
            self._can_jump = false;
            self._last_jump = 2;
        
        if (self._hurt_counter > 0):
            self.play("hurt");
        else:
            if (self._attack_counter > 0):
                self.play("attack");
            else:
                if (self.velocity.y != 0):
                    self.play("jump");
                else:
                    if (self.velocity.x == 0):
                        self.play("stopped");
                    else:
                        self.play("normal");
        self.touching=0x0000
        FlxSprite.update(self);
    
   
    def hurt(self,Damage    ):
        self._hurt_counter = 1;
        return FlxSprite.hurt(self,Damage);
    
    def throwStar(self,dir):
        from PlayState import PlayState
        from NinjaStar import NinjaStar
        XVelocity=0    ;
        if (dir):
            XVelocity = 150;
        else:
            XVelocity = -150;
        
        for i in range(len(self._eStars)):
            if (not self._eStars[i].exists):
                self._eStars[i].reset(self.x, self.y + 2, XVelocity, 0);
                return;
        
        star= NinjaStar(self.x, self.y + 2, XVelocity, 0);
        star.reset(self.x, self.y, XVelocity, 0);
        self._eStars.add(star)
        PlayState.instance.lyrSprites.add(star)
    
    def kill(self):
        if (self.dead): 
            return;
        
        FlxG.score += 10;
        FlxSprite.kill(self);
    
    def reset(self,X    , Y    ):
        self.x = X;
        self.y = Y;
        self.dead = false;
        self.exists = true;
        self.visible = true;
        self.play("normal");
