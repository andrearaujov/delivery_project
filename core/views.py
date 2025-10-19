from django.views.generic import ListView, DetailView
from django.shortcuts import render, redirect, get_object_or_404
from .models import Restaurante, Produto, Pedido, ItemPedido, Cliente

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