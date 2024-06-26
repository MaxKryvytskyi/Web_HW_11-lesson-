from sqlalchemy.orm import Session
from sqlalchemy import text, func
from datetime import datetime, timedelta, date

from src.database.models import Contact
from src.schemas import ContactUpdate, ContactBase, ContactDataUpdate, ContactResponse


async def get_contacts(skip: int, limit: int, db: Session):
    contacts = db.query(Contact).offset(skip).limit(limit).all()
    return contacts


async def get_contact(contact_id: int, db: Session):
    contact = db.query(Contact).filter(Contact.id==contact_id).first()
    return contact


async def create_contact(body: ContactBase, db: Session):
    contact = Contact(
        first_name = body.first_name,
        last_name = body.last_name,
        email = body.email,
        phone = body.phone,
        birthday = body.birthday,
        data = body.data
    )
    db.add(contact)
    db.commit()
    db.refresh(contact)
    return contact


async def update_contact(contact_id: int, body: ContactUpdate, db: Session):
    contact = db.query(Contact).filter(Contact.id==contact_id).first()
    if contact:
        contact.first_name = body.first_name
        contact.last_name = body.last_name
        contact.email = body.email
        contact.phone = body.phone
        contact.birthday = body.birthday
        contact.data = body.data
        db.commit()
    return contact


async def update_data_contact(contact_id: int, body: ContactDataUpdate, db: Session):
    contact = db.query(Contact).filter(Contact.id==contact_id).first()
    if contact:
        contact.data = body.data
        db.commit()
    return contact


async def remove_contact(contact_id: int, db: Session):
    contact = db.query(Contact).filter(Contact.id==contact_id).first()
    if contact:
        db.delete(contact)
        db.commit()
    return contact


async def get_birstdays(skip: int, limit: int, db: Session):
    today = datetime.today()
    seven_days_later = today + timedelta(days=7)
    contact_birthdays = db.query(Contact).filter(
        text("TO_CHAR(birthday, 'MM-DD') BETWEEN :start_date AND :end_date")).params(
        start_date=today.strftime('%m-%d'), 
        end_date=seven_days_later.strftime('%m-%d')).offset(skip).limit(limit).all()
    
    contact_list = []
    
    for contact in contact_birthdays:
        contact_response = ContactResponse(
            id=contact.id,
            first_name=contact.first_name,
            last_name=contact.last_name,
            email=contact.email,
            phone=contact.phone,
            birthday=contact.birthday,
            data=contact.data)
        contact_list.append(contact_response)
    return contact_list



async def search_contacts(first_name: str, last_name: str, email: str, phone: str, birthday: date, db: Session):
    query = db.query(Contact)
    contacts = []
    if first_name:
        query1 = query.filter(Contact.first_name.ilike(f"%{first_name}%"))
        contacts.extend(query1.all())
    if last_name:
        query1 = query.filter(Contact.last_name.ilike(f"%{last_name}%"))
        contacts.extend(query1.all())
    if email:
        query1 = query.filter(Contact.email.ilike(f"%{email}%"))       
        contacts.extend(query1.all())
    if phone:
        query1 = query.filter(Contact.phone.ilike(f"%{phone}%"))       
        contacts.extend(query1.all())
    if birthday:
        query1 = query.filter(func.DATE(Contact.birthday) == birthday)
        contacts.extend(query1.all())
    return list(set(contacts))