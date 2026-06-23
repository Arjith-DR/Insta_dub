import pathlib
import re

root = pathlib.Path(__file__).resolve().parent.parent
count = 0
for p in root.rglob('*.py'):
    text = p.read_text(encoding='utf-8')
    new_text = re.sub(r'\bfrom\s+INSTA\.', 'from ', text)
    new_text = re.sub(r'\bimport\s+INSTA\.', 'import ', new_text)
    if new_text != text:
        p.write_text(new_text, encoding='utf-8')
        count += 1
print(f'Updated {count} files')
