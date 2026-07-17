import streamlit as st
import pandas as pd
import os
from datetime import datetime

# Cấu hình trang cơ bản
st.set_page_config(page_title="Chiikawa Lenormand Diary", page_icon="🐰", layout="wide")

# Đổi màu nền sang màu kem sữa pastel nhẹ nhàng
# Thay đổi đoạn này để tạo nền hiệu ứng Gradient Xanh và Hồng pastel
st.markdown(
    """
    <style>
    .stApp {
        background: linear-gradient(135deg, #E3F2FD 0%, #FCE4EC 100%);
    }
    </style>
    """, 
    unsafe_allow_html=True
)

DB_FILE = "nhat_ky_lenormand.csv"

LENORMAND_CARDS = [
    "Rider", "Clover", "Ship", "House", "Tree", "Clouds", "Snake", "Coffin",
    "Bouquet", "Scythe", "Whip", "Birds", "Child", "Fox", "Bear", "Stars",
    "Stork", "Dog", "Tower", "Garden", "Mountain", "Crossroads", "Mice", "Heart",
    "Ring", "Book", "Letter", "Man", "Woman", "Lily", "Sun", "Moon",
    "Key", "Fish", "Anchor", "Cross"
]

def load_data():
    if os.path.exists(DB_FILE):
        df = pd.read_csv(DB_FILE)
        df["Ngay"] = df["Ngay"].astype(str)
        return df
    else:
        return pd.DataFrame(columns=["Ngay", "Danh_Sach_La_Bai", "Su_Kien_Thuc_Te"])

# Tải dữ liệu vào session_state
if "df" not in st.session_state:
    st.session_state.df = load_data()

# ==================== BANNER CHIILAWA & USAGI ====================
# Thay đổi tỷ lệ cột sang [2, 1] để cột bên phải rộng rãi hơn cho ảnh bự
col_title, col_img = st.columns([2, 1])
with col_title:
    st.title("🐰 YAHA! Nhật Ký Trải Bài Lenormand")
    st.write("Một không gian nhỏ để lưu giữ những phép màu và sự kiện thực tế mỗi ngày. Urara!!")
with col_img:
    # Đã tăng kích thước ảnh lên thành 350 (bạn có thể tăng thêm nếu muốn bự nữa nha)
    st.image("https://www.buyandship.today/contents/uploads/2023/09/footer-chiikawa-1024x414.jpeg", width=350)

st.write("---")

tab1, tab2, tab3 = st.tabs(["⭐ Ghi Chép Hôm Nay", "🔍 Tra Cứu Sự Kiện", "🧺 Quản Lý Lịch Sử"])

# ==================== TAB 1: NHẬP LIỆU HÀNG NGÀY ====================
with tab1:
    st.write("### 📝 Hôm nay bộ bài nói gì với bạn thế?")
    col1, col2 = st.columns([1, 2])
    
    with col1:
        date_input = st.date_input("Chọn Ngày:", datetime.now())
        date_str = date_input.strftime("%d/%m/%Y")
        
        selected_cards = st.multiselect(
            "Chọn các lá bài đã rút:", 
            options=LENORMAND_CARDS,
            key="form_cards"
        )
        
    with col2:
        actual_event = st.text_area(
            "Sự kiện thực tế diễn ra:", 
            placeholder="Ví dụ: Có một người lạ hợp gu gửi lời kết bạn hoặc nhắn tin làm quen với bạn (Rider) trên mạng xã hội (Star)....",
            height=150,
            key="form_event"
        )
        
        if st.button("✨ Lưu Nhật Ký (Yaha!)", type="primary"):
            if not selected_cards:
                st.error("Ơ kìa, chưa chọn lá bài nào hết trơn! 😲")
            elif not actual_event.strip():
                st.error("Hãy nhập sự kiện thực tế để Usagi lưu lại giúp bạn nhé! 📝")
            else:
                cards_str = ", ".join(selected_cards)
                new_row = pd.DataFrame([{
                    "Ngay": date_str,
                    "Danh_Sach_La_Bai": cards_str,
                    "Su_Kien_Thuc_Te": actual_event.strip()
                }])
                
                # Lưu dữ liệu vào file
                st.session_state.df = pd.concat([st.session_state.df, new_row], ignore_index=True)
                st.session_state.df.to_csv(DB_FILE, index=False)
                
                # Thông báo thành công
                st.toast("🎉 Đã lưu xong rồi! Ura-ra-ra-ra! 🐰⭐")
                
                # Xóa sạch ô nhập liệu
                for k in ["form_cards", "form_event"]:
                    if k in st.session_state:
                        del st.session_state[k]
                        
                st.rerun()

# ==================== TAB 2: TRA CỨU SỰ KIỆN THỰC TẾ ====================
with tab2:
    st.write("### 🔎 Tìm kiếm ký ức của những lá bài")
    search_card = st.selectbox("Chọn lá bài muốn tra cứu ngược:", options=["-- Chọn lá bài --"] + LENORMAND_CARDS)
    
    if search_card != "-- Chọn lá bài --":
        current_df = st.session_state.df
        if not current_df.empty:
            filtered_df = current_df[current_df["Danh_Sach_La_Bai"].apply(lambda x: search_card in [c.strip() for c in str(x).split(",")])]
            
            if not filtered_df.empty:
                st.write(f"### 💡 Khi lá **{search_card}** xuất hiện, thực tế bạn đã gặp:")
                for _, row in filtered_df.iterrows():
                    st.write(f"💖 {row['Su_Kien_Thuc_Te']} *(Đi kèm bộ bài: `{row['Danh_Sach_La_Bai']}`)*")
                # ---- THÊM DÒNG DÍ DỎM NÀY VÀO ĐÂY NHA HÂN ----
                st.write("") # Tạo một khoảng trống nhỏ cho đẹp
                st.success("🐰 **Ura... Nhìn bạn ngon như cà phê Laura của ca sĩ Nhật Kim Anh vậy!** ☕✨")
                # ---------------------------------------------
            else:
                st.warning(f"Hình như bạn chưa từng gặp lá **{search_card}** trong quá khứ đâu... Huba?")
        else:
            st.info("Chưa có dữ liệu nào để tra cứu cả.")

# ==================== TAB 3: QUẢN LÝ LỊCH SỬ ====================
with tab3:
    st.write("### 🧺 Kho lưu trữ trải bài")
    current_df = st.session_state.df
    
    if not current_df.empty:
        # Vòng lặp hiển thị từng trải bài
        for index, row in current_df.iterrows():
            # Thêm box (border=True) bao quanh mỗi trải bài để dễ phân biệt
            with st.container(border=True):
                col_info, col_edit, col_del = st.columns([5, 2, 1])
                
                with col_info:
                    st.markdown(f"📅 **Ngày:** `{row['Ngay']}`")
                    st.markdown(f"🔮 **Bài đã rút:** `{row['Danh_Sach_La_Bai']}`")
                    st.markdown(f"📝 **Giải nghĩa thực tế:** {row['Su_Kien_Thuc_Te']}")
                
                with col_edit:
                    new_meaning = st.text_input("Sửa nhanh giải nghĩa:", value=row['Su_Kien_Thuc_Te'], key=f"edit_{index}")
                    if new_meaning != row['Su_Kien_Thuc_Te']:
                        if st.button("📝 Cập nhật", key=f"btn_edit_{index}"):
                            st.session_state.df.at[index, "Su_Kien_Thuc_Te"] = new_meaning
                            st.session_state.df.to_csv(DB_FILE, index=False)
                            st.toast("Đã sửa thành công!")
                            st.rerun()
                            
                with col_del:
                    st.write("") # Đẩy nút xóa xuống một chút cho thẳng hàng
                    if st.button("🗑️ Xóa", key=f"btn_del_{index}"):
                        st.session_state.df = st.session_state.df.drop(index).reset_index(drop=True)
                        st.session_state.df.to_csv(DB_FILE, index=False)
                        st.toast("Đã xóa sạch!")
                        st.rerun()
    else:
        st.info("Kho trống rỗng~ Hãy đi rút bài thôi nào! 🃏")
