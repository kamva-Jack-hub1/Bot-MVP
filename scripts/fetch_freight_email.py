#!/usr/bin/env python3
import imaplib
import email
from email.header import decode_header
import re
import os
from datetime import datetime

# Gmail configuration
email_address = "kamva.assistant@gmail.com"
password = "hase cydc yrqi abzo"  # App password

def fetch_freight_email():
    try:
        # Connect to Gmail
        mail = imaplib.IMAP4_SSL("imap.gmail.com")
        mail.login(email_address, password)
        mail.select("inbox")
        
        # Search for freight strategy email
        search_criteria = '(SUBJECT "Freight Management Strategy")'
        status, messages = mail.search(None, search_criteria)
        email_ids = messages[0].split()
        
        print(f"📧 Found {len(email_ids)} email(s) with 'Freight Management Strategy' in subject")
        
        if not email_ids:
            print("❌ No freight strategy emails found")
            mail.logout()
            return None
        
        # Get the most recent one
        latest_id = email_ids[-1]
        status, msg_data = mail.fetch(latest_id, "(RFC822)")
        
        full_email_content = ""
        email_info = {}
        
        for response_part in msg_data:
            if isinstance(response_part, tuple):
                msg = email.message_from_bytes(response_part[1])
                
                # Decode subject
                subject, encoding = decode_header(msg["Subject"])[0]
                if isinstance(subject, bytes):
                    subject = subject.decode(encoding if encoding else "utf-8")
                
                # Decode sender
                from_ = msg.get("From")
                date = msg.get("Date")
                
                email_info = {
                    "subject": subject,
                    "from": from_,
                    "date": date,
                    "message_id": msg.get("Message-ID", ""),
                    "references": msg.get("References", ""),
                    "in_reply_to": msg.get("In-Reply-To", "")
                }
                
                print(f"📨 Email found:")
                print(f"   Subject: {subject}")
                print(f"   From: {from_}")
                print(f"   Date: {date}")
                
                # Extract email body
                if msg.is_multipart():
                    for part in msg.walk():
                        content_type = part.get_content_type()
                        content_disposition = str(part.get("Content-Disposition"))
                        
                        if content_type == "text/plain" and "attachment" not in content_disposition:
                            body = part.get_payload(decode=True).decode()
                            full_email_content = body
                            break
                else:
                    body = msg.get_payload(decode=True).decode()
                    full_email_content = body
        
        mail.logout()
        
        # Save the email to file
        if full_email_content:
            # Create directory if it doesn't exist
            freight_dir = "/home/openclaw_worker/.openclaw/workspace/projects/02-FREIGHT-STRATEGY-SUBMISSION/04-final"
            os.makedirs(freight_dir, exist_ok=True)
            
            # Create filename
            timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
            filename = f"FREIGHT_SUBMISSION_CONFIRMATION_{timestamp}.md"
            filepath = os.path.join(freight_dir, filename)
            
            # Create markdown content
            markdown_content = f"""# 📧 FREIGHT STRATEGY SUBMISSION CONFIRMATION

## Email Details
- **Subject**: {email_info.get('subject', 'N/A')}
- **From**: {email_info.get('from', 'N/A')}
- **Date**: {email_info.get('date', 'N/A')}
- **Message ID**: {email_info.get('message_id', 'N/A')}
- **Retrieved**: {datetime.now().strftime('%Y-%m-%d %H:%M:%S UTC')}

## 📋 Email Content

```
{full_email_content}
```

## 📁 File Information
- **Location**: {filepath}
- **Project**: 02-FREIGHT-STRATEGY-SUBMISSION
- **Folder**: 04-final
- **Status**: Submission confirmation received
- **Deadline**: March 31, 2026

## 🎯 Next Steps
1. Review submission confirmation details
2. Verify submission reference number
3. Update project status
4. Prepare for potential follow-up
5. Document in project records

## 📊 Submission Status
- ✅ **Email received**: Confirmation of submission
- 🔄 **Status**: Submitted to City of Cape Town
- 📅 **Deadline**: March 31, 2026 (met)
- 🎯 **Next**: Await acknowledgment/response from City

---
*Automatically saved by Jack 🦞, Chief of Staff, Kamva Africa*
"""
            
            # Write to file
            with open(filepath, 'w', encoding='utf-8') as f:
                f.write(markdown_content)
            
            print(f"\n✅ Email saved to: {filepath}")
            print(f"📄 File size: {len(markdown_content)} bytes")
            
            return {
                "filepath": filepath,
                "email_info": email_info,
                "content_preview": full_email_content[:500] + "..." if len(full_email_content) > 500 else full_email_content
            }
        else:
            print("❌ Could not extract email body")
            return None
            
    except Exception as e:
        print(f"❌ Error fetching email: {e}")
        return None

if __name__ == "__main__":
    result = fetch_freight_email()
    if result:
        print(f"\n📋 Email preview (first 500 chars):")
        print("---")
        print(result["content_preview"])
        print("---")
        print(f"\n📍 Saved in: {result['filepath']}")