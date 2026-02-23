import streamlit as st
import pandas as pd
import os

# רשימת כל פרשות השבוע לפי חומשים
ALL_PARASHOT = [
    "בראשית", "נח", "לך לך", "וירא", "חיי שרה", "תולדות", "ויצא", "וישלח", "וישב", "מקץ", "ויגש", "ויחי",
    "שמות", "וארא", "בא", "בשלח", "יתרו", "משפטים", "תרומה", "תצווה", "כי תשא", "ויקהל", "פקודי",
    "ויקרא", "צו", "שמיני", "תזריע", "מצורע", "אחרי מות", "קדושים", "אמור", "בהר", "בחוקותי",
    "במדבר", "נשא", "בהעלותך", "שלח", "קרח", "חקת", "בלק", "פנחס", "מטות", "מסעי",
    "דברים", "ואתחנן", "עקב", "ראה", "שופטים", "כי תצא", "כי תבוא", "נצבים", "וילך", "האזינו", "וזאת הברכה"
]

DB_FILE = "data.csv"

def load_data():
    if os.path.exists(DB_FILE):
        return pd.read_csv(DB_FILE)
    return pd.DataFrame(columns=["שם ההורה", "פרשה", "הקדשה"])

# הגדרות עיצוב (RTL לעברית)
st.set_page_config(page_title="רישום לעלון הבית ספרי", layout="centered")
st.markdown("""
    <style>
    .reportview-container .main .block-container { direction: rtl; }
    div[data-testid=\"stBlock\"] { direction: rtl; }
    </style>
    """, unsafe_allow_html=True)

st.title("📖 רישום הקדשות לעלון השבת")
st.write("הורים יקרים, כאן ניתן להשתבץ לפרשה עבור העלון הבית-ספרי.")

# ניהול נתונים
df = load_data()
taken = df["פרשה"].tolist()
available = [p for p in ALL_PARASHOT if p not in taken]

# טופס בחירה
with st.container():
    st.subheader("טופס שיבוץ")
    name = st.text_input("שם מלא:")
    parasha = st.selectbox("בחר פרשה פנויה:", ["בחר פרשה..."] + available)
    dedication = st.text_area("הקדשה (למשל: לעילוי נשמת..., להצלחת המשפחה וכו)")
    
    if st.button("אישור ושמירה"):
        if name and parasha != "בחר פרשה..." and dedication:
            new_row = pd.DataFrame([[name, parasha, dedication]], columns=["שם ההורה", "פרשה", "הקדשה"])
            df = pd.concat([df, new_row], ignore_index=True)
            df.to_csv(DB_FILE, index=False)
            st.success(f"תודה {name}! שובצת לפרשת {parasha}.")
            st.rerun()
        else:
            st.error("נא למלא את כל השדות.")

st.divider()

# ריכוז תוצאות (למנהל)
st.subheader("📊 מצב השיבוצים הנוכחי")
if not df.empty:
    st.dataframe(df, use_container_width=True)
    
    # כפתור הורדה לאקסל
    csv = df.to_csv(index=False).encode('utf-8-sig')
    st.download_button(
        label="📥 הורד את כל התוצאות (Excel/CSV)",
        data=csv,
        file_name='parasha_list.csv',
        mime='text/csv',
    )
else:
    st.info("עדיין אין שיבוצים. היו הראשונים")