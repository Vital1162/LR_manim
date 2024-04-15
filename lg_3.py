import math
import pandas as pd
from manim import *
import os 
class DataPoint(Dot):
    def __init__(self, point: list | np.ndarray, x: float, y: float, color, **kwargs):
        super().__init__(point=point, radius=.15, color=color, **kwargs)
        self.x = x
        self.y = y
        

def create_model(data: pd.DataFrame, initial_m: float, initial_b: float) -> tuple:

    m_tracker = ValueTracker(initial_m)
    b_tracker = ValueTracker(initial_b)

    ax = Axes(
        x_range=[-0.5, 10],
        y_range=[-0.2, 1.2],
        x_axis_config={"include_tip": True, "include_numbers": False},
        y_axis_config={"include_tip": True, "include_numbers": True}
    ).shift(DOWN+0.5)

    
    # plot points
    false_points = [DataPoint(point=ax.c2p(p.x, p.y), x=p.x, y=p.y, color=RED) for p in data.itertuples() if p.y == 0.0]
    true_points = [DataPoint(point=ax.c2p(p.x, p.y), x=p.x, y=p.y, color=GREEN) for p in data.itertuples() if p.y == 1.0]
    points = [*true_points, *false_points]

    # plot function
    f = lambda x: 1.0 / (1.0 + math.exp(-(b_tracker.get_value() + m_tracker.get_value() * x)))
    plot = always_redraw(lambda: ax.plot(f, color=BLUE))

    # max line
    max_line = DashedLine(start=ax.c2p(0, 1), end=ax.c2p(10, 1), color=WHITE)

    # likelihood_lines
    likelihood_lines = [
        always_redraw(
            lambda p=p: DashedLine(
                start=p.get_center(),
                end=ax.c2p(p.x, f(p.x)),
                color=p.get_color()
            )
        )
        for p in points
    ]

    return data, m_tracker, b_tracker, ax, points, true_points, false_points, plot, f, max_line, likelihood_lines

class test(Scene):
    def construct(self):
        text = Text("Ở đây để đơn giản ta sẽ chỉ nhận đầu một đầu vào duy nhất",
                      font_size=24,font='Times New Roman',
                    should_center = False,
                    line_spacing =0.5).to_edge(UL)
        
        fomula_1 = MathTex(r"\frac{1}{1 + e^{-\left(\beta_0 + \beta_1x_1)}}")
        
        self.play(Write(VGroup(text,fomula_1)))
        self.wait()
        self.play(FadeOut(fomula_1))
        #take some example data temp
        url = r"https://raw.githubusercontent.com/thomasnield/machine-learning-demo-data/master/classification/simple_logistic_regression.csv"

        
        data, m_tracker, b_tracker, ax, points, true_points, false_points, \
            plot, f, max_line, likelihood_lines = create_model(data=pd.read_csv(url),
                                                               initial_m=0,
                                                               initial_b=0
                                                               )

        
        self.play(LaggedStartMap(Write, ax),
                  Write(max_line),
                  Write(MathTex("0") \
                        .scale(.8) \
                        .next_to(ax.c2p(0, 0), DL, buff=.2)
                        )
                  )
        self.wait()
        self.play(LaggedStartMap(Write, VGroup(*true_points)))
        self.play(LaggedStartMap(Write, VGroup(*false_points)))

        self.wait()
        loss = MathTex(r"L(x_i) = ").shift(DOWN*3.5,LEFT*3.3).scale(0.6)
        self.play(Write(loss))
        transformations = []
        fomula = MathTex(r"\prod_{i=1}^{n}\frac{1}{1 + e^{-\left(\beta_0 + \beta_1x_i)}}",color=GREEN).scale(0.5).shift(DOWN*3.5,LEFT*1.5)

        for point in true_points:
            transformations.append(Transform(point.copy(), fomula.copy()))
            
        

        # Play all the transformations simultaneously
        self.play(*transformations, run_time=0.4)

        fomula = MathTex(r"\prod_{i=1}^{n}(1 - \frac{1}{1 + e^{-\left(\beta_0 + \beta_1x_i)}})",color=RED).scale(0.6).shift(DOWN*3.5,RIGHT*1.3)

        self.wait()
        transformations.clear()
        for point in false_points:
            transformations.append((Transform(point.copy(),fomula.copy())))
        
        self.play(*transformations, run_time=0.4)
        self.wait()
        # self.play(LaggedStartMap(Write, VGroup(*likelihood_lines)))
        self.wait()
        # f = lambda x: 1.0 / (1.0 + math.exp(-(b_tracker.get_value() + m_tracker.get_value() * x)))
        # plot = always_redraw(lambda: ax.plot(f, color=BLUE))
        self.play(Write(plot))
        self.wait()
        plot.add_updater(
            lambda mob:mob.become(ax.plot(lambda x: 1.0 / (1.0 + math.exp(-(b_tracker.get_value() + m_tracker.get_value() * x))),color=BLUE))
        )
        a_number = DecimalNumber(
            m_tracker.get_value(),
            color=RED,
            num_decimal_places = 3,
            show_ellipsis =True,
        )
        
        b = MathTex(r"\beta_0 = ").next_to(ax,UP).shift(LEFT*3.2)
        
        a_number.add_updater(
            lambda mob: mob.set_value(m_tracker.get_value()).next_to(b,RIGHT),
        )
        
        b2 = MathTex(r"\beta_1 = ").next_to(ax,UP)
        b_number = DecimalNumber(
            b_tracker.get_value(),
            color=RED,
            num_decimal_places=3,
            show_ellipsis=True,
        )

        # Add an updater for b_number to update its value
        b_number.add_updater(
            lambda mob: mob.set_value(b_tracker.get_value()).next_to(b2,RIGHT),
        )
        text_al = Text("Ta cần tìm các hệ số beta sao cho phù hợp nhất với dữ liệu quan (MLE)",
                      font_size=24,font='Times New Roman',
                    should_center = False,
                    line_spacing =0.5).to_edge(UL)
        self.play(Transform(text,text_al),run_time=2)
        self.wait(2)
        self.play(Unwrite(text))
        
        m_tracker = ValueTracker(0)
        b_tracker = ValueTracker(0)
        
       
        # Add numbers to the scene
        self.add(a_number, b_number,plot)

        # Fade in animations for the numbers
        self.play(FadeIn(b),FadeIn(a_number), FadeIn(b2),FadeIn(b_number))
     
        
        self.wait()

        self.play(m_tracker.animate.set_value(0.2),b_tracker.animate.set_value(-1),run_time=2)
        self.play(m_tracker.animate.set_value(0.2),b_tracker.animate.set_value(-2),run_time=2)
        self.play(m_tracker.animate.set_value(0.3),b_tracker.animate.set_value(-2.3),run_time=2)
        self.play(m_tracker.animate.set_value(0.5),b_tracker.animate.set_value(-2.8),run_time=2)
        self.play(m_tracker.animate.set_value(0.6),b_tracker.animate.set_value(-3),run_time=2)
        self.play(m_tracker.animate.set_value(0.69267212),b_tracker.animate.set_value(-3.17576395),run_time=2)
        self.wait()
        
        
        

