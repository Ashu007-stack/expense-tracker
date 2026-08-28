from typing import Optional

from pydantic import (
    BaseModel,
    ConfigDict,
    EmailStr,
    Field,
    model_validator,
)


# ============================================================
# USER REGISTRATION
# ============================================================

class UserCreate(BaseModel):
    full_name: str = Field(
        min_length=2,
        max_length=100,
    )

    email: EmailStr

    mobile_number: str = Field(
        min_length=10,
        max_length=15,
    )

    password: str = Field(
        min_length=8,
        max_length=128,
    )

    confirm_password: str = Field(
        min_length=8,
        max_length=128,
    )

    @model_validator(mode="after")
    def passwords_match(self):
        if self.password != self.confirm_password:
            raise ValueError("Passwords do not match.")

        return self


# ============================================================
# EMAIL + PASSWORD LOGIN
# ============================================================

class UserLogin(BaseModel):
    email: EmailStr

    password: str = Field(
        min_length=8,
        max_length=128,
    )


# ============================================================
# SEND MOBILE OTP
# ============================================================

class SendMobileOTPRequest(BaseModel):
    mobile_number: str = Field(
        min_length=10,
        max_length=15,
    )


# ============================================================
# VERIFY MOBILE OTP
# ============================================================

class VerifyMobileOTPRequest(BaseModel):
    verification_id: str = Field(
        min_length=1,
    )

    otp: str = Field(
        min_length=6,
        max_length=6,
        pattern=r"^\d{6}$",
    )


# ============================================================
# OTP RESPONSE
# ============================================================

class OTPResponse(BaseModel):
    message: str
    verification_id: str
    expires_in: int
    resend_in: int


# ============================================================
# TOKEN RESPONSE
# ============================================================

class Token(BaseModel):
    access_token: str
    token_type: str = "bearer"


# ============================================================
# USER RESPONSE
# ============================================================

class UserResponse(BaseModel):
    id: int
    full_name: str
    email: EmailStr
    mobile_number: Optional[str] = None

    model_config = ConfigDict(
        from_attributes=True,
    )


class ResendMobileOTPRequest(BaseModel):
    verification_id: str = Field(
        min_length=1,
    )