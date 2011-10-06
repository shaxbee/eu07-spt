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
    