precision mediump float;

varying vec2 texcoordout;

uniform sampler2D tex0;
uniform vec3 unif[20];

float TWO_PI = radians(360.0);
float INV_RT3 = inversesqrt(3.0);


vec2 eul(float angle) {
  return vec2(cos(angle), sin(angle));
}

vec2 W(float n, float m, vec2 z) {
  return (eul(TWO_PI * (n * z.x + (n  + 2.0 * m) * z.y * INV_RT3)) +
          eul(TWO_PI * (m * z.x - (2.0 * n + m) * z.y * INV_RT3)) +
          eul(TWO_PI * (-(n + m) * z.x + (n - m) * z.y * INV_RT3))) / 3.0;
}

void main(void) {
  float mix_f = smoothstep(0.2, 0.8, texcoordout.x);
  float n1 = mix(unif[11][0], unif[13][2], mix_f); 
  float m1 = mix(unif[11][1], unif[14][0], mix_f); 
  float ar1 = mix(unif[11][2], unif[14][1], mix_f); 
  float ai1 = mix(unif[12][0], unif[14][2], mix_f);
  float n2 = mix(unif[12][1], unif[15][0], mix_f); 
  float m2 = mix(unif[12][2], unif[15][1], mix_f); 
  float ar2 = mix(unif[13][0], unif[15][2], mix_f); 
  float ai2 = mix(unif[13][1], unif[16][0], mix_f);

  vec2 z = texcoordout * 3.0;
  /* This shader uses the Hexagonal lattice recipe P6 from Farris p213
  it scales using F and uses F1 and F2 as the imaginary components of the
  two a factors. There are just four Ws 1,4 -1,-4 -5,-2 5,2 
  */
  vec2 w1 = W(n1, m1, z) + W(-n1, -m1, z);
  vec2 w2 = W(n2, m2, z) + W(-n2, -m2, z);
  vec2 uv_coord = vec2(ar1 * w1.x - ai1 * w1.y + ar2 * w2.x - ai2 * w2.y,
                       ar1 * w1.y + ai1 * w1.x + ar2 * w2.y + ai2 * w2.x);
  float c_angl = mix_f * unif[16][1];
  mat2 rotn = mat2(cos(c_angl), sin(c_angl),
                  -sin(c_angl), cos(c_angl)); 
  gl_FragColor = texture2D(tex0, rotn * (uv_coord - vec2(0.5)) + vec2(0.5));

}

