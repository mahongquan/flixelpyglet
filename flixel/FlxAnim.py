class FlxAnim:
    #@desc		Constructor
    #@param	Name		What this animation should be called (e.g. "run")
    #@param	Frames		An array of numbers indicating what frames to play in what order (e.g. 1, 2, 3)
    #@param	FrameRate	The speed in frames per second that the animation should play at (e.g. 40 fps)
    #@param	Looped		Whether or not the animation is looped or just plays once
    def __init__(self,Name, Frames, FrameRate=30, Looped=1):
        self.name = Name;
        self.delay = 1.0/FrameRate;
        self.frames = Frames;
        self.looped = Looped;
