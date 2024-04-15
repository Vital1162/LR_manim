from manim import *


class ThreeD(ThreeDScene):
    def construct(self):
        self.set_camera_orientation(zoom=0.6)
        text = Text("Với nhiều biến đầu vào hơn !",
                      font_size=35,font='Times New Roman',
                    should_center = False,
                    line_spacing =0.5).to_edge(UL)
        self.play(Write(text))
        axes = ThreeDAxes()

        # 3D variant of the Dot() object
        dot = Dot3D()

        self.wait()
        # # zoom out so we see the axes
        self.set_camera_orientation(zoom=0.6)

        self.play(FadeIn(axes), FadeIn(dot))

        self.wait()


        # animate the move of the camera to properly see the axes
        self.move_camera(phi=75 * DEGREES, theta=30 * DEGREES, zoom=1, run_time=1.5)

        # built-in updater which begins camera rotation
        self.begin_ambient_camera_rotation(rate=0.15)

        self.wait()
        # https://slama.dev/manim/plotting-and-3d-scenes/
        # Move the camera back to its original position
        self.move_camera(phi=0 * DEGREES, theta=270 * DEGREES, zoom=0.6,run_time=1.5)
        self.stop_ambient_camera_rotation()
        
        self.play(FadeOut(axes), FadeOut(dot))
        fomula_1 = MathTex(r"\frac{1}{1 + e^{-\left(\beta_0 + \beta_1x_1)}}")
        
        self.play(Write(fomula_1))
        
        fomula_2 = MathTex(r"\frac{1}{1 + e^{-\left(\beta_0 + \beta_1x_1 + \beta_2x_2)}}")
        text_al = Text("Đường cong của ta cũng thay đổi",
                      font_size=35,font='Times New Roman',
                    should_center = False,
                    line_spacing =0.5).to_edge(UL)
        self.play(Transform(fomula_1,fomula_2),Transform(text,text_al))
        self.wait()
        self.play(*[FadeOut(mob)for mob in self.mobjects])
