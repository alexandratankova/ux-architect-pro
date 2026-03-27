# UX Architect Pro

**Tool di analisi strutturale per siti web**

---

## Il problema

Quando si affronta il redesign di un sito, una migrazione o un audit UX, il primo passo e sempre lo stesso: capire come e fatto il sito oggi. Quante pagine ha? Come sono organizzate? Quali hanno meta description, quali no? Dove sono i contenuti principali e come sono collegati tra loro?

Farlo a mano richiede ore. Si aprono pagine una per una, si copiano titoli in un foglio Excel, si cerca di ricostruire la struttura. E un lavoro ripetitivo che toglie tempo all'analisi vera. E la struttura che ne esce e quasi sempre incompleta o non corrisponde alla navigazione reale del sito.

## La soluzione

UX Architect Pro automatizza questo processo. Si inserisce un URL, si sceglie quanto in profondita scansionare, e in pochi minuti si ottiene una mappa completa del sito che rispecchia la navigazione reale, con tutti i dati strutturali estratti e le pagine classificate per tipologia.

La differenza rispetto ai crawler tradizionali e che UX Architect Pro parte dal menu di navigazione del sito, non dai link generici. Questo garantisce che la mappa prodotta corrisponda a come gli utenti navigano il sito, non a come i link sono distribuiti nel codice.

---

## A chi si rivolge

| Ruolo | Caso d'uso |
|---|---|
| UX Designer | Mappare un sito esistente prima di un redesign |
| Content Strategist | Analizzare la distribuzione e la qualita dei contenuti |
| SEO Specialist | Audit strutturale rapido con identificazione di errori |
| Project Manager | Presentare lo stato di un sito a clienti o stakeholder |
| Information Architect | Verificare che la struttura informativa corrisponda alla navigazione |

---

## Come funziona

### 1. Configurazione

L'utente inserisce l'URL del sito e configura due parametri:

- **Profondita massima** — fino a 10 livelli di navigazione
- **Pagine massime** — fino a 500 pagine per scansione

### 2. Crawl intelligente in 4 fasi

Il crawler non segue i link alla cieca. Opera in quattro fasi con una strategia a priorita:

**Fase 1 — Analisi del menu di navigazione.** Il sistema analizza la homepage e identifica il menu principale del sito leggendo la struttura `<nav> > <ul> > <li>` annidata. Distingue automaticamente il main menu dalla top bar e dal footer, identificando il `<nav>` piu rilevante dentro `<header>` o tramite classi CSS tipiche (main-menu, primary-menu, navbar, mega-menu). Estrae la gerarchia completa: voci di primo livello, sottomenu, sotto-sottomenu.

**Fase 2 — Sitemap XML.** Cerca la sitemap.xml del sito (anche tramite robots.txt) e la usa come rete di sicurezza per non perdere pagine importanti che potrebbero non essere linkate nel menu.

**Fase 3 — Scansione delle voci di navigazione (priorita alta).** Scansiona prima tutte le pagine trovate nel menu principale e nei sottomenu. Per ognuna, estrae anche i link di navigazione locali (sottomenu di sezione) e li aggiunge alla coda prioritaria.

**Fase 4 — Pagine secondarie.** Solo dopo aver coperto l'intero menu, scansiona le pagine secondarie (da sitemap e link nei contenuti) con il budget rimanente.

Questo approccio garantisce che le voci del menu vengano sempre mappate per prime, indipendentemente da quante pagine secondarie esistono sul sito.

Durante il crawl l'app mostra in tempo reale:

- Barra di avanzamento con contatore pagine
- Log di ogni pagina analizzata con indicazione se proviene dal menu
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

Mappa interattiva del sito renderizzata con Mermaid.js direttamente nell'app. Il diagramma rispecchia la gerarchia reale del menu di navigazione: le voci di primo livello si espandono nei rispettivi sottomenu, con i titoli effettivi delle pagine come etichette dei nodi. Ogni nodo e colorato in base alla categoria di appartenenza. Il layout e orizzontale (left-to-right) per facilitare la lettura. Le pagine non presenti nel menu sono raggruppate sotto "Altre pagine".

Se il sito non ha un menu `<nav>` riconoscibile, il diagramma usa come fallback la gerarchia dei percorsi URL.

### Sitemap ad albero

Rappresentazione testuale della struttura del sito basata sul menu di navigazione reale. Mostra le voci come le vedrebbe un utente, con la gerarchia parent-child dei sottomenu, non come slug tecnici degli URL. Include anche le pagine non presenti nel menu come sezione separata.

---

## Esportazione

### Excel multi-foglio

- **Foglio 1 — Pagine**: lista completa con URL, status, categoria, title, meta description, H1, H2, word count, breadcrumbs, profondita
- **Foglio 2 — Statistiche**: aggregazioni per categoria con numero pagine, percentuale, word count medio, pagine con/senza meta description, errori 404

### Mermaid.js

Codice del diagramma gerarchico pronto da incollare in Notion, Confluence, GitHub o qualsiasi tool che supporta Mermaid.

### Figma Export

Versione del diagramma ottimizzata per FigJam (layout orizzontale, testo quotato, senza emoji), esportabile direttamente nel workspace Figma tramite integrazione con l'assistente AI. L'app salva un file di configurazione che l'assistente usa per creare il diagramma in FigJam con un singolo comando.

---

## Design

L'interfaccia segue un approccio minimalista e professionale ispirato ai tool di design moderni: tipografia Inter, palette neutra con accenti di colore solo per le categorie, card con bordi sottili, ampio respiro tra le sezioni. Nessun uso di emoji nell'interfaccia — i colori e la tipografia guidano la gerarchia visiva.

---

## Stack tecnico

| Componente | Tecnologia |
|---|---|
| Linguaggio | Python |
| Framework UI | Streamlit |
| Parser HTML | BeautifulSoup + lxml |
| Parser Sitemap | lxml-xml |
| Diagrammi | Mermaid.js (rendering client-side) |
| Export Excel | openpyxl |
| Integrazione Figma | Figma MCP (generate_diagram) |
| Hosting | Streamlit Community Cloud |

---

## Accesso

L'app e deployata su Streamlit Community Cloud ed e accessibile da browser senza installazione:

**https://alexandratankova-ux-architect-pro.streamlit.app**

Non richiede account, login o configurazione. Basta aprire il link e iniziare a usarla.

---

## Repository

Il codice sorgente e disponibile su GitHub:

**https://github.com/alexandratankova/ux-architect-pro**
