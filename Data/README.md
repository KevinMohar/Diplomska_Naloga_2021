## Pridobitev podatkov

Zaradi velikosti posamezne datoteke, datotek s podatki ni bilo možno vključiti v repozatorij. Zahtevane datoteke prenesite iz naslednje Drive povezave v ta direktorij (Data/) in jih odpakirajte:  
[https://drive.google.com/file/d/1QQOVyMqztDZCayLTT6Q5AWg5poBZIWff/view?usp=sharing](https://drive.google.com/file/d/1QQOVyMqztDZCayLTT6Q5AWg5poBZIWff/view?usp=sharing)

Datoteke potrebne za delovanje aplikacije:

- aisles.csv
- departments.csv
- order_products_prior.csv
- order_products_train.csv
- orders.csv
- products.csv

## Opis podatkov

### Aisles.csv

Datoteka vsebuje šifrant hodnikov živil

| aisle_id   |  aisle        |
| ---------- | :-----------: |
| id hodnika | naziv hodnika |

### Departments.csv

Datoteka vsebuje šifrant oddelkov živil

### Order_products_prior.csv & Order_products_train.csv

Datoteki vsebujta podatke o košaricah.

| order_id                |         product_id         |                     add_to_cart_order |                      reordered |
| ----------------------- | :------------------------: | ------------------------------------: | -----------------------------: |
| id nakupa iz orders.csv | id izdelka iz products.csv | zaporedna številka izdelka v košarici | je bil izdelek ponovno naročen |

### Orders.csv

### Products.csv

### Sample_submissions.csv
