import json
from datetime import datetime, timezone

from django.http import JsonResponse
from django.shortcuts import render

from .mongo import fetch_portfolio_profile


def home(request):
    return render(request, "portfolio/index.html")


def portfolio_api(request):
    profile = fetch_portfolio_profile()
    payload = {
        "status": "ok",
        "source": profile["source"],
        "updatedAt": datetime.now(timezone.utc).isoformat(),
        "profile": profile["data"],
    }
    return JsonResponse(payload)


def health_api(request):
    return JsonResponse(
        {
            "status": "ok",
            "service": "portfolio-backend",
            "timestamp": datetime.now(timezone.utc).isoformat(),
        }
    )
