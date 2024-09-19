import st7789, tft_config
import gotheng as vector_font # Vector Font
import vga1_8x8 as font 
import chango_16 as bitmap_font # Bitmap Font

tft = tft_config.config(3)
tft.init()

# 3 ways for print text
tft.text(font, "LilyGO Rocks!" , 0, 0)
tft.draw(vector_font, "LilyGO Rocks!", 0, 30 )
tft.write(bitmap_font, "LilyGO Rocks!", 0, 60)