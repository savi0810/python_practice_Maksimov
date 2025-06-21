import argparse
from form_manager import FormManager
from constants import COMMAND_NAME, INVALID_COMMAND

def main():
    parser = argparse.ArgumentParser()
    parser.add_argument('command', type=str)
    args, unknown = parser.parse_known_args()
    if args.command != COMMAND_NAME:
        print(INVALID_COMMAND)
        return
    
    query_params = {}
    current_key = None
    for arg in unknown:
        if arg.startswith('--'):
            if current_key is not None:
                query_params[current_key] = " ".join(query_params[current_key])
            
            key_value = arg[2:].split('=', 1)
            current_key = key_value[0]
            query_params[current_key] = [key_value[1]] if len(key_value) > 1 else []
        else:
            if current_key is not None:
                query_params[current_key].append(arg)
    
    if current_key is not None:
        query_params[current_key] = " ".join(query_params[current_key])
    
    manager = FormManager()
    result = manager.process_query(query_params)
    print(result)

if __name__ == "__main__":
    main()
