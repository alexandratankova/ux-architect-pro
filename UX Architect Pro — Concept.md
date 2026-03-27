# UX Architect Pro

**Tool di analisi strutturale per siti web**

---

## Il problema

Quando si affronta il redesign di un sito, una migrazione o un audit UX, il primo passo e sempre lo stesso: capire come e fatto il sito oggi. Quante pagine ha? Come sono organizzate? Quali hanno meta description, quali no? Dove sono i contenuti principali?

Farlo a mano richiede ore. Si aprono pagine una per una, si copiano titoli in un foglio Excel, si cerca di ricostruire la struttura. E un lavoro ripetitivo che toglie tempo all'analisi vera.

## La soluzione

UX Architect Pro automatizza questo processo. Si inserisce un URL, si sceglie quanto in profondita scansionare, e in pochi minuti si ottiene una mappa completa del sito con tutti i dati strutturali estratti e le pagine classificate per tipologia.

---

## A chi si rivolge

| Ruolo | Caso d'uso |
|---|---|
| UX Designer | Mappare un sito esistente prima di un redesign |
| Content Strategist | Analizzare la distribuzione e la qualita dei contenuti |
| SEO Specialist | Audit strutturale rapido con identificazione di errori |
| Project Manager | Presentare lo stato di un sito a clienti o stakeholder |

---

## Come funziona

### 1. Configurazione

L'utente inserisce l'URL del sito e configura due parametri:

- **Profondita massima** — fino a 10 livelli di navigazione
- **Pagine massime** — fino a 500 pagine per scansione

### 2. Crawl in tempo reale

L'app scansiona il sito pagina per pagina seguendo i link interni. Durante il crawl mostra:

- Barra di avanzamento con contatore pagine
- Log in tempo reale di ogni pagina analizzata
- Segnalazione immediata degli errori 404 e dei problemi di rete

### 3. Estrazione dati

Per ogni pagina vengono estratti:

- **Title** — il tag title della pagina
- **Meta Description** — la descrizione per i motori di ricerca
- **H1** — il titolo principale della pagina
- **H2** — la lista di tutti i sottotitoli
- **Word Count** — il numero di parole nel contenuto
- **Status Code** — il codice di risposta HTTP
- **Breadcrumbs** — il percorso di navigazione (da JSON-LD o dal DOM)
- **Profondita** — quanti click dalla homepage

### 4. Categorizzazione automatica

Ogni pagina viene classificata automaticamente incrociando tre segnali:

- **Pattern URL** — la struttura del percorso (es. `/blog/...`, `/product/...`)
- **Meta tag Open Graph** — il tipo dichiarato nei metadati (article, product)
- **Keyword nel DOM** — classi CSS e elementi HTML tipici (es. `add-to-cart`, `contact-form`)

Le categorie riconosciute sono:

| Categoria | Cosa identifica |
|---|---|
| Home | La homepage del sito |
| Blog Post | Articoli e contenuti editoriali |
| Blog Archive | Pagine di listing degli articoli |
| Product Page | Schede prodotto |
| Product Category | Pagine di categoria prodotti |
| Checkout / Cart | Carrello e processo di acquisto |
| Contact | Pagine di contatto e supporto |
| Landing Page | Pagine promozionali e campagne |
| Legal / Privacy | Informative legali, cookie, GDPR |

---

## Visualizzazioni

### Tabella completa

Lista di tutte le pagine analizzate con filtro per categoria. Ogni riga si espande per mostrare il dettaglio completo: URL, titoli, meta description, lista H2, word count, breadcrumbs.

### Statistiche

Distribuzione delle pagine per categoria con percentuali, word count medio, e indicatori di qualita (pagine senza H1, senza meta description, errori 404 per categoria).

### Diagramma visuale

Mappa interattiva del sito che mostra la gerarchia reale delle pagine con i loro titoli effettivi. Ogni nodo e colorato in base alla categoria di appartenenza. Il layout e orizzontale per facilitare la lettura.

### Sitemap ad albero

Rappresentazione testuale della struttura URL con i nomi delle pagine come appaiono nella navigazione, non come slug tecnici.

---

## Esportazione

### Excel multi-foglio

- **Foglio 1 — Pagine**: lista completa con URL, status, categoria, title, meta description, H1, H2, word count, breadcrumbs, profondita
- **Foglio 2 — Statistiche**: aggregazioni per categoria con numero pagine, percentuale, word count medio, pagine con/senza meta description, errori 404

### Mermaid.js

Codice del diagramma gerarchico pronto da incollare in Notion, Confluence, GitHub o qualsiasi tool che supporta Mermaid.

### Figma Export

Versione del diagramma ottimizzata per FigJam, esportabile direttamente nel workspace Figma tramite integrazione con l'assistente AI.

---

## Stack tecnico

| Componente | Tecnologia |
|---|---|
| Linguaggio | Python |
| Framework UI | Streamlit |
| Parser HTML | BeautifulSoup + lxml |
| Diagrammi | Mermaid.js (rendering client-side) |
| Export Excel | openpyxl |
| Hosting | Streamlit Community Cloud |

---

## Accesso

L'app e deployata su Streamlit Community Cloud ed e accessibile da browser senza installazione:

**https://alexandratankova-ux-architect-pro.streamlit.app**

Non richiede account, login o configurazione. Basta aprire il link e iniziare a usarla.
