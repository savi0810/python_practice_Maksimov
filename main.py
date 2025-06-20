import argparse
import sys
from form_manager import FormManager
from constants import COMMAND_NAME, INVALID_COMMAND

def main():
    parser = argparse.ArgumentParser()
    parser.add_argument('command', type=str)
    args, unknown = parser.parse_known_args()
    
    if args.command != COMMAND_NAME:
        print(INVALID_COMMAND)
        sys.exit(1)
    
    # Парсинг параметров вида --ключ=значение
    query_params = {}
    for arg in unknown:
        if arg.startswith('--'):
            key_value = arg[2:].split('=', 1)
            if len(key_value) == 2:
                query_params[key_value[0]] = key_value[1]
    
    manager = FormManager()
    result = manager.process_query(query_params)
    print(result)

if __name__ == "__main__":
    main()