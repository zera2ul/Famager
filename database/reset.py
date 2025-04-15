from models import Base


if __name__ == "__main__":
    Base.delete_models()
    Base.create_models()
