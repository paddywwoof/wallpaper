from __future__ import division

W = 400
H = 400
F = 2.0 # half width factor

def setup():
    global W, H, F
    size(W, H)
    background(0)
    fname = 'dahlia'
    myphoto = loadImage(fname + '.jpg')
    img = createImage(W, H, RGB)
  
    #Create coefficients of complex number a + bi
    for counter in range(W * H):
        a = -F + (counter % W) * 2.0 * F / W
        b = -F + int(counter / H) * 2.0 * F / H
        #Create complex number as vector
        p = PVector(a, b)
        #executes the important function
        q = frieze(p)
    
        #convert range of values from -W to W => 0 to 400
        x = int(map(q.x, -1.0, 1.0, 0, myphoto.width))
        iy = int(map(q.y, -1.0, 1.0, 0, myphoto.height))
    
        #get that color in "myphoto"
        c = myphoto.get(iy, x)
    
        #put that color in the new image
        img.pixels[counter] = c

    #draw image on screen
    image(img,0,0)
    save(fname + '_threefold.jpg')

#June 9, 2017
def e(angle):
    '''defining the exponential notation'''
    return PVector(cos(angle), sin(angle))

def frieze(z):
    '''from Farris, p. 67'''

    #2pi*i*y
    term1 = TWO_PI * z.y
    #2pi*i(sqrt(3)*x-y)/2
    term2 = TWO_PI * (sqrt(3) * z.x - z.y) / 2.0
    #2pi*i(-sqrt(3)*x-y)/2
    term3 = TWO_PI * (-sqrt(3) * z.x - z.y) / 2.0
    #add together
    sum1 = PVector.add(e(term1), e(term2))
    sum1.add(e(term3))
    #multiply by 1/3
    sum1.div(3.0)
    return sum1