# Trabalho Prático 1 – Algoritmos 2

**Professor:** Renato Vimieiro  
**Semestre:** 2025.1

## 👥 Membros do Grupo

- **Bernardo Alves Miranda** – 2023028021  
- **Bernardo Venancio Cunha Oliveira** – 2023028684  
- **Lucas Albuquerque Santos Costa** – 2023028005

---

## 📁 Estrutura geral do Projeto

```
docs/
├── app.py               # API Flask com implementação da KD-Tree
├── index.html           # Interface web para visualização do mapa
├── script.js            # Callback JavaScript para interação com o mapa
├── bares_com_cdb.csv    # Dados dos estabelecimentos
├── comida_di_buteco.csv # Informações filtradas dos bares do Comida di Buteco
├── regiao_bh.geojson    # Dados usados para fazer o contorno dos distritos no mapa
└── download_images.py   # Script para baixar imagens dos pratos Comida di Buteco
```

- A pasta "data" é um apanhado das coisas que usamos para extrair os dados usados na aplicação.  
- A pasta "ponto_extra" é um apanhado das coisas que usamos para extrair/manipular os dados usados para resolver os pontos extras.

---

## 🧠 Lógica Principal

A aplicação backend implementa uma **KD-Tree** personalizada para otimizar consultas por localização geográfica, permitindo encontrar bares próximos com eficiência. A visualização no frontend é feita com mapas interativos via **Leaflet**.  

---

## ⚙️ Como rodar/usar?
Acesse o link do github pages: https://bernardoam04.github.io/TP-ALG2/  
**É necessário esperar alguns segundos ao iniciar a aplicação pela primeira vez.**  

Guia rápido de uso:  

- Clique no ícone de retângulo à esquerda da interface e selecione a área de busca desejada.  
- À direita, estão disponibilizadas as opções para visualizar somente bares/restaurantes.  
- Os pontos numerados representam locais com densidade de informação alta (possivelmente, 2 ou mais bares ou informações repetidas).

