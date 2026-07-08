import streamlit as st
import qrcode
from io import BytesIO

# --- إعدادات الصفحة ---
st.set_page_config(page_title="منصة التدريب التفاعلية", layout="wide")

# --- إدارة الحالة (State) لتخزين البيانات مؤقتاً ---
if "current_question" not in st.session_state:
    st.session_state.current_question = "ما هو رأيك في الوسائل الرقمية في التعليم؟"
if "options" not in st.session_state:
    st.session_state.options = ["ممتازة جداً", "مفيدة القيود", "تحتاج لتطوير", "غير عملية"]
if "answers" not in st.session_state:
    st.session_state.answers = []

# --- القائمة الجانبية (لوحة تحكم المُكوِّن) ---
st.sidebar.title("🛠️ لوحة تحكم المُكوِّن")
mode = st.sidebar.radio("اختر الواجهة:", ["عرض النتائج والـ QR (المُكوِّن)", "صفحة إجابة الأساتذة"])

# 1. تعديل السؤال من طرف المكون
st.sidebar.subheader("📝 إدارة السؤال الحاضر")
new_q = st.sidebar.text_input("السؤال الحالي:", st.session_state.current_question)
if new_q != st.session_state.current_question:
    st.session_state.current_question = new_q
    st.session_state.answers = [] # إعادة تعيين الإجابات عند تغيير السؤال

# --- الواجهة الرئيسية ---

if mode == "عرض النتائج والـ QR (المُكوِّن)":
    st.title("📊 لوحة عرض النتائج المباشرة")
    
    col1, col2 = st.columns([1, 2])
    
    with col1:
        st.subheader("📱 امسح الرمز للإجابة")
        
        # توليد رابط ديناميكي (سيتم استبداله برابط الموقع الحقيقي بعد النشر)
        # لتجربته محلياً نستخدم الرابط الافتراضي لـ Streamlit
        app_url = "https://share.streamlit.io/" # ضع رابط موقعك هنا لاحقاً
        
        # توليد الـ QR Code
        qr = qrcode.QRCode(version=1, box_size=10, border=4)
        qr.add_data(app_url)
        qr.make(fit=True)
        img = qr.make_image(fill_color="black", back_color="white")
        
        # تحويل الصورة إلى بايتات لعرضها في Streamlit
        buf = BytesIO()
        img.save(buf, format="PNG")
        byte_im = buf.getvalue()
        
        st.image(byte_im, caption="وجه هاتفك نحو الرمز", use_column_width=True)
        
    with col2:
        st.subheader(f"❓ السؤال الحالي: {st.session_state.current_question}")
        
        # عرض الإحصائيات الحالية
        total_answers = len(st.session_state.answers)
        st.metric(label="عدد المجيبين الحركي", value=total_answers)
        
        if total_answers > 0:
            # حساب توزيع الإجابات
            stats = {opt: st.session_state.answers.count(opt) for opt in st.session_state.options}
            st.bar_chart(stats)
            
            # عرض التفاصيل بنسب مئوية
            for opt, count in stats.items():
                percentage = (count / total_answers) * 100
                st.write(f"**{opt}**: {count} إجابة ({percentage:.1f}%)")
        else:
            st.info("في انتظار إجابات الأساتذة...")

elif mode == "صفحة إجابة الأساتذة":
    st.title("📝 الإجابة على السؤال")
    st.subheader(st.session_state.current_question)
    
    # نموذج الإجابة
    with st.form(key="answer_form"):
        user_choice = st.radio("اختر إجابة واحدة:", st.session_state.options)
        submit_button = st.form_submit_button(label="إرسال الإجابة")
        
        if submit_button:
            st.session_state.answers.append(user_choice)
            st.success("تم إرسال إجابتك بنجاح! شكراً لك.")
