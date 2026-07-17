import streamlit as st
import pandas as pd
import os
from datetime import datetime

# Cấu hình trang web (Giao diện rộng rãi, icon huyền học)
st.set_page_config(page_title="Lenormand Diary", page_icon="🔮", layout="wide")

DB_FILE = "nhat_ky_lenormand.csv"

# Danh sách 36 lá bài Lenormand chuẩn (Bạn có thể đổi sang tiếng Việt nếu muốn)
LENORMAND_CARDS = [
    "Rider", "Clover", "Ship", "House", "Tree", "Clouds", "Snake", "Coffin",
    "Bouquet", "Scythe", "Whip", "Birds", "Child", "Fox", "Bear", "Stars",
    "Stork", "Dog", "Tower", "Garden", "Mountain", "Crossroads", "Mice", "Heart",
    "Ring", "Book", "Letter", "Man", "Woman", "Lily", "Sun", "Moon",
    "Key", "Fish", "Anchor", "Cross"
]

# Hàm load dữ liệu từ file CSV, nếu chưa có thì tạo mới
def load_data():
    if os.path.exists(DB_FILE):
        df = pd.read_csv(DB_FILE)
        # Đảm bảo cột Ngày hiển thị đúng định dạng chuỗi
        df["Ngay"] = df["Ngay"].astype(str)
        return df
    else:
        return pd.DataFrame(columns=["Ngay", "Danh_Sach_La_Bai", "Su_Kien_Thuc_Te"])

df = load_data()

st.title("🔮 Nhật Ký Trải Bài & Tra Cứu Ứng Nghiệm")
st.markdown("---")

# Chia ứng dụng thành 2 Tab rõ ràng: Nhập liệu và Tra cứu
tab1, tab2 = st.tabs(["✍️ Ghi Chép Trải Bài Hôm Nay", "📚 Tra Cứu Lịch Sử Lá Bài"])

# ==================== TAB 1: NHẬP LIỆU HÀNG NGÀY ====================
with tab1:
    st.subheader("Ghi lại trải bài và sự kiện thực tế")
    
    col1, col2 = st.columns([1, 2])
    
    with col1:
        # Chọn ngày
        date_input = st.date_input("Chọn Ngày:", datetime.now())
        date_str = date_input.strftime("%d/%m/%Y")
        
        # Chọn nhiều lá bài cùng lúc (Rút mấy lá cũng được)
        selected_cards = st.multiselect(
            "Chọn các lá bài đã rút hôm nay:", 
            options=LENORMAND_CARDS,
            help="Bạn có thể chọn 1, 2, 3 hoặc nhiều lá bài cùng lúc."
        )
        
    with col2:
        # Nhập sự kiện thực tế xảy ra (Validation)
        actual_event = st.text_area(
            "Sự kiện thực tế diễn ra (Validation):", 
            placeholder="Ví dụ: Ngồi cạnh một người phụ nữ sắc sảo (Snake) ở trường học (Tower)...",
            height=150
        )
        
        # Nút lưu dữ liệu
        if st.button("💾 Lưu Nhật Ký", type="primary"):
            if not selected_cards:
                st.error("Vui lòng chọn ít nhất một lá bài trước khi lưu!")
            elif not actual_event.strip():
                st.error("Vui lòng nhập sự kiện thực tế diễn ra để sau này tra cứu!")
            else:
                # Gộp các lá bài lại thành chuỗi ngăn cách bằng dấu phẩy
                cards_str = ", ".join(selected_cards)
                
                # Tạo dòng dữ liệu mới
                new_row = pd.DataFrame([{
                    "Ngay": date_str,
                    "Danh_Sach_La_Bai": cards_str,
                    "Su_Kien_Thuc_Te": actual_event.strip()
                }])
                
                # Thêm vào database và lưu lại
                df = pd.concat([df, new_row], ignore_index=True)
                df.to_csv(DB_FILE, index=False)
                
                st.success(f"🎉 Đã lưu thành công trải bài ngày {date_str}!")
                # Refresh dữ liệu để tab tra cứu cập nhật ngay
                st.rerun()

# ==================== TAB 2: TRA CỨU THÔNG MINH ====================
with tab2:
    st.subheader("Chọn 1 lá bài để xem lại tất cả các sự kiện thực tế trong quá khứ")
    
    search_card = st.selectbox("Chọn lá bài muốn tra cứu ngược:", options=["-- Chọn lá bài --"] + LENORMAND_CARDS)
    
    if search_card != "-- Chọn lá bài --":
        if not df.empty:
            # Lọc thông minh: Tìm các dòng mà cột 'Danh_Sach_La_Bai' có chứa tên lá bài đang chọn
            # Dùng toán tử lambda để xử lý chuỗi chính xác, tránh bắt nhầm ký tự trùng nhau
            filtered_df = df[df["Danh_Sach_La_Bai"].apply(lambda x: search_card in [c.strip() for c in str(x).split(",")])]
            
            if not filtered_df.empty:
                st.write(f"📊 Tìm thấy **{len(filtered_df)}** ngày xuất hiện lá **{search_card}**:")
                
                # Hiển thị kết quả dạng danh sách thả xuống (Expander) cho đẹp và gọn
                for _, row in filtered_df.sort_values(by="Ngay", ascending=False).iterrows():
                    with st.expander(f"📅 Ngày {row['Ngay']} | Trải bài: {row['Danh_Sach_La_Bai']}"):
                        st.info(f"**Ý nghĩa/Sự kiện thực tế:**\n{row['Su_Kien_Thuc_Te']}")
            else:
                st.warning(f"Bạn chưa từng lưu trải bài nào có xuất hiện lá bài **{search_card}**.")
        else:
            st.info("Nhật ký hiện tại chưa có dữ liệu. Hãy nhập trải bài ở Tab 1 trước nhé!")

# ==================== PHẦN XEM TOÀN BỘ DATA (Tùy chọn) ====================
st.markdown("---")
with st.expander("📂 Xem toàn bộ bảng dữ liệu thô (Database)"):
    if not df.empty:
        st.dataframe(df, use_container_width=True)
    else:
        st.caption("Chưa có dữ liệu.")
