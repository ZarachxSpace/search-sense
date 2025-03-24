from sqlalchemy.future import select
from sqlalchemy.ext.asyncio import AsyncSession
from database.models import User, UserPreferences

# ✅ 1. Create a new user
async def create_user(db: AsyncSession, username: str, email: str):
    """Inserts a new user into the database."""
    new_user = User(username=username, email=email)
    db.add(new_user)
    await db.commit()
    await db.refresh(new_user)
    return new_user

# ✅ 2. Get user by ID
async def get_user_by_id(db: AsyncSession, user_id: int):
    """Fetches user details by ID."""
    result = await db.execute(select(User).filter(User.id == user_id))
    return result.scalars().first()

# ✅ 3. Get user by email
async def get_user_by_email(db: AsyncSession, email: str):
    """Fetches user details by email."""
    result = await db.execute(select(User).filter(User.email == email))
    return result.scalars().first()

# ✅ 4. Store user preferences
async def store_user_preferences(db: AsyncSession, user_id: int, preferences: dict):
    """Stores or updates user preferences."""
    existing_preferences = await db.execute(
        select(UserPreferences).filter(UserPreferences.user_id == user_id)
    )
    existing_preferences = existing_preferences.scalars().first()

    if existing_preferences:
        existing_preferences.preferred_keywords = preferences  # ✅ Update existing preferences
    else:
        new_preferences = UserPreferences(user_id=user_id, preferred_keywords=preferences)
        db.add(new_preferences)

    await db.commit()
    return preferences

# ✅ 5. Get user preferences
async def get_user_preferences(db: AsyncSession, user_id: int):
    """Retrieves user preferences for personalized ranking."""
    result = await db.execute(select(UserPreferences).filter(UserPreferences.user_id == user_id))
    preferences = result.scalars().first()
    return preferences.preferred_keywords if preferences else []