import streamlit as st
from contract_logic import generate_prompt, get_contract_text, string_to_word_doc
from groq import Groq
from datetime import datetime

# === Groq API Key Setup ===

from dotenv import load_dotenv
import os

# Load the .env file
load_dotenv()

# Get the API key from environment variable
API = os.getenv("GROQ_API_KEY")

from groq import Groq  # or wherever you import Groq from

client = Groq(api_key=API)


# === Streamlit Page Setup ===
st.set_page_config(page_title="Legal Contract Generator", layout="centered")
st.title("📜 Legal Contract Generator")

# === Parties Involved ===
st.subheader("🔹 Parties Involved")
party_a = st.text_input("Party A Name")
party_b = st.text_input("Party B Name")

# === Contract Category ===
category = st.radio("Contract Category", ["Normal Contract", "Registration Document"])

# === Contract Type Specifics ===
selected_contract = ""
custom_contract = ""
payment_amount = payment_schedule = payment_due_days = ""
property_location = price = payment_date = currency = payment_method = possession_date = ""
termination_notice_days = dispute_resolution = ""

if category == "Normal Contract":
    normal_options = ["Construction Agreement", "Rental Agreement", "Service Contract", "Other (Custom)"]
    selected_contract = st.selectbox("Choose Type", normal_options)

    if selected_contract == "Other (Custom)":
        custom_contract = st.text_input("Enter Custom Contract Title (e.g., Freelance Design Agreement)")

    st.markdown("###  Payment Details")
    payment_amount = st.text_input("Total Payment Amount (₹)")
    payment_schedule = st.text_input("Payment Schedule (e.g., milestone-based)")
    payment_due_days = st.text_input("Number of Days for Final Payment After Invoice")

elif category == "Registration Document":
    selected_contract = st.selectbox("Choose Type", ["Sale Deed", "Gift Deed", "Transfer of Property"])

    if selected_contract in ["Sale Deed", "Transfer of Property"]:
        st.markdown("###  Property Details")
        property_location = st.text_input("Property Address")
        price = st.text_input("Consideration Amount (₹)")
        payment_schedule = st.text_input("Payment Schedule")
        payment_date = st.text_input("Payment Date")
        currency = st.text_input("Currency")
        payment_method = st.text_input("Payment Method")
        possession_date = st.text_input("Date of Possession")
        termination_notice_days = st.text_input("Termination Notice Period")
        dispute_resolution = st.text_input(
            "Dispute Resolution",
            value="Arbitration under Arbitration & Conciliation Act, 1996"
        )

# === Common Fields ===
st.subheader("🔹 Other Information")
project_type = st.text_input("Project or Property Description (Used as Title for Custom Contracts)")
duration = st.text_input("Contract Duration")
effective_date = st.text_input("Effective Date")
jurisdiction = st.text_input("Governing Law Jurisdiction")

# === Generate Contract ===
if st.button("Generate Contract"):
    st.markdown("###  Summary of Inputs")
    st.write(f"**Contract Type:** {custom_contract or selected_contract}")
    st.write(f"**Party A:** {party_a}")
    st.write(f"**Party B:** {party_b}")
    st.write(f"**Effective Date:** {effective_date}")
    st.write(f"**Jurisdiction:** {jurisdiction}")

    # Determine final contract type to use as heading/title
    final_contract_type = custom_contract.strip() if selected_contract == "Other (Custom)" else selected_contract

    # Build Inputs
    inputs = {
        "party_a": party_a,
        "party_b": party_b,
        "contract_type": selected_contract,
        "final_contract_type": final_contract_type,
        "category": category,
        "project_type": project_type,
        "duration": duration,
        "effective_date": effective_date,
        "jurisdiction": jurisdiction,
        "payment_amount": payment_amount,
        "payment_schedule": payment_schedule,
        "payment_due_days": payment_due_days,
        "property_location": property_location,
        "price": price,
        "payment_date": payment_date,
        "currency": currency,
        "payment_method": payment_method,
        "possession_date": possession_date,
        "termination_notice_days": termination_notice_days,
        "dispute_resolution": dispute_resolution
    }

    with st.spinner("Generating legal contract in a moment..."):
        prompt = generate_prompt(inputs)
        contract_text = get_contract_text(prompt)

        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
        filename_title = final_contract_type.replace(' ', '_')
        file_name = f"{filename_title}_{timestamp}.docx"
        file_path = string_to_word_doc(contract_text, file_name, final_contract_type)

    with open(file_path, "rb") as file:
        st.success("🎉 Contract generated successfully!")
        st.download_button(" Download Contract Here:", file, file_name, mime="application/vnd.openxmlformats-officedocument.wordprocessingml.document")