from flixel import *
from Enemy import Enemy
import pyglet
class Spawner (FlxSprite):
    ImgSpawner= pyglet.resource.image('data/Spawner.png')#] private var ImgSpawner:Class;
    def __init__(self,X    , Y    , Enemies, ThePlayer, Stars):
        FlxSprite.__init__(self,Spawner.ImgSpawner, X, Y, true, true);
        self._create_counter     = 0;
        self._e = Enemies;
        self._player = ThePlayer;
        self._eStars = Stars;
    
    def update(self):
        FlxSprite.update(self);
        self._create_counter+=FlxG.elapsed
        if (self._create_counter > 5):
            
            self._create_counter =0;
            self.spawn();
    
    def spawn(self):
        from PlayState import PlayState
        for  i in range(len(self._e)):
            if (not self._e[i].exists):
                self._e[i].reset(self.x, self.y);
                return;
        
        enemy = Enemy(self.x, self.y, self._player, self._eStars);
        
        self._e.add(enemy)
        PlayState.instance.lyrSprites.add(enemy)
