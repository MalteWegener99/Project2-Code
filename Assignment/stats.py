from PIL import Image
import os
import statistics 
images = os.listdir(r'pics')

widths, heights, sizes = [], [], []

for img in images:
    imga = Image.open(r'pics/'+img)
    imga.save(r'bmps/'+img[:-3]+'bmp')
    width, height = imga.size
    widths.append(width)
    heights.append(height)

    sizes.append(os.path.getsize(r'bmps/'+img[:-3]+'bmp')/1000)

avg_w = sum(widths)/len(widths)
avg_h = sum(heights)/len(heights)
avg_s = sum(sizes)/len(sizes)

ssd_w = statistics.stdev(widths)
ssd_h = statistics.stdev(heights)
ssd_s = statistics.stdev(sizes)

print(avg_w, ssd_w, sep=", ")
print(avg_h, ssd_h, sep=", ")
print(avg_s, ssd_s, sep=", ")
