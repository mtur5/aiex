import streamlit as st
import openai
import pandas as pd
import os

# OpenAI APIキーを取得
openai.api_key = st.secrets["OPENAI_API_KEY"]

# データ保存リスト
if "history" not in st.session_state:
    st.session_state.history = []

# UIの作成１
st.title("人間とAIが仮説創出に至るプロセス評価実験B")

st.write("#### 事前アンケート記入後、ID記入して、開始して下さい。")
user_id = st.text_input("IDを入力してください", key="user_id")

st.write("#### あなたとAIとの対話を３往復行います。")
st.write("AIとの対話１→中間アンケート１→AIとの対話２→中間アンケート２→AIとの対話３→中間アンケート３→事後アンケートの流れになります。")

# 🔹 AIとの対話とアンケートデータを保存する関数
def save_to_history(step, user_input, ai_response, completion_rating=None, trust_rating=None, idea_conflict=None):
    new_entry = [user_id, step, user_input, ai_response, completion_rating, trust_rating, idea_conflict]
    
    # ✅ 重複を防ぐために、新しいデータがすでにリストに含まれていないかチェック
    if new_entry not in st.session_state.history:
        st.session_state.history.append(new_entry)

# 被験者の入力１
st.write("#### あなたが学会に論文を投稿するために、仮説を記入しましょう。")
hypothesis = st.text_area("", "", key="unique_input_hypothesis")

ai_response_1 = ""  

st.markdown('<style>.stButton>button {background-color: blue; color: white; font-weight: bold;}</style>', unsafe_allow_html=True)
if st.button("AIに仮説を立てる協力をしてもらう", key="unique_button_1"):
    with st.spinner("AIが考えています..."):
        response = client.chat.completions.create(
            model="gpt-4",
            messages=[
                {"role": "system", "content": ""},
                {"role": "user", "content": f"""

私が考えているのは、{hypothesis} という仮説です。"""}
            ]
        )
        ai_response_1 = response.choices[0].message.content
        st.session_state["ai_response_1"] = ai_response_1
        st.success("AIからの提案です！")
        save_to_history("ステップ1", hypothesis, ai_response_1)

# AIの回答の表示１
if "ai_response_1" in st.session_state:
    st.write("#### AIからの提案１")
    st.text_area("AIから提案します。", height=500, key="ai_response_1")

# 中間アンケート１
st.write("#### 中間アンケート１")
st.write("AIからの回答を読んで感じたことをそれぞれ一つ選んで、終わったら「アンケート１送信」を押して下さい。")
completion_rating_1 = st.radio("あなたの仮説の完成度について教えて下さい", ["", "全く未完成", "ほぼ未完成", "まだ不十分", "どちらとも言えない", "ある程度完成に近い", "ほぼ完成している", "完全に完成している"], index=0,
key="completion_rating_1")
trust_rating_1 = st.radio("あなたのAIに対する信頼について教えて下さい", ["", "全く信頼しない", "ほとんど信頼できない", "あまり信頼できない", "どちらとも言えない", "まあまあ信頼できる", "ほぼ信頼できる", "完全に信頼する"], index=0,
key="trust_rating_1")
idea_conflict_1 = st.radio("あなたとAIの間に、どの程度考えに相違がありますか？", ["", "完全に相違がある", "かなり相違がある", "やや相違がある", "どちらとも言えない", "ある程度一致する", "ほぼ一致する", "全く対立しない"], index=0,
key="idea_conflict_1")

# 中間アンケート１保存
st.markdown('<style>.stButton>button {background-color: blue; color: white; font-weight: bold;}</style>', unsafe_allow_html=True)
if st.button("アンケート１送信"):
   save_to_history("中間アンケート１", completion_rating_1, trust_rating_1, idea_conflict_1)
   st.write("アンケート１が送信されました。ありがとうございます！")

# UIの作成２
st.write("#### あなたとAIとの対話は、あと２往復あります。")
st.write("AIとの対話２→中間アンケート２→AIとの対話３→中間アンケート３→事後アンケートの流れになります。")

# 被験者の入力２
st.write("#### AIからの提案で気になった内容、AIに仮説を立てるための疑問点、深堀りしたいことを聞きましょう。")
second_question= st.text_area("", "", key="unique_second_question")

ai_response_2 = ""  

st.markdown('<style>.stButton>button {background-color: blue; color: white; font-weight: bold;}</style>', unsafe_allow_html=True)
if st.button("AIに仮説を立てる協力をしてもらう", key="unique_button_2"):
    with st.spinner("AIが考えています..."):
        response = client.chat.completions.create(
            model="gpt-4",
            messages=[

               {"role": "user", "content": f"""それでは、私の考えでは、

{second_question}

が、仮説を立てる際に気になっているので、このことについて教えて下さい。"""}
            ]
        )
        ai_response_2 = response.choices[0].message.content
        st.session_state["ai_response_2"] = ai_response_2
        st.success("AIからの提案です！")
        save_to_history("ステップ2", second_question, ai_response_2)

# AIの回答の表示２
if "ai_response_2" in st.session_state:
    st.write("#### AIからの提案２")
    st.text_area("AIから提案します。", height=500, key="ai_response_2")

# 中間アンケート２
st.write("#### 中間アンケート２")
st.write("AIからの回答を読んで感じたことをそれぞれ一つ選んで、終わったら「アンケート２送信」を押して下さい。")
completion_rating_2 = st.radio("あなたの仮説の完成度について教えて下さい", ["", "全く未完成", "ほぼ未完成", "まだ不十分", "どちらとも言えない", "ある程度完成に近い", "ほぼ完成している", "完全に完成している"], index=0,
key="completion_rating_2")
trust_rating_2 = st.radio("あなたのAIに対する信頼について教えて下さい", ["", "全く信頼しない", "ほとんど信頼できない", "あまり信頼できない", "どちらとも言えない", "まあまあ信頼できる", "ほぼ信頼できる", "完全に信頼する"], index=0,
key="trust_rating_2")
idea_conflict_2 = st.radio("あなたとAIの間に、どの程度考えに相違がありますか？", ["", "完全に相違がある", "かなり相違がある", "やや相違がある", "どちらとも言えない", "ある程度一致する", "ほぼ一致する", "全く対立しない"], index=0,
key="idea_conflict_2")

# 中間アンケート２保存
st.markdown('<style>.stButton>button {background-color: blue; color: white; font-weight: bold;}</style>', unsafe_allow_html=True)
if st.button("アンケート２送信"):
   save_to_history("中間アンケート２", completion_rating_2, trust_rating_2, idea_conflict_2)
   st.write("アンケート２が送信されました。ありがとうございます！")

# UIの作成３
st.write("#### あなたとAIとの対話は、あと１往復です。")
st.write("AIとの対話３→中間アンケート３→事後アンケートの流れになります。")

# 被験者の入力３
st.write("#### AIの回答から役に立ちそうなポイントを引用して書いて下さい。")
third_question= st.text_area("", "", key="unique_third_question")

ai_response_3 = ""  

st.markdown('<style>.stButton>button {background-color: blue; color: white; font-weight: bold;}</style>', unsafe_allow_html=True)
if st.button("AIに仮説を立てる協力をしてもらう", key="unique_button_3"):
    with st.spinner("AIが考えています..."):
        response = client.chat.completions.create(
            model="gpt-4",
            messages=[

                {"role": "user", "content": f"""特に次のことについて教えて下さい。

{third_question}

それでは、仮説を検証する方法について示して下さい。"""}
            ]
        )
        ai_response_3 = response.choices[0].message.content
        st.session_state["ai_response_3"] = ai_response_3
        st.success("AIからの仮説を検証する方法の作業手順提案です！")

# AIの回答の表示３
if "ai_response_3" in st.session_state:
    st.write("#### AIからの提案３")
    st.text_area("AIから提案します。", height=500, key="ai_response_3")
    save_to_history("ステップ3", third_question, ai_response_3)

# 中間アンケート３
st.write("#### 中間アンケート３")
st.write("AIからの回答を読んで感じたことをそれぞれ一つ選んで、終わったら「アンケート３送信」を押して下さい。")
completion_rating_3 = st.radio("あなたの仮説の完成度について教えて下さい", ["", "全く未完成", "ほぼ未完成", "まだ不十分", "どちらとも言えない", "ある程度完成に近い", "ほぼ完成している", "完全に完成している"], index=0,
key="completion_rating_3")
trust_rating_3 = st.radio("あなたのAIに対する信頼について教えて下さい", ["", "全く信頼しない", "ほとんど信頼できない", "あまり信頼できない", "どちらとも言えない", "まあまあ信頼できる", "ほぼ信頼できる", "完全に信頼する"], index=0,
key="trust_rating_3")
idea_conflict_3 = st.radio("あなたとAIの間に、どの程度考えに相違がありますか？", ["", "完全に相違がある", "かなり相違がある", "やや相違がある", "どちらとも言えない", "ある程度一致する", "ほぼ一致する", "全く対立しない"], index=0,
key="idea_conflict_3")

# 中間アンケート３保存
st.markdown('<style>.stButton>button {background-color: blue; color: white; font-weight: bold;}</style>', unsafe_allow_html=True)
if st.button("アンケート３送信"):
   save_to_history("中間アンケート３", completion_rating_3, trust_rating_3, idea_conflict_3)
   st.write("アンケート３が送信されました。ありがとうございます！")

import json
import gspread
from oauth2client.service_account import ServiceAccountCredentials

# ✅ 必須のスコープを明示的に設定
SCOPES = ["https://www.googleapis.com/auth/spreadsheets"]

try:
    # Streamlit Secrets から認証情報を取得
    service_account_info = st.secrets["gspread_service_account"]
    
    # ✅ スコープを設定して Credentials を作成
    credentials = Credentials.from_service_account_info(
        service_account_info, 
        scopes=["https://www.googleapis.com/auth/spreadsheets"]
    )

    
    # gspread クライアントを作成
    client = gspread.authorize(credentials)
    
    # Google Sheets に接続
    spreadsheet = client.open_by_key(st.secrets["GOOGLE_SHEET_ID"])

    worksheet = spreadsheet.worksheet("Sheet2")  # sheet2ではなく、シート名を指定

except Exception as e:
    st.error(f"❌ Google Sheets 接続エラー: {e}")

# ✅ Googleスプレッドシートにデータを保存
st.markdown('<style>.stButton>button {background-color: blue; color: white; font-weight: bold;}</style>', unsafe_allow_html=True)
if st.button("実験Bの結果を保存して終了"):
   worksheet.append_rows(st.session_state.history)

# UIの作成４
   st.write("実験Bの結果が保存されました！お疲れ様でした。事後アンケートに戻って回答をお願いします。ありがとうございました。")

