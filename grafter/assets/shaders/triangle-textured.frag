#version 460

layout(binding = 0) uniform sampler2DArray samplerArray;

layout(location = 0) in vec4 inLightLevel;
layout(location = 1) in vec3 inFragTextureCoords;
layout(location = 2) in vec3 inFragTextureVariableCoords;
layout(location = 3) in flat int inRenderInventory;

layout(location = 0) out vec4 outFragColor;

void main() {
  if(inRenderInventory == 1) {
    vec4 valueColor = texture(samplerArray, inFragTextureVariableCoords/2.0) * inLightLevel;
    if (valueColor.w == 0) {
      outFragColor = texture(samplerArray, inFragTextureCoords) * inLightLevel;
    } else {
      outFragColor = valueColor;
    }

  } else {
    outFragColor = texture(samplerArray, inFragTextureCoords) * inLightLevel;
  }
}