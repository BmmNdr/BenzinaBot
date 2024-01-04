import subprocess

def install_package(package_list):
    
    for package_name in package_list:
        try:
            subprocess.check_call(['pip', 'install', package_name])
            print(f"Successfully installed {package_name}")
        except subprocess.CalledProcessError:
            print(f"Failed to install {package_name}")

# Replace 'package_name' with the actual name of the package you want to install
package_list = ["time", "os", "json", "datetime", "mysql.connector", "requests"]

install_package(package_list)