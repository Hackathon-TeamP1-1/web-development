import streamlit as st
import os
import base64  # ✅ Use Python's built-in base64 module

def get_base64_image(image_path):
    """Encodes an image to base64 format for embedding in HTML."""
    if os.path.exists(image_path):
        with open(image_path, "rb") as img_file:
            return base64.b64encode(img_file.read()).decode()
    return None  # Return None if image does not exist

def show_header():
    # ✅ Define profile image path
    profile_img_path = "assets/yyyyy.jpg"

    # ✅ Convert image to base64 if it exists
    base64_img = get_base64_image(profile_img_path)

    # ✅ Generate Data URL (or fallback image)
    if base64_img:
        profile_img_url = f"data:image/jpeg;base64,{base64_img}"
    else:
        profile_img_url = "https://via.placeholder.com/40"

    st.markdown(f"""
        <style>
            header {{visibility: hidden;}}
            .custom-header {{
                display: flex;
                justify-content: space-between;
                align-items: center;
                width: 100%;
                height: 60px;
                padding: 10px 40px;
                background-color: #FFFFFF;
                color: #000000;
                font-size: 22px;
                font-weight: bold;
                position: fixed;
                top: 0;
                left: 0;
                right: 0;
                z-index: 10000;
                box-shadow: 0px 2px 8px rgba(0, 0, 0, 0.1);
            }}
            .header-title {{
                display: flex;
                align-items: center;
                font-size: 24px;
                font-weight: bold;
            }}
            .header-profile {{
                display: flex;
                align-items: center;
                gap: 12px;
            }}
            .profile-img {{
                width: 40px;
                height: 40px;
                border-radius: 50%;
                object-fit: cover;
                cursor: pointer;
                border: 2px solid #ccc;
            }}
        </style>
        <div class="custom-header">
            <div class="header-title">⚡ Sumud</div>
            <div class="header-profile">
                <img src="{profile_img_url}" alt="Profile" class="profile-img">
            </div>
        </div>
    """, unsafe_allow_html=True)
