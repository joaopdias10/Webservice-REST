from fastapi import FastAPI, status, Path, HTTPException, Body
from typing import Annotated
from banco import DB

app = FastAPI()
db = DB()

# READs - GET
@app.get("/boletim", status_code=status.HTTP_200_OK)
def read_All():
    dados = db.readAll()
    if dados is None:
        return {'info':'Não há dados'}
    
    else:
        retorno = []
        for dado in dados:
            dado_resp = db.readResponsaveis(dado[0])
            if dado_resp is not None:
                info_resp = {
                    'id': dado_resp[0],
                    'idmateria': dado_resp[1],
                    'professor': dado_resp[2],
                    'monitor1': dado_resp[3],
                    'monitor2': dado_resp[4]
                }
            else:
                info_resp = {}

            info = {
                'id':dado[0],
                'codigo':dado[1],
                'disciplina':dado[2],
                'turma':dado[3],
                'faltas':dado[4],
                'nota':dado[5],
                'responsaveis': info_resp
            }
            retorno.append(info)
        return retorno

@app.get("/boletim/{id_materia}", status_code=status.HTTP_200_OK)
def read_Materia(id_materia : Annotated[int, Path(ge=0)]):
    dados = db.read(id_materia)
    if dados is None:
        raise HTTPException(status.HTTP_404_NOT_FOUND,"Não encontrado")
    
    else:
        dado_resp = db.readResponsaveis(dados[0])
        if dado_resp is not None:
            info_resp = {
                'id': dado_resp[0],
                'idmateria': dado_resp[1],
                'professor': dado_resp[2],
                'monitor1': dado_resp[3],
                'monitor2': dado_resp[4]
                }
        else:
            info_resp = {}
        retorno = {
                'id':dados[0],
                'codigo':dados[1],
                'disciplina':dados[2],
                'turma':dados[3],
                'faltas':dados[4],
                'nota':dados[5],
                'responsaveis': info_resp
        }
        return retorno

@app.get("/boletim/{id_materia}/responsaveis", status_code=status.HTTP_200_OK)
def read_Responsaveis(id_materia : Annotated[int, Path(ge=0)]):
    dados = db.readResponsaveis(id_materia)
    if dados is None:
        raise HTTPException(status.HTTP_404_NOT_FOUND,"Não encontrado")
    else:
        retorno = {
                'id':dados[0],
                'idmateria':dados[1],
                'professor':dados[2],
                'monitor1':dados[3],
                'monitor2':dados[4]
        }
        return retorno



# CREATEs - POST
@app.post("/boletim",status_code=status.HTTP_201_CREATED)
def create_Materia(codigo:Annotated[str, Body(min_length=5)],
           disciplina:Annotated[str, Body(min_length=5)], 
           turma:Annotated[str, Body(min_length=4)], 
           faltas:Annotated[int, Body(ge=0, le=80)], 
           nota:Annotated[float, Body(ge=0, le=100)]):
    id = db.create(codigo, disciplina, turma, faltas, nota)
    if id is None:
        raise HTTPException(status.HTTP_500_INTERNAL_SERVER_ERROR,"Erro no banco")
    else:
        return {'id':id}
    
@app.post("/boletim/{id_materia}", status_code=status.HTTP_201_CREATED)
def create_Responsaveis(id_materia:Annotated[int,Path(ge=0)],
                 professor:Annotated[str,Body(min_length=3)],
                 monitor1:Annotated[str,Body(min_length=3)],
                 monitor2:Annotated[str,Body(min_length=3)]):
    if db.read(id_materia) is None:
        raise HTTPException(status.HTTP_404_NOT_FOUND,"Materia não cadastrado")
    
    id = db.createResponsaveis(id_materia, professor, monitor1, monitor2)
    if id is None:
        raise HTTPException(status.HTTP_500_INTERNAL_SERVER_ERROR,"Erro no banco")
    else:
        return {'id':id}



# UPDATEs - PUT
@app.put("/boletim/{id_materia}",status_code=status.HTTP_200_OK)
def update_Put_Materia(id_materia:Annotated[int,Path(ge=0)],
           codigo:Annotated[str, Body(min_length=5)],
           disciplina:Annotated[str, Body(min_length=5)], 
           turma:Annotated[str, Body(min_length=4)], 
           faltas:Annotated[int, Body(ge=0, le=80)], 
           nota:Annotated[float, Body(ge=0, le=100)]):
    if db.read(id_materia) is None:
        raise HTTPException(status.HTTP_404_NOT_FOUND,"Materia não cadastrado")
    
    dados = db.update(id_materia, codigo, disciplina, turma, faltas, nota)
    if dados is None:
        raise HTTPException(status.HTTP_500_INTERNAL_SERVER_ERROR,"Erro no banco")
    else:
        retorno = {
                'id':dados[0],
                'codigo':dados[1],
                'disciplina':dados[2],
                'turma':dados[3],
                'faltas':dados[4],
                'nota':dados[5]
        }
        return retorno
    
@app.put("/boletim/{id_materia}/responsaveis", status_code=status.HTTP_200_OK)
def update_Put_Responsaveis(id_materia:Annotated[int,Path(ge=0)],
                 professor:Annotated[str,Body(min_length=3)],
                 monitor1:Annotated[str,Body(min_length=3)],
                 monitor2:Annotated[str,Body(min_length=3)]):
    if db.read(id_materia) is None:
        raise HTTPException(status.HTTP_404_NOT_FOUND,"Materia não cadastrado")
    
    if db.readResponsaveis(id_materia) is None:
        raise HTTPException(status.HTTP_404_NOT_FOUND,"Responsaveis não cadastrado")
    
    dados = db.updateResponsaveis(id_materia, professor, monitor1, monitor2)
    if dados is None:
        raise HTTPException(status.HTTP_500_INTERNAL_SERVER_ERROR,"Erro no banco")
    else:
        retorno = {
                'id':dados[0],
                'idmateria':dados[1],
                'professor':dados[2],
                'monitor1':dados[3],
                'monitor2':dados[4]
        }
        return retorno


# UPDATEs - patch
@app.patch("/boletim/{id_materia}",status_code=status.HTTP_200_OK)
def update_Patch_Materia(
    id_materia: Annotated[int, Path(ge=0)],
    codigo: Annotated[str | None, Body(min_length=5)] = None,
    disciplina: Annotated[str | None, Body(min_length=5)] = None,
    turma: Annotated[str | None, Body(min_length=4)] = None,
    faltas: Annotated[int | None, Body(ge=0, le=80)] = None,
    nota: Annotated[float | None, Body(ge=0, le=100)] = None):
    if db.read(id_materia) is None:
        raise HTTPException(status.HTTP_404_NOT_FOUND,"Materia não cadastrado")

    dados = db.update(id_materia, codigo, disciplina, turma, faltas, nota)
    if dados is None:
        raise HTTPException(status.HTTP_500_INTERNAL_SERVER_ERROR,"Erro no banco")
    else:
        retorno = {
                'id':dados[0],
                'codigo':dados[1],
                'disciplina':dados[2],
                'turma':dados[3],
                'faltas':dados[4],
                'nota':dados[5]
        }
        return retorno

@app.patch("/boletim/{id_materia}/responsaveis", status_code=status.HTTP_200_OK)
def update_Patch_Responsaveis(id_materia:Annotated[int,Path(ge=0)],
                 professor: Annotated[str | None, Body(min_length=3)] = None,
                 monitor1: Annotated[str | None, Body(min_length=3)] = None,
                 monitor2: Annotated[str | None, Body(min_length=3)] = None):
    if db.read(id_materia) is None:
        raise HTTPException(status.HTTP_404_NOT_FOUND,"Materia não cadastrado")
    
    if db.readResponsaveis(id_materia) is None:
        raise HTTPException(status.HTTP_404_NOT_FOUND,"Responsaveis não cadastrado")
    
    dados = db.updateResponsaveis(id_materia, professor, monitor1, monitor2)
    if dados is None:
        raise HTTPException(status.HTTP_500_INTERNAL_SERVER_ERROR,"Erro no banco")
    else:
        retorno = {
                'id':dados[0],
                'idmateria':dados[1],
                'professor':dados[2],
                'monitor1':dados[3],
                'monitor2':dados[4]
        }
        return retorno

# DELETEs - DELETE
@app.delete("/boletim/{id_materia}", status_code=status.HTTP_200_OK)
def delete_Materia(id_materia : Annotated[int, Path(ge=0)]):
    if db.read(id_materia) is None:
        raise HTTPException(status.HTTP_404_NOT_FOUND,"Materia não cadastrado")

    dados = db.delete(id_materia)
    if dados is None:
        raise HTTPException(status.HTTP_500_INTERNAL_SERVER_ERROR,"Erro no banco")
    else:
        retorno = {
                'id':dados[0],
                'codigo':dados[1],
                'disciplina':dados[2],
                'turma':dados[3],
                'faltas':dados[4],
                'nota':dados[5]
        }
        return retorno

@app.delete("/boletim/{id_materia}/responsaveis", status_code=status.HTTP_200_OK)
def delete_Responsaveis(id_materia : Annotated[int, Path(ge=0)]):
    if db.read(id_materia) is None:
        raise HTTPException(status.HTTP_404_NOT_FOUND,"Materia não cadastrado")
    
    if db.readResponsaveis(id_materia) is None:
        raise HTTPException(status.HTTP_404_NOT_FOUND,"Responsaveis não cadastrado")

    dados = db.deleteResponsaveis(id_materia)
    if dados is None:
        raise HTTPException(status.HTTP_500_INTERNAL_SERVER_ERROR,"Erro no banco")
    else:
        retorno = {
                'id':dados[0],
                'idmateria':dados[1],
                'professor':dados[2],
                'monitor1':dados[3],
                'monitor2':dados[4]
        }
        return retorno