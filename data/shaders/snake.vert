#version 410 core

in vec2 aPos;
in vec2 aTexCoord;

out vec2 TexCoord;

uniform vec2 res;

void main() {
  vec2 ndc = aPos / res * 2.0 - 1.0;
  ndc.y = -ndc.y;
  TexCoord = aTexCoord;
  gl_Position = vec4(ndc, 0.0, 1.0);
}