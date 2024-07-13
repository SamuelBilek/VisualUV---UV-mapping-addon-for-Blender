import gpu

shared_functions = \
'''
    vec3 hsv2rgb(vec3 c);
    vec3 hsv2rgb(vec3 c)
    {
        // this function is from: https://gist.github.com/983/e170a24ae8eba2cd174f
        vec4 K = vec4(1.0f, 2.0f / 3.0f, 1.0f / 3.0f, 3.0f);
        vec3 p = abs(fract(c.xxx + K.xyz) * 6.0f - K.www);
        return c.z * mix(K.xxx, clamp(p - K.xxx, 0.0f, 1.0f), c.y);
    }

    float get_division(float a, float b);
    float get_division(float a, float b)
    {
        if (a == 0.0f || b == 0.0f)
        {
            return 0.0f;
        }
        if (a > b) 
        {
            return a / b;
        }
        return b / a;
    }

    float normalized_value(float value, float max_value);
    float normalized_value(float value, float max_value) 
    {
        if (value > max_value)
            {
                value = max_value;
            }
            float COLOR_BLUE = 2.0f / 3.0f;
            float MIN_DIVISION = 1.0f;
            return COLOR_BLUE - (value - MIN_DIVISION) / (max_value - MIN_DIVISION) * COLOR_BLUE;
    }
'''

# shader info for the 3D Viewport shader
vert_out = gpu.types.GPUStageInterfaceInfo("shader_interface")
vert_out.smooth('VEC2', "uvInterp")
vert_out.smooth('VEC4', "tempColor")
vert_out.smooth('FLOAT', "fragmentHue")
shader_info = gpu.types.GPUShaderCreateInfo()
shader_info.push_constant('MAT4', "viewProjectionMatrix")
shader_info.push_constant('MAT4', "worldMatrix")

shader_info.typedef_source("struct UBO_3D {float hue_shift; \
                                            float hue_multiply; \
                                            float saturation; \
                                            float value; \
                                            float alpha; \
                                            float scale_factor; \
                                            int tex_enabled; \
                                            int tex_only; \
                                            float vert_offset; \
                                            float x_offset; \
                                            float y_offset; \
                                            float z_offset; \
                                            float explosion_offset; \
                                            float max_division;};")
shader_info.uniform_buf(0, 'UBO_3D', "ubo_3d")

shader_info.sampler(0, 'FLOAT_2D', "image")
shader_info.vertex_in(0, 'VEC3', "position")
shader_info.vertex_in(1, 'VEC3', "normal")
shader_info.vertex_in(2, 'VEC3', "uv")
shader_info.vertex_in(3, 'VEC2', "input")
shader_info.vertex_in(4, 'VEC3', "direction")
shader_info.vertex_out(vert_out)
shader_info.fragment_out(0, 'VEC4', "FragColor")

shader_info.vertex_source(shared_functions +
'''
    void main()
    {
        float color = 0.0f;
        if (ubo_3d.max_division > 0.0f) 
        {
            color = get_division(input.x, input.y);
            color = normalized_value(color, ubo_3d.max_division);
        }
        else
        {
            color = input.x;
        }
        uvInterp = uv.xy;
        vec3 hsv = vec3(mod((color + 0.001f) * ubo_3d.hue_multiply + ubo_3d.hue_shift, 1.0), ubo_3d.saturation, ubo_3d.value);
        fragmentHue = color;
        tempColor = vec4(hsv2rgb(hsv), ubo_3d.alpha);
        vec3 location_offset = vec3(ubo_3d.x_offset, ubo_3d.y_offset, ubo_3d.z_offset);
        gl_Position = viewProjectionMatrix * worldMatrix * vec4(position + normal * ubo_3d.vert_offset + direction * ubo_3d.explosion_offset + location_offset, 1.0f);
    }

'''
)

shader_info.fragment_source(
'''
    void main()
    {
        if (tempColor.a == 0) discard;
        vec4 tex = texture(image, uvInterp / abs(ubo_3d.scale_factor));
        if (ubo_3d.tex_enabled <= 0  && fragmentHue < 0.0f)
        {
            discard;
        }
        else if (ubo_3d.tex_enabled > 0 && ubo_3d.tex_only > 0)
        {
            FragColor = vec4(tex.r, tex.g, tex.b, tempColor.a);
        }
        else if (ubo_3d.tex_enabled > 0  && fragmentHue < 0.0f)
        {
            FragColor = vec4(tex.r, tex.g, tex.b, tempColor.a);
        }
        else if (ubo_3d.tex_enabled > 0) 
        {
            FragColor = vec4(tex.r * tempColor.r, tex.g * tempColor.g, tex.b * tempColor.b, tempColor.a);
        }
        else
        {
            FragColor = tempColor;
        }
    }
'''
)

SHADER_3D = gpu.shader.create_from_info(shader_info)


# shader info for the wireframe shader
vert_out_wireframe = gpu.types.GPUStageInterfaceInfo("uv_shader_interface_wireframe")
vert_out_wireframe.smooth('VEC4', "tempColor")
shader_info_wireframe = gpu.types.GPUShaderCreateInfo()
shader_info_wireframe.push_constant('MAT4', "viewProjectionMatrix")
shader_info_wireframe.push_constant('MAT4', "worldMatrix")
shader_info_wireframe.typedef_source("struct UBO_WIRE {float x_offset; \
                                                        float y_offset; \
                                                        float z_offset; \
                                                        float explosion_offset; \
                                                        float offset;};")
shader_info_wireframe.uniform_buf(0, 'UBO_WIRE', "ubo_wire")
shader_info_wireframe.vertex_in(0, 'VEC3', "position")
shader_info_wireframe.vertex_in(1, 'VEC3', "normal")
shader_info_wireframe.vertex_in(2, 'VEC3', "direction")
shader_info_wireframe.vertex_in(3, 'VEC4', "color")
shader_info_wireframe.vertex_out(vert_out_wireframe)
shader_info_wireframe.fragment_out(0, 'VEC4', "FragColor")

shader_info_wireframe.vertex_source(
'''
    void main()
    {
        tempColor = color;
        vec3 location_offset = vec3(ubo_wire.x_offset, ubo_wire.y_offset, ubo_wire.z_offset);
        gl_Position = viewProjectionMatrix * worldMatrix * vec4(position + normal * ubo_wire.offset + direction * ubo_wire.explosion_offset + location_offset, 1.0f);
    }
'''
)

shader_info_wireframe.fragment_source(
'''
    void main()
    {
        if (tempColor.a == 0) discard;
        FragColor = tempColor;
    }
'''
)

SHADER_WIREFRAME = gpu.shader.create_from_info(shader_info_wireframe)

# shader info for the UV Editor shader
vert_out_2D = gpu.types.GPUStageInterfaceInfo("uv_shader_interface_2D")
vert_out_2D.smooth('VEC4', "tempColor")
shader_info_2D = gpu.types.GPUShaderCreateInfo()
shader_info_2D.push_constant('MAT4', "ModelViewProjectionMatrix")
shader_info_2D.typedef_source("struct UBO_COLOR {float hue_shift; \
                                                float hue_multiply; \
                                                float saturation; \
                                                float value; \
                                                float alpha; \
                                                float layer; \
                                                float max_division;};")
shader_info_2D.uniform_buf(0, 'UBO_COLOR', "ubo_color")

shader_info_2D.vertex_in(0, 'VEC3', "position")
shader_info_2D.vertex_in(1, 'VEC2', "input")
shader_info_2D.vertex_out(vert_out_2D)
shader_info_2D.fragment_out(0, 'VEC4', "FragColor")

shader_info_2D.vertex_source(shared_functions +
'''
    void main()
    {
        float color = 0.0f;
        if (ubo_color.max_division > 0.0f) 
        {
            color = get_division(input.x, input.y);
            color = normalized_value(color, ubo_color.max_division);
        }
        else
        {
            color = input.x;
        }
        gl_Position = ModelViewProjectionMatrix * vec4(position.xy, 0.0f, 1.0f);
        gl_Position.z = 0.5f * (2f - ubo_color.layer);
        vec3 hsv = vec3(mod((color + 0.001f) * ubo_color.hue_multiply + ubo_color.hue_shift, 1.0), ubo_color.saturation, ubo_color.value);
        if (color < 0) 
        {
            tempColor = vec4(0.0f);
        }
        else 
        {
            tempColor = vec4(hsv2rgb(hsv), ubo_color.alpha);
        }
    }
'''
)

shader_info_2D.fragment_source(
'''
    void main()
    {
        if (tempColor.a == 0) discard;
        FragColor = vec4(tempColor.r, tempColor.g, tempColor.b, tempColor.a);
    }
'''
)

SHADER_2D = gpu.shader.create_from_info(shader_info_2D)

# shader info for the UV Editor texture shader
vert_out_texture = gpu.types.GPUStageInterfaceInfo("uv_texture_shader_interface_2D")
vert_out_texture.smooth('VEC2', "uvInterp")
shader_info_texture = gpu.types.GPUShaderCreateInfo()
shader_info_texture.push_constant('MAT4', "ModelViewProjectionMatrix")
shader_info_texture.typedef_source("struct UBO_TEX2D {float scale_factor; \
                                                        float alpha; \
                                                        float layer;};")
shader_info_texture.uniform_buf(0, 'UBO_TEX2D', "ubo_tex2d")
shader_info_texture.sampler(0, 'FLOAT_2D', "image")
shader_info_texture.vertex_in(0, 'VEC3', "position")
shader_info_texture.vertex_out(vert_out_texture)
shader_info_texture.fragment_out(0, 'VEC4', "FragColor")

shader_info_texture.vertex_source(
'''
    void main()
    {
        uvInterp = position.xy;
        gl_Position = ModelViewProjectionMatrix * vec4(position.xy, 0.0f, 1.0f);
        gl_Position.z = 0.5 * (2f - ubo_tex2d.layer);
    }
'''
)

shader_info_texture.fragment_source(
'''
    void main()
    {
        if (ubo_tex2d.alpha == 0) discard;
        vec4 tex = texture(image, uvInterp / abs(ubo_tex2d.scale_factor));
        FragColor = vec4(tex.r, tex.g, tex.b, tex.a * ubo_tex2d.alpha);
    }
'''
)

SHADER_TEXTURE_2D = gpu.shader.create_from_info(shader_info_texture)
