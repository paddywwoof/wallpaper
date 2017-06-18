precision mediump float;

varying vec2 texcoordout;

uniform sampler2D tex0;
uniform vec3 unif[20];
//uniform float F =========> unif[16][0]
//uniform float F1 ========> unif[16][1]
//uniform float F2 ========> unif[16][2]

float TWO_PI = radians(360.0);
float INV_RT3 = 1.0 / sqrt(3.0);
float R1 = 0.5;
float R2 = 0.25;


vec2 eul(float angle) {
  return vec2(cos(angle), sin(angle));
}

vec2 W(float n, float m, vec2 z) {
  return (eul(TWO_PI * (n * z.x + (n  + 2.0 * m) * z.y * INV_RT3)) +
          eul(TWO_PI * (m * z.x - (2.0 * n + m) * z.y * INV_RT3)) +
          eul(TWO_PI * (-(n + m) * z.x + (n - m) * z.y * INV_RT3))) / 3.0;
}

void main(void) {
  float F =  unif[16][0]; // multiplied by texcoordout to increase pattern frequency
  float F1 = unif[16][1]; // imagnry part of a14 = a-1-4 (real part is const R1 0.5)
  float F2 = unif[16][2]; // imagnry part of a-5-2 = a52 (real part is const R2 0.25)
  vec2 z = texcoordout * F;
  /* This shader uses the Hexagonal lattice recipe P6 from Farris p213
  it scales using F and uses F1 and F2 as the imaginary components of the
  two a factors. There are just four Ws 1,4 -1,-4 -5,-2 5,2 
  */
  vec2 w1 = W(1.0, 4.0, z) + W(-1.0, -4.0, z);
  vec2 w2 = W(-5.0, -2.0, z) + W(5.0, 2.0, z);
  vec2 uv_coord = vec2(R1 * w1.x - F1 * w1.y + R2 * w2.x - F2 * w2.y,
                       R1 * w1.y + F1 * w1.x + R2 * w2.y + F2 * w2.x);
  gl_FragColor = texture2D(tex0, uv_coord);

}

