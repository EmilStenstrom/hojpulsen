from django.shortcuts import render

def startpage(request):
	return render(request, "startpage.html")
