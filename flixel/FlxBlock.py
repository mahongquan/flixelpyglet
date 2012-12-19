from FlxCore import FlxCore
from FlxPoint import FlxPoint
from FlxRect import FlxRect
#@desc		This is the basic "environment object" class, used to create walls and floors
class FlxBlock (FlxCore):
    #@desc		Constructor
    #@param	X			The X position of the block
    #@param	Y			The Y position of the block
    #@param	Width		The width of the block
    #@param	Height		The height of the block
    #@param	TileGraphic The graphic class that contains the tiles that should fill this block
    #@param	Empties		The number of "empty" tiles to add to the auto-fill algorithm (e.g. 8 tiles + 4 empties = 1/3 of block will be open holes)
    def __init__(self,X,Y,Width,Height,TileGraphic,Empties=0):
        FlxCore.__init__(self);
        self._tileSize=0;
        self.x = X;
        self.y = Y;
        self.width = Width;
        self.height = Height;
        if(TileGraphic == None):
            print "block None graphic"
            return;
        self._pixels = TileGraphic
        self._rects = FlxArray();
        self._p = FlxPoint();
        self._tileSize = self._pixels.height;
        self.widthInTiles = math.ceil(self.width/self._tileSize);
        self.heightInTiles = math.ceil(self.height/self._tileSize);
        self.width = self.widthInTiles*self._tileSize;
        self.height = self.heightInTiles*self._tileSize;
        self.numTiles = self.widthInTiles*self.heightInTiles;
        self.numGraphics = self._pixels.get_width()/self._tileSize;
        for i in range( numTiles):
            if(math.random()*(numGraphics+Empties) > Empties):
                self._rects.append(Rect(self._tileSize*Math.floor(Math.random()*self.numGraphics),0,self._tileSize,self._tileSize));
            else:
                self._rects.append(None);
    
    #@desc		Draws this block
    def render(self):
        FlxCore.render(self);
        self.getScreenXY(self._p);
        opx = self._p.x;
        for i in range( len(self._rects)):
            if(self._rects[i] != None):
                FlxG.buffer.blit(self._pixels,_rects[i],self._p,None,None,true);
            self._p.x += self._tileSize;
            if(self._p.x >= opx + self.width):
                self._p.x = opx;
                self._p.y += self._tileSize;
