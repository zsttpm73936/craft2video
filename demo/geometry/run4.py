import subprocess
import os
import glob
import json
import openai
import time

openai.api_base = ''
openai.api_key = ""

MAX_GENERATION_ATTEMPTS = 4  # Maximum attempts to generate video for each file

def generate_manim_code_from_problem_and_solution(math_problem, solution, is_physics=False, model="gpt-4", attempt=0, max_retries=MAX_GENERATION_ATTEMPTS):
    try:
        problem_type = "physics" if is_physics else "mathematics"
        prompt = f"""
Given the following {problem_type} problem and its solution, create Manim code to visually represent both the solution process and the key concepts. The code should use Manim's capabilities to create any necessary diagrams or models directly in the animation, such as cylinders or cones for geometric problems, without relying on any external images. Here are specific guidelines:

1. Start with the problem statement at the top, aligning it to the upper edge of the animation.
2. Automatically include visual diagrams or models at each step where they help visualize the concept being explained.
3. Use next_to for positioning equations and explanations, maintaining proper spacing.
4. Set the font size to 24 for all text and math elements.
5. Clearly distinguish between the problem statement and the solution process.
6. Use smooth visual transitions to ensure viewer comprehension without haste.
7. Space out text and graphics evenly to avoid clutter.
8. Intuitively interpret solution steps to include relevant diagrams or graphics such as force diagrams in physics or geometric constructions in mathematics.
9. Ensure mathematical expressions and shapes are properly displayed.
10. Manage text overflow to keep all elements on-screen.

For physics problems:
- Automatically draw force diagrams, free-body diagrams, or motion paths where applicable.

For mathematics problems:
- Automatically generate graphs, geometric constructions, or other illustrative diagrams as needed to elucidate the solution.

Enhance clarity with:
- Concise text explanations alongside relevant visuals, split into multiple lines if necessary.
- Limit each line to 10 words and each page to 10 lines.

Example Solution: {solution}

Manim code requirements:
- Interpret and visualize crucial steps using diagrams.
- Include FadeIn and corresponding FadeOut animations to prevent overlapping.

Problem: {math_problem}

Solution: {solution}

Manim Code:
"""

        response = openai.ChatCompletion.create(
            model=model,
            messages=[{"role": "user", "content": prompt}]
        )
        code = response['choices'][0]['message']['content']
        if code and not code.startswith("Error"):
            # Ensure the generated code starts with "from manim import *"
            if not code.startswith("from manim import *"):
                code = "from manim import *\n\n" + code
            return code
        else:
            raise ValueError("Failed to generate valid Manim code.")
    except Exception as e:
        if attempt < max_retries:
            print(f"Retrying to generate code... Attempt {attempt + 1}")
            time.sleep(2)  # short delay before retrying
            return generate_manim_code_from_problem_and_solution(math_problem, solution, is_physics=is_physics, model=model, attempt=attempt + 1, max_retries=max_retries)
        else:
            return f"Error: {e}"

def extract_manim_code(content):
    """Extract Manim code from the provided content"""
    start_index = content.find("```python")
    if start_index != -1:
        end_index = content.rfind("```")
        return content[start_index + 9:end_index].strip()  # Return content delimited by triple backticks
    else:
        return content  # Return all content if "```python" is not found

def merge_human_messages(conversation):
    merged_conversation = []
    buffer = []

    for message in conversation:
        if message['from'] == 'human':
            buffer.append(message['value'])
        else:
            if buffer:
                merged_conversation.append({
                    'from': 'human',
                    'value': '\n'.join(buffer)
                })
                buffer = []
            merged_conversation.append(message)

    if buffer:
        merged_conversation.append({
            'from': 'human',
            'value': '\n'.join(buffer)
        })

    return merged_conversation

def process_files():
    files = glob.glob('./geometry_data/*.json')[60:63]
    all_conversations = []

    for file_path in files:
        file_name = os.path.basename(file_path)
        base_name = os.path.splitext(file_name)[0]

        conversation = []
        conversation_id = base_name

        with open(file_path, 'r') as file:
            data = json.load(file)
            math_problem = data['problem']
            solution = data['solution']

        attempt = 0
        while attempt < MAX_GENERATION_ATTEMPTS:
            prompt = f"Generate Manim code for the following problem and solution.\n\nProblem: {math_problem}\n\nSolution: {solution}"
            conversation.append({"from": "human", "value": prompt})

            manim_code = generate_manim_code_from_problem_and_solution(math_problem, solution, attempt=attempt)
            conversation.append({"from": "gpt", "value": manim_code})

            if manim_code and not manim_code.startswith("Error"):
                manim_code = extract_manim_code(manim_code)
                print(f"Code generated successfully for {file_name}.")
                conversation.append({"from": "human", "value": "Manim code generated successfully."})
                break
            else:
                error_prompt = f"Attempt {attempt + 1}: Manim code generation failed with error:\n{manim_code}"
                conversation.append({"from": "human", "value": error_prompt})
                attempt += 1

        merged_conversation = merge_human_messages(conversation)
        all_conversations.append({
            "conversation_id": conversation_id,
            "conversation": merged_conversation
        })

    with open("all_conversations.json", 'w', encoding='utf-8') as convo_file:
        json.dump(all_conversations, convo_file, ensure_ascii=False, indent=4)

def main():
    process_files()

if __name__ == "__main__":
    main()
