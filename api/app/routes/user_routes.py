from typing import List
from fastapi import APIRouter, Response, Depends, status, Query, HTTPException
from sqlalchemy.orm import Session
from db.database import engine,SessionLocal
from db.models import User as UserModel
from schemas.user import User as UserOutput
from sqlalchemy.orm import Session

from db.base import Base


#cria a tabela
Base.metadata.create_all(bind=engine)
router = APIRouter(prefix="/user")   

def get_db():
    try:
        db = SessionLocal()
        #TODO 
        yield db
    finally:
        db.close()


@router.post("/addComSchema", status_code=status.HTTP_201_CREATED, description='Adicionar usuário')
def add_user(request:UserOutput, db: Session = Depends(get_db)):
        # produto_on_db = ProdutosModel(id=request.id, item=request.item, peso=request.peso, numero_caixas=request.numero_caixas)
        user_on_db = UserModel(**request.dict())
        db.add(user_on_db)
        db.commit()
        return Response(status_code=status.HTTP_201_CREATED)

@router.get("/{user_name}", description="Listar o usuário pelo nome")
def get_user(user_name,db: Session = Depends(get_db)):
    user_on_db= db.query(UserModel).filter(UserModel.item == user_name).first()
    return user_on_db


@router.get("/user/listar")
async def get_tarefas(db: Session = Depends(get_db)):
    user = db.query(UserModel).all()
    return user

#validação no código
@router.delete("/{id}", description="Deletar o usuário pelo id")
def delete_user(id: int, db: Session = Depends(get_db)):


    user_on_db = db.query(UserModel).filter(UserModel.id == id).first()
    if user_on_db is None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail='Sem usuário com este id')
    db.delete(user_on_db)
    db.commit()
    return f"Banco with id {id} deletado.", Response(status_code=status.HTTP_200_OK)

@router.put('/update/{id}', description='Update user')
def update_user(
    id: int,
    user: UserOutput,
    db: Session = Depends(get_db)
    
    ):
    user_on_db = db.query(UserModel).filter_by(id=id).first()
    if user_on_db is None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail='No user was found with the given id')
        
    user_on_db.username = user.username
    user_on_db.password = user.password
    user_on_db.idade = user.idade
    user_on_db.cpf = user.cpf

    

    db.add(user_on_db)
    db.commit()
    return "ok"
