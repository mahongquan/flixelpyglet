from FlxCore import FlxCore
from FlxSprite import FlxSprite
from FlxArray import FlxArray
from FlxPoint import FlxPoint
from FlxTile import FlxTile
from FlxG import *
from Math import  Math
from FlxRect import FlxRect
import mycollide
class FlxTilemap(FlxCore):
    #@desc		Constructor
    #@param	MapData			A string of comma and line-return delineated indices indicating what order the tiles should go in
    #@param	TileGraphic		All the tiles you want to use, arranged in a strip corresponding to the numbers in MapData
    #@param	CollisionIndex	The index of the first tile that should be treated as a hard surface
    #@param	DrawIndex		The index of the first tile that should actually be drawn
    def __init__(self,MapData, TileGraphic, CollisionIndex=1, DrawIndex=1):
        #image = pyglet.resource.image("data/logo.png")
        FlxCore.__init__(self);
        self.CollideIndex = CollisionIndex;self.DrawIndex = 1;
        self._ci = CollisionIndex;
        self.widthInTiles = 0;
        self.heightInTiles = 0;
        self._data = FlxArray();
        #c;
        #cols:Array;
        rows = open(MapData).read().split("\n");
        
        rows.reverse()
        rows=rows[2:]
        self.heightInTiles = len(rows);
        for  r  in range(self.heightInTiles):
            cols = rows[r].split(",");
            if(len(cols) <= 1):
                self.heightInTiles-=1;
                continue;
            if(self.widthInTiles == 0):
                self.widthInTiles = len(cols);
            for c in range(self.widthInTiles):
                self._data.append(int(cols[c]));
                  
        self._pixels = TileGraphic
        self._rects = FlxArray();
        self._p = FlxPoint();
        self._tileSize =self._pixels.height;
        self.width = self.widthInTiles*self._tileSize;
        self.height = self.heightInTiles*self._tileSize;
        self.numTiles = self.widthInTiles*self.heightInTiles;
        for i in range(self.numTiles):
            if(self._data[i] >= DrawIndex):
                self._rects.append(FlxRect(self._tileSize*self._data[i],0,self._tileSize,self._tileSize));
            else:
                self._rects.append(None);
        #self._block = FlxBlock(0,0,self._tileSize,self._tileSize,None);
        
        self._screenRows =int( Math.ceil(FlxG.height/self._tileSize)+1);
        if(self._screenRows > self.heightInTiles):
            self._screenRows = self.heightInTiles;
        self._screenCols = int(Math.ceil(FlxG.width/self._tileSize)+1);
        if(self._screenCols > self.widthInTiles):
            self._screenCols = self.widthInTiles;
        
        self._tileObjects = range(self._pixels.width/self._pixels.height)
        i=0
        while(i < self._pixels.width/self._pixels.height):
            collide=FlxCore.NONE
            if(i>= self.CollideIndex):
                collide=self.allowCollisions
            self._tileObjects[i] =FlxTile(self,i,self._tileSize,self._tileSize,(i >= self.DrawIndex),collide)
            i+=1;
    #@desc		Draws the tilemap
    def render(self):
        #NOTE: While this will only draw the tiles that are actually on screen, it will ALWAYS draw one screen's worth of tiles
        FlxCore.render(self)
        self.getScreenXY(self._p);
        #print self._p.x,self._p.y
        #self.position=(self._p.x,self._p.y)
        #raw_input()
        tx = Math.floor(-self._p.x/self._tileSize);
        ty = Math.floor(-self._p.y/self._tileSize);
        if(tx < 0): 
            tx = 0;
        if(tx > self.widthInTiles-self._screenCols): 
            tx = self.widthInTiles-self._screenCols;
        if(ty < 0): 
            ty = 0;
        if(ty > self.heightInTiles-self._screenRows): 
            ty = self.heightInTiles-self._screenRows;
        ri =int(ty*self.widthInTiles+tx);
        self._p.x += tx*self._tileSize;
        self._p.y += ty*self._tileSize;
        opx = self._p.x;
        for r in range(self._screenRows):
            cri = ri;
            for c in range(self._screenCols):
                #print self._rects[cri]
                #raw_input()
                if(self._rects[cri] != None):
                    im=self._pixels.get_region(self._rects[cri].x,self._rects[cri].y,self._rects[cri].width,self._rects[cri].height)#.x,self._rects[cri].y, self._rects[cri].width,self._rects[cri].height)
                    #tmp=Sprite(im)
                    #tmp.position=(self._p.x,self._p.y)
                    #print r,c,"tile",self._p.x,self._p.y
                    #self.add(tmp)
                    r=FlxRect(self._p.x,self._p.y,self._rects[cri].width,self._rects[cri].height)
                    im.blit(self._p.x,self._p.y);
                cri+=1;
                self._p.x += self._tileSize;
            ri += self.widthInTiles;
            self._p.x = opx;
            self._p.y += self._tileSize;
    
    #@desc		Collides a FlxSprite against the tilemap
    #@param	Spr		The FlxSprite you want to collide
    def old_collide(self,Spr):
        #print "map collide"#Spr.velocity.x
        ix =int(Math.floor((Spr.x - self.x)/self._tileSize))
        iy =int(Math.floor((Spr.y - self.y)/self._tileSize))
        for r in [iy-1,iy,iy+1]:
            if((r < 0) or (r >= self.heightInTiles)): 
                continue;
            for c in [ix-1,ix,ix+1]:
                if((c < 0) or (c >= self.widthInTiles)): 
                    continue;
                at=(r)*self.widthInTiles+c
                #print "at=",at
                if( self._data[at] >= self._ci):
                    self._block.x = self.x+c*self._tileSize;
                    self._block.y = self.y+r*self._tileSize;
                    self._block.collide(Spr);
                    #print at,self._block.x,self._block.y
        return 
        #old
        ix =int(Math.floor((Spr.x - self.x)/self._tileSize))
        iy =int(Math.floor((Spr.y - self.y)/self._tileSize))
        iw =int( Math.ceil(float(Spr.width)/self._tileSize)+1)
        ih =int(Math.ceil(float(Spr.height)/self._tileSize)+1)
        print "map collide",ih,iw
        print Spr.width,self._tileSize,Spr.x,Spr.y
        for r in range( ih):
            if((r < 0) or (r >= self.heightInTiles)): 
                continue;
            for c in range(iw):
                if((c < 0) or (c >= self.widthInTiles)): 
                    continue;
                at=(iy+r)*self.widthInTiles+ix+c
                print "at=",at,
                if(at<len(self._data) and self._data[at] >= self._ci):
                    self._block.x = self.x+(ix+c)*self._tileSize;
                    self._block.y = self.y+(iy+r)*self._tileSize;
                    self._block.collide(Spr);
                    #print Spr.ySpr.y,Spr.velocity.y,"block",self._block.x,self._block.y,self._block.width,self._block.height
        #raw_input()
    # def collide(self,Spr):
        # self.overlapsWithCallback(Spr,FlxCore.separate)
    def setTileProperties(self,Tile,AllowCollisions=0x1111,Callback=None,CallbackFilter=None,Range=1):
        if(Range <= 0):
            Range = 1;
        i = Tile;
        l = Tile+Range;
        while(i < l):
            tile = self._tileObjects[i]
            i+=1
            tile.allowCollisions = AllowCollisions;
            tile.callback = Callback;
            tile.filter = CallbackFilter;
    def overlapsArr(self,Array,callback):
        #print "overlapsArr"
        
        for i in range(len( Array)):
            
            c = Array[i];
            #print dir(c)
            if(c.exists):#,c.visible
                self.overlapsWithCallback(c,callback)
    def collideArr(self,Array):
        for i in range(len( Array)):
            c = Array[i];
            self.collide(c)
    def collide(self,Object):
        results = false;
        Position=None
        X = self.x;
        Y = self.y;
        if(Position != None):
            X = Position.x;
            Y = Position.y;
        #Figure out what tiles we need to check against
        selectionX = Math.floor((Object.x - X)/self._tileSize)
        selectionY = Math.floor((Object.y - Y)/self._tileSize)
        selectionWidth = selectionX + (Math.ceil(Object.width/self._tileSize)) + 1;
        selectionHeight = selectionY + Math.ceil(Object.height/self._tileSize) + 1;
        
        #Then bound these coordinates by the map edges
        if(selectionX < 0):
            selectionX = 0;
        if(selectionY < 0):
            selectionY = 0;
        if(selectionWidth > self.widthInTiles):
            selectionWidth = self.widthInTiles;
        if(selectionHeight > self.heightInTiles):
            selectionHeight = self.heightInTiles;
        
        #Then loop through this selection of tiles and call FlxObject.separate() accordingly
        rowStart = selectionY*self.widthInTiles;
        row = selectionY;
        overlapFound=false;
        deltaX = X - self.last.x;
        deltaY = Y - self.last.y;
        #print "selection====="
        
        #print selectionX,selectionY,selectionWidth,selectionHeight
        
        while(row <= selectionHeight):
            column = selectionX;
            while(column <=selectionWidth):
                
                overlapFound = false;
                #print "at="+str(int(rowStart+column))
                tile = self._tileObjects[self._data[int(rowStart+column)]];
                #print "row,column",row,column,tile.allowCollisions
                #print "data="+str(self._data[int(rowStart+column)])
                
                if(tile.allowCollisions):
                    tile.x = X+column*self._tileSize;
                    tile.y = Y+row*self._tileSize;
                    tile.last.x = tile.x - deltaX;
                    tile.last.y = tile.y - deltaY;
                    #print "==========="
                    #print tile.x,tile.y,self._tileSize
                    #print Object.x,Object.y,Object.width,Object.height
                    mycollide.collide(Object,tile)
                #raw_input()
                column+=1;
            rowStart += self.widthInTiles;
            row+=1;
        return results;
    def overlapsWithCallback(self,Object,Callback=None,FlipCallbackParams=false,Position=None):
        results = false;
        X = self.x;
        Y = self.y;
        if(Position != None):
            X = Position.x;
            Y = Position.y;
        #Figure out what tiles we need to check against
        selectionX = Math.floor((Object.x - X)/self._tileSize)
        selectionY = Math.floor((Object.y - Y)/self._tileSize)
        selectionWidth = selectionX + (Math.ceil(Object.width/self._tileSize)) + 1;
        selectionHeight = selectionY + Math.ceil(Object.height/self._tileSize) + 1;
        
        #Then bound these coordinates by the map edges
        if(selectionX < 0):
            selectionX = 0;
        if(selectionY < 0):
            selectionY = 0;
        if(selectionWidth > self.widthInTiles):
            selectionWidth = self.widthInTiles;
        if(selectionHeight > self.heightInTiles):
            selectionHeight = self.heightInTiles;
        
        #Then loop through this selection of tiles and call FlxObject.separate() accordingly
        rowStart = selectionY*self.widthInTiles;
        row = selectionY;
        overlapFound=false;
        deltaX = X - self.last.x;
        deltaY = Y - self.last.y;
        while(row < selectionHeight):
            column = selectionX;
            while(column < selectionWidth):
                #print "row,column",row,column
                overlapFound = false;
                tile = self._tileObjects[self._data[int(rowStart+column)]];
                if(tile.allowCollisions):
                    tile.x = X+column*self._tileSize;
                    tile.y = Y+row*self._tileSize;
                    tile.last.x = tile.x - deltaX;
                    tile.last.y = tile.y - deltaY;
                    if(Callback != None):
                        if(FlipCallbackParams):
                            overlapFound = Callback(Object,tile);
                        else:
                            overlapFound = Callback(tile,Object);
                    else:
                        overlapFound = (Object.x + Object.width > tile.x) and (Object.x < tile.x + tile.width) and (Object.y + Object.height > tile.y) and (Object.y < tile.y + tile.height);
                    if(overlapFound):
                        if((tile.callback != None) and ((tile.filter == None) or (Object is tile.filter))):
                            tile.mapIndex = rowStart+column;
                            tile.callback(tile,Object);
                        results = true;
                elif((tile.callback != None) and ((tile.filter == None) or (Object is tile.filter))):
                    tile.mapIndex = rowStart+column;
                    tile.callback(tile,Object);
                column+=1;
            rowStart += self.widthInTiles;
            row+=1;
        return results;