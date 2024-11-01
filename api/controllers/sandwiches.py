from sqlalchemy.orm import Session
from fastapi import HTTPException, status, Response, Depends
from ..models import models, schemas




# Create function to add a new sandwich
def create(db: Session, sandwich):
    # Create a new instance of the Sandwich model with the provided data
    db_sandwich = models.Sandwich(
        name=sandwich.name,
        ingredients=sandwich.ingredients,
        price=sandwich.price
    )
    # Add the new Sandwich to the database session
    db.add(db_sandwich)
    # Commit the changes to the database
    db.commit()
    # Refresh the Sandwich object to reflect the current state in the database
    db.refresh(db_sandwich)
    # Return the newly created Sandwich object
    return db_sandwich


# Update function to modify an existing sandwich
def update(db: Session, sandwich_id, sandwich):
    # Query the database for the specific sandwich to update
    db_sandwich = db.query(models.Sandwich).filter(models.Sandwich.id == sandwich_id)
    # Extract update data from the provided 'sandwich' object, excluding unset fields
    update_data = sandwich.model_dump(exclude_unset=True)
    # Update the database record with the new data
    db_sandwich.update(update_data, synchronize_session=False)
    # Commit the changes to the database
    db.commit()
    # Return the updated Sandwich object
    return db_sandwich.first()


# Delete function to remove a sandwich
def delete(db: Session, sandwich_id):
    # Query the database for the specific sandwich to delete
    db_sandwich = db.query(models.Sandwich).filter(models.Sandwich.id == sandwich_id)
    # Delete the sandwich from the database
    db_sandwich.delete(synchronize_session=False)
    # Commit the changes to the database
    db.commit()
    # Return a response indicating successful deletion (204 No Content)
    return Response(status_code=status.HTTP_204_NO_CONTENT)


# Read all sandwiches from the database
def read_all(db: Session):
    return db.query(models.Sandwich).all()


# Read a specific sandwich by its ID
def read_one(db: Session, sandwich_id):
    return db.query(models.Sandwich).filter(models.Sandwich.id == sandwich_id).first()



