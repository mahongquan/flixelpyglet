from FlxRect import FlxRect
true=1
false=0
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
def separate(Object1,Object2):#:FlxObject, Object2:FlxObject):Boolean
    separatedX = separateX(Object1,Object2);
    separatedY = separateY(Object1,Object2);
    return separatedX or separatedY;
def collide(object,Spr):
    #print "collide",self,Spr
    #print "last",self.last.x,self.last.y,self.x,self.y
    overlap(object,Spr,separate,None)
def overlap(_object,checkObject,_processingCallback=None,_notifyCallback=None):
    #calculate bulk hull for _object
    if(_object.x < _object.last.x):
        _objectHullX = _object.x
    else:
        _objectHullX =_object.last.x;
    if(_object.y < _object.last.y):
        _objectHullY = _object.y
    else:
        _objectHullY =_object.last.y;
    _objectHullWidth = _object.x - _object.last.x;
    if(_objectHullWidth>0):
        _objectHullWidth = _object.width + _objectHullWidth
    else:
        _objectHullWidth = _object.width - _objectHullWidth;
    _objectHullHeight = _object.y - _object.last.y;
    if(_objectHullHeight>0):
        _objectHullHeight = _object.height + _objectHullHeight
    else:
        _objectHullHeight = _object.height-_objectHullHeight
    
    #calculate bulk hull for checkObject
    if(checkObject.x < checkObject.last.x):
        _checkObjectHullX = checkObject.x
    else:
        _checkObjectHullX = checkObject.last.x;
    if(checkObject.y < checkObject.last.y):
        _checkObjectHullY = checkObject.y
    else:
        _checkObjectHullY =checkObject.last.y;
    _checkObjectHullWidth = checkObject.x - checkObject.last.x;
    if(_checkObjectHullWidth>0):
        _checkObjectHullWidth = checkObject.width + _checkObjectHullWidth
    else:
        _checkObjectHullWidth = checkObject.width-_checkObjectHullWidth
    _checkObjectHullHeight = checkObject.y - checkObject.last.y;
    if(_checkObjectHullHeight>0):
        _checkObjectHullHeight = checkObject.height + _checkObjectHullHeight
    else:
        _checkObjectHullHeight = checkObject.height-_checkObjectHullHeight
    
    #check for intersection of the two hulls
    if(    (_objectHullX + _objectHullWidth > _checkObjectHullX) and
        (_objectHullX < _checkObjectHullX + _checkObjectHullWidth) and
        (_objectHullY + _objectHullHeight > _checkObjectHullY) and
        (_objectHullY < _checkObjectHullY + _checkObjectHullHeight) ):
        #Execute callback functions if they exist
        overlapProcessed=false;
        if((_processingCallback == None) or _processingCallback(_object,checkObject)):
            overlapProcessed = true;
        if(overlapProcessed and (_notifyCallback != None)):
            _notifyCallback(_object,checkObject);
#@desc        Call this function to figure out the post-scrolling "screen" position of the object
#@param    p    Takes a Flash Point object and assigns the post-scrolled self.x and self.y values of this object to it
def separateX(Object1,Object2):#Object1:FlxObject, Object2:FlxObject):Boolean
    from FlxTilemap import FlxTilemap
    #can't separate two immovable objects
    obj1immovable = Object1.immovable;
    obj2immovable = Object2.immovable;
    #print obj1immovable,obj2immovable
    #raw_input()
    if(obj1immovable and obj2immovable):
        return false;
    
    #If one of the objects is a tilemap, just pass it off.
    if(Object1.__class__ is FlxTilemap):
        #print "tilemap"
        return Object1.overlapsWithCallback(Object2,separateX);
    if(Object2.__class__ is FlxTilemap):
        #print "tilemap"
        return Object2.overlapsWithCallback(Object1,separateX,true);
    #print Object1,Object2
    #First, get the two object deltas
    overlap = 0;
    obj1delta = Object1.x - Object1.last.x;
    obj2delta = Object2.x - Object2.last.x;
    #print obj1delta,obj2delta
    if(obj1delta != obj2delta):
    
        #Check if the X hulls actually overlap
        if(obj1delta > 0):
            obj1deltaAbs = obj1delta;
            tmpx1=obj1delta
        else:
            obj1deltaAbs = -obj1delta;
            tmpx1=0
        if(obj2delta > 0):
            obj2deltaAbs = obj2delta;
            tmpx2=obj2delta
        else:
            tmpx2=0
            obj2deltaAbs = -obj2delta;
        
        obj1rect = FlxRect(Object1.x-tmpx1,Object1.last.y,Object1.width+obj1deltaAbs,Object1.height);
        obj2rect = FlxRect(Object2.x-tmpx2,Object2.last.y,Object2.width+obj2deltaAbs,Object2.height);
        if((obj1rect.x + obj1rect.width > obj2rect.x) and (obj1rect.x < obj2rect.x + obj2rect.width) and (obj1rect.y + obj1rect.height > obj2rect.y) and (obj1rect.y < obj2rect.y + obj2rect.height)):
        
            maxOverlap = obj1deltaAbs + obj2deltaAbs + OVERLAP_BIAS;
            
            #If they did overlap (and can), figure out by how much and flip the corresponding flags
            if(obj1delta > obj2delta):
            
                overlap = Object1.x + Object1.width - Object2.x;
                if((overlap > maxOverlap) or not(Object1.allowCollisions & RIGHT) or not(Object2.allowCollisions & LEFT)):
                    overlap = 0;
                else:
                
                    Object1.touching |= RIGHT;
                    Object2.touching |= LEFT;
                
            elif(obj1delta < obj2delta):
            
                overlap = Object1.x - Object2.width - Object2.x;
                if((-overlap > maxOverlap) or not(Object1.allowCollisions & LEFT) or not(Object2.allowCollisions & RIGHT)):
                    overlap = 0;
                else:
                    Object1.touching |= LEFT;
                    Object2.touching |= RIGHT;
    
    #Then adjust their positions and velocities accordingly (if there was any overlap)
    if(overlap != 0):
        obj1v = Object1.velocity.x;
        obj2v = Object2.velocity.x;
        
        if( not obj1immovable and not obj2immovable):
            overlap *= 0.5;
            Object1.x = Object1.x - overlap;
            Object2.x += overlap;
            if(obj2v > 0):
                tmp=1
            else:
                tmp=-1
            obj1velocity = Math.sqrt((obj2v * obj2v * Object2.mass)/Object1.mass) * tmp;
            if(obj1v > 0):
                tmp=1
            else:
                tmp=-1
            obj2velocity = Math.sqrt((obj1v * obj1v * Object1.mass)/Object2.mass) * tmp;
            average = (obj1velocity + obj2velocity)*0.5;
            obj1velocity -= average;
            obj2velocity -= average;
            Object1.velocity.x = average + obj1velocity * Object1.elasticity;
            Object2.velocity.x = average + obj2velocity * Object2.elasticity;
        
        elif(not obj1immovable):
        
            Object1.x = Object1.x - overlap;
            Object1.velocity.x = obj2v - obj1v*Object1.elasticity;
        
        elif(not obj2immovable):
        
            Object2.x += overlap;
            Object2.velocity.x = obj1v - obj2v*Object2.elasticity;
        
        return true;
    
    else:
        return false;

    
    #
    # The Y-axis component of the object separation process.
    # @param    Object1     Any <code>FlxObject</code>.
     # * @param    Object2        Any other <code>FlxObject</code>.
     # * 
     # * @return    Whether the objects in fact touched and were separated along the Y axis.
     # */
def separateY(Object1, Object2):
    #can't separate two immovable objects
    obj1immovable = Object1.immovable;
    obj2immovable = Object2.immovable;
    if(obj1immovable and obj2immovable):
        return false;
    #First, get the two object deltas
    overlap = 0;
    obj1delta = Object1.y - Object1.last.y;
    obj2delta = Object2.y - Object2.last.y;
    
    if(obj1delta != obj2delta):
        #Check if the Y hulls actually overlap
        if(obj1delta > 0):
            obj1deltaAbs = obj1delta
            tmpy1=obj1delta
            obj1rect = FlxRect(Object1.x,Object1.last.y,Object1.width,Object1.height+obj1deltaAbs);
        else:
            tmpy1=-obj1delta
            obj1deltaAbs =-obj1delta
            obj1rect = FlxRect(Object1.x,Object1.y,Object1.width,Object1.height+obj1deltaAbs);
        if(obj2delta > 0):
            tmpy2=obj2delta
            obj2deltaAbs = obj2delta# > 0)?obj2delta:-obj2delta;
            obj2rect = FlxRect(Object2.x,Object2.last.y,Object2.width,Object2.height+obj2deltaAbs);
        else:
            tmpy2=-obj2delta
            obj2deltaAbs=-obj2delta
            obj2rect = FlxRect(Object2.x,Object2.y,Object2.width,Object2.height+obj2deltaAbs);
        
        #print "here"
        #print raw_input()
        if((obj1rect.x + obj1rect.width > obj2rect.x) and (obj1rect.x < obj2rect.x + obj2rect.width) and (obj1rect.y + obj1rect.height > obj2rect.y) and (obj1rect.y < obj2rect.y + obj2rect.height)):
            maxOverlap = obj1deltaAbs + obj2deltaAbs + OVERLAP_BIAS;
            #print "calc overlap"
            #If they did overlap (and can), figure out by how much and flip the corresponding flags
            if(obj1delta > obj2delta):
                #obj2delta=-.12
                overlap = Object1.y + Object1.height - Object2.y;
                #print Object1,Object2
                #print overlap,maxOverlap,overlap>maxOverlap,not(Object1.allowCollisions & UP),not(Object2.allowCollisions & UP)
                #raw_input()
                if((overlap > maxOverlap) or not(Object1.allowCollisions & UP) or not(Object2.allowCollisions & DOWN)):
                    overlap = 0;
                else:
                
                    Object1.touching |= UP;
                    Object2.touching |= DOWN;
            elif(obj1delta < obj2delta):
                #print "obj1deta<obj2delta"
                #raw_input()
                overlap = Object1.y - Object2.height - Object2.y;
                #print overlap,maxOverlap,Object1.allowCollisions,Object2.allowCollisions
                #raw_input()
                if((-overlap > maxOverlap) or not(Object1.allowCollisions & DOWN) or not(Object2.allowCollisions & UP)):
                    overlap = 0;
                else:
                    Object1.touching |= DOWN;
                    Object2.touching |= UP;
    
    #Then adjust their positions and velocities accordingly (if there was any overlap)
    if(overlap != 0):
        #print "overlap",overlap
        #raw_input()
        obj1v = Object1.velocity.y;
        obj2v = Object2.velocity.y;
        
        if(not obj1immovable and not obj2immovable):
            overlap *= 0.5;
            Object1.y = Object1.y - overlap;
            Object2.y += overlap;
            if (obj2v>0):
                tmp=1
            else:
                tmp=-1
            obj1velocity = Math.sqrt((obj2v * obj2v * Object2.mass)/Object1.mass) * tmp;
            if(obj1v>0):
                tmp=1
            else:
                tmp=-1
            obj2velocity = Math.sqrt((obj1v * obj1v * Object1.mass)/Object2.mass) *tmp;
            average = (obj1velocity + obj2velocity)*0.5;
            obj1velocity -= average;
            obj2velocity -= average;
            Object1.velocity.y = average + obj1velocity * Object1.elasticity;
            Object2.velocity.y = average + obj2velocity * Object2.elasticity;
        elif(not obj1immovable):
            Object1.y = Object1.y - overlap;
            Object1.velocity.y = obj2v - obj1v*Object1.elasticity;
            #This is special case code that handles cases like horizontal moving platforms you can ride
            if(Object2.active and Object2.moves and (obj1delta > obj2delta)):
                Object1.x += Object2.x - Object2.last.x;
        elif(not obj2immovable):
            Object2.y += overlap;
            Object2.velocity.y = obj1v - obj2v*Object2.elasticity;
            #This is special case code that handles cases like horizontal moving platforms you can ride
            if(Object1.active and Object1.moves and (obj1delta < obj2delta)):
                Object2.x += Object1.x - Object1.last.x;
        return true;
    else:
        return false;
