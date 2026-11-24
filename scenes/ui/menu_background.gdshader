shader_type canvas_item;

uniform sampler2D screen_tex : hint_screen_texture, filter_linear_mipmap;
uniform float blur : hint_range(0.0, 5.0) = 1;
uniform float dim : hint_range(0.0, 1.0) = 0.25;
uniform float vignette : hint_range(0.0, 1.0) = 0.5;
uniform vec4 tint : source_color = vec4(0.02, 0.04, 0.11, 1.0);

void fragment() {
	vec3 c = textureLod(screen_tex, SCREEN_UV, blur).rgb;
	c = mix(c, tint.rgb, dim);
	float d = distance(UV, vec2(0.5));
	c = mix(c, tint.rgb * 0.5, smoothstep(0.35, 0.85, d) * vignette);
	COLOR = vec4(c, 1.0);
}