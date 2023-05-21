# supervisionhack2

### model
- data - folder zawierający dane, używane do trenowania modeli
  - imgs_cropped - podane przykłady oszukańczych reklam z wyciętymi obrazami oraz przykładowe prawdziwe reklamy
  - imgs4training - dane przygotowane do fine-tune'owania sieci resnet do klasyfikacji oszukańczych reklam
  - \*.csv - pliki csv zawierające niezbędne dane do trenowania modeli. W tym dane treningowe i testowe do modelu sieci neuronowej MLP do klasyfikacji reklam na podstawie linków i modelu LLM fine-tune'owanego do klasyfikacji reklam na podstawie tekstu, w nich występującego.
- model_link - folder zawierający wytrenowany model MLP do klasyfikacji reklam na podstawie linków
- model_res - folder zawierający fine-tune'owaną sieć ResNet18 do klasyfikacji reklam na podstawie zdjęcia
- model_text - folder zawierający fine-tune'owany transformer do klasyfikacji reklam na podstawie tekstu występującego na zdjęciu
- extract_text.py - skrypt pythonowy wyodrębniający tekst z obrazka
- model.py - skrypt pythonowy tworzący ostatyczne predykcje za pomocą ensembling'u trzech modeli klasyfikacyjnych przy pomocy ich głosowania.
- process_data.ipynb - notatnik do przetwarzania danych treningowych/testowych
- process_data_for_links.ipynb - notatnik do przetwarzania danych treningowych/testowych
- train_link.py - skrypt uczący model MLP do klasyfikacji reklam na podstawie linków
- train_res.py - skrypt fine-tune'ujący ResNet18 do klasyfikacji reklam na podstawie zdjęcia
- train_text.py - skrypt fine-tune'ujący transformer do klasyfikacji reklam na podstawie tekstu występującego na zdjęciu
- utils - plik z używanymi funkcjami do wyciągania tekstu ze zdjęcia oraz tworzący zmienne predykcyjne do modelu klasyfikującego reklamy na postawie linku
