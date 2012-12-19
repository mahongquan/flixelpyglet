#@desc		This class wraps the normal Flash array and adds a couple of extra functions...
import random
class FlxArray(list):# extends Array
    #@desc		Constructor
    def __init__(self):
        pass
        #super();

    #@desc		Picks an entry at random from an array
    #@param	Arr		The array you want to pick the object from
    #@return	Any object
    @staticmethod
    def getRandom(arr):
        return arr[random.randrange(0,len(arr))];
    
    #@desc		Find the first entry in the array that doesn't "exist"
    #@return	Anything based on FlxCore (FlxSprite, FlxText, FlxBlock, etc)
    def getNonexist(self):
        if(len(self) <= 0):
            return None;
        i= 0;
        while(i < len(self)):
            if(not self[i].exists):
                return self[i];
            i+=1
        return None;
    
    #@desc		Add an object to this array
    #@param	Obj		The object you want to add to the array
    #@return	Just returns the object you passed in in the first place
    def add(self,Obj):
        for i  in range(len(self)):
            if(self[i] == None):
                self[i] = Obj
                return Obj;
        self.append(Obj)
        return Obj;
    
    #@desc		Remove any object from this array
    #@param	Core	The object you want to remove from this array
    def remove(self,Obj,Splice=0):
        
        self.removeAt(self.index(Obj),Splice);
    
    #@desc		Remove any object from this array
    #@param	Index	The entry in the array that you want to remove
    def removeAt(self,Index,Splice=0):
        if(Splice):
            self.pop(Index);
        else:
            self[Index] = None;
    
    #@desc		Kills the specified FlxCore-based object (FlxSprite, FlxText, etc) in this array
    #@param	Core	The object you want to kill
    def kill(self,Core):
        killAt(self.index(Core));
    
    #@desc		Kills the specified FlxCore-based object (FlxSprite, FlxText, etc) in this array
    #@param	Index	The entry in the array that you want to kill
    def killAt(self,Index):
        if(type(self[Index])==FlxCore):
            self[Index].kill()
    
    #@desc		Pops every entry out of the array
    def clear(self):
        self=[];
