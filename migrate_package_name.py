import os
import re

def find_build_gradle_files():
    build_gradle_files = []
    for root, _, files in os.walk("."):
        for file in files:
            if file == "build.gradle":
                build_gradle_files.append(os.path.join(root, file))
    return build_gradle_files

def get_package_name_from_manifest(manifest_path):
    with open(manifest_path, "r") as file:
        content = file.read()
        match = re.search(r'package="([^"]*)"', content)
        if match:
            return match.group(1)
    return None

def add_namespace_to_build_gradle(build_gradle_path, package_name):
    with open(build_gradle_path, "a") as file:
        file.write(f"\nandroid {{\n    namespace = '{package_name}'\n}}\n")

def main():
    build_gradle_files = find_build_gradle_files()
    for build_gradle_file in build_gradle_files:
        module_dir = os.path.dirname(build_gradle_file)
        manifest_path = os.path.join(module_dir, "src", "main", "AndroidManifest.xml")
        if os.path.exists(manifest_path):
            package_name = get_package_name_from_manifest(manifest_path)
            if package_name:
                add_namespace_to_build_gradle(build_gradle_file, package_name)
                print(f"Updated {build_gradle_file} with namespace '{package_name}'")
            else:
                print(f"Could not find package name in {manifest_path}")
        else:
            print(f"Could not find AndroidManifest.xml for {build_gradle_file}")

if __name__ == "__main__":
    main()
