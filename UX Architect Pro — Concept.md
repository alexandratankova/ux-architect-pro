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

Dopo il crawl, i risultati sono organizzati in **schede nell'ordine seguente** (allineato al flusso di lavoro IA → vista grafica → dettaglio → export):

1. **Sitemap** — albero testuale dell'Information Architecture  
2. **Diagramma** — mappa Mermaid interattiva  
3. **Tabella** — elenco pagine con filtri  
4. **Esporta** — download Excel, Mermaid, condivisione rapporto

Sopra le schede, un **Riepilogo** in quattro card mostra in sintesi: numero di pagine, **word count medio**, numero di **categorie** rilevate e conteggio **errori 404** (con colore di stato verde/rosso).

### Sitemap / Information Architecture (prima scheda)

Nel tab **Sitemap** la struttura e introdotta con il titolo **Information Architecture**. Ogni navigazione estratta ha il **suo blocco** (HTML) con intestazione in stile etichetta (es. Main Navigation (Header)) e l'albero delle voci in **monospace** (`├──`, `└──`, …), come una vista ad albero classica. La **profondità gerarchica** è suggerita in modo leggero da **peso**, **colore** e **dimensione del testo** sulle righe (livelli superficiali più scuri e marcati; livelli profondi leggermente più tenui e compatti), **senza barra colorata** sul lato sinistro. Le pagine non coperte da nessuna navigazione compaiono in una sezione **Altre pagine**. Se non si riesce a estrarre navigazioni, la vista torna alla gerarchia basata sui **percorsi URL**.

### Diagramma visuale (seconda scheda)

Mappa interattiva del sito renderizzata con **Mermaid.js** in un iframe dedicato. Il diagramma rispecchia le **navigazioni estratte**: ogni tipo (Main Navigation (Header), Secondary Navigation (Footer), ecc.) appare come **nodo sezione** tra la root e le voci (sfondo viola molto chiaro, testo scuro in grassetto); sotto ogni sezione si espandono voci e sottomenu con i **titoli effettivi delle pagine** come etichette. I **nodi pagina** usano una **palette pastello** per **categoria**; il colore del testo su ogni riquadro e scelto automaticamente (**nero o bianco**) in base al contrasto sullo sfondo. La **distanza dalla home** nel grafo si legge anche da **spessore del bordo** del riquadro e **dimensione del font** (più marcato vicino alla root, più leggero in profondità). Il flowchart e **orizzontale** (LR), con **padding** e **spaziatura** tra nodi (`nodeSpacing` / `rankSpacing`) per aerare il disegno.

Nella toolbar dell'iframe: **zoom + / − / Reset**, zoom con **Ctrl + rotellina** sul diagramma, scroll nel riquadro per spostarsi. In alto a destra, due export dal **SVG** renderizzato da Mermaid: **Scarica SVG** (file vettoriale `.svg`, adatto a Figma, Illustrator o il web) e **Scarica JPEG** (raster ad alta risoluzione via canvas, utile per slide).

Le pagine crawlate ma assenti da tutte le navigazioni sono raggruppate sotto **Altre pagine**.

Se il sito non espone navigazioni riconoscibili, il diagramma usa come fallback la gerarchia dei percorsi URL.

### Tabella completa

Lista di tutte le pagine analizzate con **filtro multiplo per categoria**. Ogni riga si espande per mostrare il dettaglio: URL, title, H1, meta description, elenco H2, word count, depth, breadcrumbs. Nella colonna di destra compare un **badge categoria** colorato (stessa logica pastello / contrasto del diagramma).

---

## Esportazione

I nomi dei file scaricati includono un **slug dell'host** del sito analizzato (URL di partenza del crawl, senza `www.`, porta rimossa, caratteri non sicuri normalizzati), cosi si riconoscono subito i report sul disco. Esempi: `ux_architect_pro_rapporto_example.org.json`, `ux_architect_pro_ia_example.org.xlsx`, `ux_architect_pro_mermaid_example.org.md`, `ux_architect_pro_diagram_example.org.svg`.

### Excel — Information Architecture

Il file Excel non e una lista casuale di URL: i fogli seguono la **stessa logica dell'IA** e delle viste usate in app.

- **Foglio "Information Architecture"**: una riga per ogni voce di menu nell'ordine gerarchico, con **zona di navigazione** (es. Main Navigation (Header)), **livello**, **percorso IA** (es. `Voce > Sottovoce`), **voce menu**, **URL**, **title** e campi SEO (categoria, status, meta, H1, H2, word count, breadcrumbs, profondita di crawl). In coda, sezione **Altre pagine (non in menu)** per le pagine scansionate ma non presenti in nessun menu. Se il sito non ha navigazioni riconoscibili, il foglio usa la **struttura URL** come fallback (`Struttura URL (fallback)`), in linea con la Sitemap testuale.
- **Foglio "Sitemap"** (Excel funzionale, allineato al tab Sitemap): colonne **Navigazione / zona**, poi **Livello 1 … Livello N** (fino a **12** livelli, in base alla profondita massima trovata), **Anteprima albero (ASCII)** come nel tab, e **URL (clic per aprire)** con **hyperlink** nativi (testo abbreviato se l'URL e molto lungo, stile link blu sottolineato). Sulla tabella sono attivi **filtri automatici** sulla riga intestazioni e **righe/colonne congelate** con ancoraggio su **B2** (resta fissa la colonna della zona e la riga delle intestazioni). Sotto i dati, una riga di suggerimento ricorda filtri, freeze e link cliccabili.
- **Foglio "Diagramma"**: immagine PNG del flowchart Mermaid (quando il rendering e disponibile), equivalente al tab Diagramma.

I testi delle celle sono sanitizzati per compatibilita con Excel (nessun carattere di controllo illegale tipico degli HTML scrapati).

### Condivisione del rapporto

Dal tab **Esporta** si puo **scaricare un file .json** con l'intero snapshot (risultati, navigazioni, errori 404) da inviare a un collega; dalla **sidebar** si puo **importare** quel file per rivedere lo stesso rapporto senza rifare il crawl. Per rapporti compatti e disponibile anche l'aggiornamento dell'URL con parametro `r` (link da copiare dalla barra del browser).

### Mermaid.js

Dal tab **Esporta** si puo scaricare il codice del diagramma in formato Markdown con blocco Mermaid, pronto per Notion, Confluence, GitHub o altri renderer.

### Immagine del diagramma

Dal tab **Diagramma**, dall'iframe si puo scaricare il grafico come **SVG** (nativo, stesso output vettoriale del renderer) o come **JPEG** (esportazione raster per presentazioni).

---

## Design

L'interfaccia e **minimalista e professionale**: tipografia **Inter**, sfondo chiaro, **card** con bordi sottili e ampio respiro tra le sezioni.

- **Azioni primarie** — i pulsanti principali (es. avvio crawl, scarica) sono **neri** (`#111827`) con hover grigio scuro; non c'e un arancione di brand.
- **Accent UI** — slider, valori numerici accanto agli slider e link nelle etichette dei widget usano un **grigio ardesia** (`#475569`), allineato al `primaryColor` del tema Streamlit in `config.toml`.
- **Categorie** — nel diagramma, nella **legenda in sidebar**, nei badge in tabella e nelle celle colorate del foglio Excel (dove previsto), le categorie usano **colori pastello** distinti; il **testo** su ogni sfondo e scelto per **contrasto** (chiaro/scuro) cosi resta leggibile.
- **Contenuto dell'app** — nessuna emoji nei testi o nei controlli della UI; colori e tipografia guidano la gerarchia. (Il favicon della pagina Streamlit puo restare un'icona separata dal contenuto.)

La **sidebar** ospita la scelta **fonte dati** (nuovo crawl da URL oppure caricamento rapporto **.json**), i parametri di crawl e, dopo i risultati, la **legenda categorie** con punti colorati allineati alla palette.

---

## Stack tecnico

| Componente | Tecnologia |
|---|---|
| Linguaggio | Python |
| Framework UI | Streamlit |
| Crawl | `requests` (Session + pool connessioni), `concurrent.futures` per fetch paralleli |
| Parser HTML | BeautifulSoup + lxml |
| Parser Sitemap | lxml-xml |
| Diagrammi | Mermaid.js (client-side), export **SVG** (serializzazione DOM) e **JPEG** (canvas) nel browser |
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

Nel repo e presente anche **`preview-hierarchy.html`**: pagina HTML statica (con stessi stili Sitemap di esempio e un mini diagramma Mermaid) utile per un'**anteprima in locale** dopo `python3 -m http.server` nella cartella del progetto; non fa parte del flusso Streamlit in produzione.
