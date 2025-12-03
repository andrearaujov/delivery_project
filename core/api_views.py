from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
from django.shortcuts import get_object_or_404
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.models import User
from .models import Restaurante, Produto, Pedido, ItemPedido, Cliente
import json

def restaurant_list_api(request):
    restaurantes = Restaurante.objects.all()
    data = []
    for r in restaurantes:
        data.append({
            'id': r.id,
            'nome': r.nome,
            'endereco': r.endereco,
            'tipo_cozinha': r.tipo_cozinha,
            'horario_funcionamento': r.horario_funcionamento,
            'imagem_url': r.produtos.first().foto.url if r.produtos.exists() and r.produtos.first().foto else None # Exemplo simples
        })
    return JsonResponse(data, safe=False)

def restaurant_detail_api(request, pk):
    restaurante = get_object_or_404(Restaurante, pk=pk)
    produtos = restaurante.produtos.all()
    produtos_data = []
    for p in produtos:
        produtos_data.append({
            'id': p.id,
            'nome': p.nome,
            'descricao': p.descricao,
            'preco': str(p.preco),
            'foto_url': p.foto.url if p.foto else None
        })
    
    data = {
        'id': restaurante.id,
        'nome': restaurante.nome,
        'endereco': restaurante.endereco,
        'tipo_cozinha': restaurante.tipo_cozinha,
        'produtos': produtos_data
    }
    return JsonResponse(data)

@csrf_exempt
def login_api(request):
    if request.method == 'POST':
        data = json.loads(request.body)
        username = data.get('username')
        password = data.get('password')
        user = authenticate(request, username=username, password=password)
        if user is not None:
            login(request, user)
            return JsonResponse({'success': True, 'username': user.username})
        else:
            return JsonResponse({'success': False, 'error': 'Invalid credentials'}, status=401)
    return JsonResponse({'error': 'Method not allowed'}, status=405)

@csrf_exempt
def logout_api(request):
    logout(request)
    return JsonResponse({'success': True})

def user_info_api(request):
    if request.user.is_authenticated:
        return JsonResponse({
            'is_authenticated': True,
            'username': request.user.username,
            'id': request.user.id
        })
    return JsonResponse({'is_authenticated': False})

@csrf_exempt
def add_to_cart_api(request):
    if not request.user.is_authenticated:
        return JsonResponse({'error': 'Login required'}, status=401)
        
    if request.method == 'POST':
        data = json.loads(request.body)
        produto_id = str(data.get('produto_id'))
        
        carrinho = request.session.get('carrinho', {})
        if produto_id in carrinho:
            carrinho[produto_id] += 1
        else:
            carrinho[produto_id] = 1
            
        request.session['carrinho'] = carrinho
        return JsonResponse({'success': True, 'carrinho': carrinho})
    return JsonResponse({'error': 'Method not allowed'}, status=405)

def cart_api(request):
    carrinho = request.session.get('carrinho', {})
    if not carrinho:
        return JsonResponse({'itens': [], 'total': 0})
        
    produto_ids = carrinho.keys()
    produtos = Produto.objects.filter(id__in=produto_ids)
    itens = []
    total = 0
    
    for p in produtos:
        qtd = carrinho[str(p.id)]
        subtotal = p.preco * qtd
        itens.append({
            'produto_id': p.id,
            'nome': p.nome,
            'preco': str(p.preco),
            'quantidade': qtd,
            'subtotal': str(subtotal)
        })
        total += subtotal
        
    return JsonResponse({'itens': itens, 'total': str(total)})

@csrf_exempt
def checkout_api(request):
    if not request.user.is_authenticated:
        return JsonResponse({'error': 'Login required'}, status=401)
        
    if request.method == 'POST':
        carrinho = request.session.get('carrinho', {})
        if not carrinho:
            return JsonResponse({'error': 'Cart is empty'}, status=400)
            
        produto_ids = carrinho.keys()
        produtos = Produto.objects.filter(id__in=produto_ids)
        
        if not produtos.exists():
             return JsonResponse({'error': 'Invalid products'}, status=400)
             
        restaurante = produtos.first().restaurante
        try:
            cliente = request.user.cliente
        except:
             return JsonResponse({'error': 'User is not a client'}, status=400)

        pedido = Pedido.objects.create(
            cliente=cliente,
            restaurante=restaurante,
            status='Pendente'
        )
        
        total = 0
        for p in produtos:
            qtd = carrinho[str(p.id)]
            ItemPedido.objects.create(
                pedido=pedido,
                produto=p,
                quantidade=qtd,
                preco_unitario=p.preco
            )
            total += p.preco * qtd
            
        pedido.valor_total = total
        pedido.save()
        
        request.session['carrinho'] = {}
        return JsonResponse({'success': True, 'pedido_id': pedido.id})
        
    return JsonResponse({'error': 'Method not allowed'}, status=405)
