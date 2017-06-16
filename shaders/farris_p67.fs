precision mediump float;

varying vec2 texcoordout;

uniform sampler2D tex0;
uniform vec3 unif[20];
//uniform float F =========> unif[16][0]
//uniform float F1 ========> unif[16][1]
//uniform float F2 ========> unif[16][2]

float TWO_PI = radians(360.0);
float ROOT_3 = sqrt(3.0);
float F3 = 0.5;

vec2 eul(float angle) {
  return vec2(cos(angle), sin(angle));
}

void main(void) {
  float F =  unif[16][0]; // easier to read
  float F1 = unif[16][1];
  float F2 = unif[16][2];
  vec2 z = texcoordout * F;

  vec2 uv_coord = (eul(TWO_PI * z.y) + 
                   eul(TWO_PI * (ROOT_3 * z.x - z.y) * F1) + 
                   eul(TWO_PI * (-ROOT_3 * z.x - z.y) * F2)) / 6.0 + 0.5;
  gl_FragColor = texture2D(tex0, uv_coord);

}

