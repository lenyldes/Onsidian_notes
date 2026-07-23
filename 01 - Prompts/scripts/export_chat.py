import json
import sys
import os
import datetime

conv_id = sys.argv[1]
app_dir = sys.argv[2]
out_dir = os.getcwd()

log_path = os.path.join(app_dir, "brain", conv_id, ".system_generated", "logs", "transcript_full.jsonl")
output_path = os.path.join(out_dir, f"chat_export_{conv_id[:8]}.md")

try:
    with open(log_path, 'r', encoding='utf-8') as f:
        lines = f.readlines()
        
    with open(output_path, 'w', encoding='utf-8') as out:
        out.write(f"# Chat Export (ID: {conv_id[:8]})\n\n")
        out.write(f"**Date:** {datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S')}\n\n")
        out.write("---\n\n")
        
        for line in lines:
            try:
                step = json.loads(line.strip())
            except json.JSONDecodeError:
                continue
                
            step_type = step.get('type')
            content = step.get('content', '')
            
            if not content:
                continue
                
            if step_type == 'USER_INPUT':
                out.write(f"### 🧑 Пользователь\n")
                out.write(f"{content}\n\n")
            elif step_type in ('PLANNER_RESPONSE', 'MODEL', 'AGENT_RESPONSE'):
                out.write(f"### 🤖 Antigravity\n")
                out.write(f"{content}\n\n")
                
    print(f"✅ Чат успешно экспортирован в файл: {output_path}")
except Exception as e:
    print(f"Ошибка при экспорте: {e}")
