import subprocess
import json
import speedtest
import socket

def word_string(word, text):
    return word in text

def remove_keyword(command, keyword):
    index = command.find(keyword)
    return command[index + len(keyword):].strip() if index != -1 else ""


def get_text_after_keyword(keyword, text):
    keyword = keyword.strip()  
    if keyword in text:
        return text.split(keyword, 1)[1].strip() 


def run_script(env_path, script_path):
    try:
        command = f"bash -c 'source {env_path}/bin/activate && python {script_path} && deactivate'"
        subprocess.run(command, shell=True, check=True)
        print("Script executado com sucesso!")
    except subprocess.CalledProcessError as e:
        print("Erro ao executar o script!")
        print(e)

def add_to_json(json_file, new_data):
    try:
        with open(json_file, 'r', encoding='utf-8') as file:
            try:
                data = json.load(file)
            except json.JSONDecodeError:
                data = []
        
        if isinstance(data, list):
            data.append(new_data)
        else:
            raise ValueError("The JSON file does not contain a list.")
        
        with open(json_file, 'w', encoding='utf-8') as file:
            json.dump(data, file, ensure_ascii=False, indent=4)
        print("Data added successfully!")
    
    except FileNotFoundError:
        print(f"The file {json_file} was not found.")
    except Exception as e:
        print(f"Error adding data: {e}")