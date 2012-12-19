#@desc		A simple button class that calls a function when mouse-clicked
class FlxButton(FlxCore):
    # private var _onToggle:Boolean;
    # private var _off:FlxSprite;
    # private var _on:FlxSprite;
    # private var _offT:FlxText;
    # private var _offTO:Point;
    # private var _onT:FlxText;
    # private var _onTO:Point;
    # private var _callback:Function;
    # private var _pressed:Boolean;
    
    #@desc		Constructor
    #@param	X			The X position of the button
    #@param	Y			The Y position of the button
    #@param	Image		A FlxSprite object to use for the button background
    #@param	Callback	The function to call whenever the button is clicked
    #@param	ImageOn		A FlxSprite object to use for the button background when highlighted (optional)
    #@param	Text		A FlxText object to use to display text on this button (optional)
    #@param	TextOn		A FlxText object that is used when the button is highlighted (optional)
    def __init__(self,X:int,Y:int,Image:FlxSprite,Callback:Function,ImageOn:FlxSprite=None,Text:FlxText=None,TextOn:FlxText=None):
        FlxCore.__init__(self);
        x = X;
        y = Y;
        _off = Image;
        if(ImageOn == None) _on = _off;
        else _on = ImageOn;
        width = _off.width;
        height = _off.height;
        if(Text != None) _offT = Text;
        if(TextOn == None) _onT = _offT;
        else _onT = TextOn;
        if(_offT != None) _offTO = Point(_offT.x,_offT.y);
        if(_onT != None) _onTO = Point(_onT.x,_onT.y);
        
        _off.scrollFactor = scrollFactor;
        _on.scrollFactor = scrollFactor;
        if(_offT != None)
        {
            _offT.scrollFactor = scrollFactor;
            _onT.scrollFactor = scrollFactor;
        }
        
        _callback = Callback;
        _onToggle = false;
        _pressed = false;
        
        updatePositions();
    }
    
    #@desc		Called by the game loop automatically, handles mouseover and click detection
    def update(self):
        FlxCore.update(self);

        if((_off != None) && _off.exists && _off.active) _off.update();
        if((_on != None) && _on.exists && _on.active) _on.update();
        if(_offT != None)
        {
            if((_offT != None) && _offT.exists && _offT.active) _offT.update();
            if((_onT != None) && _onT.exists && _onT.active) _onT.update();
        }

        visibility(false);
        if(_off.overlapsPoint(FlxG.mouse.x,FlxG.mouse.y))
        {
            if(!FlxG.kMouse)
                _pressed = false;
            else if(!_pressed)
            {
                _pressed = true;
                _callback();
            }
            visibility(!_pressed);
        }
        if(_onToggle) visibility(_off.visible);
        updatePositions();
    }
    
    override public function render():void
    {
        super.render();
        if((_off != None) && _off.exists && _off.visible) _off.render();
        if((_on != None) && _on.exists && _on.visible) _on.render();
        if(_offT != None)
        {
            if((_offT != None) && _offT.exists && _offT.visible) _offT.render();
            if((_onT != None) && _onT.exists && _onT.visible) _onT.render();
        }
    }
    
    #@desc		Call this function from your callback to toggle the button off, like a checkbox
    public function switchOff():void
    {
        _onToggle = false;
    }
    
    #@desc		Call this function from your callback to toggle the button on, like a checkbox
    public function switchOn():void
    {
        _onToggle = true;
    }
    
    #@desc		Check to see if the button is toggled on, like a checkbox
    #@return	Whether the button is toggled
    public function on():Boolean
    {
        return _onToggle;
    }
    
    #@desc		Internal function for handling the visibility of the off and on graphics
    #@param	On		Whether the button should be on or off
    def visibility(self,On):
        if(On):
            _off.visible = false;
            if(_offT != None) _offT.visible = false;
            _on.visible = true;
            if(_onT != None) _onT.visible = true;
        else:
            _on.visible = false;
            if(_onT != None) _onT.visible = false;
            _off.visible = true;
            if(_offT != None) _offT.visible = true;
    
    #@desc		Internal function that just updates the X and Y position of the button's graphics
    def updatePositions(self):
        _off.x = x;
        _off.y = y;
        if(_offT):
            _offT.x = _offTO.x+x;
            _offT.y = _offTO.y+y;
        _on.x = x;
        _on.y = y;
        if(_onT):
            _onT.x = _onTO.x+x;
            _onT.y = _onTO.y+y;
