# SCalc - Calculadora Estatística e Gráfica

Uma ferramenta para análise estatística de dados em arquivos Excel, com geração automática de tabelas e gráficos.

## 📊 Funcionalidades

- **Leitura de arquivos Excel (.xlsx)**: Importa dados de planilhas existentes
- **Processamento estatístico**: Calcula estatísticas descritivas dos dados
- **Exportação de resultados**: Gera novas planilhas com os dados processados
- **Visualização gráfica**: Cria gráficos estatísticos para análise visual dos dados

## 🚀 Como Usar

### Pré-requisitos

- Python 3.x
- Bibliotecas necessárias (instale com o comando abaixo)

```bash
pip install -r requirements.txt
```

### Instalação

1. Clone o repositório:
```bash
git clone https://github.com/ZilchHarpy/SCalc.git
cd SCalc
```

2. Crie e ative o ambiente virtual:
```bash
python -m venv .venv
.venv\Scripts\Activate.ps1  # Windows
source .venv/bin/activate    # Linux/Mac
```

3. Instale as dependências:
```bash
pip install -r requirements.txt
```

### Execução

```bash
python scalc.py
```

## 📁 Estrutura do Projeto

```
SCalc/
├── src/                  # Pasta fonte
    ├── analysis/         # Pasta de análises estatísticas (ainda não elaborada)
    ├── data/             # Pasta onde os arquivos das tabelas xlsx ficam armazenados
    ├── models/           # Pasta onde os modelos estatísticos gerados ficam armazenados (ainda não elaborada)
    ├── visualization/    # Pasta de visualização (ainda não elaborada)
    ├── utils.py          # Arquivo de funções utilitárias
├── scalc.py              # Arquivo principal
├── requirements.txt      # Dependências do projeto
├── .gitignore            # Arquivos ignorados pelo Git
├── LICENSE               # Licensa MIT
└── README.md             # Documentação
```

## 🛠️ Tecnologias Utilizadas

- **Python**: Linguagem principal
- **Pandas**: Manipulação de arquivos Excel
- **Matplotlib**: Geração de gráficos estatísticos
- **Numpy**: Cálculos numéricos e estatísticos

## 📈 Exemplo de Uso

1. Prepare seu arquivo Excel com os dados seguindo o padrão fornecido;
2. Execute o programa;
3. Selecione o arquivo de entrada;
4. Aguarde o processamento;
5. Visualize os gráficos gerados;
6. Gere a planilha de saída com os resultados;
7. Finalize a execução.

## 🤝 Contribuindo

Contribuições são bem-vindas! Sinta-se à vontade para:

1. Fazer um fork do projeto
2. Criar uma branch para sua feature (`git checkout -b feature/NovaFuncionalidade`)
3. Commitar suas mudanças (`git commit -m 'Adiciona nova funcionalidade'`)
4. Fazer push para a branch (`git push origin feature/NovaFuncionalidade`)
5. Abrir um Pull Request

## 📝 Licença

Este projeto está sob a licença MIT. Veja o arquivo `LICENSE` para mais detalhes.

## 👤 Autor

**Caio Aquilino Merino**

- GitHub: [@ZilchHarpy](https://github.com/ZilchHarpy)
- Email: caioaquilinomerino@gmail.com

## 📞 Suporte

Se encontrar algum problema ou tiver sugestões, abra uma [issue](https://github.com/ZilchHarpy/SCalc/issues) no GitHub.

---

⭐ Se este projeto foi útil para você, considere dar uma estrela no repositório!
