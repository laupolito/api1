from pydantic import BaseModel
from pydantic import validator
import re

class User(BaseModel):
     id : int
     username: str
     password: str
     idade: int
     cpf: str
     
     @validator('password')
     def validate_password(cls , value):
          if len(value) <=8:
               raise ValueError('Senha deve conter no minimo 8 caracteres')
          return value
     
     @validator('idade')
     def validate_idade(cls, value):
          if value <18:
               raise ValueError('Proibido menores de 18 anos')
          return value
        