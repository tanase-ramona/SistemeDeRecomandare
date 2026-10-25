# Laborator 2: Recombee - înregistrarea proprietăților catalogului

## Domeniul ales: Cărți

Sistemul de recomandare va recomanda **cărți**. Fiecare carte din catalog are informații despre autori, categorie, anul publicării, numărul de pagini și rating-ul cititorilor.

## Dataset

- **Fișier:** [`books.csv`](books.csv)
- **Număr de item-uri:** 6810 cărți
- **Sursă:** [Kaggle – 7k Books with Metadata](https://www.kaggle.com/datasets/dylanjcastillo/7k-books-with-metadata) (date colectate din Google Books API și Goodreads), folosit fără modificări
- **Identificator unic:** `isbn13`. Este unic pentru fiecare carte și **nu** se înregistrează ca proprietate; Recombee îl va folosi ca `itemId` la încărcarea produselor.

## Proprietăți (atribute)

| Proprietate | Tip Recombee | Descriere | Exemplu |
| --- | --- | --- | --- |
| `title` | `string` | Titlul cărții | `Gilead` |
| `subtitle` | `string` | Subtitlul (poate lipsi) | `A Novel` |
| `authors` | `string` | Autorii, separați prin `;` | `Charles Osborne;Agatha Christie` |
| `categories` | `string` | Categoria / genul | `Fiction` |
| `description` | `string` | Descrierea cărții | `A NOVEL THAT READERS and critics...` |
| `thumbnail` | `image` | URL-ul imaginii copertei | `http://books.google.com/books/content?id=...` |
| `published_year` | `int` | Anul publicării | `2004` |
| `average_rating` | `double` | Rating-ul mediu (0–5) | `3.85` |
| `num_pages` | `int` | Numărul de pagini | `247` |
| `ratings_count` | `int` | Numărul de rating-uri primite | `361` |

Coloana `isbn10` nu este înregistrată, fiind doar un alt identificator al aceleiași cărți.

## Rulare

```powershell
pip install recombee-api-client pandas

# credențialele din Recombee Admin UI -> Settings -> API Logins
$env:RECOMBEE_DB = "numele-bazei-de-date"
$env:RECOMBEE_TOKEN = "private-token"
$env:RECOMBEE_REGION = "eu-west"

python recombee_properties.py
```

Scriptul [`recombee_properties.py`](recombee_properties.py) verifică dataset-ul, definește proprietățile în Recombee cu `AddItemProperty` și apoi le listează cu `ListItemProperties` pentru confirmare.
