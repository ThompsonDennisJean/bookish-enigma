"""
Streamlit UI for IT Helpdesk Auto-Responder
Copyright (c) 2025 IT Helpdesk Auto-Responder Contributors
MIT License - See LICENSE file
"""

import streamlit as st
import httpx
import json
from datetime import datetime

# Page config
st.set_page_config(
    page_title="IT Helpdesk Auto-Responder",
    page_icon="🤖",
    layout="wide"
)

# Title and description
st.title("🤖 IT Helpdesk Auto-Responder")
st.markdown("""
This tool uses AI to diagnose common IT issues and suggest fixes.
It can run safe diagnostic commands and provide step-by-step solutions.
""")

# Input form
with st.form("helpdesk_form"):
    username = st.text_input("Your Name")
    issue = st.text_area(
        "Describe Your Issue",
        placeholder="Example: 'My internet connection is slow' or 'I can't print'"
    )
    submitted = st.form_submit_button("Get Help")

# Handle form submission
if submitted and username and issue:
    with st.spinner("Analyzing your issue..."):
        try:
            # Call FastAPI backend
            async with httpx.AsyncClient() as client:
                response = await client.post(
                    "http://localhost:8000/diagnose",
                    json={"username": username, "issue": issue},
                    timeout=30.0
                )
                
                if response.status_code != 200:
                    st.error(f"Error: {response.text}")
                else:
                    data = response.json()
                    
                    # Display results in expandable sections
                    col1, col2 = st.columns(2)
                    
                    with col1:
                        st.success(f"Ticket #{data['ticket_id']} Created")
                        
                        st.subheader("📋 Diagnosis")
                        st.write(data["diagnosis"])
                        
                        st.subheader("🔧 Suggested Fix")
                        st.write(data["suggested_fix"])
                    
                    with col2:
                        if data.get("executed_command"):
                            st.subheader("🖥️ Diagnostic Command")
                            st.code(data["executed_command"])
                            
                            st.subheader("📄 Command Output")
                            st.text_area(
                                "Output",
                                value=data.get("command_output", "No output"),
                                height=200,
                                disabled=True
                            )
                        
                        # Download results button
                        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
                        results = {
                            "timestamp": timestamp,
                            "ticket_id": data["ticket_id"],
                            "username": username,
                            "issue": issue,
                            **data
                        }
                        
                        st.download_button(
                            "📥 Download Results",
                            json.dumps(results, indent=2),
                            f"ticket_{data['ticket_id']}_{timestamp}.json",
                            "application/json"
                        )
                    
        except Exception as e:
            st.error(f"Error communicating with backend: {str(e)}")
            
else:
    if submitted:
        st.warning("Please fill in both your name and issue description.")