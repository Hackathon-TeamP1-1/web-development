import streamlit as st

def show_contact():
    st.subheader("📩 Contact Me")
    
    # Email
    st.write("📧 **Email:** [yazansedih@gmail.com](mailto:yazansedih@gmail.com)")
    
    # Social Media
    st.write("🔗 **Social Media:**")
    st.markdown("""
    - [LinkedIn](https://www.linkedin.com/feed/)
    - [GitHub](https://github.com/yazansedih)
    """)

    # Contact Form
    st.subheader("📬 Get in Touch")
    with st.form(key="contact_form"):
        name = st.text_input("Name")
        email = st.text_input("Email")
        subject = st.text_input("Subject")
        message = st.text_area("Message")

        submit_button = st.form_submit_button(label="Send Message")

        if submit_button:
            if name and email and message:
                st.success("✅ Message sent successfully! I will get back to you soon.")
            else:
                st.error("⚠️ Please fill in all required fields.")

    # Optional: Embed Google Map
    st.subheader("📍 Location")
    st.map()  # Or embed a specific Google Maps iframe

# Run
if __name__ == "__main__":
    show_contact()
