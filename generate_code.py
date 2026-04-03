import pandas as pd
import openai
import time

# 设置API密钥
# openai.api_base = 'https://one.opengptgod.com/v1'
# openai.api_key="sk-stxknfDHd1T3VdeB64E30c45F199430a90A692CcA0359eFe"  # 替换为你的API密钥

openai.api_base = 'https://api.pumpkinaigc.online/v1'
openai.api_key = "sk-0CWkNk0GQj590n7N6688F6F1Ee72426d9fCcE4093051315d"
    
def generate_solution_from_problem(math_problem, model="gpt-4", attempt=0, max_retries=3):
    try:
        # 生成解题过程的提示
        prompt = f"""用英文一步一步给出以下数学题的详细解题过程。
                    示例：
                    数学题：求函数$f(x) = x^2 - 4x + 3$的顶点，并画出其图像。
                    解题过程: 1.Derive the Function: First, we find the derivative of $f(x)$, which is $f'(x) = 2x - 4$.
                        2.Find the Zero of the Derivative: Setting $f'(x) = 0$, we solve for $x$ and get $x = 2$. This means the function has an extremum at $x = 2$.
                        3.Compute the $y$ Coordinate of the Vertex: Substituting $x = 2$ into the original function, we get $f(2) = 2^2 - 4*2 + 3 = -1$. Thus, the vertex is at $(2, -1)$.
                        4.Determine the Type of the Vertex: Since the coefficient of the quadratic term is positive, we know this vertex represents the minimum point of the function, i.e., the lowest point on the graph.
                    数学题：{math_problem}
                    解题过程：
                    """

        # 调用OpenAI API生成解题过程
        response = openai.ChatCompletion.create(
            model=model,
            messages=[
                {"role": "user", "content": prompt}
            ]
        )

        # 返回生成的解题过程
        return response['choices'][0]['message']['content']

    except (openai.error.RateLimitError, openai.error.ServiceUnavailableError, openai.error.APIError, OSError) as e:
        print(f"An error occurred: {e}.")
        if attempt < max_retries:
            print(f"Retrying... Attempt {attempt + 1} of {max_retries}")
            time.sleep(5)  # 等待5秒再重试
            return generate_solution_from_problem(math_problem, model=model, attempt=attempt + 1, max_retries=max_retries)
        else:
            print("Max retries reached. Moving to the next word.")
            return "Error: Max retries reached."

    except Exception as e:
        print(f"An unexpected error occurred: {e}. Moving to the next word.")
        return "Error: An unexpected error occurred."
    
def generate_manim_code_from_solution(solution, model="gpt-4", attempt=0, max_retries=3):
    try:
        # 生成Manim代码的提示
        prompt = f"""根据下面的解题过程,生成相应的Manim代码来展示这个解题过程中的数学函数图像和解题步骤。首先需要一步一步写出解题过程,然后要画出对应的函数图像来可视化解题方法。
                    示例：
                    解题过程:1.Derive the Function: First, we find the derivative of $f(x)$, which is $f'(x) = 2x - 4$.
                        2.Find the Zero of the Derivative: Setting $f'(x) = 0$, we solve for $x$ and get $x = 2$. This means the function has an extremum at $x = 2$.
                        3.Compute the $y$ Coordinate of the Vertex: Substituting $x = 2$ into the original function, we get $f(2) = 2^2 - 4*2 + 3 = -1$. Thus, the vertex is at $(2, -1)$.
                        4.Determine the Type of the Vertex: Since the coefficient of the quadratic term is positive, we know this vertex represents the minimum point of the function, i.e., the lowest point on the graph.
                    Manim代码:from manim import *
                            class SolveAndVisualizeFunction(Scene):
                                def construct(self):
                                    self.show_solution_steps()
                                    self.plot_function()

                                def show_solution_steps(self):
                                    steps = VGroup(
                                        Tex(r"1. Derive the function: $f'(x) = 2x - 4$"),
                                        Tex(r"2. Find the zero of the derivative: $x = 2$"),
                                        Tex(r"3. Compute the $y$ coordinate of the vertex: $f(2) = -1$"),
                                        Tex(r"4. Determine the type of the vertex: minimum point"),
                                    )
                                    steps.arrange(DOWN, aligned_edge=LEFT)
                                    for step in steps:
                                        self.play(Write(step))
                                        self.wait(1)
                                    self.play(*[FadeOut(step) for step in steps])

                                def plot_function(self):
                                    axes = Axes(
                                        x_range=[-1, 5],
                                        y_range=[-2, 6],
                                    )
                                    quadratic_graph = axes.plot(lambda x: x**2 - 4*x + 3, color=GREEN)
                                    graph_label = axes.get_graph_label(quadratic_graph, label='f(x)=x^2-4x+3')
                                    
                                    vertex_dot = Dot(axes.c2p(2, -1), color=RED)
                                    vertex_label = MathTex("(2, -1)").next_to(vertex_dot, DOWN)
                                    
                                    self.play(Create(axes), Create(quadratic_graph), Write(graph_label))
                                    self.play(FadeIn(vertex_dot), Write(vertex_label))
                                    self.wait(2)

                    解题过程：{solution}
                    Manim代码:
                    """

        # 调用OpenAI API生成Manim代码
        response = openai.ChatCompletion.create(
            model=model,
            messages=[
                {"role": "user", "content": prompt}
            ]
        )

        # 返回生成的Manim代码
        return response['choices'][0]['message']['content']
    
    except (openai.error.RateLimitError, openai.error.ServiceUnavailableError, openai.error.APIError, OSError) as e:
        print(f"An error occurred: {e}.")
        if attempt < max_retries:
            print(f"Retrying... Attempt {attempt + 1} of {max_retries}")
            time.sleep(5)  # 等待5秒再重试
            return generate_manim_code_from_solution(solution, model=model, attempt=attempt + 1, max_retries=max_retries)
        else:
            print("Max retries reached. Moving to the next word.")
            return "Error: Max retries reached."

    except Exception as e:
        print(f"An unexpected error occurred: {e}. Moving to the next word.")
        return "Error: An unexpected error occurred."
    
math_problem = "解释二项式定理并给出(n+1)^3的展开。并画出对应函数图像"
solution = generate_solution_from_problem(math_problem)
manim_code = generate_manim_code_from_solution(solution)

print("解题过程：", solution)
print("Manim代码:", manim_code)