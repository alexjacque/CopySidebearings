# The MIT License (MIT)

# Copyright (c) 2015 Alex Jacque <alexjacque.com>

# Permission is hereby granted, free of charge, to any person obtaining a copy
# of this software and associated documentation files (the "Software"), to deal
# in the Software without restriction, including without limitation the rights
# to use, copy, modify, merge, publish, distribute, sublicense, and/or sell
# copies of the Software, and to permit persons to whom the Software is
# furnished to do so, subject to the following conditions:

# The above copyright notice and this permission notice shall be included in
# all copies or substantial portions of the Software.

# THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
# IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
# FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE
# AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
# LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM,
# OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN
# THE SOFTWARE.

# import our magic makers
from AppKit import *
import vanilla
from defcon import Font
from defconAppKit.windows.baseWindow import BaseWindowController
from defconAppKit.controls.fontList import makeDefaultIDString
from robofab.interface.all.dialogs import Message

class CopySidebearings(BaseWindowController):

    def __init__(self):
        windowWidth = 200
        windowHeight = 180
        
        self.w = vanilla.FloatingWindow((50,50,windowWidth,windowHeight),"CopySidebearings")
        
        self.fonts = [(makeDefaultIDString(font), font) for font in AllFonts()]
        fontNames = [i[0] for i in self.fonts]
        
        # dropdowns
        self.w.sourceUFOText = vanilla.TextBox((15,15,90,22),"Source UFO:",sizeStyle="small")
        self.w.sourceUFODropDown = vanilla.PopUpButton((15,30,170,20), fontNames)
        self.w.sourceUFODropDown.set(0)
        
        self.w.destinationUFOText = vanilla.TextBox((15,60,90,22),"Destination UFO:",sizeStyle="small")
        self.w.destinationUFODropDown = vanilla.PopUpButton((15,75,170,20), fontNames)
        self.w.destinationUFODropDown.set(1)
        
        # divider
        self.w.divider1 = vanilla.HorizontalLine((15,110,-15,1))
        
        # commit button
        self.w.commitButton = vanilla.Button((15,125,-15,20), "Copy Sidebearings", sizeStyle="small", callback=self._commitButtonCallback)
        
        # note
        self.w.note = vanilla.TextBox((15,155,-15,15),"Open output window for results.",sizeStyle="mini",alignment="center")
        
        self.w.open() # go go gadget window
        
    def _commitButtonCallback(self, sender):
        
        sourceFont = self.fonts[self.w.sourceUFODropDown.get()][1]
        destinationFont = self.fonts[self.w.destinationUFODropDown.get()][1]
        
        sourceGlyphsCopied = [] # glyphs with successfully copied side bearings 
        sourceGlyphsNotInDestination = [] # glyphs from source not in destination font
        destGlyphsNotInSource = [] # glyphs in destination not contained in source
        
        for glyph in sourceFont:
            if glyph.name in destinationFont:# if glyph from font1 exists in font2
                destinationFont[glyph.name].prepareUndo("Metric Adjustment")
                destinationFont[glyph.name].leftMargin = glyph.leftMargin # set left margin
                destinationFont[glyph.name].rightMargin = glyph.rightMargin # set right margin
                destinationFont[glyph.name].performUndo()
                sourceGlyphsCopied.append(glyph.name) # add glyph name to array of glyphs successfully copied
            elif glyph.name not in destinationFont:
                sourceGlyphsNotInDestination.append(glyph.name) # add glyph name to arry of glyphs not in destination font
        
        for glyph in destinationFont:
            if glyph.name not in sourceFont: # if glyph from destination font is not in source font
                destGlyphsNotInSource.append(glyph.name) # add glyph name to array of glyphs not in the source font
       
        # prettify things
        sourceGlyphsCopied.sort()
        sourceGlyphsNotInDestination.sort()
        destGlyphsNotInSource.sort()
        
        print("### Source Glyph Sidebearings Successfully Copied ###")
        for i in range(len(sourceGlyphsCopied)):
            print(sourceGlyphsCopied[i])
        print("")
        
        print("### Source Glyphs NOT in Destination (skipped) ###")
        for i in range(len(sourceGlyphsNotInDestination)):
            print(sourceGlyphsNotInDestination[i])
        print("")
        
        print("### Glyphs in Destination NOT in Source (missed) ###")
        for i in range(len(destGlyphsNotInSource)):
            print(destGlyphsNotInSource[i])
        print("")
        
        return # done-zo
        


if __name__ == "__main__":
    count = len(AllFonts())
    if count < 2:
        Message("Requires two fonts to be open.")
    else:
        CopySidebearings()