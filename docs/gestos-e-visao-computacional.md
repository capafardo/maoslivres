# 🖐️ Visão Computacional, Gestos & Filtros Espaciais

## 1. Rastreamento Holográfico Bare-Hands

O sistema utiliza a biblioteca **MediaPipe Hands** para capturar a mão do usuário em 3D através de uma webcam comum, sem requerer luvas, sensores vestíveis ou dispositivos táteis.

* **Pontos Articulares**: 21 marcos 3D (polegar, nós dos dedos, pontas e palma).
* **Mira Touchless**: O ponto do dedo indicador (`Landmark 8`) é suavizado por interpolação linear (*Lerp 0.45*) para eliminar tremores naturais.
* **Gesto de Pinça (*Pinch*)**: Calculado pela distância euclidiana no espaço da tela entre o polegar (`Landmark 4`) e o indicador (`Landmark 8`).

---

## 2. Filtro Espacial de Usuário Principal (Imunidade a Pessoas ao Fundo)

Em salas de aula e clínicas com mediadores, outros alunos e familiares em movimento, o algoritmo aplica uma filtragem multicritério para focar exclusivamente no aluno atendido:

1. **Filtro de Proximidade (Escala da Mão)**:
   * A mão do aluno em primeiro plano possui uma envergadura (*span*) consideravelmente maior que a de pessoas em pé atrás. Mãos com envergadura inferior a `0.08` da altura da tela são descartadas.
2. **Centralidade**:
   * Prioriza o centro da câmera, onde o aluno em atendimento senta.
3. **Trava Temporal de Continuidade (*Hand Lock Anchor*)**:
   * O sistema cria uma âncora na posição `(X, Y)` da mão detectada. Nos quadros subsequentes, aplica um bônus de continuidade que impede que o cursor pule para a mão de outra pessoa que acene no ambiente.

---

## 3. Estabilização de Pinça (*Anti-Jitter*)

Para evitar que movimentos acidentais ou acenos rápidos disparem comandos:
* A pinça deve ser mantida por pelo menos **4 quadros consecutivos (~120ms)** para ser validada como intenção voluntária.

---

## 4. Cooldown de 10 Segundos (Anti-Duplo Acionamento)

Após cada acionamento bem-sucedido de um cartão:
* O sistema entra em um intervalo de bloqueio temporário de **10 segundos** (configurável no painel entre 3s e 25s).
* O cursor exibe um anel de progresso em contagem regressiva âmbar (`10s... 9s...`).
* O banner central exibe a contagem e os cartões entram em estado de repouso, prevenindo repetições acidentais por hiperfoco ou permanência da mão sobre o alvo.
