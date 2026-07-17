import streamlit as st
import pandas as pd
import os
from datetime import datetime

st.set_page_config(page_title="Lenormand Diary", page_icon="🔮", layout="wide")

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

# Khởi tạo hoặc load database
if "df" not in st.session_state:
    st.session_state.df = load_data()

# Khởi tạo các biến tạm để Clear Form sau khi lưu
if "form_cards" not in st.session_state:
    st.session_state.form_cards = []
if "form_event" not in st.session_state:
    st.session_state.form_event = ""

st.title("🔮 Nhật Ký Trải Bài & Tra Cứu Ứng Nghiệm")
st.markdown("---")

tab1, tab2, tab3 = st.tabs(["✍️ Ghi Chép Hôm Nay", "📚 Tra Cứu Sự Kiện", "⚙️ Quản Lý Lịch Sử (Sửa/Xóa)"])

# ==================== TAB 1: NHẬP LIỆU HÀNG NGÀY (CÓ TỰ CLEAR) ====================
with tab1:
    st.subheader("Ghi lại trải bài hôm nay")
    col1, col2 = st.columns([1, 2])
    
    with col1:
        date_input = st.date_input("Chọn Ngày:", datetime.now())
        date_str = date_input.strftime("%d/%m/%Y")
        
        # Sử dụng key để có thể xóa dữ liệu sau khi bấm lưu
        selected_cards = st.multiselect(
            "Chọn các lá bài đã rút:", 
            options=LENORMAND_CARDS,
            key="form_cards"
        )
        
    with col2:
        actual_event = st.text_area(
            "Sự kiện thực tế diễn ra (Validation):", 
            placeholder="Ví dụ: Ngồi cạnh một người phụ nữ sắc sảo ở trường...",
            height=150,
            key="form_event"
        )
        
        if st.button("💾 Lưu Nhật Ký", type="primary"):
            if not selected_cards:
                st.error("Vui lòng chọn ít nhất một lá bài!")
            elif not actual_event.strip():
                st.error("Vui lòng nhập sự kiện thực tế!")
            else:
                cards_str = ", ".join(selected_cards)
                new_row = pd.DataFrame([{
                    "Ngay": date_str,
                    "Danh_Sach_La_Bai": cards_str,
                    "Su_Kien_Thuc_Te": actual_event.strip()
                }])
                
                # Cập nhật vào dữ liệu hiện tại
                st.session_state.df = pd.concat([st.session_state.df, new_row], ignore_index=True)
                st.session_state.df.to_csv(DB_FILE, index=False)
                
                st.success(f"🎉 Đã lưu thành công dữ liệu!")
                
                # Tiến hành XÓA SẠCH FORM để tránh hiểu lầm chưa lưu
                st.session_state.form_cards = []
                st.session_state.form_event = ""
                st.rerun()

# ==================== TAB 2: TRA CỨU SỰ KIỆN THỰC TẾ (ẨN NGÀY) ====================
with tab2:
    st.subheader("Tra cứu nghĩa thực tế theo lá bài")
    search_card = st.selectbox("Chọn lá bài muốn tra cứu:", options=["-- Chọn lá bài --"] + LENORMAND_CARDS)
    
    if search_card != "-- Chọn lá bài --":
        current_df = st.session_state.df
        if not current_df.empty:
            # Lọc các dòng chứa lá bài chọn
            filtered_df = current_df[current_df["Danh_Sach_La_Bai"].apply(lambda x: search_card in [c.strip() for c in str(x).split(",")])]
            
            if not filtered_df.empty:
                st.write(f"💡 Những lần gặp lá **{search_card}**, thực tế đã xảy ra các sự kiện:")
                # Hiện danh sách sự kiện thuần túy, không hiện ngày
                for _, row in filtered_df.iterrows():
                    st.markdown(f"- {row['Su_Kien_Thuc_Te']} *(Trải bài: {row['Danh_Sach_La_Bai']})*")
            else:
                st.warning(f"Chưa có lịch sử sự kiện nào cho lá **{search_card}**.")
        else:
            st.info("Chưa có dữ liệu nhật ký.")

# ==================== TAB 3: QUẢN LÝ LỊCH SỬ (EDIT / DELETE) ====================
with tab3:
    st.subheader("Danh sách trải bài đã lưu")
    current_df = st.session_state.df
    
    if not current_df.empty:
        for index, row in current_df.iterrows():
            # Tạo một khung bao quanh mỗi dòng trải bài
            with st.container(border=True):
                col_info, col_edit, col_del = st.columns([5, 2, 1])
                
                with col_info:
                    st.markdown(f"📅 **Ngày:** {row['Ngay']} | 🔮 **Bài:** `{row['Danh_Sach_La_Bai']}`")
                    st.markdown(f"📝 **Giải nghĩa thực tế:** {row['Su_Kien_Thuc_Te']}")
                
                with col_edit:
                    # Ô nhập văn bản mới để sửa trực tiếp lời giải thích
                    new_meaning = st.text_input("Sửa giải nghĩa:", value=row['Su_Kien_Thuc_Te'], key=f"edit_{index}")
                    if new_meaning != row['Su_Kien_Thuc_Te']:
                        if st.button("📝 Cập nhật", key=f"btn_edit_{index}"):
                            st.session_state.df.at[index, "Su_Kien_Thuc_Te"] = new_meaning
                            st.session_state.df.to_csv(DB_FILE, index=False)
                            st.success("Đã cập nhật!")
                            st.rerun()
                            
                with col_del:
                    # Nút xóa dòng trải bài này
                    st.write("") # Tạo khoảng cách cho bằng hàng với ô text
                    if st.button("🗑️ Xóa", key=f"btn_del_{index}", type="secondary"):
                        st.session_state.df = st.session_state.df.drop(index).reset_index(drop=True)
                        st.session_state.df.to_csv(DB_FILE, index=False)
                        st.success("Đã xóa dòng này!")
                        st.rerun()
    else:
        st.info("Chưa có lịch sử trải bài nào được lưu.")
