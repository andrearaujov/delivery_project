from django.views.generic import ListView, DetailView
from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth import login  
from django.contrib.auth.decorators import login_required
from .models import Restaurante, Produto, Pedido, ItemPedido, Cliente
from .forms import CadastroForm

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


def adicionar_ao_carrinho(request, produto_id):
    produto = get_object_or_404(Produto, id=produto_id)
    carrinho = request.session.get("carrinho", {})

    produto_id_str = str(produto.id)

    if produto_id_str in carrinho:
        carrinho[produto_id_str] += 1
    else:
        carrinho[produto_id_str] = 1

    request.session["carrinho"] = carrinho

    return redirect("core:detalhe_restaurante", pk=produto.restaurante.id)


def ver_carrinho(request):
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
        cliente=cliente_logado,  # <--- USA O CLIENTE CORRETO
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
    # Se o método for POST, significa que o usuário enviou o formulário
    if request.method == 'POST':
        form = CadastroForm(request.POST)
        if form.is_valid():
            # 1. Salva o objeto User, mas não no banco ainda (commit=False)
            user = form.save(commit=False)
            
            # 2. Define a senha de forma segura (com hash)
            user.set_password(form.cleaned_data['password'])
            
            # 3. Agora sim, salva o User no banco de dados
            user.save()

            # 4. Cria o perfil Cliente associado a este User
            Cliente.objects.create(
                user=user,
                telefone=form.cleaned_data['telefone'],
                endereco=form.cleaned_data['endereco']
            )

            # 5. Loga o usuário automaticamente após o cadastro
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