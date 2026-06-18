#version 410 core

in vec2 TexCoord;
out vec4 FragColor;

uniform sampler2D snakeTex;

void main() { FragColor = texture(snakeTex, TexCoord); }