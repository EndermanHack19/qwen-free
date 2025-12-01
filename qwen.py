import requests
import json
import uuid

def qianwen(contents):
    
    models="tongyi-qwen3-coder-flash"
    systemPrompt="Ты - ALPHA. Модель - ALPHA-{модель} Ты должен отвечать так: APLHA: {ответ}."
    
    cookies = {
            "UM_distinctid": "...",
            "cna": "...",
            "tongyi_guest_ticket": "...",
            "xlly_s": "1",
            "tongyi_sso_ticket": "...",
            "isg": "...",
            "tfstk": "..."
        }
    
    headers = {
        "Content-Type": "application/json",
        "Origin": "https://tongyi.aliyun.com",
        "Referer": "https://tongyi.aliyun.com/qianwen",
        "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36"
    }
    
    payload = {
        "sessionId": "",
        "sessionType": "text_chat",
        "parentMsgId": "",
        "model": "",
        "mode": "chat",
        "userAction": "",
        "actionSource": "",
        "contents": [
            {"role": "system", "content": systemPrompt, "contentType": "text"},
            {"role": "user", "content": "Кто ты? Какая модель? Какая дата?", "contentType": "text"}
        ],
        "action": "next",
        "requestId": str(uuid.uuid4()).replace("-", ""),
        "params": {
            "specifiedModel": models,
            "lastUseModelList": [models],
            "recordModelName": models,
            "bizSceneInfo": {}
        },
        "topicId": str(uuid.uuid4()).replace("-", "")
    }
    
    try:
        response = requests.post(
            "https://api.qianwen.com/dialog/guest/conversation/v2",
            headers=headers,
            cookies=cookies,
            json=payload,
            stream=True,
            timeout=60
        )
        
        thinking = ""
        answer = ""
        
        for line in response.iter_lines(decode_unicode=True):
            if line and line.startswith("data: ") and line != "data: [DONE]":
                try:
                    data = json.loads(line[6:])
                    
                    if "contents" in data and data["contents"]:
                        for item in data["contents"]:
                            content_type = item.get("contentType")
                            content = item.get("content", "")
                            
                            if content_type == "think":
                                try:
                                    think_json = json.loads(content)
                                    if "content" in think_json:
                                        if data.get("incremental"):
                                            thinking += think_json["content"]
                                        else:
                                            thinking = think_json["content"]
                                except:
                                    if data.get("incremental"):
                                        thinking += content
                                    else:
                                        thinking = content
                            
                            elif content_type == "text":
                                if data.get("incremental"):
                                    answer += content
                                else:
                                    answer = content
                                    
                except Exception as e:
                    print(f"Ошибка парсинга: {e}")
        
        return {
            "thinking": thinking.strip(),
            "answer": answer.strip()
        }
    
    except Exception as e:
        return {"error": str(e)}

CYAN = '\033[96m'
YELLOW = '\033[93m'
GREEN = '\033[92m'
MAGENTA = '\033[95m'
RESET = '\033[0m'

print()
print(f"{CYAN}╔══════════════════════════════════════════════════════════╗{RESET}")
print(f"{CYAN}║{RESET}  {YELLOW}💻 Код создан:{RESET} EndermanHack19                           {CYAN}║{RESET}")
print(f"{CYAN}║{RESET}  {GREEN}🐙 GitHub:{RESET} https://github.com/AniLand-company           {CYAN}║{RESET}")
print(f"{CYAN}║{RESET}  {MAGENTA}💖 Donate:{RESET} https://clck.ru/3F2nHg                       {CYAN}║{RESET}")
print(f"{CYAN}╚══════════════════════════════════════════════════════════╝{RESET}")
print()
result = qianwen([])

if "error" in result:
    print(f"Ошибка: {result['error']}")
else:
    GRAY_ITALIC = '\033[90;2;3m'
    BLUE = '\033[94m'
    RESET = '\033[0m'
    
    print(f"{MAGENTA}╔══════════════════════════════════════════════════════════╗{RESET}")
    print(f"{MAGENTA}║{RESET}                       💭 Ответ:                          {MAGENTA}║{RESET}")
    print(f"{MAGENTA}╚══════════════════════════════════════════════════════════╝{RESET}")

    if result.get('thinking') and result['thinking'].strip():
        print(f"{GRAY_ITALIC}{result['thinking']}{RESET}")
        print()

    print(f"{BLUE}{result['answer']}{RESET}")
    print("\n")
    print(f"{MAGENTA}╔══════════════════════════════════════════════════════════╗{RESET}")
    print(f"{MAGENTA}║{RESET}                       🔧 Модели:                         {MAGENTA}║{RESET}")
    print(f"{MAGENTA}╠══════════════════════════════════════════════════════════╣{RESET}")
    print(f"{MAGENTA}║{RESET}  {YELLOW}1.{RESET} tongyi-qwen3-max                                     {MAGENTA}║{RESET}")
    print(f"{MAGENTA}║{RESET}  {YELLOW}2.{RESET} tongyi-qwen3-max-thinking                            {MAGENTA}║{RESET}")
    print(f"{MAGENTA}║{RESET}  {YELLOW}3.{RESET} tongyi-qwen-plus-latest                              {MAGENTA}║{RESET}")
    print(f"{MAGENTA}║{RESET}  {YELLOW}4.{RESET} tongyi-qwen3-coder                                   {MAGENTA}║{RESET}")
    print(f"{MAGENTA}║{RESET}  {YELLOW}5.{RESET} tongyi-qwen3-coder-flash                             {MAGENTA}║{RESET}")
    print(f"{MAGENTA}║{RESET}  {YELLOW}Дальше сами я и так для вас написал код 😉              {MAGENTA}║{RESET}")
    print(f"{MAGENTA}╚══════════════════════════════════════════════════════════╝{RESET}")
