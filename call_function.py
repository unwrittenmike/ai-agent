from google.genai import types

from functions.get_files_info import schema_get_files_info, get_files_info
from functions.get_file_content import schema_get_file_content, get_file_content
from functions.run_python_file import schema_run_python_file, run_python_file
from functions.write_file import schema_write_file, write_file

available_functions = types.Tool(
    function_declarations=[
        schema_get_files_info,
        schema_get_file_content,
        schema_run_python_file,
        schema_write_file
    ]
)

def call_function(function_call_part, verbose=False):
    args = function_call_part.args
    args["working_directory"] = "./calculator"
    function_name = function_call_part.name
    
    if verbose:
        print(f"Calling function: {function_name}({function_call_part.args})")
    else:
        print(f" - Calling function: {function_name}")   
    
    result = None
    
    if function_name == "get_files_info":
        result = get_files_info(**function_call_part.args)

    elif function_name == "get_file_content":
        result = get_file_content(**function_call_part.args)

    elif function_name == "run_python_file":
        result = run_python_file(**function_call_part.args)

    elif function_name == "write_file":
        result = write_file(**function_call_part.args)

    else:
        return types.Content(
            role="tool",
            parts=[
                types.Part.from_function_response(
                    name=function_name,
                    response={"error": f"Unknown function: {function_name}"},
            )
        ],
    )
        
    return types.Content(
        role="tool",
        parts=[
            types.Part.from_function_response(
                name=function_name,
                response={"result": result},
            )
        ],
    )
