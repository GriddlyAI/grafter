#version 460

layout(location = 0) in vec3 inPosition;
layout(location = 1) in vec2 inFragTextureCoords;

layout(location = 0) out vec4 outLightLevel;
layout(location = 1) out vec3 outFragTextureCoords;
layout(location = 2) out vec3 outFragTextureVariableCoords;
layout(location = 3) out flat int outRenderInventory;

out gl_PerVertex {
    vec4 gl_Position;
};

struct GlobalVariable {
    int value;
};

struct ObjectVariable {
    int value;
};

struct PlayerInfo {
    vec4 playerColor;
};

struct ObjectData {
    mat4 modelMatrix;
    vec4 color;
    vec2 textureMultiply;
    int textureIndex;
    int objectType;
    int playerId;
    int zIdx;
};

layout(std140, binding = 1) uniform EnvironmentData {
    mat4 projectionMatrix;
    mat4 viewMatrix;
    vec2 gridDims;
    int playerId;
    int globalVariableCount;
    int objectVariableCount;
    int highlightPlayers;
}
environmentData;

layout(std430, binding = 2) readonly buffer PlayerInfoBuffer {
    PlayerInfo variables[];
}
playerInfoBuffer;

layout(std430, binding = 3) readonly buffer ObjectDataBuffer {
    uint size;
    ObjectData variables[];
}
objectDataBuffer;

layout(std430, binding = 4) readonly buffer GlobalVariableBuffer {
    GlobalVariable variables[];
}
globalVariableBuffer;

layout(std430, binding = 5) readonly buffer ObjectVariableBuffer {
    ObjectVariable variables[];
}
objectVariableBuffer;

layout(push_constant) uniform PushConsts {
    int idx;
}
pushConsts;

#define PI 3.1415926538

/* Texture indexes

1 = 0
2 = 1
3 = 2
4 = 3
5 = 4
6 = 5
7 = 6
8 = 7
9 = 8
drink = 17
energy = 18
food = 20
health = 23
log = 28
stone = 40
stone_pickaxe = 41
stone_sword = 42
coal = 13
iron = 24
iron_pickaxe = 26
iron_sword = 27
wood_pickaxe = 46
wood_sword = 47
*/


void main() {
    ObjectData object = objectDataBuffer.variables[pushConsts.idx];

    float steps = float(globalVariableBuffer.variables[0].value);

    int health = int(globalVariableBuffer.variables[16].value);
    int food = int(globalVariableBuffer.variables[13].value);
    int drink = int(globalVariableBuffer.variables[14].value);
    int energy = int(globalVariableBuffer.variables[15].value);

    int wood = int(globalVariableBuffer.variables[10].value);
    int stone = int(globalVariableBuffer.variables[8].value);
    int coal = int(globalVariableBuffer.variables[9].value);
    int iron = int(globalVariableBuffer.variables[11].value);

    mat4 mvp = environmentData.projectionMatrix * environmentData.viewMatrix * object.modelMatrix;

    vec4 pos = mvp * vec4(
    inPosition.x,
    inPosition.y,
    inPosition.z,
    1.);

    gl_Position = pos;



    if (gl_Position.y >= 15.0/9.0 - 1.0 && (gl_Position.y <= 15.0/9.0 - 1.0 && inPosition.y == -0.5 || gl_Position.y <= 17.0/9.0 - 1.0 && inPosition.y == 0.5)) {

        outRenderInventory = 1;

        outLightLevel = vec4(1);

        int inventoryTexture;
        int inventoryValueTexture;
        if (gl_Position.x  <= 1.0/9.0 - 1 && inPosition.x == -0.5 || gl_Position.x <= 3.0/9.0 - 1 && inPosition.x == 0.5) {
            inventoryTexture = 23;
            inventoryValueTexture = health;
        } else if (gl_Position.x <= 3.0/9.0 - 1 && inPosition.x == -0.5 || gl_Position.x <= 5.0/9.0 - 1.0 && inPosition.x == 0.5) {
            inventoryTexture = 20;
            inventoryValueTexture = food;
        } else if (gl_Position.x <= 5.0/9.0 - 1.0 && inPosition.x == -0.5 || gl_Position.x <= 7.0/9.0 - 1.0 && inPosition.x == 0.5) {
            inventoryTexture = 17;
            inventoryValueTexture = drink;
        } else if (gl_Position.x <= 7.0/9.0 - 1.0 && inPosition.x == -0.5 || gl_Position.x <= 9.0/9.0 - 1.0 && inPosition.x == 0.5) {
            inventoryTexture = 18;
            inventoryValueTexture = energy;
        } else if (gl_Position.x <= 9.0/9.0 - 1.0 && inPosition.x == -0.5 || gl_Position.x <= 11.0/9.0 - 1.0 && inPosition.x == 0.5) {
            inventoryTexture = 0;
            inventoryValueTexture = 0;

        } else if (gl_Position.x <= 11.0/9.0 - 1.0 && inPosition.x == -0.5 || gl_Position.x <= 13.0/9.0 - 1.0 && inPosition.x == 0.5) {
            inventoryTexture = 28;
            inventoryValueTexture = wood;
        } else if (gl_Position.x <= 13.0/9.0 - 1.0 && inPosition.x == -0.5 || gl_Position.x <= 15.0/9.0 - 1.0 && inPosition.x == 0.5) {
            inventoryTexture = 40;
            inventoryValueTexture = stone;
        } else if (gl_Position.x <= 15.0/9.0 - 1.0 && inPosition.x == -0.5 || gl_Position.x <= 17.0/9.0 - 1.0 && inPosition.x == 0.5) {
            inventoryTexture = 13;
            inventoryValueTexture = coal;
        } else if (gl_Position.x <= 17.0/9.0 - 1.0 && inPosition.x == -0.5 || gl_Position.x <= 19.0/9.0 - 1.0 && inPosition.x == 0.5) {
            inventoryTexture = 24;
            inventoryValueTexture = iron;
        }

        if (inventoryValueTexture == 0) {
            outLightLevel = vec4(0);
        }

        outFragTextureCoords = vec3(
        inFragTextureCoords.x,
        inFragTextureCoords.y,
        inventoryTexture);

        outFragTextureVariableCoords = vec3(
        inFragTextureCoords.x,
        inFragTextureCoords.y,
        inventoryValueTexture);

    } else {

        outRenderInventory = 0;

        float lightLevel = clamp(cos(PI*steps/360)+1.0, 0.0, 1.0);
        outLightLevel = vec4(lightLevel, lightLevel, lightLevel, 1.0);

        outFragTextureCoords = vec3(
        inFragTextureCoords.x * object.textureMultiply.x,
        inFragTextureCoords.y * object.textureMultiply.y,
        object.textureIndex);
    }


}