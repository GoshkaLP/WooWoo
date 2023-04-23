from fastapi import HTTPException, status

wrong_credentials_exception = HTTPException(
    status_code=status.HTTP_401_UNAUTHORIZED,
    detail="Could not validate credentials"
)

wrong_token_exception = HTTPException(
    status_code=status.HTTP_401_UNAUTHORIZED,
    detail='Wrong token'
)

user_not_found_exception = HTTPException(
    status_code=status.HTTP_401_UNAUTHORIZED,
    detail='User not found'
)

wrong_password_exception = HTTPException(
    status_code=status.HTTP_401_UNAUTHORIZED,
    detail='Wrong password'
)

passwords_match_exception = HTTPException(
    status_code=status.HTTP_401_UNAUTHORIZED,
    detail='Passwords do not match'
)

user_not_create_exception = HTTPException(
    status_code=status.HTTP_401_UNAUTHORIZED,
    detail='Could not create user'
)

user_exists_exception = HTTPException(
    status_code=status.HTTP_401_UNAUTHORIZED,
    detail='User with this email already exists'
)

city_not_create_exception = HTTPException(
    status_code=status.HTTP_400_BAD_REQUEST,
    detail='Could not create city'
)

city_exists_exception = HTTPException(
    status_code=status.HTTP_400_BAD_REQUEST,
    detail='This city already exists'
)


interest_not_create_exception = HTTPException(
    status_code=status.HTTP_400_BAD_REQUEST,
    detail='Could not create interest'
)

interest_not_add_exception = HTTPException(
    status_code=status.HTTP_400_BAD_REQUEST,
    detail='Could not add interests'
)

interest_exists_exception = HTTPException(
    status_code=status.HTTP_400_BAD_REQUEST,
    detail='This interest already exists'
)

no_interest_exception = HTTPException(
    status_code=status.HTTP_400_BAD_REQUEST,
    detail='Wrong interest id'
)

form_not_create_exception = HTTPException(
    status_code=status.HTTP_400_BAD_REQUEST,
    detail='Could not create form'
)

form_exists_exception = HTTPException(
    status_code=status.HTTP_400_BAD_REQUEST,
    detail='This form already exists'
)

photo_not_add_exception = HTTPException(
    status_code=status.HTTP_400_BAD_REQUEST,
    detail='Could not add photo'
)

no_photo_exception = HTTPException(
    status_code=status.HTTP_400_BAD_REQUEST,
    detail='No photo'
)
