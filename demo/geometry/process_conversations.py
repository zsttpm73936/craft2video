import json

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

def process_json_file(input_filename, output_filename):
    with open(input_filename, 'r', encoding='utf-8') as file:
        data = json.load(file)

    for conversation in data:
        conversation['conversation'] = merge_human_messages(conversation['conversation'])

    with open(output_filename, 'w', encoding='utf-8') as file:
        json.dump(data, file, ensure_ascii=False, indent=4)

def main():
    input_filename = 'all_conversations1.json'
    output_filename = 'processed_conversations.json'
    process_json_file(input_filename, output_filename)

if __name__ == "__main__":
    main()
