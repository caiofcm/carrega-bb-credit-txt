# carrega_bb_credit_txt

Carrega arquivos de Cartão Banco do Brasil no formato .txt e separa despesas por pessoas e tipos

## Usage

```bash
git clone https://github.com/caiofcm/carrega-bb-credit-txt.git
pip install .
```

Acione como módulo para printar no console:

```bash
python -m carrega_bb_credit_txt.py ARQUIVO-BB.txt
```

Ou como package

```python
import carrega_bb_credit
card_infos = carrega_bb_credit.parse_text_file(ARQUIVOPATH)
```

## Development

```
pip install pipenv
pipenv install --dev
```

## Features

- Separa despesas por nome
- Separa por categorias (_to do_)
