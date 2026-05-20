import os

# Create directory structure
base_path = r"c:\Users\Vetle.ITK\OneDrive - Innlandet fylkeskommune\Gjevre, Audun sine filer - Vetle\OppgaverFraAudun\Prøver\Ny mappe"

directories = [
    'templates',
    'templates/components',
    'static',
    'static/css',
    'static/js',
    'db',
]

for dir_path in directories:
    full_path = os.path.join(base_path, dir_path)
    os.makedirs(full_path, exist_ok=True)
    print(f"Created: {full_path}")

print("All directories created successfully!")
