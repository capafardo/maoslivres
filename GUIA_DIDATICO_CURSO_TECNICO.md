# 📘 Guia Didático: Projeto Mãos Livres no Curso Técnico de Manutenção
### Roteiro Pedagógico e Técnico para Professores e Alunos de TI

---

## 🎯 1. Objetivos Pedagógicos do Projeto

Este projeto foi desenhado para elevar o nível da turma de **Manutenção e Suporte em Informática**, indo muito além da formatação de computadores e troca de peças básicas. Ele conecta:
1. **Infraestrutura e Hardware de Periféricos:** Otimização de câmeras, monitores, GPU e iluminação.
2. **Visão Computacional no Navegador:** IA em tempo real com baixa latência usando WebAssembly/WebGL.
3. **Tecnologia Assistiva e Inclusão:** Desenvolvimento de soluções com impacto real para pessoas com Transtorno do Espectro Autista (TEA).

---

## 🖥️ 2. Guia de Hardware e Montagem do Laboratório (Para a Turma)

### A. Posicionamento e Iluminação da Câmera
* **Webcam Recomendada:** Câmeras com resolução mínima de 720p a 30fps (preferencialmente 60fps) com amplo ângulo de visão (FOV $\ge 70^\circ$).
* **Iluminação do Ambiente:** 
  * A visão computacional baseada em IA depende do contraste da mão contra o fundo.
  * **Dica de Manutenção:** Evite luz direta atrás do aluno (contra-luz). Posicione uma luz difusa e suave na frente ou acima da tela.
* **Ergonomia Touchless:** O aluno deve estar posicionado entre 50 cm e 1 metro da tela, permitindo que a mão fique dentro do campo visual sem causar fadiga nos ombros.

### B. Aceleração de Hardware e Otimização do Navegador
Ensine os alunos a verificarem se o computador está usando a GPU para processar o MediaPipe:
1. No Chrome/Brave/Edge, digite na barra de endereço: `chrome://gpu`
2. Certifique-se de que **"Rasterization"** e **"WebGL"** estão em **"Hardware accelerated"**.
3. Em computadores com placas de vídeo dedicadas (NVIDIA/AMD) ou gráficos integrados Intel/AMD, verifique os drivers de vídeo atualizados.

### C. Otimização para Computadores Modestos (Modo Eco)
Em laboratórios escolares com computadores de entrada (i3 antigos, Celeron ou gráficos integrados Intel HD), o sistema conta com o **Modo Eco**:
* **MediaPipe Lite (`modelComplexity: 0`):** Reduz o grafo neural convolucional da IA em ~60% dos FLOPs, mantendo excelente precisão espacial da ponta dos dedos.
* **Frame Throttling Inteligente:** Processa a inferência de visão computacional em frames alternados (30 FPS de IA) enquanto interpola o cursor a 60 FPS fluidos via filtro *Lerp*.
* **Bypass de Shaders e Canvas Glow:** Substitui o cálculo pesado de desfoque gaussiano no Canvas 2D (`shadowBlur: 0`) e filtros de GPU (`backdrop-filter`) por linhas neon sólidas e vidro semi-opaco.
* **Ativação:** Pode ser ativado no Painel do Profissional (tecla `[P]`), reduzindo o consumo de CPU/GPU em até **65%**.

---

## 🧠 3. Como Funciona a Visão Computacional (MediaPipe Hands)

O sistema utiliza a biblioteca **MediaPipe Hands** do Google, que roda diretamente no navegador via WebAssembly:

```
[ Imagem da Câmera (60fps) ]
              │
              ▼
   [ Detector de Palma ] ──► Localiza a mão na cena
              │
              ▼
  [ Regressão de Landmarks ] ──► Mapeia 21 pontos 3D da mão
              │
              ▼
 [ Conversão de Coordenadas ] ──► Inverte o eixo X (Modo Espelho)
              │
              ▼
  [ Algoritmo de Gestos ] ──► Calcula Pinça e Dwell Time
```

### A. Cálculo da Distância de Pinça (Pinch)
Para saber se o aluno juntou o polegar com o indicador (para "agarrar" o holograma), usamos a fórmula da **Distância Euclidiana** entre os marcos 4 (ponta do polegar) e 8 (ponta do indicador):

$$d = \sqrt{(x_4 - x_8)^2 + (y_4 - y_8)^2}$$

Se $d < 0.055$ (limiar configurável no painel do profissional), o sistema ativa o estado `isPinching = true`.

### B. Suavização de Jitter (Filtro Lerp / Média Móvel)
Mãos humanas tremem naturalmente. Para que o cursor holográfico não fique instável, aplicamos uma interpolação linear (*Lerp*):

$$P_{\text{novo}} = P_{\text{anterior}} + \alpha \times (P_{\text{medido}} - P_{\text{anterior}})$$

Onde $\alpha = 0.45$ garante resposta rápida com movimento suave e orgânico.

---

## 🧩 4. Tecnologia Assistiva e o Apoio ao TEA

### Por que a Interface Touchless é Revolucionária para o Autismo?
1. **Sensibilidade Tátil e Propriocepção:** Alguns indivíduos no espectro autista apresentam aversão ao contato físico repetido com superfícies (mouses com fios, telas com impressões digitais, teclados sujos). O controle no ar oferece total liberdade tátil.
2. **Engajamento Lúdico (Efeito JARVIS):** A interface futurista estimula o foco visual e o interesse do aluno, transformando a sessão com o psicólogo em uma experiência de alta tecnologia e empoderamento.
3. **Comunicação Aumentativa e Alternativa (CAA):** Pessoas com TEA não-verbais ou em episódios de sobrecarga sensorial (*shutdown*) podem apontar no ar para que a máquina expresse suas necessidades em voz alta.

---

## 🛠️ 5. Desafios Práticos para os Alunos do Curso Técnico

Incentive os alunos a realizarem melhorias no projeto:

1. **Desafio 1 (Redes):** Configurar o servidor Python `app.py` para rodar na rede local do laboratório (`0.0.0.0`) e conectar um tablet ou segundo monitor para que o psicólogo veja a tela de controle remotamente.
2. **Desafio 2 (Hardware IoT):** Integrar com um Arduino ou ESP32 via porta Serial ou WebSocket para acender fitas de LED no laboratório na cor verde/amarela/vermelha quando o aluno manifestar o estado.
3. **Desafio 3 (Personalização):** Adicionar novos conjuntos de cartões e ícones em `cards.json` com fotos reais dos ambientes da escola (ex: biblioteca, cantina, sala de jogos).
