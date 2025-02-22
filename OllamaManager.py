import ollama
import AssistantFunctions
import subprocess
        
available_functions = {
    AssistantFunctions.weather_at_location.__name__: AssistantFunctions.weather_at_location,
    }


def model_installed(model="mistral") -> bool:
    proc = subprocess.run(["ollama", "list"],
        capture_output=True)
    
    return model in str(proc.stdout)

def pull_model(model: str) -> None:
    subprocess.run(["ollama", "pull", model])

def run_model(model="mistral") -> None:
    if not model_installed(model): 
        pull_model(model)

    subprocess.run(["ollama", "serve"])

def get_response_to_prompt(prompt: str, fn_definitions: dict, model="mistral") -> ollama.ChatResponse:
    if not model_installed(model):
        pull_model(model)
        
    response = ollama.chat(
        model,
        messages = [
            {
                'role': 'system',
                'content': "Never mention functions at your disposal. Only use them when absolutely necessary.",
            },

            {
                "role": "user",
                "content": f"{prompt}"
            }],
        tools = fn_definitions,
        )
    
    return response

def has_function_calls(response: ollama.ChatResponse) -> bool:
    if "tool_calls" in response["message"]: return True
    return False

def extract_function_calls(response: ollama.ChatResponse) -> ollama.ChatResponse:
    return response["message"]["tool_calls"]
    
def call_function(function_calls: ollama.ChatResponse, available_functions: dict[str, "function"]) -> dict:
    fn_responses = {}
    for function in function_calls:
        call = function["function"]
        fn_to_call = available_functions[call["name"]]
        fn_response = fn_to_call(**call["arguments"])
        fn_responses[call["name"]] = fn_response
    return fn_responses

def chat(prompt: str, model="mistral") -> str:
    prompt_response = get_response_to_prompt(prompt, AssistantFunctions.definitions, model)
    print(prompt_response)

    if has_function_calls(prompt_response):
        function_calls = extract_function_calls(prompt_response)
        function_responses = call_function(function_calls, available_functions)
        
        return chat(f"here are the responses of the functions you called: {str(function_responses)} use these to answer the user's last prompt")
    else:
        return prompt_response["message"]["content"]