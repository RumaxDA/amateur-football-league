from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from app.schemas.user import UserCreate, UserUpdate, User, UserLogin, UserChangePassword
from app.services.user import UserService
from app.database import get_db
from app.utils.auth import create_access_token, get_current_user

router = APIRouter(prefix="/users", tags=["users"])


@router.get("/me")
async def read_users_me(current_user: str = Depends(get_current_user)):
    return current_user

@router.post("/", response_model=User)
def create_user(user: UserCreate, db: Session = Depends(get_db)):
    user_service = UserService(db)
    return user_service.create_user(user)

@router.get("/{user_id}", response_model=User)
async def read_user(user_id: int, db: Session = Depends(get_db)):
    user_service = UserService(db)
    return user_service.get_user(user_id)


@router.get("/", response_model=list[User])
def read_users(
    db: Session = Depends(get_db), 
    current_user: User = Depends(get_current_user)
):
    if not current_user.is_superuser:
        raise HTTPException(status_code=403, detail="Tylko admin widzi wszystkich")
    user_service = UserService(db)
    return user_service.get_all_users()


@router.put("/{user_id}", response_model=User)
def update_user(
    user_id: int, 
    user: UserUpdate, 
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user) # Dodaj to
):
    
    if user_id != current_user.id and not current_user.is_superuser:
        raise HTTPException(status_code=403, detail="Nie możesz edytować cudzego konta")

    user_service = UserService(db)
    db_user = user_service.get_user(user_id)
    if db_user is None:
        raise HTTPException(status_code=404, detail="User not found")
    return user_service.update_user(user, user_id)


@router.post("/login")
def login_for_access_token(user: UserLogin, db: Session = Depends(get_db)):
    user_service = UserService(db)
    db_user = user_service.authenticate_user(user.email, user.password)
    if not db_user:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Incorrect email or password")
    access_token = create_access_token(db_user.id)
    return {"access_token": access_token}


@router.put("/{user_id}/password", response_model=User)
def change_password(change_password_data: UserChangePassword, db: Session = Depends(get_db), current_user: dict = Depends(get_current_user)):
    user_service = UserService(db)
    user_id = current_user['user_id']
    if change_password_data.new_password != change_password_data.confirm_new_password:
        raise HTTPException(status_code=400, detail="New passwords do not match")
    return user_service.change_password(user_id, change_password_data.password, change_password_data.new_password)

@router.delete("/{user_id}")
async def delete_user(
    user_id: int, 
    db: Session = Depends(get_db), 
    current_user: User = Depends(get_current_user)
):
    is_owner = (user_id == current_user.id)
    is_admin = current_user.is_superuser

    if not is_owner and not is_admin:
        raise HTTPException(
            status_code=403, 
            detail="Nie masz uprawnień do usunięcia tego konta"
        )

    user_service = UserService(db)
    
    if is_admin and is_owner:
        raise HTTPException(400, "Admin nie może usunąć samego siebie w ten sposób")

    return user_service.delete_user(user_id)