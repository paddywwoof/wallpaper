#!/usr/bin/python
from __future__ import absolute_import, division, print_function, unicode_literals
""" Starting from Frank Farris book Creating Symmetry p 67 
via Peter Farrell aka Hacking Math """
import demo
import pi3d

DISPLAY = pi3d.Display.create(x=50, y=50, frames_per_second=30)
CAMERA = pi3d.Camera() # for 3D projection - box
CAMERA2D = pi3d.Camera(is_3d=False) # for 2D projection - background and text display
shader = pi3d.Shader("shaders/farris_p67a") # try the different shaders, explanation in the files
tex = pi3d.Texture("stripes2.jpg") # load different images
box = pi3d.Cuboid(camera=CAMERA, x=0, y=0, z=2.2)
box.set_draw_details(shader,[tex])

backplane = pi3d.ImageSprite(tex, camera=CAMERA2D, shader=shader, 
                  w=DISPLAY.width, h=DISPLAY.width, z=7000.0) # see FAQ explanation of z

pointFont = pi3d.Font('fonts/NotoSans-Regular.ttf')
text = pi3d.PointText(pointFont, CAMERA2D, max_chars=200, point_size=64)
F_txt = pi3d.TextBlock(-700, -100, 0.1, 0.0, 20, spacing='F', space=0.1, text_format='F')
text.add_text_block(F_txt)
F1_txt = pi3d.TextBlock(-700, -140, 0.1, 0.0, 20, spacing='F', space=0.1, text_format='F1')
text.add_text_block(F1_txt)
F2_txt = pi3d.TextBlock(-700, -180, 0.1, 0.0, 20, spacing='F', space=0.1, text_format='F2')
text.add_text_block(F2_txt)

mouse = pi3d.Mouse(restrict = False)
mouse.start()
m_start = mouse.position()
#       in  basic shader - type_a shader
F = 1.0  # scale texcoord
dt = 0.005   
F1 = 0.5      
F2 = 0.5

fr = 0

mykeys = pi3d.Keyboard()
while DISPLAY.loop_running():
  box.set_custom_data(48, [F, F1, F2]) # this is how to pass uniform variable to the shader
  backplane.set_custom_data(48, [F, F1, F2])
  """Three custom unif 
  values used by star shader to animate image
  """
  F += dt
  if F > 4.0 and dt > 0.0:
    dt = -0.001
  elif F < 0.1 and dt < 0.0:
    dt = 0.001
  m_pos = mouse.position()
  F1, F2 = (0.5 + (m - m_start[i]) / 1000 for i, m in enumerate(m_pos))
  F_txt.set_text('F  => {:04.3g}    '.format(F))
  F1_txt.set_text('F1 => {:04.3g}    '.format(F1))
  F2_txt.set_text('F2 => {:04.3g}    '.format(F2))
  box.rotateIncX(0.051)
  box.rotateIncY(0.171)
  box.draw()
  text.regen()
  text.draw()
  backplane.draw()

  k = mykeys.read()
  if k == 27:
    mykeys.close()
    DISPLAY.destroy()
    break
  elif k == ord('r'):
    F = 2.0
    m_start = mouse.position()
  #
  #pi3d.screenshot("/home/patrick/Downloads/Untitled Folder/scr_caps/rgus/fr{:05d}.jpg".format(fr))
  #fr += 1
