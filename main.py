from fastapi import FastAPI, Request, Form
from fastapi.templating import Jinja2Templates
from fastapi.staticfiles import StaticFiles
from ai import ask_ai, analyze_message
import sqlite3

app = FastAPI()
app.mount("/static", StaticFiles(directory="static"), name="static")

templates = Jinja2Templates(directory="templates")

def init_db():
    conn = sqlite3.connect("jobmentor.db")
    cursor = conn.cursor()

    cursor.execute("""
        CREATE TABLE IF NOT EXISTS chat_logs (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            message TEXT,
            ai_reply TEXT,
            category TEXT,
            root_cause TEXT
        )
    """)

    conn.commit()
    conn.close()

init_db()

@app.get("/")
def home(request: Request):
    return templates.TemplateResponse(
        request=request, 
        name="chat.html",
        context={}    
    )

@app.post("/chat")
def chat(request: Request, message: str = Form(...)):
    
    ai_reply = ask_ai(message)
    category, root_cause = analyze_message(message)

    conn = sqlite3.connect("jobmentor.db")
    cursor = conn.cursor()

    cursor.execute("INSERT INTO chat_logs (message, ai_reply, category, root_cause) VALUES (?, ?, ?, ?)",
                   (message, ai_reply, category, root_cause)
    )

    conn.commit()
    conn.close()

    conn = sqlite3.connect("jobmentor.db")
    cursor = conn.cursor()

    cursor.execute("SELECT message, ai_reply, category, root_cause FROM chat_logs ORDER BY id DESC")
    logs = cursor.fetchall()

    conn.close()

    return templates.TemplateResponse(
        request=request,
        name="chat.html",
        context={  
            "message": message,
            "ai_reply": ai_reply,
            "category": category,
            "root_cause": root_cause,
            "logs": logs

        }
    )

@app.get("/dashboard")
def dashboard(request: Request):
    conn = sqlite3.connect("jobmentor.db")
    cursor = conn.cursor()

    cursor.execute("""
        SELECT category, COUNT(*)
        FROM chat_logs
        WHERE category IS NOT NULL
            AND category != 'None'
        GROUP BY category
        ORDER BY COUNT(*) DESC
    """)

    category_counts = cursor.fetchall()

    total = sum(count for _, count in category_counts)

    analysis_data = ""
    if total > 0:
        for category, count in category_counts:
            percent = count / total * 100
            analysis_data += f"{category}: {count}件 ({percent:.1f}%)\n"
    else:
        analysis_data = "相談データはありません。"

    cursor.execute("""
    SELECT message
    FROM chat_logs
    ORDER BY id DESC
    LIMIT 30
    """)
    logs = cursor.fetchall()

    conn.close()

    logs_text = "\n".join([log[0] for log in logs])

    business_analysis = ask_ai(f"""

    以下はカテゴリ別の相談割合です
    {analysis_data}                              

    以下は相談履歴です。       
    {logs_text}
    
    この相談割合と相談履歴を分析し、割合が高いカテゴリから優先順位をつけて、企業向けに改善案を出して下さい。
    『出力形式』
    ▪️ 優先課題
    ・最もわりあいが高いカテゴリと割合
    ・2番目に割合が高いカテゴリと割合

    ▪️ 根拠
    ・相談履歴から見える理由

    ▪️ 改善提案
    ・優先度が高い順に提案
    
    ▪️ 期待できる効果
    ・
    相談内容から根拠を考え、決めつけでなく分析して下さい。
    回答は300文字以内
    """)
    
    return templates.TemplateResponse(
        request=request,
        name="dashboard.html",
        context={
            "category_counts": category_counts,
            "top_category": category_counts[0][0] if category_counts else "",
            "top_count": category_counts[0][1] if category_counts else 0,
            "business_analysis": business_analysis
        }
    )

    