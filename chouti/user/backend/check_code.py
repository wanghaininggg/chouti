import random
from PIL import Image, ImageDraw, ImageFont, ImageFilter


def ran_char():
    return random.choice([chr(random.randint(65, 90)), str(random.randint(0, 9))])


def rnd_color():
    return (random.randint(64, 255), random.randint(64, 255), random.randint(64, 255))


def rnd_color2():
    return (random.randint(32, 127), random.randint(32, 127), random.randint(32, 127))


def rand_dis():
    return random.choice(['^', '~', '*', '_', '.', '-'])


def create_code():
    width = 60 * 4
    height = 60
    image = Image.new('RGB', (width, height), (192, 192, 192))

    font = ImageFont.truetype('eee.ttf', 36)
    draw = ImageDraw.Draw(image)

    for x in range(0, width, 20):
        for y in range(0, height, 10):
            draw.point((x, y), fill=rnd_color())
    code = ''
    for i in range(0, 4):
        v = ran_char()
        code += v
        h = random.randint(1, height-30)
        w = width/4 * i + 10
        draw.text((w, h), v, font=font, fill=rnd_color2())
    
        for j in range(0, width, 30):
            dis = rand_dis()
            w = i * 15 + j
            h = random.randint(1, height - 30)
            draw.text((w, h), dis, font=font, fill=rnd_color())

    image.filter(ImageFilter.BLUR)
    image.save('xxx.jpg', 'png')
    return image, code


