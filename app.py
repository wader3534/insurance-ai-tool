import streamlit as st
import google.generativeai as genai

# --- 1. 網頁基本設定 ---
st.set_page_config(page_title="保險商品多方比較平台", page_icon="🛡️", layout="wide")
st.title("🛡️ 團隊專屬：AI 保險商品多方比較神器 (升級版)")
st.markdown("可自由選擇比較家數，將各家保單條款貼上，讓 AI 幫您一秒畫出橫向比較表！")

# --- 2. 側邊欄：設定 API Key 與 比較數量 ---
st.sidebar.header("系統設定")
api_key = st.sidebar.text_input("請輸入您的 Gemini API Key", type="password")

st.sidebar.divider()
st.sidebar.markdown("### ⚙️ 比較設定")
# 讓您動態選擇要比較幾家 (預設3家，最多5家，避免畫面太擠)
num_products = st.sidebar.number_input("請選擇要比較的商品數量", min_value=2, max_value=5, value=3)

# --- 3. 主程式 ---
if api_key:
    genai.configure(api_key=api_key)
    model = genai.GenerativeModel('gemini-2.5-pro') 

    # 根據您選擇的數量，動態產生對應的欄位
    cols = st.columns(num_products)
    
    product_names = []
    product_terms = []

    # 利用迴圈產生輸入框
    for i in range(num_products):
        with cols[i]:
            st.subheader(f"🏢 產險/壽險公司 {i+1}")
            # 注意：在迴圈中產生元件，必須給予不同的 key，否則系統會搞混
            name = st.text_input(f"商品 {i+1} 名稱", key=f"name_{i}")
            term = st.text_area(f"請貼上商品 {i+1} 的條款或特色", height=250, key=f"term_{i}")
            product_names.append(name)
            product_terms.append(term)

    # --- 4. 執行比較按鈕 ---
    if st.button("🚀 產出 AI 多方比較表"):
        # 檢查是否每個文字框都有輸入內容
        if all(product_terms): 
            with st.spinner(f'AI 正在為您逐條解析 {num_products} 家保單，請稍候...'):
                
                # 動態組合給 AI 的指令 (Prompt)
                prompt_text = "你是一位台灣專業的保險理賠與商品專家。請幫我比較以下多張保單。\n"
                prompt_text += "請用清晰的「Markdown 表格」呈現橫向比較，比較維度需包含：承保範圍、除外責任、關鍵差異與優劣勢等。\n"
                prompt_text += "表格產出後，請給出一段客觀的總結，以及針對業務團隊的「銷售與規劃建議」。\n\n"
                
                # 把每一家的內容塞進指令中
                for i in range(num_products):
                    # 如果沒填名稱，就預設叫 商品 1, 商品 2...
                    current_name = product_names[i] if product_names[i] else f"商品 {i+1}"
                    prompt_text += f"【{current_name}】條款內容：\n{product_terms[i]}\n\n"
                
                try:
                    response = model.generate_content(prompt_text)
                    st.divider()
                    st.markdown("### 📊 AI 多方分析結果")
                    st.write(response.text)
                except Exception as e:
                    st.error(f"發生錯誤，請檢查 API Key 是否正確：{e}")
        else:
            st.warning("請確保所有開啟的商品欄位都有貼上內容喔！如果不需要這麼多間，可以到左側調整數量。")
else:
    st.info("👈 請先在左側欄位貼上您的 API Key 才能啟用比較功能喔！")