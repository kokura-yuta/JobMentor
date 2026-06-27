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

    conn.close()

    top_category = None
    top_count = 0
    analysis = ""
    suggestion = ""


    if category_counts:
        top_category = category_counts[0][0]
        top_count = category_counts[0][1]

    if top_category == "面接":
        analysis = "面接相談が最も多く、回答準備や受け答えに課題を感じる利用者が多いと考えられます。"
        suggestion = "模擬面接・想定質問生成・回答フィードバック機能を強化する。"

    elif top_category == "ES":
        analysis = "ES相談が最も多く、応募書類の作成段階で多くの利用者が苦戦していることが分かりました。"
        suggestion = "ES添削AI・ガクチカ整理・志望動機生成機能を優先的に強化する。"

    elif top_category == "ガクチカ":
        analysis = "ガクチカ相談が最も多く、経験の整理や言語化に悩む利用者が多いことが分かりました。"
        suggestion = "経験整理・深掘り質問・成果の言語化支援を強化する。"

    elif top_category == "自己分析":
        analysis = "自己分析相談が多く、自分の強みや価値観の整理に課題がある利用者が多いと考えられます。"
        suggestion = "価値観分析・強み発見・適職診断機能を強化する。"

    else:
        analysis = "その他の相談が多いため、既存カテゴリでは分類しきれない課題が発生している可能性があります。"
        suggestion = "相談内容を再分類し、新しい支援領域の追加を検討する。"
    
    
    return templates.TemplateResponse(
        request=request,
        name="dashboard.html",
        context={
            "category_counts": category_counts,
            "top_category": top_category,
            "top_count": top_count,
            "analysis": analysis,
            "suggestion": suggestion
        }
    )

   