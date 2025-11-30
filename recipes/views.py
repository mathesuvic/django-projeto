from django.shortcuts import render
from .services.planejamento_mt_correntes import excel_para_html

def home(request):
    return render(request, "recipes/home.html")

def planejamentomt(request):
    return render(request, "recipes/planejamentomt.html")

def correcao_correntes(request):
    contexto = {}
    if request.method == "POST" and request.FILES.get("arquivo"):
        try:
            ctx = excel_para_html(request.FILES["arquivo"])
            contexto.update(ctx)
        except Exception as e:
            contexto["erro"] = f"Não foi possível ler o Excel: {e}"
    return render(request, "recipes/correcao_correntes.html", contexto)
