# UX Architect Pro

**Tool di analisi strutturale per siti web**

---

## Il problema

Quando si affronta il redesign di un sito, una migrazione o un audit UX, il primo passo e sempre lo stesso: capire come e fatto il sito oggi. Quante pagine ha? Come sono organizzate? Quali hanno meta description, quali no? Dove sono i contenuti principali e come sono collegati tra loro?

Farlo a mano richiede ore. Si aprono pagine una per una, si copiano titoli in un foglio Excel, si cerca di ricostruire la struttura. E un lavoro ripetitivo che toglie tempo all'analisi vera. E la struttura che ne esce e quasi sempre incompleta o non corrisponde alla navigazione reale del sito.

## La soluzione

UX Architect Pro automatizza questo processo. Si inserisce un URL, si sceglie quanto in profondita scansionare, e in pochi minuti si ottiene una mappa completa del sito che rispecchia la navigazione reale, con tutti i dati strutturali estratti e le pagine classificate per tipologia.

La differenza rispetto ai crawler tradizionali e che UX Architect Pro parte dalle strutture di navigazione del sito (header, footer, sidebar), non solo dai link generici. Questo garantisce che la mappa prodotta corrisponda a come gli utenti navigano il sito, con terminologia da Information Architecture.

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

Il crawler non segue i link alla cieca. Opera in quattro fasi con una strategia a priorita e **richieste HTTP concorrenti** (piu pagine scaricate in parallelo) per ridurre i tempi di attesa rispetto a uno scan sequenziale.

**Fase 1 — Estrazione delle navigazioni.** Il sistema analizza la homepage e costruisce una o piu strutture ad albero leggendo `<nav>`, `<ul>/<li>` annidati e pattern tipici. Le sezioni sono etichettate con terminologia professionale:

| Etichetta | Cosa rappresenta |
|---|---|
| **Main Navigation (Header)** | Menu principale nel `<header>` (il `<nav>` con piu link, o quello con classi tipo main, primary, navbar) |
| **Utility Navigation (Header)** | Eventuale secondo `<nav>` nell'header (es. lingua, login, link rapidi) |
| **Secondary Navigation (Footer)** | Link nel `<footer>` (`<nav>` o liste `<ul>`) |
| **Sidebar Navigation** | Contenuto in `<aside>` o div con classi sidebar / side-nav |

I wrapper "colonna" dei mega-menu (classi tipo `column`, `mega-col`) vengono appiattiti: le voci figlie compaiono direttamente sotto la voce parent, senza nodi fittizi.

**Fase 2 — Sitemap XML.** Cerca la sitemap.xml del sito (anche tramite robots.txt) e la usa come rete di sicurezza per non perdere pagine importanti che potrebbero non essere linkate nel menu.

**Fase 3 — Scansione prioritaria.** Scansiona prima tutte le URL raccolte dalle navigazioni (header, footer, sidebar). I link scoperti sulle pagine visitate entrano in coda prioritaria; i link "di contenuto" non prioritari finiscono nella coda secondaria.

**Fase 4 — Pagine secondarie.** Solo dopo aver esaurito la coda prioritaria (entro il limite di pagine e profondita), elabora sitemap e altri link dalla coda secondaria.

**Prestazioni.** Il download usa piu worker in parallelo, pool di connessioni dedicato, code `deque` e timeout di rete contenuti, cosi una scansione su decine o centinaia di pagine richiede molto meno tempo rispetto a una richiesta alla volta.

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

Mappa interattiva del sito renderizzata con Mermaid.js direttamente nell'app. Il diagramma rispecchia le **navigazioni estratte**: ogni tipo (Main Navigation (Header), Secondary Navigation (Footer), ecc.) appare come nodo intermedio tra la root e le voci, con stile distinto; sotto ogni sezione si espandono le voci e i sottomenu con i **titoli effettivi delle pagine** come etichette. Ogni nodo pagina e colorato in base alla categoria. Il layout del flowchart e **orizzontale** (left-to-right), senza schiacciare il grafico nel contenitore, cosi la lettura segue l'asse orizzontale. Un pulsante **Scarica JPEG** (nell'iframe del diagramma) esporta l'immagine del grafico in alta risoluzione per slide o documenti.

Le pagine crawlate ma assenti da tutte le navigazioni sono raggruppate sotto **Altre pagine**.

Se il sito non espone navigazioni riconoscibili, il diagramma usa come fallback la gerarchia dei percorsi URL.

### Sitemap / Information Architecture

Nel tab **Sitemap** la struttura e introdotta con il titolo **Information Architecture**. Ogni navigazione estratta ha il **suo blocco testuale** con l'etichetta professionale (es. Main Navigation (Header)) e l'albero delle voci come le vedrebbe un utente, con gerarchia parent-child; le pagine non coperte da nessuna navigazione compaiono in una sezione **Altre pagine**. Se non si riesce a estrarre navigazioni, la vista torna alla gerarchia basata sui percorsi URL.

---

## Esportazione

### Excel multi-foglio

- **Foglio 1 — Pagine**: lista completa con URL, status, categoria, title, meta description, H1, H2, word count, breadcrumbs, profondita
- **Foglio 2 — Statistiche**: aggregazioni per categoria con numero pagine, percentuale, word count medio, pagine con/senza meta description, errori 404

### Mermaid.js

Dal tab **Esporta** si puo scaricare il codice del diagramma in formato Markdown con blocco Mermaid, pronto per Notion, Confluence, GitHub o altri renderer.

### Immagine del diagramma

Dal tab **Diagramma**, il pulsante **Scarica JPEG** genera un file immagine del grafico renderizzato (utile per presentazioni e report senza dipendere da tool esterni).

---

## Design

L'interfaccia segue un approccio minimalista e professionale ispirato ai tool di design moderni: tipografia Inter, palette neutra con accenti di colore solo per le categorie, card con bordi sottili, ampio respiro tra le sezioni. Nessun uso di emoji nell'interfaccia — i colori e la tipografia guidano la gerarchia visiva.

---

## Stack tecnico

| Componente | Tecnologia |
|---|---|
| Linguaggio | Python |
| Framework UI | Streamlit |
| Crawl | `requests` (Session + pool connessioni), `concurrent.futures` per fetch paralleli |
| Parser HTML | BeautifulSoup + lxml |
| Parser Sitemap | lxml-xml |
| Diagrammi | Mermaid.js (rendering client-side), export JPEG via canvas nel browser |
| Export Excel | openpyxl |
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
