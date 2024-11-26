import requests
import pandas as pd
from tabulate import tabulate
from colorama import init, Fore, Style

# Initialize colorama for Windows
init()

def print_header(text):
    print(f"\n{Fore.GREEN}=== {text} ==={Style.RESET_ALL}")

def main():
    try:
        print_header("Fetching Research Projects")
        response = requests.get('http://127.0.0.1:8000/api/research-projects/')
        response.raise_for_status()
        
        data = response.json()
        df = pd.DataFrame(data)
        
        # 1. Summary Count
        print_header("Summary")
        print(f"Total Projects: {len(df)}")
        
        # 2. Detailed Project List
        print_header("Project Details")
        for index, row in df.iterrows():
            print(f"{Fore.CYAN}Project {index + 1}:{Style.RESET_ALL}")
            for column in df.columns:
                print(f"{column}: {row[column]}")
            print("-" * 50)
        
        # 3. Tabulated Format
        print_header("Tabulated View")
        print(tabulate(df, headers='keys', tablefmt='grid', showindex=False))
        
        # 4. Statistics (if numerical data exists)
        if df.select_dtypes(include=['float64', 'int64']).columns.any():
            print_header("Statistics")
            print(df.describe())
            
    except requests.exceptions.RequestException as e:
        print(f"{Fore.RED}Error fetching data: {e}{Style.RESET_ALL}")
    except Exception as e:
        print(f"{Fore.RED}An error occurred: {e}{Style.RESET_ALL}")

if __name__ == "__main__":
    main()