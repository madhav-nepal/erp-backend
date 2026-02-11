from database import SessionLocal, engine
import models
from passlib.context import CryptContext

# 1. Setup Password Hashing
pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")

def get_password_hash(password):
    return pwd_context.hash(password)

# 2. Connect to the DB
db = SessionLocal()

def seed_data():
    print("🌱 Seeding data...")

    # --- TENANT SECTION ---
    tenant = db.query(models.Tenant).filter(models.Tenant.domain == "acme").first()
    
    if tenant:
        print(f"⚠️  Tenant 'Acme Corp' already exists (ID: {tenant.id}). Using it.")
    else:
        tenant = models.Tenant(
            name="Acme Corp",
            domain="acme"
        )
        db.add(tenant)
        db.commit()
        db.refresh(tenant)
        print(f"✅ Created Tenant: {tenant.name} (ID: {tenant.id})")

    # --- USER SECTION ---
    # Check if the admin user already exists to prevent duplicates
    existing_user = db.query(models.User).filter(models.User.email == "admin@acme.com").first()
    
    if existing_user:
        print("⚠️  User 'admin@acme.com' already exists.")
    else:
        new_user = models.User(
            email="admin@acme.com",
            full_name="Admin User",
            hashed_password=get_password_hash("secret123"), 
            role="admin",
            tenant_id=tenant.id # Link to the tenant we found or created above
        )
        db.add(new_user)
        db.commit()
        print(f"✅ Created User: {new_user.email}")
    
    print("🚀 Seeding Complete!")

if __name__ == "__main__":
    seed_data()