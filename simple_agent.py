#!/usr/bin/env python3
"""
Simple Agent - 一个基础的对话Agent
使用OpenAI兼容API调用LLM（纯标准库实现，无需额外依赖）
"""

import os
import json
import urllib.request
import urllib.error

class SimpleAgent:
    def __init__(self):
        self.base_url = os.environ.get("OPENAI_BASE_URL")
        self.api_key = os.environ.get("OPENAI_API_KEY")
        self.model = "claude-opus-4-5-20251101"
        self.messages = []
        self.system_prompt = "你是一个有帮助的AI助手。"

        if not self.base_url or not self.api_key:
            raise ValueError("请设置环境变量 OPENAI_BASE_URL 和 OPENAI_API_KEY")

    def chat(self, user_input: str) -> str:
        """发送消息并获取响应"""
        self.messages.append({"role": "user", "content": user_input})

        payload = {
            "model": self.model,
            "messages": [
                {"role": "system", "content": self.system_prompt},
                *self.messages
            ],
            "max_tokens": 1000
        }

        headers = {
            "Authorization": f"Bearer {self.api_key}",
            "Content-Type": "application/json"
        }

        try:
            data = json.dumps(payload).encode("utf-8")
            req = urllib.request.Request(
                f"{self.base_url}/chat/completions",
                data=data,
                headers=headers,
                method="POST"
            )

            with urllib.request.urlopen(req, timeout=60) as response:
                result = json.loads(response.read().decode("utf-8"))

            assistant_message = result["choices"][0]["message"]["content"]
            self.messages.append({"role": "assistant", "content": assistant_message})

            return assistant_message

        except urllib.error.URLError as e:
            return f"请求错误: {e}"
        except (KeyError, IndexError, json.JSONDecodeError) as e:
            return f"解析响应错误: {e}"
    
    def reset(self):
        """重置对话历史"""
        self.messages = []
        print("对话已重置")

def main():
    """主函数 - 交互式对话"""
    print("=" * 50)
    print("Simple Agent - 简单对话助手")
    print("=" * 50)
    print("命令: 'quit' 退出, 'reset' 重置对话")
    print("-" * 50)
    
    try:
        agent = SimpleAgent()
    except ValueError as e:
        print(f"初始化失败: {e}")
        return
    
    while True:
        try:
            user_input = input("\n你: ").strip()
            
            if not user_input:
                continue
            if user_input.lower() == "quit":
                print("再见!")
                break
            if user_input.lower() == "reset":
                agent.reset()
                continue
            
            print("\nAgent: ", end="", flush=True)
            response = agent.chat(user_input)
            print(response)
            
        except KeyboardInterrupt:
            print("\n\n再见!")
            break

if __name__ == "__main__":
    main()
