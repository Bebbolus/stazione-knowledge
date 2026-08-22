import os
import re
import yaml
import json

def parse_markdown_file(filepath):
    with open(filepath, 'r', encoding='utf-8') as f:
        content = f.read()

    # Parse Frontmatter
    frontmatter = {}
    aliases = []
    resources = []
    frontmatter_match = re.match(r'^---\s*\n(.*?)\n---\s*\n', content, re.DOTALL)
    body_content = content
    if frontmatter_match:
        try:
            frontmatter = yaml.safe_load(frontmatter_match.group(1))
            aliases = frontmatter.get('aliases', [])
            resources = frontmatter.get('resources', [])
        except Exception as e:
            print(f"Error parsing frontmatter in {filepath}: {e}")
        body_content = content[frontmatter_match.end():]

    # Find H1
    h1_match = re.search(r'^#\s+(.+)$', body_content, re.MULTILINE)
    title = ""
    if h1_match:
        title = h1_match.group(1).strip()
        body_content = body_content[h1_match.end():]

    # First paragraph (Inverted Pyramid) -> Now takes all content before the first H2
    first_h2_match = re.search(r'^##\s+', body_content, re.MULTILINE)
    if first_h2_match:
        inverted_pyramid = body_content[:first_h2_match.start()].strip()
    else:
        inverted_pyramid = body_content.strip()

    # Extract all entities: [Name](URL) (description in Italian)
    # Regex details: [Name](URL) (description)
    entity_pattern = r'\[([^\]]+)\]\((https?://[^)]+)\)\s*\(([^)]+)\)'
    entities = []
    seen_entity_names = set()
    for match in re.finditer(entity_pattern, content):
        name = match.group(1).strip()
        url = match.group(2).strip()
        desc = match.group(3).strip()
        if name not in seen_entity_names:
            entities.append({
                "name": name,
                "url": url,
                "description": desc
            })
            seen_entity_names.add(name)

    # Parse sections
    # Find all H2 sections
    sections = []
    h2_matches = list(re.finditer(r'^##\s+(.+)$', body_content, re.MULTILINE))
    for i, match in enumerate(h2_matches):
        sec_title = match.group(1).strip()
        start = match.end()
        end = h2_matches[i+1].start() if i + 1 < len(h2_matches) else len(body_content)
        sec_content = body_content[start:end].strip()
        
        # Exclude references and labs from generic sections to keep them clean
        if "riferimenti" in sec_title.lower() or "appendice" in sec_title.lower():
            continue
            
        sections.append({
            "title": sec_title,
            "content": sec_content
        })

    # Parse labs
    labs = []
    labs_match = re.search(r'## Appendice Operativa: Laboratori Pratici\s*\n(.*)', body_content, re.DOTALL | re.IGNORECASE)
    if labs_match:
        labs_content = labs_match.group(1).strip()
        # Find numbered list items
        lab_items = re.findall(r'^\d+\.\s+(.+)$', labs_content, re.MULTILINE)
        if lab_items:
            labs = [item.strip() for item in lab_items]
        else:
            # Fallback to lines if no numbered list
            labs = [line.strip() for line in labs_content.split('\n') if line.strip()]

    result = {
        "title": title,
        "aliases": aliases,
        "inverted_pyramid": inverted_pyramid,
        "sections": sections,
        "entities": entities,
        "labs": labs
    }
    if resources:
        result["resources"] = resources
        
    return result

def main():
    docs_dir = r"c:\codeproject\Stazione\stazione-knowledge\docs"
    output_dir = r"c:\codeproject\Stazione\interactive-app\src\data"
    os.makedirs(output_dir, exist_ok=True)
    
    lessons = {}
    
    # Sort files by their Dxx code
    files = sorted(os.listdir(docs_dir))
    for filename in files:
        if filename.startswith('D') and filename.endswith('.md'):
            # Extract lesson ID from name (e.g. D01, D02b)
            parts = filename.split('-')
            lesson_id = parts[0]
            
            filepath = os.path.join(docs_dir, filename)
            print(f"Parsing {lesson_id} from {filename}...")
            lesson_data = parse_markdown_file(filepath)
            lesson_data["id"] = lesson_id
            lessons[lesson_id] = lesson_data

    output_path = os.path.join(output_path_dir := output_dir, "lessons-db.json")
    output_path = os.path.join(output_path_dir, "lessons-db.json")
    with open(output_path, 'w', encoding='utf-8') as f:
        json.dump(lessons, f, indent=2, ensure_ascii=False)
        
    print(f"Successfully compiled {len(lessons)} lessons into {output_path}")

if __name__ == '__main__':
    main()
