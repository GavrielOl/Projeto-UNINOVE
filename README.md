# Sistema de Gestão de Estoque - Documentação

## Visão Geral
O **Sistema de Gestão de Estoque** é um aplicativo desenvolvido em Python utilizando a biblioteca `Tkinter` para a interface gráfica e `SQLite` para o gerenciamento de dados. Ele permite a gestão de produtos em estoque, com funcionalidades de adicionar, editar e remover produtos. Além disso, o sistema registra o histórico das operações realizadas (entradas e saídas de produtos).

## Funcionalidades

- **Adicionar Produto**: Permite adicionar novos produtos ao estoque, especificando o nome, preço e quantidade.
- **Editar Produto**: Permite editar as informações de um produto existente, como preço e quantidade.
- **Remover Produto**: Permite remover produtos do estoque, com a possibilidade de especificar a quantidade a ser retirada.
- **Histórico de Movimentações**: Registra e exibe todas as entradas e saídas de produtos no estoque, com detalhes como nome, preço, quantidade, tipo de movimentação (entrada ou saída) e data/hora da operação.
- **Exibição de Valor Total**: Mostra o valor total do estoque, calculado com base no preço e quantidade dos produtos.

## Dependências

- **tkinter**: Biblioteca de interface gráfica para Python.
- **ttkbootstrap**: Extensão do `ttk` (Themed Tkinter) para criar interfaces gráficas com temas modernos.
- **sqlite3**: Biblioteca para gerenciar o banco de dados SQLite.
- **datetime**: Biblioteca para manipulação de data e hora.

## Estrutura do Código

### Classe `InventoryManager`

A classe `InventoryManager` contém a lógica principal do aplicativo, com os seguintes componentes:

#### 1. **Construtor `__init__`**

- Inicializa a interface gráfica (GUI).
- Configura o banco de dados SQLite.
- Cria as tabelas necessárias no banco de dados.
- Cria os componentes da interface gráfica, como botões, labels e frames.
- Carrega os dados do estoque e o histórico de movimentações.

#### 2. **Método `create_tables`**

Este método cria as tabelas no banco de dados, caso ainda não existam:
- **estoque**: Armazena os produtos no estoque, com os campos `id`, `nome`, `preco` e `quantidade`.
- **historico**: Armazena o histórico de movimentações de produtos, com os campos `id`, `nome`, `preco`, `quantidade`, `tipo` (entrada ou saída) e `data_hora`.

#### 3. **Método `load_data`**

Carrega os dados do estoque do banco de dados e exibe na interface gráfica. Também calcula e exibe o valor total do estoque.

#### 4. **Método `load_history`**

Carrega o histórico de movimentações (entradas e saídas de produtos) do banco de dados e exibe na interface gráfica.

#### 5. **Método `update_total_label`**

Atualiza o valor total do estoque exibido na interface gráfica.

#### 6. **Métodos de Ação**

- **add_product**: Solicita ao usuário o nome, preço e quantidade do produto a ser adicionado. Após a inserção, o produto é registrado no banco de dados e o histórico de movimentações é atualizado.
- **edit_product**: Permite ao usuário editar o preço e a quantidade de um produto existente no estoque. A diferença de quantidade é registrada no histórico de movimentações.
- **remove_product**: Permite ao usuário remover uma quantidade de um produto do estoque. O histórico de movimentações é atualizado, e o valor total do estoque é recalculado.

## Interface Gráfica

A interface gráfica é composta por:

1. **Controle de Ações**: Uma barra com botões para adicionar, editar e remover produtos.
2. **Tabela de Estoque**: Exibe os produtos no estoque, com as colunas "Nome", "Preço" e "Quantidade".
3. **Tabela de Histórico**: Exibe o histórico de movimentações (entradas e saídas) com as colunas "Nome", "Preço", "Quantidade", "Tipo" e "Data e Hora".
4. **Valor Total do Estoque**: Exibe o valor total do estoque calculado com base no preço e quantidade dos produtos.

## Estrutura do Banco de Dados

### Tabela `estoque`

| Campo      | Tipo    | Descrição                             |
|------------|---------|---------------------------------------|
| `id`       | INTEGER | Identificador único do produto       |
| `nome`     | TEXT    | Nome do produto                      |
| `preco`    | REAL    | Preço do produto                     |
| `quantidade` | INTEGER | Quantidade disponível no estoque     |

### Tabela `historico`

| Campo      | Tipo    | Descrição                             |
|------------|---------|---------------------------------------|
| `id`       | INTEGER | Identificador único da movimentação   |
| `nome`     | TEXT    | Nome do produto                      |
| `preco`    | REAL    | Preço do produto na movimentação      |
| `quantidade` | INTEGER | Quantidade movimentada               |
| `tipo`     | TEXT    | Tipo da movimentação ("Entrada" ou "Saída") |
| `data_hora`| TEXT    | Data e hora da movimentação          |

## Execução do Sistema

Para executar o sistema, basta rodar o script Python. A interface gráfica será aberta, e você poderá interagir com o estoque de produtos. As modificações são salvas automaticamente no banco de dados SQLite.

### Exemplos de Uso

1. **Adicionar Produto**:
   - O usuário é solicitado a inserir o nome, preço e quantidade do produto a ser adicionado. Após a confirmação, o produto é registrado no estoque e no histórico.
   
2. **Editar Produto**:
   - O usuário pode editar o preço e a quantidade de um produto existente. A diferença na quantidade é registrada como uma entrada ou saída no histórico.

3. **Remover Produto**:
   - O usuário pode remover uma quantidade de um produto. Se a quantidade total se tornar zero, o produto será excluído do estoque.

## Conclusão

Este sistema de gestão de estoque é uma ferramenta simples e eficaz para controlar o inventário de produtos, com a vantagem de registrar todas as operações realizadas e calcular o valor total do estoque automaticamente. Ele é ideal para pequenos negócios que necessitam de uma solução prática e sem custos com softwares comerciais.
