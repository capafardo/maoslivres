# 🔌 Referência da API & Endpoints FastAPI

O servidor HTTP local (`app.py`) fornece uma API REST para gerenciamento de cartões e registros de sessão.

## Endpoints Disponíveis

### 1. `GET /`
* **Descrição**: Serve a aplicação web principal (`index.html`).
* **Headers**: `Cache-Control: no-cache, no-store, must-revalidate` para garantir versões atualizadas.

---

### 2. `GET /api/cards`
* **Descrição**: Retorna o catálogo completo dos 4 quadrantes com categorias, cartões e caminhos dos pictogramas.
* **Resposta (Exemplo)**:
```json
{
  "categories": [
    {
      "id": "sensorial",
      "nome": "Sensorial & Conforto",
      "icone": "🧘",
      "cor": "#00f0ff",
      "cards": [
        {
          "id": "s1",
          "label": "Estou Confortável",
          "texto": "Estou me sentindo confortável e bem no ambiente.",
          "tipo": "sucesso",
          "icone": "🟢",
          "pictograma": "static/pictograms/s1_confortavel.png",
          "arasaac_id": "31310"
        }
      ]
    }
  ]
}
```

---

### 3. `POST /api/cards`
* **Descrição**: Atualiza e persiste alterações na lista de cartões em `cards.json`.

---

### 4. `GET /api/logs` (ou `/api/log`)
* **Descrição**: Retorna o histórico de manifestações registradas na sessão.

---

### 5. `POST /api/logs` (ou `/api/log`)
* **Descrição**: Registra um novo evento de comunicação.
* **Payload**:
```json
{
  "card_id": "s1",
  "label": "Estou Confortável",
  "texto": "Estou me sentindo confortável e bem no ambiente.",
  "categoria": "Sensorial & Conforto",
  "icone": "🟢",
  "pictograma": "static/pictograms/s1_confortavel.png",
  "timestamp": "10:15:30",
  "origem": "gesto_pinça"
}
```

---

### 6. `DELETE /api/logs`
* **Descrição**: Limpa os registros da sessão atual.

---

### 7. `GET /static/pictograms/{filename}`
* **Descrição**: Serve diretamente os arquivos de imagem PNG dos pictogramas ARASAAC locais.
