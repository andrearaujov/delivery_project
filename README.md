# Sistema de Delivery Genérico em Django

Este é um projeto de um sistema de delivery completo, similar ao iFood, construído com Python e Django. O projeto foi arquitetado para suportar uma plataforma com duas visões principais: uma interface para **Clientes** que fazem pedidos e um painel de gerenciamento para **Donos de Restaurante**.

O foco foi construir um backend robusto, seguro e funcional, com toda a lógica de negócios necessária para ambos os lados da plataforma.

---

## ✨ Funcionalidades Principais

O sistema é dividido em duas experiências de usuário distintas:

### 1. Visão do Cliente
* **Autenticação Completa:** Cadastro (como Cliente), Login e Logout.
* **Navegação:** Visualização da lista de restaurantes disponíveis.
* **Cardápio:** Visualização do cardápio detalhado de cada restaurante.
* **Carrinho de Compras:** Usuários logados podem adicionar produtos ao carrinho (protegido contra usuários anônimos ou donos de restaurante).
* **Fluxo de Pedido:** Finalização de compra, transformando o carrinho em um `Pedido` real no banco de dados, associado ao cliente.
* **Histórico de Pedidos:** Uma página protegida ("Meus Pedidos") onde o cliente pode ver todos os pedidos que já fez, ordenados do mais recente para o mais antigo.

### 2. Visão do Dono de Restaurante
* **Cadastro com Papel:** Permite o cadastro com o tipo de usuário "Dono de Restaurante".
* **Painel de Controle Exclusivo:** Uma área (`/painel/`) segura e acessível apenas para donos de restaurante.
* **Gerenciamento de Restaurante:** Permite ao dono cadastrar seu próprio restaurante através do painel.
* **Gerenciamento Completo de Cardápio (CRUD):**
    * **Adicionar** novos produtos ao seu restaurante.
    * **Editar** produtos existentes (preço, descrição, foto, etc.).
    * **Excluir** produtos do cardápio.
* **Gerenciamento de Pedidos:**
    * Visualização em tempo real de todos os pedidos recebidos pelo seu restaurante.
    * **Atualização de Status:** Capacidade de mudar o status de um pedido (Pendente -> Em preparação -> A caminho -> Entregue), informando o cliente sobre o progresso.

---

## 🛠️ Tecnologias Utilizadas
* **Backend:** Python 3, Django
* **Banco de Dados:** SQLite 3 (padrão do Django)
* **Frontend:** Templates do Django (HTML puro com lógica de templates)
* **Features do Django:** `ModelForm`, Views baseadas em Classe e Função, Sistema de Autenticação, Decorators (`@login_required`), Sessões.

---

## 🚀 Como Rodar o Projeto

Siga os passos abaixo para executar o projeto em sua máquina local.

**1. Clone o Repositório:**
```bash
git clone [URL_DO_SEU_REPOSITORIO_GIT]
cd [NOME_DA_PASTA_DO_PROJETO]
```

**2. Crie e Ative o Ambiente Virtual:**
```bash
# Para Windows
python -m venv venv
.\venv\Scripts\activate

# Para macOS/Linux
python3 -m venv venv
source venv/bin/activate
```

**3. Instale as Dependências:**
(O `Pillow` é necessário para o upload de imagens dos produtos)
```bash
pip install Django Pillow
```

**4. Aplique as Migrações do Banco de Dados:**
Isso criará o arquivo `db.sqlite3` com todas as tabelas.
```bash
python manage.py migrate
```

**5. Crie um Superusuário:**
Este usuário terá acesso ao painel de administração (`/admin/`) para gerenciar o sistema.
```bash
python manage.py createsuperuser
```
(Siga as instruções para criar seu usuário e senha).

**6. Execute o Servidor de Desenvolvimento:**
```bash
python manage.py runserver
```

**7. Acesse a Aplicação:**
Abra seu navegador e acesse `http://127.0.0.1:8000/`.

* Para testar, crie contas usando a página de **Cadastro** (`/cadastro/`), uma do tipo "Cliente" e outra do tipo "Dono de Restaurante".
* Acesse o painel de admin em `http://127.0.0.1:8000/admin/` com o superusuário para visualizar os dados brutos.