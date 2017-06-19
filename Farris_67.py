#!/usr/bin/python
from __future__ import absolute_import, division, print_function, unicode_literals
""" Starting from Frank Farris book Creating Symmetry p 67 
via Peter Farrell aka Hacking Math """
import demo
import pi3d
import pickle

class Param(object):
  def __init__(self, name, u_num, val, incr=0.1):
    self.name = name
    self.u_num = u_num
    self.val = val
    self.incr = incr
  def __getstate__(self):
    ''' this and __setstate__() needed for pickling diy classes '''
    return {'name': self.name, 'u_num':self.u_num, 'val':self.val, 'incr':self.incr}
  def __setstate__(self, state):
    self.name = state['name']
    self.u_num = state['u_num']
    self.val = state['val']
    self.incr = state['incr']

def reset_f_list():
  global f_list
  # 33=>11,0 34=>11,1 35=>11,2 36=>12,0 # conversion to vec3 locations in shader
  # 37=>12,1 38=>12,2 39=>13,0 40=>13,1
  # 41=>13,2 42=>14,0 43=>14,1 44=>14,2
  # 45=>15,0 46=>15,1 47=>15,2 48=>16,0
  # 49=>16,1
  f_list = [Param('L-n1', 33, 1.0), Param('L-m1', 34, 4.0), Param('L-ar1', 35, -0.2, 0.01), Param('L-ai1', 36, 0.2,0.01),
            Param('L-n2', 37, -5.0), Param('L-m2', 38, -2.0), Param('L-ar2', 39, 0.1, 0.01), Param('L-ai2', 40, 0.2, 0.01),
            Param('R-n1', 41, 1.0), Param('R-m1', 42, 4.0), Param('R-ar1', 43, -0.2, 0.01), Param('R-ai1', 44, 0.2,0.01),
            Param('R-n2', 45, -5.0), Param('R-m2', 46, -2.0), Param('R-ar2', 47, 0.1, 0.01), Param('R-ai2', 48, 0.2, 0.01),
            Param('R-rot', 49, 0.0)]

try: # if previously saved by pressing 's'
  with open('dump.pkl', 'rb') as f:
    f_list = pickle.load(f)
except:
  reset_f_list()

DISPLAY = pi3d.Display.create(x=50, y=50, frames_per_second=30)
CAMERA = pi3d.Camera() # for 3D projection - box
CAMERA2D = pi3d.Camera(is_3d=False) # for 2D projection - background and text display
shader = pi3d.Shader("shaders/farris_p67b") # try the different shaders, explanation in the files
tex = pi3d.Texture("dahlia2.jpg") # load different images
box = pi3d.Cuboid(camera=CAMERA, x=0, y=0, z=2.2)
box.set_draw_details(shader,[tex])

backplane = pi3d.ImageSprite(tex, camera=CAMERA2D, shader=shader, 
                  w=DISPLAY.width, h=DISPLAY.width, z=7000.0) # see FAQ explanation of z

i = 0
pointFont = pi3d.Font('fonts/NotoSans-Regular.ttf', background_color=(0, 0, 0, 0))
text = pi3d.PointText(pointFont, CAMERA2D, max_chars=200, point_size=64)
f_txt = pi3d.TextBlock(-700, -380, 0.1, 0.0, 25, spacing='F', space=0.1, 
        text_format='{} => {: 4.3g}    '.format(f_list[i].name, f_list[i].val))
text.add_text_block(f_txt)
for f in f_list:
  box.unif[f.u_num] = f.val
  backplane.unif[f.u_num] = f.val

mouse = pi3d.Mouse(restrict = False)
mouse.start()
m_start = mouse.position()
#       in  basic shader - type_a shader
F = 1.0  # scale texcoord
dt = DT = 0.005   

fr = 2014

mykeys = pi3d.Keyboard()
while DISPLAY.loop_running():
  F += dt
  if F > 4.0 and dt > 0.0:
    dt = -DT
  elif F < 0.1 and dt < 0.0:
    dt = DT
  m_pos = mouse.position()
  box.rotateIncX(0.051)
  box.rotateIncY(0.171)
  box.draw()
  text.draw()
  backplane.draw()

  k = mykeys.read()
  ch = False
  if k == 27:
    mykeys.close()
    DISPLAY.destroy()
    break
  elif k == 261 or k == 137: # rgt
    f_list[i].val += f_list[i].incr
    ch = True
  elif k == 260 or k == 136: # lft
    f_list[i].val -= f_list[i].incr
    ch = True
  elif k == 259 or k == 134: # up
    i += 1
    if i >= len(f_list):
      i = 0
    ch = True
  elif k == 258 or k == 135: # dwn
    i -= 1
    if i < 0:
      i = len(f_list) - 1
    ch = True
  elif k == ord('s'):
    with open('dump.pkl', 'wb') as f:
      pickle.dump(f_list, f)
  elif k == ord('r'):
    reset_f_list()
    for f in f_list:
      box.unif[f.u_num] = backplane.unif[f.u_num] = f.val
  if ch:
    f = f_list[i]
    f_txt.set_text('{} => {: 4.3g}    '.format(f.name, f.val))
    text.regen()
    box.unif[f.u_num] = backplane.unif[f.u_num] = f.val
  #
  pi3d.screenshot("/home/patrick/Downloads/Untitled Folder/scr_caps/rgus/fr{:05d}.jpg".format(fr))
  fr += 1
