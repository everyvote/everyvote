from django.shortcuts import render
from django.http import HttpResponse
from django.template.loader import get_template
from django.shortcuts import render_to_response
from django.template import Context
from django.views.generic.base import TemplateView

def hello(request):
    name = "Mitch"
    html = "<html><body>Hi %s, this seems to have worked!</body></html>" % name
    return HttpResponse(html)

def hello_template(request):
    name = "Mitch"
    t = get_template('hello.html')
    html = t.render(Context({'name': name}))
    return HttpResponse(html)

def hello_template_simple(request):
    name = "Mike"
    return render_to_response('hello.html', {'name': name})

class HelloTemplate(TemplateView):
    
    template_name = 'hello_class.html'
    
    def get_context_data(self, **kwargs):
        context = super(HelloTemplate, self).get_context_data(**kwargs)
        context['name'] = 'Mike'
        return context