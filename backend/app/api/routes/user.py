from fastapi import APIRouter, Depends, HTTPException, status
from fastapi.security import OAuth2PasswordRequestForm
from sqlalchemy.orm import Session

from app.database.session import get_db
from app.dependencies.auth import get_current_user
from app.models.user import User

from app.schemas.user import (
    UserCreate,
    UserResponse,
    Token,
    SendMobileOTPRequest,
    VerifyMobileOTPRequest,
    ResendMobileOTPRequest,
    OTPResponse,
)

from app.services.user_service import (
    create_user,
    get_user_by_email,
    get_user_by_mobile,
    authenticate_user,
)

from app.core.security import create_access_token

from app.utils.otp import generate_otp
from app.utils.otp_store import (
    save_otp,
    verify_otp,
    resend_otp,
)


# ============================================================
# ROUTER
# ============================================================

router = APIRouter(
    prefix="/users",
    tags=["Users"],
)


# ============================================================
# REGISTER USER
# ============================================================

@router.post(
    "/register",
    response_model=UserResponse,
    status_code=status.HTTP_201_CREATED,
)
def register_user(
    user: UserCreate,
    db: Session = Depends(get_db),
):
    # Check whether email already exists
    existing_user = get_user_by_email(
        db,
        user.email,
    )

    if existing_user:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Email already registered.",
        )

    # Check whether mobile number already exists
    existing_mobile = get_user_by_mobile(
        db,
        user.mobile_number,
    )

    if existing_mobile:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Mobile number already registered.",
        )

    # Create user
    return create_user(
        db,
        user,
    )


# ============================================================
# SEND MOBILE OTP
# ============================================================

@router.post(
    "/send-mobile-otp",
    response_model=OTPResponse,
)
def send_mobile_otp(
    request: SendMobileOTPRequest,
    db: Session = Depends(get_db),
):
    # Check whether this mobile number belongs to a user
    user = get_user_by_mobile(
        db,
        request.mobile_number,
    )

    if not user:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="No account found with this mobile number.",
        )

    # Generate OTP
    otp = generate_otp()

    # Save OTP and receive verification ID
    verification_id = save_otp(
        request.mobile_number,
        otp,
    )

    # Development only
    print("\n================================")
    print("          MOBILE OTP")
    print("================================")
    print(f"Mobile Number: {request.mobile_number}")
    print(f"OTP: {otp}")
    print(f"Verification ID: {verification_id}")
    print("Expires in: 5 minutes")
    print("Resend available in: 60 seconds")
    print("================================\n")

    return {
        "message": "OTP sent successfully.",
        "verification_id": verification_id,
        "expires_in": 300,
        "resend_in": 60,
    }
# ============================================================
# RESEND MOBILE OTP
# ============================================================

@router.post(
    "/resend-mobile-otp",
    response_model=OTPResponse,
)
def resend_mobile_otp(
    request: ResendMobileOTPRequest,
):
    # Generate a new OTP
    otp = generate_otp()

    # Try to resend
    result = resend_otp(
        request.verification_id,
        otp,
    )

    # Verification session doesn't exist or expired
    if result is None:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="OTP session expired. Please request a new OTP.",
        )

    # Still inside 60-second cooldown
    if result.get("error") == "cooldown":
        raise HTTPException(
            status_code=status.HTTP_429_TOO_MANY_REQUESTS,
            detail=f"Please wait {result['remaining']} seconds before requesting another OTP.",
        )

    # Development only
    print("\n================================")
    print("        RESENT MOBILE OTP")
    print("================================")
    print(f"Mobile Number: {result['mobile_number']}")
    print(f"OTP: {otp}")
    print("Expires in: 5 minutes")
    print("Resend available in: 60 seconds")
    print("================================\n")

    return {
        "message": "OTP resent successfully.",
        "verification_id": request.verification_id,
        "expires_in": 300,
        "resend_in": 60,
    }
# ============================================================
# VERIFY MOBILE OTP
# ============================================================

@router.post(
    "/verify-mobile-otp",
    response_model=OTPResponse,
)
def verify_mobile_otp(
    request: VerifyMobileOTPRequest,
    db: Session = Depends(get_db),
):
    # Verify OTP using verification ID
    mobile_number = verify_otp(
        request.verification_id,
        request.otp,
    )

    # OTP invalid or expired
    if not mobile_number:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Invalid or expired OTP.",
        )

    # Find user using mobile number
    user = get_user_by_mobile(
        db,
        mobile_number,
    )

    if not user:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="User not found.",
        )

    # Mark mobile number as verified
    user.is_mobile_verified = True

    db.commit()
    db.refresh(user)

    return {
        "message": "Mobile number verified successfully.",
        "verification_id": request.verification_id,
        "expires_in": 0,
        "resend_in": 0,
    }

# ============================================================
# EMAIL + PASSWORD LOGIN
# ============================================================

@router.post(
    "/login",
    response_model=Token,
)
def login_user(
    form_data: OAuth2PasswordRequestForm = Depends(),
    db: Session = Depends(get_db),
):
    # Authenticate user
    authenticated_user = authenticate_user(
        db=db,
        email=form_data.username,
        password=form_data.password,
    )

    if authenticated_user is None:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Invalid email or password.",
        )

    # Check whether account is active
    if not authenticated_user.is_active:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="User account is inactive.",
        )

    # Create JWT access token
    access_token = create_access_token(
        {
            "sub": authenticated_user.email,
            "user_id": authenticated_user.id,
        }
    )

    return {
        "access_token": access_token,
        "token_type": "bearer",
    }


# ============================================================
# GET CURRENT USER
# ============================================================

@router.get(
    "/me",
    response_model=UserResponse,
)
def get_me(
    current_user: User = Depends(get_current_user),
):
    return current_user

