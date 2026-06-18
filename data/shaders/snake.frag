#version 410 core

in vec2 TexCoord;
out vec4 FragColor;

uniform sampler2D snakeTex;

void main() {
  vec4 texSample = texture(snakeTex, vec2(TexCoord.x, TexCoord.y));
  FragColor = texSample;
}