#!/usr/bin/env python3
"""
Script to update all agent files to use OpenRouter instead of OpenAI
"""

import os
import re
from pathlib import Path

def update_crewai_agent(file_path):
    """Update a CrewAI agent file to use OpenRouter"""
    with open(file_path, 'r', encoding='utf-8') as f:
        content = f.read()
    
    # Skip if already updated
    if 'OPENROUTER_API_KEY' in content:
        print(f"Skipping {file_path} - already updated")
        return
    
    # Add imports and OpenRouter configuration
    if 'import os' not in content:
        content = re.sub(
            r'("""[^"]*""")\n\n',
            r'\1\n\nimport os\n',
            content
        )
    
    # Add OpenRouter configuration after imports
    if 'os.environ["OPENROUTER_API_KEY"]' not in content:
        import_section_end = content.find('\n\n', content.find('from'))
        if import_section_end != -1:
            openrouter_config = '\n# Configure OpenRouter for litellm\nos.environ["OPENROUTER_API_KEY"] = os.getenv("OPENROUTER_API_KEY", "")\nos.environ["OPENROUTER_API_BASE"] = "https://openrouter.ai/api/v1"\n'
            content = content[:import_section_end] + openrouter_config + content[import_section_end:]
    
    # Update model calls
    content = re.sub(
        r'model="openai/gpt-4o"',
        r'model="openrouter/openai/gpt-4o",\n                api_key=os.getenv("OPENROUTER_API_KEY"),\n                base_url="https://openrouter.ai/api/v1"',
        content
    )
    
    with open(file_path, 'w', encoding='utf-8') as f:
        f.write(content)
    
    print(f"Updated CrewAI agent: {file_path}")

def update_langgraph_agent(file_path):
    """Update a LangGraph agent file to use OpenRouter"""
    with open(file_path, 'r', encoding='utf-8') as f:
        content = f.read()
    
    # Skip if already updated
    if 'OPENROUTER_API_KEY' in content:
        print(f"Skipping {file_path} - already updated")
        return
    
    # Add import os
    if 'import os' not in content:
        content = re.sub(
            r'("""[^"]*""")\n\n',
            r'\1\n\nimport os\n',
            content
        )
    
    # Update ChatOpenAI calls
    content = re.sub(
        r'ChatOpenAI\(model="gpt-4o"\)',
        r'''ChatOpenAI(
        model="gpt-4o",
        api_key=os.getenv("OPENROUTER_API_KEY"),
        base_url="https://openrouter.ai/api/v1",
        default_headers={
            "HTTP-Referer": os.getenv("YOUR_SITE_URL", "http://localhost:3000"),
            "X-Title": os.getenv("YOUR_SITE_NAME", "CopilotKit Demo Viewer"),
        }
    )''',
        content
    )
    
    with open(file_path, 'w', encoding='utf-8') as f:
        f.write(content)
    
    print(f"Updated LangGraph agent: {file_path}")

def main():
    """Main function to update all agent files"""
    agent_dir = Path("agent/demo")
    
    if not agent_dir.exists():
        print(f"Agent directory {agent_dir} not found")
        return
    
    # Find all agent.py files
    agent_files = list(agent_dir.glob("*/agent.py"))
    
    for agent_file in agent_files:
        print(f"Processing: {agent_file}")
        
        # Determine if it's CrewAI or LangGraph based on directory name
        if agent_file.parent.name.startswith('crewai_'):
            update_crewai_agent(agent_file)
        elif agent_file.parent.name.startswith('langgraph_'):
            update_langgraph_agent(agent_file)
        else:
            print(f"Skipping {agent_file} - unknown type")

if __name__ == "__main__":
    main()
