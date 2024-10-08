from flask_login import UserMixin
from sqlalchemy import Boolean, Column, DateTime, ForeignKey, Integer, String, Enum
from sqlalchemy.orm import relationship, declarative_base

Base = declarative_base()


# Employee Table
class Employee(Base, UserMixin):
    __tablename__ = "employees"

    name = Column(String(60), nullable=False)
    employee_number = Column(Integer, unique=True, nullable=False, primary_key=True)
    username = Column(String(40), unique=True, nullable=False)
    email = Column(String(120), unique=True, nullable=False)
    password = Column(String(40), nullable=False)
    is_admin = Column(Boolean, default=False)

    # Define one-to-many relationship with Review
    reviews = relationship("Review", backref="employee", lazy=True)

    def __repr__(self):
        return f"<Employee {self.name}>"

    # Manually set ID as employee_number, ID does not exist in table
    def get_id(self):
        return self.employee_number


# Review Table
class Review(Base):
    __tablename__ = "reviews"

    review_id = Column(Integer, primary_key=True)

    # Link employee number as foreign key
    employee_number = Column(
        Integer, ForeignKey("employees.employee_number"), nullable=False
    )
    review_date = Column(DateTime, nullable=False)
    reviewer_id = Column(Integer, nullable=False)
    overall_performance_rating = Column(
        Enum(
            "Excellent", "Good", "Satisfactory", "Needs Improvement", "Unsatisfactory"
        ),
        nullable=False,
    )
    goals = Column(String, nullable=False)
    reviewer_comments = Column(String, nullable=False)

    def __repr__(self):
        return f"<Review {self.review_id} - Employee {self.reviewer_id}>"
