#!/usr/bin/env python3
import argparse
import json
import os
import sys
import importlib.util
from datetime import datetime

def main():
    parser = argparse.ArgumentParser(description='Run a single benchmark task')
    parser.add_argument('--framework', required=True, help='Framework name')
    parser.add_argument('--task', required=True, help='Path to task JSON')
    parser.add_argument('--repeat', type=int, default=1, help='Repeat number')
    args = parser.parse_args()
    
    # Generate output path automatically (batch_run.py doesn't pass --output)
    task_name = os.path.basename(args.task).replace('.json', '')
    timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
    output_path = f"logs/{task_name}_{args.framework}_r{args.repeat}_{timestamp}.json"
    
    adapter_path = f"frameworks/{args.framework}_adapter.py"
    
    if not os.path.exists(adapter_path):
        print(f"ERROR: Adapter not found: {adapter_path}", file=sys.stderr)
        sys.exit(1)
    
    try:
        # Import the adapter module
        spec = importlib.util.spec_from_file_location("adapter", adapter_path)
        adapter_module = importlib.util.module_from_spec(spec)
        sys.path.insert(0, os.getcwd())
        spec.loader.exec_module(adapter_module)
        
        # Call run_task function
        if hasattr(adapter_module, 'run_task'):
            result = adapter_module.run_task(args.task)
            
            # Load task data to get task_id
            with open(args.task, 'r') as f:
                task_data = json.load(f)
            
            # Build log
            log = {
                'task_id': task_data.get('id', task_name),
                'success': True,
                'final_answer': result['final_answer'],
                'checker_details': '',
                'time_taken': result.get('time_taken', 0),
                'framework': args.framework,
                'repeat': args.repeat
            }
            
            os.makedirs(os.path.dirname(output_path), exist_ok=True)
            with open(output_path, 'w') as f:
                json.dump(log, f, indent=2)
            
            print(f"SUCCESS: {log['task_id']} -> {log['final_answer'][:50]}")
            sys.exit(0)
        else:
            raise AttributeError("run_task function not found in adapter")
            
    except Exception as e:
        # Write failure log
        log = {
            'task_id': task_name,
            'success': False,
            'final_answer': '',
            'checker_details': f'Error: {str(e)}',
            'time_taken': 0,
            'framework': args.framework,
            'repeat': args.repeat
        }
        os.makedirs(os.path.dirname(output_path), exist_ok=True)
        with open(output_path, 'w') as f:
            json.dump(log, f, indent=2)
        print(f"FAIL: {log['task_id']} -> {str(e)}")
        sys.exit(1)

if __name__ == '__main__':
    main()