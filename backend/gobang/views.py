from django.shortcuts import render
from django.http import JsonResponse
# Create your views here.

from gmcts.test import execute, createit

def create(request):
  createit()
  return JsonResponse({'msg': 'ok'})

def hello(request):
  x = request.GET.get('x')
  y = request.GET.get('y')
  print('x:', x, 'y:', y)
  # AI的决策
  aix, aiy, agent_win_rate, pre_visits, avg_visits, l = execute(int(x)-1, int(y)-1)
  h = []
  for i in range(10):
    h.append([])
    for j in range(10):
      h[i].append(l[j][i])
  obj = JsonResponse({'x': aix+1, 'y': aiy+1, 'rate': agent_win_rate, 'pre_visits': pre_visits, 'avg_visits': avg_visits, 'l': h})
  obj['Access-Control-Allow-Origin'] = '*'
  return obj