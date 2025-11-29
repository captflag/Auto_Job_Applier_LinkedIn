import os
import re

# Files to process
files_to_clean = [
    # Sai Vignesh Golla files
    "modules/helpers.py",
    "modules/clickers_and_finders.py",
    "modules/validator.py",
    "modules/resumes/extractor.py",
    "modules/resumes/generator.py",
    "modules/__deprecated__/resume_generator.py",
    "modules/__deprecated__/__setup__/config.py",
    "modules/ai/openaiConnections.py",
    "modules/ai/prompts.py",
    # Divyansh Dewangan files
    "config/settings.py",
    "config/secrets.py",
    "config/search.py",
    "config/resume.py",
    "config/questions.py",
    "config/personals.py",
    "runAiBot.py"
]

# Header pattern to remove (matches both authors)
header_pattern = re.compile(
    r"'''\s*\n"
    r"Author:\s+(?:Sai Vignesh Golla|Divyansh Dewangan)\s*\n"
    r"LinkedIn:\s+https://www\.linkedin\.com/in/(?:saivigneshgolla|divyansh-dewangan)/?\s*\n"
    r"\s*\n"
    r"Copyright \(C\) 2024 (?:Sai Vignesh Golla|Divyansh Dewangan)\s*\n"
    r"\s*\n"
    r"License:\s+GNU Affero General Public License\s*\n"
    r"\s+https://www\.gnu\.org/licenses/agpl-3\.0\.en\.html\s*\n"
    r"\s+\n"
    r"GitHub:\s+https://github\.com/(?:GodsScion/Auto_job_applier_linkedIn|divyansh-dewangan/Auto_job_applier_linkedIn)\s*\n"
    r"\s*\n"
    r"version:\s+[\d.]+\s*\n"
    r"'''\s*\n",
    re.MULTILINE
)

base_dir = os.path.dirname(os.path.abspath(__file__))

for file_path in files_to_clean:
    full_path = os.path.join(base_dir, file_path)
    if os.path.exists(full_path):
        try:
            with open(full_path, 'r', encoding='utf-8') as f:
                content = f.read()
            
            # Remove the header
            new_content = header_pattern.sub('', content, count=1)
            
            if new_content != content:
                with open(full_path, 'w', encoding='utf-8') as f:
                    f.write(new_content)
                print(f"✓ Cleaned: {file_path}")
            else:
                print(f"- Skipped (no header found): {file_path}")
        except Exception as e:
            print(f"✗ Error processing {file_path}: {e}")
    else:
        print(f"✗ File not found: {file_path}")

print("\nDone! All headers removed.")
