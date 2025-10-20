from django.views.generic import ListView, DetailView
from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth import login  
from django.contrib.auth.decorators import login_required
from .models import Restaurante, Produto, Pedido, ItemPedido, Cliente
from .forms import CadastroForm, RestauranteForm, ProdutoForm

class RestauranteListView(ListView):
    model = Restaurante
    template_name = "core/index.html"
    context_object_name = "restaurantes"


class RestauranteDetailView(DetailView):
    model = Restaurante
    template_name = "core/restaurante_detail.html"
    context_object_name = "restaurante"

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["produtos"] = self.get_object().produtos.all()
        return context


@login_required
def adicionar_ao_carrinho(request, produto_id):
    
    if request.user.cliente.tipo_usuario == 'RESTAURANTE':
        # Se for dono, não pode adicionar ao carrinho. Redireciona para o painel dele.
        return redirect('core:painel_restaurante')
    
    produto = get_object_or_404(Produto, id=produto_id)

    carrinho = request.session.get('carrinho', {})

    produto_id_str = str(produto.id)

    if produto_id_str in carrinho:
        carrinho[produto_id_str] += 1
    else:
        carrinho[produto_id_str] = 1

    request.session['carrinho'] = carrinho

    return redirect('core:detalhe_restaurante', pk=produto.restaurante.id)
@login_required
def ver_carrinho(request):
    if request.user.cliente.tipo_usuario == 'RESTAURANTE':
        return redirect('core:painel_restaurante')
    
    carrinho = request.session.get("carrinho", {})
    produto_ids = carrinho.keys()
    produtos_no_carrinho = Produto.objects.filter(id__in=produto_ids)
    itens_carrinho = []
    valor_total = 0

    for produto in produtos_no_carrinho:
        produto_id_str = str(produto.id)
        quantidade = carrinho[produto_id_str]
        subtotal = produto.preco * quantidade

        itens_carrinho.append(
            {
                "produto": produto,
                "quantidade": quantidade,
                "subtotal": subtotal,
            }
        )
        valor_total += subtotal

    contexto = {
        "itens_carrinho": itens_carrinho,
        "valor_total": valor_total,
    }

    return render(request, "core/carrinho.html", contexto)

@login_required
def finalizar_pedido(request):
    if request.user.cliente.tipo_usuario == 'RESTAURANTE':
        return redirect('core:painel_restaurante')
    
    carrinho = request.session.get('carrinho', {})
    if not carrinho:
        return redirect('core:lista_restaurantes')

    # Pega o perfil de Cliente associado ao usuário que está logado na sessão.
    # A mágica acontece aqui: request.user é o User logado, e .cliente é
    # o perfil Cliente ligado a ele pelo OneToOneField que criamos.
    cliente_logado = request.user.cliente

    # O resto da lógica para pegar os produtos e calcular o total continua
    produto_ids = carrinho.keys()
    produtos = Produto.objects.filter(id__in=produto_ids)

    # Validação para caso os produtos não existam mais
    if not produtos.exists():
        request.session['carrinho'] = {} # Limpa o carrinho inválido
        return redirect('core:lista_restaurantes')

    restaurante_do_pedido = produtos.first().restaurante

    # Cria o objeto Pedido, agora com o cliente correto
    novo_pedido = Pedido.objects.create(
        cliente=cliente_logado, 
        restaurante=restaurante_do_pedido,
        status='Pendente'
    )

    valor_total = 0
    # Cria os Itens do Pedido
    for produto in produtos:
        produto_id_str = str(produto.id)
        quantidade = carrinho[produto_id_str]
        subtotal = produto.preco * quantidade

        ItemPedido.objects.create(
            pedido=novo_pedido,
            produto=produto,
            quantidade=quantidade,
            preco_unitario=produto.preco
        )
        valor_total += subtotal

    #  Atualiza o valor total no pedido
    novo_pedido.valor_total = valor_total
    novo_pedido.save()

    #  Limpa o carrinho da sessão
    request.session['carrinho'] = {}

    #  Redireciona para a página de confirmação
    return redirect('core:pedido_confirmado', pedido_id=novo_pedido.id)
    
def pedido_confirmado(request, pedido_id):
    pedido = get_object_or_404(Pedido, id=pedido_id)
    contexto = {
        'pedido': pedido}
    return render(request, 'core/pedido_confirmado.html', contexto)

def cadastro(request):
    if request.method == 'POST':
        form = CadastroForm(request.POST)
        if form.is_valid():
            user = form.save(commit=False)
            user.set_password(form.cleaned_data['password'])
            user.save()

            # Cria o perfil Cliente associado, agora incluindo o tipo_usuario
            Cliente.objects.create(
                user=user,
                telefone=form.cleaned_data['telefone'],
                endereco=form.cleaned_data['endereco'],
                # Pega a escolha do usuário no formulário e salva no modelo
                tipo_usuario=form.cleaned_data['tipo_usuario']
            )

            login(request, user)
            return redirect('core:lista_restaurantes')
    else:
        form = CadastroForm()
        
    return render(request, 'core/cadastro.html', {'form': form})

@login_required 
def meus_pedidos(request):
    # Filtra os pedidos buscando pelo usuário logado (request.user)
    #    A busca 'cliente__user' atravessa a relação do Pedido -> Cliente -> User
    pedidos_do_usuario = Pedido.objects.filter(cliente__user=request.user).order_by('-data_pedido')

    contexto = {
        'pedidos': pedidos_do_usuario
    }
    return render(request, 'core/meus_pedidos.html', contexto)

@login_required
def painel_restaurante(request):
    # Garante que apenas donos de restaurante acessem
    if request.user.cliente.tipo_usuario != 'RESTAURANTE':
        return redirect('core:lista_restaurantes') # Ou uma página de acesso negado

    # Busca os restaurantes que pertencem ao usuário logado
    restaurantes_do_dono = Restaurante.objects.filter(dono=request.user)
    
    contexto = {
        'restaurantes': restaurantes_do_dono
    }
    return render(request, 'core/painel_restaurante.html', contexto)


@login_required
def cadastrar_restaurante(request):
    if request.user.cliente.tipo_usuario != 'RESTAURANTE':
        return redirect('core:lista_restaurantes')

    if request.method == 'POST':
        form = RestauranteForm(request.POST)
        if form.is_valid():
            restaurante = form.save(commit=False)
            # Associa o restaurante ao usuário logado (o dono)
            restaurante.dono = request.user
            restaurante.save()
            # Redireciona para o painel após o sucesso
            return redirect('core:painel_restaurante')
    else:
        form = RestauranteForm()

    return render(request, 'core/cadastrar_restaurante.html', {'form': form})

@login_required
def gerenciar_cardapio(request):
    # Proteção de segurança
    if not hasattr(request.user, 'cliente') or request.user.cliente.tipo_usuario != 'RESTAURANTE':
        return redirect('core:lista_restaurantes')

    try:
        # Busca o primeiro restaurante do dono logado.
        restaurante_do_dono = Restaurante.objects.get(dono=request.user)
        # Busca os produtos associados a esse restaurante
        produtos = Produto.objects.filter(restaurante=restaurante_do_dono)
    except Restaurante.DoesNotExist:
        # Se ele não tiver restaurante, não há produtos para mostrar
        restaurante_do_dono = None
        produtos = []

    contexto = {
        'restaurante': restaurante_do_dono,
        'produtos': produtos
    }
    return render(request, 'core/gerenciar_cardapio.html', contexto)


@login_required
def adicionar_produto(request):
    if not hasattr(request.user, 'cliente') or request.user.cliente.tipo_usuario != 'RESTAURANTE':
        return redirect('core:lista_restaurantes')

    try:
        restaurante_do_dono = Restaurante.objects.get(dono=request.user)
    except Restaurante.DoesNotExist:
        # Não deixa adicionar produto se não tiver restaurante cadastrado
        return redirect('core:painel_restaurante')

    if request.method == 'POST':
        # request.FILES é necessário para upload de imagens
        form = ProdutoForm(request.POST, request.FILES)
        if form.is_valid():
            produto = form.save(commit=False)
            # Associa o produto ao restaurante do dono logado
            produto.restaurante = restaurante_do_dono
            produto.save()
            # Redireciona para a lista de produtos após o sucesso
            return redirect('core:gerenciar_cardapio')
    else:
        form = ProdutoForm()

    return render(request, 'core/adicionar_produto.html', {'form': form})


@login_required
def editar_produto(request, produto_id):
    # Proteção de segurança
    if not hasattr(request.user, 'cliente') or request.user.cliente.tipo_usuario != 'RESTAURANTE':
        return redirect('core:lista_restaurantes')

    # Busca o produto que será editado
    produto = get_object_or_404(Produto, id=produto_id)

    # Mais uma camada de segurança: garante que o dono do restaurante
    # só pode editar os produtos do seu próprio restaurante.
    if produto.restaurante.dono != request.user:
        return redirect('core:painel_restaurante') # Ou uma página de acesso negado

    if request.method == 'POST':
        # Ao submeter, passa a 'instance' para que o Django saiba qual produto atualizar
        form = ProdutoForm(request.POST, request.FILES, instance=produto)
        if form.is_valid():
            form.save()
            return redirect('core:gerenciar_cardapio')
    else:
        # Ao carregar a página, preenche o formulário com os dados do produto existente
        form = ProdutoForm(instance=produto)

    return render(request, 'core/editar_produto.html', {'form': form, 'produto': produto})

@login_required
def excluir_produto(request, produto_id):
    # Proteções de segurança (tipo de usuário e dono do produto)
    if not hasattr(request.user, 'cliente') or request.user.cliente.tipo_usuario != 'RESTAURANTE':
        return redirect('core:lista_restaurantes')
    
    produto = get_object_or_404(Produto, id=produto_id)
    if produto.restaurante.dono != request.user:
        return redirect('core:painel_restaurante')

    if request.method == 'POST':
        # Se o formulário de confirmação foi enviado, exclui o produto
        produto.delete()
        return redirect('core:gerenciar_cardapio')

    # Se for um GET, apenas mostra a página de confirmação
    return render(request, 'core/excluir_produto_confirm.html', {'produto': produto})

@login_required
def ver_pedidos_restaurante(request):
    # Proteção de segurança
    if not hasattr(request.user, 'cliente') or request.user.cliente.tipo_usuario != 'RESTAURANTE':
        return redirect('core:lista_restaurantes')

    try:
        # Busca o restaurante do dono logado
        restaurante_do_dono = Restaurante.objects.get(dono=request.user)
        # Busca todos os pedidos feitos para esse restaurante, dos mais novos para os mais antigos
        pedidos = Pedido.objects.filter(restaurante=restaurante_do_dono).order_by('-data_pedido')
    except Restaurante.DoesNotExist:
        # Se ele não tiver restaurante, não há pedidos para mostrar
        return redirect('core:painel_restaurante')

    contexto = {
        'pedidos': pedidos
    }
    return render(request, 'core/ver_pedidos.html', contexto)


@login_required
def atualizar_status_pedido(request, pedido_id):
    # Proteções de segurança
    if not hasattr(request.user, 'cliente') or request.user.cliente.tipo_usuario != 'RESTAURANTE':
        return redirect('core:lista_restaurantes')

    # Garante que a requisição seja do tipo POST
    if request.method == 'POST':
        pedido = get_object_or_404(Pedido, id=pedido_id)

        # Segurança: Garante que o dono só pode alterar pedidos do seu próprio restaurante
        if pedido.restaurante.dono != request.user:
            return redirect('core:painel_restaurante') # Ou acesso negado

        # Pega o novo status enviado pelo formulário
        novo_status = request.POST.get('novo_status')

        # Valida se o novo status é uma das opções válidas no modelo Pedido
        valid_statuses = [status[0] for status in Pedido.STATUS_CHOICES]
        if novo_status in valid_statuses:
            pedido.status = novo_status
            pedido.save()

    # Redireciona de volta para a lista de pedidos em qualquer caso
    return redirect('core:ver_pedidos_restaurante')