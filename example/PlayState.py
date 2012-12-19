from flixel import *
from NinjaStar import NinjaStar
from Player import Player
from Enemy import Enemy
from Spawner import Spawner
from GameOverState import GameOverState
import pyglet
class PlayState(FlxState):
    DataMap='data/map.txt'
    ImgHearts= pyglet.resource.image('data/hearts.png')
    ImgTiles=pyglet.resource.image('data/ntiles.PNG')
    ImgS=pyglet.resource.image('data/b.png')
    instance=None
    def __init__(self):
        FlxState.__init__(self)
        PlayState.instance=self
        self.lyrStage = FlxLayer();
        self.lyrSprites = FlxLayer();
        self.lyrHUD = FlxLayer();
        
        self._pStars =FlxArray();
        for  n in range(40):#(var n:int = 0; n < 40; n += 1) {
            t=NinjaStar(0, 0, 0, 0)
            self.lyrSprites.add(t)
            self._pStars.add(t);
        
        self._eStars = FlxArray();
        for en  in range(40):# (var en:int = 0; en < 40; en += 1) {
            t=NinjaStar(0, 0, 0, 0)
            self.lyrSprites.add(t)
            self._eStars.add(t);
        
        self.player = Player(52, 52, self._pStars);
        self.lyrSprites.add(self.player);
        
        self._hearts = FlxArray();
        tmpH=None;
        for  hCount in range( self.player._max_health):
            tmpH =FlxSprite(PlayState.ImgHearts, 2 + (hCount * 10), FlxG.height-PlayState.ImgHearts.height, true, false);
            tmpH.scrollFactor.x =0
            tmpH.scrollFactor.y =0;
            tmpH.addAnimation("on", [0]);
            tmpH.addAnimation("off", [1]);
            tmpH.play("on");
            self._hearts.add(self.lyrHUD.add(tmpH));
        
        FlxG.follow(self.player, 2.5);
        FlxG.followAdjust(0.5, 0.5);
        FlxG.followBounds(1, 1, 640 - 1, 480 - 1);
        
        #self._map = self.loadmap();
        self._map=FlxTilemap(PlayState.DataMap, PlayState.ImgTiles, 1);
        self.lyrStage.add(self._map);
        
        self.add(self.lyrStage);
        self.add(self.lyrSprites);
        self.add(self.lyrHUD);
        
        self._e = FlxArray();
        #ma self._e.add(self.lyrSprites.add(Enemy(576, 16, self._p, self._eStars)));
        #X, Y, Text="", Color=0x000000, Font=None, Size=8, Justification=None, Angle=0
        self._scoreDisplay = FlxText(FlxG.width - 50, FlxG.height-10,  str(FlxG.score), 0xffffffff, None, 8);
        self._scoreDisplay.text="00000"
        self._scoreDisplay.scrollFactor.x = 0
        self._scoreDisplay.scrollFactor.y = 0;
        self.lyrHUD.add(self._scoreDisplay);
        
        self._spawners = FlxArray();
        self.RandomSpawner();
        
        #FlxG.setMusic(SndNinja);
    def loadmap(self):
        rows = open(PlayState.DataMap).read().split("\n");
        heightInTiles = len(rows);
        widthInTiles=0
        sprites=[]
        imageh=PlayState.ImgS.height
        # print imageh
        # imageone=PlayState3.ImgTiles.subsurface(0,0,imageh,imageh)
        for  r  in range(heightInTiles):
            cols = rows[r].split(",");
            if(len(cols) <= 1):
                heightInTiles-=1;
                continue;
            if(widthInTiles == 0):
                widthInTiles = len(cols);
            for c in range(widthInTiles):
                if (int(cols[c])!=0):
                    s=FlxSprite(PlayState.ImgS,c*imageh,(heightInTiles-1-r)*imageh)
                    self.lyrStage.add(s)
                    sprites.append(s)
        return sprites
    
    def update(self):
        from MenuState import MenuState
        #print FlxG.elapsed
        _old_health = self.player.health;
        _old_score = FlxG.score;
        
        FlxState.update(self);            
        #FlxG.collideArray(self._map,self.player);
        self._map.collide(self.player)
        #FlxG.collideArrays(self._map, self._e);
        self._map.collideArr(self._e)
        FlxG.overlapArray(self._e, self.player, self.EnemyHit);
        #FlxG.collideArrays(self._map, self._pStars);
        self._map.overlapsArr(self._pStars,self.StarHitMap)
        FlxG.overlapArrays(self._pStars, self._e, self.StarHitsEnemy);
        #FlxG.collideArrays(self._map, self._eStars);
        self._map.overlapsArr(self._eStars,self.StarHitMap)
        FlxG.overlapArray(self._eStars, self.player, self.StarHitsPlayer);
        
        if (self.player.dead):
            FlxG.flash(0xffffffff, 0.75);
            #FlxG.play(SndDie);
            FlxG.stopMusic();
            FlxG.switchState(MenuState);
        
        if (_old_score != FlxG.score):
            #print(dir(self._scoreDisplay))
            self._scoreDisplay.text=str(FlxG.score);
            #FlxG.play(SndDie);
        
        if (self.player.health != _old_health):
            for  i in range(self.player._max_health):
                if (i >= self.player.health):
                    self._hearts[i].play("off");
                else:
                    self._hearts[i].play("on");
    
    def EnemyHit(self,E, P):
        FlxG.log(str(P._hurt_counter));
        if (P._hurt_counter <= 0):
            if (E.x > P.x):
                P.velocity.x = -100;
                E.velocity.x = 100;
            else:
                P.velocity.x = 100;
                E.velocity.x = -100;
            P.hurt(1);
    def RandomX(self):
        return (Math.random() * (576 - 16)) + 16;
    
    def RandomY(self):
        return (Math.random() * (464 - 16)) + 16;
    
    def StarHitsEnemy(self,colStar, colEnemy):
        colStar.kill();
        colEnemy.hurt(1);
        self._spawner.kill();
        self.RandomSpawner();
    def StarHitMap(self,maptile, P):
        P.kill()
    def StarHitsPlayer(self,colStar, P):
        if (P._hurt_counter <= 0):
            if (colStar.x > P.x):
                P.velocity.x = -100;
            else:
                P.velocity.x = 100;
            
            P.hurt(1);
            colStar.kill();
    
    def RandomSpawner(self):
        #print "spawner"
        self._spawner = Spawner(32, 132, self._e, self.player, self._eStars);
        #print "after spawner",self.player.x,self.player.y
        self.lyrStage.add(self._spawner)
        #print "after spawner",self.player.x,self.player.y
        self._spawners.add(self._spawner);
