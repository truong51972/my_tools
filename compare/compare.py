import os
import subprocess
import sys

def read_requirements(file_path):
    with open(file_path, 'r') as file:
        reqs = {}
        for line in file:
            line = line.strip()
            if line:
                package_name, *version_info = line.split('==')
                reqs[package_name.lower()] = version_info[0] if version_info else None
        return reqs

def compare_requirements(reqs_old, reqs_new):
    new_packages = {}
    version_differences = {}
    
    for package, version in reqs_new.items():
        if package not in reqs_old:
            new_packages[package] = version
        elif reqs_old[package] != version:
            version_differences[package] = (reqs_old[package], version)

    return new_packages, version_differences

def write_comparison_to_file(new_reqs, version_diffs, output_file):
    with open(output_file, 'w') as file:
        file.write("The version is always newest by default!\n\n")
        if new_reqs:
            file.write("New scanned packages:\n")
            for item, version in new_reqs.items():
                file.write(f" - {item}=={version}\n")
        
        if version_diffs:
            file.write("\nVersion differences:\n")
            for item, (old_version, new_version) in version_diffs.items():
                file.write(f" - {item}: {old_version} -> {new_version}\n")

def run_pipreqs(output_file_name):
    try:
        subprocess.run(['pip', 'show', 'pipreqs'], check=True, stdout=subprocess.PIPE, stderr=subprocess.PIPE)
        print("pipreqs is already installed.")
    except subprocess.CalledProcessError:
        print("pipreqs not found. Installing pipreqs...")
        subprocess.run([sys.executable, '-m', 'pip', 'install', 'pipreqs'], check=True)
        print("pipreqs has been installed.")

    current_directory = os.path.dirname(os.path.abspath(__file__))
    
    command = ['pipreqs', current_directory, '--force', '--savepath', f"{output_file_name}"]
    
    try:
        subprocess.run(command, check=True)
        print(f"requirements.txt has been generated/updated in {current_directory}")
    except subprocess.CalledProcessError as e:
        print(f"An error occurred while running pipreqs: {e}")

if __name__ == "__main__":
    current_reqs = 'requirements0.txt'
    scanned_new_reqs = '.scanned_libs.txt'
    output_comparison_path = '.requirements_comparison.txt'

    run_pipreqs(scanned_new_reqs)


    reqs_old = read_requirements(current_reqs)
    reqs_new = read_requirements(scanned_new_reqs)

    new_requirements, version_differences = compare_requirements(reqs_old, reqs_new)

    write_comparison_to_file(new_requirements, version_differences, output_comparison_path)

    print(f"Comparison results have been written to '{output_comparison_path}'")
