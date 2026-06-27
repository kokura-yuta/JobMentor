from openai import OpenAI

client = OpenAI()

def ask_ai(message):
    response = client.responses.create(
        model="gpt-4.1-mini",
        input=f"""
    あなたは就活生を支援するAIコーチです。

    重要ルール：
    - すぐに答えを与えない
    - まず相談内容から考えられる原因を1〜2個だけ仮説として出す
    - その上で、原因を絞るための質問を1つだけする
    - 返答は日本語で短くする

    返答の形
    1. 考えられる原因：
    2. 確認したいこと：
    3. 今すぐやること：

    ユーザーの相談：
    {message}
    """
        )

    return response.output_text

def analyze_message(message):
    if "ES" in message or "エントリーシート" in message:
        return "ES", "内容の具体性不足"
    elif "面接" in message:
        return "面接", "回答準備不足"
    elif "ガクチカ" in message or "サッカー" in message:
        return "ガクチカ", "経験の整理不足"
    elif "自己分析" in message:
        return "自己分析", "強みの言語化不足"
    else:
        return "その他", "原因未分類"