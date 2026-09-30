import sqlite3

class DB:

    def __init__(self):
        self.conexao = sqlite3.connect("banco.db",check_same_thread=False)
        self.conexao.execute("PRAGMA foreign_keys = ON")
        cursor = self.conexao.cursor()
        cursor.execute("CREATE TABLE IF NOT EXISTS boletim(id INTEGER PRIMARY KEY, codigo, disciplina, turma, faltas, nota)")
        cursor.execute("CREATE TABLE IF NOT EXISTS responsaveis(id INTEGER PRIMARY KEY, idmateria, professor, monitor1, monitor2, FOREIGN KEY(idmateria) REFERENCES boletim(id) ON DELETE CASCADE)")
        self.conexao.commit()
        cursor.close()

    def create(self, codigo, disciplina, turma, faltas, nota):
        cursor = self.conexao.cursor()
        cursor.execute("INSERT INTO boletim(codigo, disciplina, turma, faltas, nota) VALUES (?,?,?,?,?)",(codigo, disciplina, turma, faltas, nota))
        
        if (cursor.rowcount > 0):
            id = cursor.lastrowid
        else:
            id = None

        self.conexao.commit()
        cursor.close()
        return id
    
    def createResponsaveis(self, id_materia, professor, monitor1, monitor2):
        cursor = self.conexao.cursor()
        cursor.execute("INSERT INTO responsaveis(idmateria, professor, monitor1, monitor2) VALUES (?,?,?,?)",(id_materia, professor, monitor1, monitor2))
        
        if (cursor.rowcount > 0):
            id = cursor.lastrowid
        else:
            id = None

        self.conexao.commit()
        cursor.close()
        return id

    def read(self, id):
        cursor = self.conexao.cursor()
        cursor.execute("SELECT * FROM boletim WHERE id = ?", (id,))
        materia = cursor.fetchone()
        cursor.close()
        return materia
    
    def readAll(self):
        cursor = self.conexao.cursor()
        cursor.execute("SELECT * FROM boletim")
        materias = cursor.fetchall()
        cursor.close()
        return materias

    def readResponsaveis(self, id_materia):
        cursor = self.conexao.cursor()
        cursor.execute("SELECT * FROM responsaveis WHERE idmateria = ?", (id_materia,))
        responsaveis = cursor.fetchone()
        cursor.close()
        return responsaveis
    
    def readAllResponsaveis(self):
        cursor = self.conexao.cursor()
        cursor.execute("SELECT * FROM responsaveis")
        responsaveis = cursor.fetchall()
        cursor.close()
        return responsaveis

    def update(self, id, codigo, disciplina, turma, faltas, nota):
        materia = self.read(id)
        if materia is None:
            return None

        codigo = codigo if codigo is not None else materia[1]
        disciplina = disciplina if disciplina is not None else materia[2]
        turma = turma if turma is not None else materia[3]
        faltas = faltas if faltas is not None else materia[4]
        nota = nota if nota is not None else materia[5]

        cursor = self.conexao.cursor()
        cursor.execute("UPDATE boletim SET codigo = ?, disciplina = ?, turma = ?, faltas = ?, nota = ? WHERE id = ?", (codigo, disciplina, turma, faltas, nota, id))
        self.conexao.commit()
        cursor.close()
        materia = self.read(id)
        return materia

    def updateResponsaveis(self, id_materia, professor, monitor1, monitor2):
        responsaveis = self.readResponsaveis(id_materia)
        if responsaveis is None:
            return None

        #print(responsaveis)
        professor = professor if professor is not None else responsaveis[2]
        monitor1 = monitor1 if monitor1 is not None else responsaveis[3]
        monitor2 = monitor2 if monitor2 is not None else responsaveis[4]

        cursor = self.conexao.cursor()
        cursor.execute("UPDATE responsaveis SET professor = ?, monitor1 = ?, monitor2 = ? WHERE idmateria = ?", (professor, monitor1, monitor2, id_materia))
        self.conexao.commit()
        cursor.close()
        responsaveis = self.readResponsaveis(id_materia)
        return responsaveis

    def delete(self, id):
        cursor = self.conexao.cursor()
        materia = self.read(id)
        cursor.execute("DELETE FROM boletim WHERE id = ?", (id,))
        self.conexao.commit()
        cursor.close()
        return materia

    def deleteResponsaveis(self, id_materia):
        cursor = self.conexao.cursor()
        responsaveis = self.readResponsaveis(id_materia)
        cursor.execute("DELETE FROM responsaveis WHERE idmateria = ?", (id_materia,))
        self.conexao.commit()
        cursor.close()
        return responsaveis