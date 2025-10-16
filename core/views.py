from django.views.generic import ListView, DetailView
from .models import Restaurante


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
