import streamlit as st
import smtplib
import os
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
from dotenv import load_dotenv  # Load .env variables

# Load environment variables from .env file
load_dotenv()

# Fetch credentials securely
smtp_username = os.getenv("EMAIL_USERNAME")
smtp_password = os.getenv("EMAIL_PASSWORD")
receiver_email = os.getenv("RECEIVER_EMAIL")  # Now hidden

# Function to send email
def send_email(name, sender_email, subject, message):
    smtp_server = "smtp.gmail.com"
    smtp_port = 587

    msg = MIMEMultipart()
    msg["From"] = smtp_username
    msg["To"] = receiver_email  # Securely fetched from .env
    msg["Subject"] = f"New Contact Form Submission: {subject}"

    # Include project details in the email body
    body = f"""
    🔋Project: Renewable Energy Consumption Tracker🔋

    Name: {name}  
    Email: {sender_email}  
    Subject: {subject}  

    Message: 
    {message}

    📩 This message was sent via the contact form on the Renewable Energy Consumption Tracker website.
    """
    
    msg.attach(MIMEText(body, "plain"))

    try:
        # Initialize SMTP server
        server = smtplib.SMTP(smtp_server, smtp_port)
        server.starttls()
        server.login(smtp_username, smtp_password)
        server.sendmail(smtp_username, receiver_email, msg.as_string())
        server.quit()
        return True
    except Exception as e:
        st.error(f"⚠️ Email sending failed: {str(e)}")
        return False

# Streamlit UI
def show_contact():
    st.subheader("📩 Contact Me")

    st.write("📧 **Email:** [yazansedih@gmail.com](mailto:yazansedih@gmail.com)")
    st.write("🔗 **Social Media:**")
    st.markdown("""
    - [LinkedIn](https://www.linkedin.com/feed/)
    - [GitHub](https://github.com/yazansedih)
    """)

    # Contact Form
    st.subheader("📬 Get in Touch")
    with st.form(key="contact_form"):
        name = st.text_input("Name", placeholder="Enter your name")
        email = st.text_input("Email", placeholder="Enter your email")
        subject = st.text_input("Subject", placeholder="Subject of your message")
        message = st.text_area("Message", placeholder="Write your message here...")

        submit_button = st.form_submit_button(label="Send Message")

        if submit_button:
            if name and email and message:
                success = send_email(name, email, subject, message)
                if success:
                    st.success("✅ Message sent successfully! I will get back to you soon.")
                else:
                    st.error("⚠️ Error sending the email. Please try again later.")
            else:
                st.error("⚠️ Please fill in all required fields.")

# Run the Streamlit app
if __name__ == "__main__":
    show_contact()
