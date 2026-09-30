# Webservice REST — Boletim

Webservice REST desenvolvido para a disciplina de **Sistemas Distribuídos** (Engenharia de Computação — UTFPR, Campus Toledo).

A API gerencia um boletim escolar composto por duas entidades relacionadas:

- **boletim** (matéria): código, disciplina, turma, faltas e nota.
- **responsaveis**: professor e monitores vinculados a uma matéria (relação 1:1, com exclusão em cascata).

## Tecnologias

- [Python 3](https://www.python.org/)
- [FastAPI](https://fastapi.tiangolo.com/) — framework web
- [Uvicorn](https://www.uvicorn.org/) — servidor ASGI
- [SQLite](https://www.sqlite.org/) — banco de dados (biblioteca padrão `sqlite3`)

## Requisitos

- Python 3.10 ou superior (o código usa a sintaxe `str | None`)

## Instalação

```bash
# (opcional) crie e ative um ambiente virtual
python -m venv venv
# Windows
venv\Scripts\activate
# Linux/macOS
source venv/bin/activate

# instale as dependências
pip install fastapi uvicorn
```

## Como executar

```bash
uvicorn main:app --reload
```

O banco `banco.db` e as tabelas são criados automaticamente na primeira execução.

- Documentação interativa (Swagger): http://127.0.0.1:8000/docs
- Alternativa para testes: https://reqbin.com/post-online

## Endpoints

Base: `/boletim`

### Matérias

| Método   | Rota                    | Descrição                                    |
| -------- | ----------------------- | -------------------------------------------- |
| `GET`    | `/boletim`              | Lista todas as matérias (com responsáveis)   |
| `GET`    | `/boletim/{id}`         | Retorna uma matéria pelo id                   |
| `POST`   | `/boletim`              | Cria uma matéria                              |
| `PUT`    | `/boletim/{id}`         | Atualiza todos os campos de uma matéria       |
| `PATCH`  | `/boletim/{id}`         | Atualiza parcialmente uma matéria             |
| `DELETE` | `/boletim/{id}`         | Remove uma matéria (e seus responsáveis)      |

### Responsáveis

| Método   | Rota                             | Descrição                          |
| -------- | -------------------------------- | ---------------------------------- |
| `GET`    | `/boletim/{id}/responsaveis`     | Retorna os responsáveis da matéria |
| `POST`   | `/boletim/{id}`                  | Cria os responsáveis da matéria    |
| `PUT`    | `/boletim/{id}/responsaveis`     | Atualiza todos os responsáveis     |
| `PATCH`  | `/boletim/{id}/responsaveis`     | Atualiza parcialmente              |
| `DELETE` | `/boletim/{id}/responsaveis`     | Remove os responsáveis             |

### Exemplo de criação de matéria

```bash
curl -X POST http://127.0.0.1:8000/boletim \
  -H "Content-Type: application/json" \
  -d '{"codigo": "SD001", "disciplina": "Sistemas Distribuidos", "turma": "9ENC", "faltas": 4, "nota": 85.5}'
```

## Estrutura do projeto

```
Webservice-REST/
├── main.py         # rotas da API (FastAPI)
├── banco.py        # camada de acesso ao banco (classe DB, SQLite)
├── banco.db        # banco SQLite (gerado em tempo de execução)
├── Relatorio.pdf   # relatório da atividade
└── README.md
```

## Licença

MIT. Ver [LICENSE](LICENSE).
