from django.shortcuts import render
from .services.planejamento_mt_correntes import excel_para_html

def home(request):
    return render(request, "recipes/home.html")

def planejamentomt(request):
    return render(request, "recipes/planejamentomt.html")

def capex(request):
    return render(request, "recipes/capex.html")

def correcao_correntes(request):
    contexto = {}
    if request.method == "POST" and request.FILES.get("arquivo"):
        try:
            ctx = excel_para_html(request.FILES["arquivo"])
            contexto.update(ctx)
        except Exception as e:
            contexto["erro"] = f"Não foi possível ler o Excel: {e}"
    return render(request, "recipes/correcao_correntes.html", contexto)


from decimal import Decimal
from django.db.models import Sum, F
from django.shortcuts import get_object_or_404, redirect, render
from django.contrib import messages
from .models import Plan, MonthlyCapex, Transferencia
from .forms import PrevisaoMesFormSet, TransferenciaForm

def _resumo_plan(plan: Plan, year: int):
    qs = plan.mensal.filter(year=year)
    realizado = qs.aggregate(t=Sum("realizado"))["t"] or Decimal("0")
    previsto  = qs.aggregate(t=Sum("previsto"))["t"]  or Decimal("0")
    melhor_visao = realizado + previsto
    transf = (plan.transferencias.filter(year=year)
              .aggregate(t=Sum("valor"))["t"] or Decimal("0"))
    saldo = plan.rev3_meta - melhor_visao + transf
    return {
        "realizado": realizado, "previsto": previsto,
        "melhor_visao": melhor_visao, "rev3": plan.rev3_meta,
        "transferencia": transf, "saldo": saldo,
    }

def capex(request, year=2025):
    # mostre apenas subplanos (tem parent)
    subplanos = (Plan.objects.filter(parent__isnull=False)
                 .select_related("parent")
                 .prefetch_related("mensal", "transferencias"))
    linhas = []
    for p in subplanos:
        r = _resumo_plan(p, year)
        linhas.append({"plan": p, **r})
    # também o total geral
    total = {
        "realizado": sum(l["realizado"] for l in linhas),
        "previsto": sum(l["previsto"] for l in linhas),
        "melhor_visao": sum(l["melhor_visao"] for l in linhas),
        "rev3": sum(l["plan"].rev3_meta for l in linhas),
        "transferencia": sum(l["transferencia"] for l in linhas),
    }
    total["saldo"] = total["rev3"] - total["melhor_visao"] + total["transferencia"]
    return render(request, "recipes/capex_overview.html", {
        "linhas": linhas, "total": total, "year": year
    })

def capex_editar(request, plan_id, year=2025):
    plan = get_object_or_404(Plan, pk=plan_id)
    # garanta os 12 registros
    for m in range(1, 13):
        MonthlyCapex.objects.get_or_create(plan=plan, year=year, mes=m)

    qs = MonthlyCapex.objects.filter(plan=plan, year=year).order_by("mes")
    Formset = PrevisaoMesFormSet
    if request.method == "POST":
        formset = Formset(request.POST, queryset=qs)
        transf = Transferencia.objects.filter(plan=plan, year=year).first()
        transf_form = TransferenciaForm(request.POST, instance=transf)
        if formset.is_valid() and transf_form.is_valid():
            formset.save()
            obj = transf_form.save(commit=False)
            obj.plan = plan
            obj.year = year
            obj.save()
            messages.success(request, "Dados salvos.")
            return redirect("capex")
        else:
            messages.error(request, "Verifique os campos destacados.")
    else:
        formset = Formset(queryset=qs)
        transf = Transferencia.objects.filter(plan=plan, year=year).first()
        transf_form = TransferenciaForm(instance=transf)

    resumo = _resumo_plan(plan, year)
    return render(request, "recipes/capex_edit.html", {
        "plan": plan, "formset": formset, "transf_form": transf_form,
        "meses": list(range(1, 13)), "year": year, "resumo": resumo
    })