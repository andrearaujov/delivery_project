from django.views.generic import ListView, DetailView
from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth import login  
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

def finalizar_pedido(request):
    carrinho = request.session.get('carrinho',{})
    if not carrinho:
        return redirect('core:lista_restaurantes')
    
    try:
        cliente = Cliente.objects.get()
        if not cliente:
            cliente = Cliente.objects.create(nome="Cliente Padrão", email="cliente@teste.com", telefone="99999", endereco="Rua Teste")
    except Cliente.DoesNotExist:
        return redirect('core:ver_carrinho')
    
    
    produto_ids = carrinho.keys()
    produtos = Produto.objects.filter(id__in=produto_ids)
    
    restaurante_do_pedido = produtos.first().restaurante
    
    novo_pedido = Pedido.objects.create(
        cliente=cliente,
        restaurante=restaurante_do_pedido,
        status='Pendente' # Status inicial
    )

    valor_total = 0
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
    
    novo_pedido.valor_total = valor_total
    novo_pedido.save()

    request.session['carrinho'] = {}

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