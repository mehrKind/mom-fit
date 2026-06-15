from sms_ir import SmsIr

sms_api_key = "N0TNmRnjBLQ63tGbKNIP3lfRfhhpt61SahmNuSh6S9e8b9gg"
linenumber = " 30002101007292 "
# sms
sms_ir = SmsIr(
sms_api_key,
linenumber,
)

sms_ir.send_verify_code("09224850196")