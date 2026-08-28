from datetime import datetime, timedelta
import secrets


otp_store = {}

OTP_EXPIRY_MINUTES = 5
RESEND_COOLDOWN_SECONDS = 60


# ============================================================
# CREATE VERIFICATION ID
# ============================================================

def create_verification_id() -> str:
    return secrets.token_urlsafe(32)


# ============================================================
# SAVE OTP
# ============================================================

def save_otp(
    mobile_number: str,
    otp: str,
) -> str:

    verification_id = create_verification_id()

    otp_store[verification_id] = {
        "mobile_number": mobile_number,
        "otp": otp,
        "expires_at": (
            datetime.now()
            + timedelta(minutes=OTP_EXPIRY_MINUTES)
        ),
        "resend_available_at": (
            datetime.now()
            + timedelta(seconds=RESEND_COOLDOWN_SECONDS)
        ),
    }

    return verification_id


# ============================================================
# VERIFY OTP
# ============================================================

def verify_otp(
    verification_id: str,
    otp: str,
):
    data = otp_store.get(verification_id)

    if not data:
        return None

    # Check whether OTP has expired
    if datetime.now() > data["expires_at"]:
        del otp_store[verification_id]
        return None

    # Check OTP
    if data["otp"] != otp:
        return None

    mobile_number = data["mobile_number"]

    # OTP can only be used once
    del otp_store[verification_id]

    return mobile_number


# ============================================================
# CHECK RESEND COOLDOWN
# ============================================================

def can_resend_otp(
    verification_id: str,
) -> tuple[bool, int]:

    data = otp_store.get(verification_id)

    if not data:
        return False, 0

    remaining = (
        data["resend_available_at"]
        - datetime.now()
    ).total_seconds()

    if remaining <= 0:
        return True, 0

    return False, int(remaining)


# ============================================================
# RESEND OTP
# ============================================================

def resend_otp(
    verification_id: str,
    otp: str,
):
    data = otp_store.get(verification_id)

    if not data:
        return None

    now = datetime.now()

    # Check whether verification session expired
    if now > data["expires_at"]:
        del otp_store[verification_id]
        return None

    # Check 60-second resend cooldown
    if now < data["resend_available_at"]:
        remaining = int(
            (
                data["resend_available_at"] - now
            ).total_seconds()
        )

        return {
            "error": "cooldown",
            "remaining": remaining,
        }

    # Replace old OTP with new OTP
    data["otp"] = otp

    # Reset resend timer
    data["resend_available_at"] = (
        now
        + timedelta(seconds=RESEND_COOLDOWN_SECONDS)
    )

    return {
        "mobile_number": data["mobile_number"],
        "remaining": RESEND_COOLDOWN_SECONDS,
    }