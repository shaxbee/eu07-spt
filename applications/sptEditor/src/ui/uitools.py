'''
Created on 24-07-2011

@author: Grzesiek
'''

import wx

def ResizeBitmap(bitmap, size):
    '''Method for resizing icons on bar'''
    if isinstance(bitmap,wx.Bitmap):
        img = bitmap.ConvertToImage()
        img.Rescale(size, size, wx.IMAGE_QUALITY_HIGH)
        return wx.BitmapFromImage(img)
    return None
    
def SelectButton(menu, id):
    "only for compatibility purposes with ribbon"
    b = FindItemById(menu, id)
    b.Select(True)
    menu.Refresh(False)

def DeselectButton(menu, id):
    "only for compatibility purposes"
    b = FindItemById(menu, id)
    b.Select(False)
    menu.Refresh(False)
    
def FindItemById(menu, id):
    for b in menu._tbButtons:
        if b._tbItem._id == id:
            return b._tbItem
    return None
