from manim import *
class SolveAndVisualizeFunction(Scene):
    def construct(self):
        self.show_solution_steps()
        self.plot_functions()

    def show_solution_steps(self):
        steps = VGroup(
            Tex(r"1. $f(x+a)$ is the graph of $f(x)$ shifted by the absolute value of '|a|' to the left or right.", font_size=24),
            Tex(r"2. To make $f(x+a) \geq g(x)$, the graph of $f(x)$ should be shifted to the left by 'a' units, and a>0.", font_size=24),
            Tex(r"3. When the graph of $f(x+a)$ passes through the point $(\frac{1}{2},4)$, |$\frac{1}{2}+a-2$| = 4, solving for 'a' gives $a=\frac{11}{2}$.", font_size=24),
            Tex(r"4. Therefore, to make $f(x+a) \geq g(x)$, $a \geq \frac{11}{2}$.",font_size=24),
            Tex(r"5. The range of 'a' is [$\frac{11}{2}$ , +$\infty$).", font_size=24),
        )
        steps.arrange(DOWN, aligned_edge=LEFT)
        for step in steps:
            self.play(Write(step))
            self.wait(1)
        self.play(*[FadeOut(step) for step in steps])

    def plot_functions(self):
        axes = Axes(
            x_range=[-2, 4],
            y_range=[-5, 5],
        )
        f_graph = axes.plot(lambda x: abs(x-2), color=GREEN)
        g_graph = axes.plot(lambda x: abs(2*x+3)-abs(2*x-1), color=BLUE)

        f_label = axes.get_graph_label(f_graph, label='f(x)=|x-2|')
        g_label = axes.get_graph_label(g_graph, label='g(x)=|2x+3|-|2x-1|',x_val=-0.2)

        a_dot = Dot(axes.c2p(11/2, 0), color=RED)
        a_label = MathTex("a").next_to(a_dot, DOWN)

        self.play(Create(axes), Create(f_graph), Create(g_graph), Write(f_label), Write(g_label))
        self.play(FadeIn(a_dot), Write(a_label))
        self.wait(2)