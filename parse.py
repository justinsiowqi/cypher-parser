import re
import json
import subprocess


# Use Libcypher Parser to Parse the Cypher Statement
def run_cypher_lint(cyp_file_path):
    try:
        # Execute the cypher-lint command
        result = subprocess.run(
            ['cypher-lint', '-a', cyp_file_path],
            check=True,
            stdout=subprocess.PIPE,
            stderr=subprocess.PIPE,
            text=True
        )
        return result.stdout
    except subprocess.CalledProcessError as e:
        print("Error running cypher-lint:", e.stderr)
        return None

if __name__ == "__main__":
    
    # Use Libcypher Parser to Parse the Cypher Statement
    cyp_file = 'sample.cyp'
    output = run_cypher_lint(cyp_file)
    print(output)
