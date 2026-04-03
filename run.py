import subprocess
import openai
import time
from manim import *
from sympy import *
import numpy as np

openai.api_base = 'https://api.pumpkinaigc.online/v1'
openai.api_key = ""
# openai.api_key = ""

def generate_solution_from_problem(math_problem, model="gpt-4", attempt=0, max_retries=3):
    try:
        # 生成解题过程的提示
        prompt = f"""用英文一步一步给出以下数学题的详细解题过程。
                    示例：
                    数学题：求函数$f(x) = x^2 - 4x + 3$的顶点，并画出其图像。需要写出英文的解题步骤。
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

def generate_manim_code_from_problem_and_solution(math_problem, solution, model="gpt-4", attempt=0, max_retries=3):
    try:
        # 将题目和解题过程组合成一个提示
        prompt = f"""根据下面的题目和解题过程,生成相应的Manim代码来展示这个解题过程中的数学函数图像和解题步骤。首先需要拆解解题过程为多个解题步骤,生成的代码需要先展示解题步骤，然后最后一步固定是要画出对应的函数图像或者其它来可视化解题方法并且需要说明图像的含义。如果问题和解题过程不是英文,需要先转成英文。
                    示例：
                    题目: 求函数$f(x) = x^2 - 4x + 3$的顶点，并画出其图像。

                    解题方案： Derive the Function: First, we find the derivative of $f(x)$, which is $f'(x) = 2x - 4$.Find the Zero of the Derivative: Setting $f'(x) = 0$, we solve for $x$ and get $x = 2$. 
                    This means the function has an extremum at $x = 2$.Compute the $y$ Coordinate of the Vertex: Substituting $x = 2$ into the original function, we get $f(2) = 2^2 - 4*2 + 3 = -1$. Thus, the vertex is at $(2, -1)$.
                    Determine the Type of the Vertex: Since the coefficient of the quadratic term is positive, we know this vertex represents the minimum point of the function, i.e., the lowest point on the graph.
                    
                    Manim代码:from manim import *
                            class SolveAndVisualizeFunction(Scene):
                                def construct(self):
                                    self.show_solution_steps()
                                    self.plot_function()

                                def show_solution_steps(self):
                                    steps = VGroup(
                                        Tex(r"1. Derive the function: $f'(x) = 2x - 4$",font_size=24),
                                        Tex(r"2. Find the zero of the derivative: $x = 2$",font_size=24),
                                        Tex(r"3. Compute the $y$ coordinate of the vertex: $f(2) = -1$",font_size=24),
                                        Tex(r"4. Determine the type of the vertex: minimum point",font_size=24),
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

                    题目：{math_problem}

                    解题方案：{solution}

                    Manim代码:
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
            return generate_manim_code_from_problem_and_solution(math_problem, solution, model=model, attempt=attempt + 1, max_retries=max_retries)
        else:
            print("Max retries reached. Moving to the next word.")
            return "Error: Max retries reached."

    except Exception as e:
        print(f"An unexpected error occurred: {e}. Moving to the next word.")
        return "Error: An unexpected error occurred."


def write_code_to_file(code):
    with open("generated_scene.py", "w") as file:
        file.write(code)

def run_manim():
    try:
        subprocess.run(["manim", "-p", "-ql", "generated_scene.py"], check=True)
        return True  # 成功生成视频
    except subprocess.CalledProcessError:
        return False  # 生成视频失败

def main():
    max_attempts = 5  # 最大尝试次数
    attempt = 0
    success = False

    while attempt < max_attempts and not success:
        attempt += 1
        print(f"Attempt {attempt} of {max_attempts}")

        math_problem = "$已知函数 f(x)=|x-2|, g(x)=|2x+3|-|2x-1|.$\n\n<img_7>\n$若f(x+a)\\geq g(x),求a的取值范围. 并画出对应的函数图像$"
        # solution = generate_solution_from_problem(math_problem)
        # print("解题过程：", solution)
        # manim_code = generate_manim_code_from_solution(solution)
        solution = "$函数 f(x+a)的图象是由f(x)的图象向左或向右平移 |a| 个单位长度所得，由(1)中图象可知，要使 f(x+a) \\geq g(x)，则需要 f(x) 的图象向左平移 a 个单位长度，且 a>0,当 f(x+a) 的图象过点 (\\frac{1}{2},4) 时， |\\frac{1}{2}+a-2| = 4,解得 a=\\frac{11}{2} ,\\therefore 要使 f(x+a) \\geq g(x)，则 a \\geq \\frac{11}{2},$\n$\\therefore  a 的取值范围为 \\left[\\frac{11}{2},+\\infty \\right)。$\n\n"
        manim_code = generate_manim_code_from_problem_and_solution(math_problem, solution)
        print("Manim代码:", manim_code)

        write_code_to_file(manim_code)
        success = run_manim()

        if success:
            print("Video generated successfully.")
        else:
            print("Failed to generate video. Regenerating code...")

        time.sleep(5)  # 等待一段时间再尝试，避免过于频繁的请求

    if not success:
        print("Failed to generate video after maximum attempts.")


if __name__ == "__main__":
    main()
