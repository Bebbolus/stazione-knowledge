import os
import re
import yaml

DOCS_DIR = r"C:\codeproject\Stazione\stazione-knowledge\docs"

RESOURCES_MAP = {
    "D01": [
        {"title": "Learn Git Branching (Simulatore Visuale)", "url": "https://learngitbranching.js.org/", "type": "lab"},
        {"title": "Obsidian Official Help", "url": "https://help.obsidian.md/", "type": "ref"}
    ],
    "D02": [
        {"title": "Corey Schafer: Python OOP Tutorial", "url": "https://www.youtube.com/watch?v=ZDa-Z5JzLYM", "type": "video"},
        {"title": "Real Python Learning Paths", "url": "https://realpython.com/learning-paths/", "type": "ref"},
        {"title": "Pytest Official Docs", "url": "https://docs.pytest.org/", "type": "ref"}
    ],
    "D02b": [
        {"title": "Docker in 100 Seconds", "url": "https://www.youtube.com/watch?v=Gjnup-PuquQ", "type": "video"},
        {"title": "Play with Docker (Simulatore)", "url": "https://labs.play-with-docker.com/", "type": "lab"}
    ],
    "D02c": [
        {"title": "LiteLLM Official Documentation", "url": "https://docs.litellm.ai/", "type": "ref"}
    ],
    "D03": [
        {"title": "SQLBolt (Esercizi SQL Interattivi)", "url": "https://sqlbolt.com/", "type": "lab"},
        {"title": "Google Data Cards Playbook", "url": "https://developers.google.com/learn/pathways/data-cards-playbook", "type": "ref"},
        {"title": "Pandas Documentation", "url": "https://pandas.pydata.org/docs/", "type": "ref"}
    ],
    "D04": [
        {"title": "Essence of Linear Algebra (3Blue1Brown)", "url": "https://www.youtube.com/watch?v=fNk_zzaMoSs&list=PLZHQObOWTQDPD3MizzM2xVFitgF8hE_ab", "type": "video"},
        {"title": "StatQuest: Statistics Fundamentals", "url": "https://statquest.org/video-index/", "type": "video"}
    ],
    "D05": [
        {"title": "Teachable Machine (Google)", "url": "https://teachablemachine.withgoogle.com/", "type": "lab"},
        {"title": "Stanford CS229: Machine Learning", "url": "https://cs229.stanford.edu/", "type": "video"}
    ],
    "D06": [
        {"title": "Scikit-Learn Tutorials", "url": "https://scikit-learn.org/stable/tutorial/index.html", "type": "ref"}
    ],
    "D07": [
        {"title": "K-Means Clustering Visualizer", "url": "https://www.naftaliharris.com/blog/visualizing-k-means-clustering/", "type": "lab"}
    ],
    "D08": [
        {"title": "TensorFlow Playground (Rete Neurale nel Browser)", "url": "https://playground.tensorflow.org/", "type": "lab"},
        {"title": "But what is a neural network? (3Blue1Brown)", "url": "https://www.youtube.com/watch?v=aircAruvnKk", "type": "video"}
    ],
    "D09": [
        {"title": "Let's build GPT: from scratch (Andrej Karpathy)", "url": "https://www.youtube.com/watch?v=kCc8FmEb1nY", "type": "video"},
        {"title": "Attention in transformers (3Blue1Brown)", "url": "https://www.youtube.com/watch?v=eMlx5fFNoYc", "type": "video"},
        {"title": "Transformer Explainer (Interattivo 3D)", "url": "https://poloclub.github.io/transformer-explainer/", "type": "lab"}
    ],
    "D10": [
        {"title": "LangChain Documentation", "url": "https://python.langchain.com/docs/get_started/introduction", "type": "ref"},
        {"title": "OSINT Framework", "url": "https://osintframework.com/", "type": "ref"}
    ],
    "D12": [
        {"title": "OpenAI Prompt Engineering Guide", "url": "https://platform.openai.com/docs/guides/prompt-engineering", "type": "ref"},
        {"title": "PromptingGuide.ai", "url": "https://www.promptingguide.ai/", "type": "ref"}
    ],
    "D12c": [
        {"title": "Anthropic Claude Prompt Engineering", "url": "https://docs.anthropic.com/claude/docs/prompt-engineering", "type": "ref"}
    ],
    "D13": [
        {"title": "Illustrating RLHF (HuggingFace Blog)", "url": "https://huggingface.co/blog/rlhf", "type": "ref"}
    ],
    "D14": [
        {"title": "OWASP Top 10 for LLMs", "url": "https://owasp.org/www-project-top-10-for-large-language-model-applications/", "type": "ref"}
    ],
    "D14b": [
        {"title": "Llama Guard (Meta)", "url": "https://ai.meta.com/research/publications/llama-guard-safeguarding-llms/", "type": "ref"}
    ],
    "D15": [
        {"title": "MLflow Documentation", "url": "https://mlflow.org/docs/latest/index.html", "type": "ref"}
    ],
    "D16": [
        {"title": "Model Context Protocol (MCP) Official Docs", "url": "https://modelcontextprotocol.io/", "type": "ref"}
    ],
    "D17": [
        {"title": "Anthropic Desktop App (Claude with MCP)", "url": "https://claude.ai/download", "type": "ref"}
    ],
    "D18": [
        {"title": "LM Studio", "url": "https://lmstudio.ai/", "type": "lab"},
        {"title": "Gradio Documentation", "url": "https://www.gradio.app/docs/", "type": "ref"}
    ]
}

def inject_resources():
    for filename in os.listdir(DOCS_DIR):
        if not filename.endswith(".md"):
            continue
            
        filepath = os.path.join(DOCS_DIR, filename)
        
        prefix_match = re.match(r"^(D\d+[a-z]?)-", filename)
        if not prefix_match:
            continue
            
        module_id = prefix_match.group(1)
        new_resources = RESOURCES_MAP.get(module_id, [])
        if not new_resources:
            continue
        
        with open(filepath, "r", encoding="utf-8") as f:
            content = f.read()
            
        frontmatter_match = re.match(r"^---\s*\n(.*?)\n---\s*\n", content, re.DOTALL)
        
        if frontmatter_match:
            try:
                frontmatter = yaml.safe_load(frontmatter_match.group(1))
            except Exception as e:
                print(f"Error reading yaml in {filename}: {e}")
                continue
                
            body = content[frontmatter_match.end():]
            
            existing_resources = frontmatter.get("resources", [])
            existing_urls = {r.get("url") for r in existing_resources if isinstance(r, dict)}
            
            for nr in new_resources:
                if nr["url"] not in existing_urls:
                    existing_resources.append(nr)
                    
            if existing_resources:
                frontmatter["resources"] = existing_resources
                
            new_yaml = yaml.dump(frontmatter, sort_keys=False, allow_unicode=True, default_flow_style=False)
            new_content = f"---\n{new_yaml}---\n{body}"
            
            with open(filepath, "w", encoding="utf-8") as f:
                f.write(new_content)
                
            print(f"Updated {filename} with {len(new_resources)} resources.")

if __name__ == "__main__":
    inject_resources()
