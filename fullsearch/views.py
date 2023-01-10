from django.shortcuts import render
from .forms import FullSearchForm, TweetsCountForm
from .scripts import formatDates,getTweetsFullArchive,exportExcelFile, getTweetsCount, getDaysBetweenDates
from django.contrib import messages
# Create your views here.
def index(request):
    if(request.method == 'POST'):
        form = FullSearchForm(request.POST)
        if form.is_valid():
            query = form.cleaned_data['Query']
            lang = form.cleaned_data['Lang']
            print(lang)
            date1 = form.cleaned_data['Date1']
            date2 = form.cleaned_data['Date2']            
            
            if getDaysBetweenDates(date1, date2) <= 3:                
                fromDate, toDate = formatDates(date1,date2)                        
                df_output = getTweetsFullArchive(query,lang, fromDate, toDate)
                
                if df_output.empty:
                    print('a consulta não retornou nenhum registro!')   
                    messages.add_message(request, messages.WARNING, 'A consulta não retornou nenhum registro')             
                else:                
                    res = exportExcelFile(df_output, f"full_search_"+query+".xlsx")
                    return res
            else:
                messages.add_message(request, messages.WARNING, 'O período não pode ser maior que 1 mês!')       
    else:
        form = FullSearchForm()
    
    return render(request, 'fullsearch.html', {"form": form})
    
def executafuncao(request):    
    print('testeste ')
    form = FullSearchForm()
    return render(request, 'fullsearch.html', {"form": form})

def tweetscount(request):
    if(request.method == 'POST'):
        form = TweetsCountForm(request.POST)
        if form.is_valid():
            query = form.cleaned_data['Query']
            lang = form.cleaned_data['Lang']            
            date1 = form.cleaned_data['Date1']
            date2 = form.cleaned_data['Date2']            
                        
            if getDaysBetweenDates(date1, date2) <= 365:            
                fromDate, toDate = formatDates(date1,date2)            
                df_output = getTweetsCount(query,lang, fromDate, toDate)
                            
                if df_output.empty:
                    print('a consulta não retornou nenhum registro!')   
                    messages.add_message(request, messages.WARNING, 'A consulta não retornou nenhum registro. Verifique os parâmetros, ou se o numero de requisições foi excedido')             
                else:                
                    res = exportExcelFile(df_output, f"tweets_count_"+query+"_"+date1+"_to_"+date2+".xlsx")
                    return res
            else:
                messages.add_message(request, messages.WARNING, 'O período não pode ser maior que 1 ano!')             
    else:
        form = TweetsCountForm()
    
    return render(request, 'tweetscount.html', {"form": form}) 
    